



# polymarket.py
import os
import json
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, ClassVar
from web3 import Web3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from loguru import logger
from whoischarman.struct.user import ExchangeRawConfig
from whoischarman.struct.exchange import Item, Event
from .base import BaseExchange



# --- 导入基类和配置 ---
# from base_market import BaseMarket, RegistryClass
# from user_config import ExchangeRawConfig
# (假设这些文件在同一个目录或Python路径中)

class PolymarketItem(Item):
    _ALIAS = {
        "slug": "id",
        "endDate": "close_time",
        "startDate": "open_time",
        "groupItemTitle": "name",
        "question" : "title",
    }

class PolymarketEvent(Event):
    _ALIAS = {
        "slug": "id",
        "createdAt": "open_time",
        "startDate": "open_time",
        "closedTime": "close_time",
        "endDate": "close_time",
        "description": "desc",
        "question": "title",

    }
    Itype: ClassVar[type] = PolymarketItem 

class PolymarketExchange(BaseExchange):
    """
    Real implementation for the Polymarket API.
    """
    Etype = PolymarketEvent
    Itype = PolymarketItem
    def init(self,  user_config: ExchangeRawConfig = None):
        if not self.user_config.endpoint:
            self.user_config.endpoint = "https://gamma-api.polymarket.com/"
        
        # Setup GraphQL transport and client
        self._transport = RequestsHTTPTransport(url=self.user_config.endpoint)
        self._client = Client(transport=self._transport, fetch_schema_from_transport=False)

        # Authentication state
        self._jwt_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

        # EIP-712 signing data for authentication
        # This data is specific to the Polymarket CTF (Conditional Token Framework) Exchange
        self.eip712_domain = {
            "name": "Polymarket",
            "version": "1",
            "chainId": 137,  # Polygon Mainnet
            "verifyingContract": "0x4bFb41d1577F8c6A804BA79Ea1917e3E684535f3" # CTF Exchange Address
        }
        self.eip712_types = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Login": [
                {"name": "msg", "type": "string"}
            ]
        }

    # def _get_auth_headers(self) -> Dict[str, str]:
    #     """Retrieves or refreshes the JWT token and returns the auth headers."""
    #     if not self.user_config.api_secret or not self.user_config.api_passphrase:
    #         return {} # No credentials, no auth headers

    #     now = datetime.utcnow()
    #     if self._jwt_token and self._token_expiry and now < self._token_expiry:
    #         return {"Authorization": f"Bearer {self._jwt_token}"}

    #     print("JWT token is missing or expired. Requesting a new one...")
    #     try:
    #         # The message to be signed
    #         message_to_sign = {"msg": "Signing in to Polymarket."}
            
    #         # Sign the message
    #         w3 = Web3()
    #         signed_message = w3.eth.account.sign_message(
    #             data=Web3.to_hex(text=message_to_sign["msg"]),
    #             private_key=self.user_config.api_secret
    #         )
            
    #         signature = signed_message.signature.hex()

    #         # GraphQL mutation to sign in
    #         sign_in_mutation = gql("""
    #             mutation SignIn($signature: String!, $address: String!) {
    #                 signIn(signature: $signature, address: $address) {
    #                     accessToken
    #                     expiresIn
    #                 }
    #             }
    #         """)
            
    #         variables = {
    #             "signature": signature,
    #             "address": self.user_config.api_passphrase
    #         }

    #         result = self._client.execute(sign_in_mutation, variable_values=variables)
            
    #         self._jwt_token = result["signIn"]["accessToken"]
    #         self._token_expiry = now + timedelta(seconds=result["signIn"]["expiresIn"])
            
    #         print("Successfully obtained new JWT token.")
    #         return {"Authorization": f"Bearer {self._jwt_token}"}

    #     except Exception as e:
    #         print(f"Error during authentication: {e}")
    #         return {}
    def get_items(self, event_id:str) -> List[PolymarketItem]:
        res = self / {
            "url": "/events",
            "params": {
                "slug":event_id
            }
        }
         
        es = []
        for i in res["markets"]:
            es.append(PolymarketItem.from_exchange(i))
        return es

    def get_event(self, event_id: str, user_config: ExchangeRawConfig=None) -> PolymarketEvent:
        """Fetches a single market/event by its ID."""
        res = (self / {
            "url": "/events",
            "params": {
                "slug":event_id
            }
        })[0]
        event = PolymarketEvent.from_exchange(res)
        iss = []
        for m in res["markets"]:
            mi = PolymarketItem.from_exchange(m)
            iss.append(mi)
        event.items = iss
        return event


    
    def get_events(self,user_config: ExchangeRawConfig=None) -> List[PolymarketEvent]:
        """Fetches events from the API."""
        es = []
        end_dt   = self.utc_now()
        start_dt = end_dt - timedelta(days=30)

        exists_ids = self.Etype.get_all_ids()
        if len(exists_ids) == 0:
            start_dt = end_dt - timedelta(days=365)
        else:
            last = self.Etype.get_last()
            start_dt = last.open_time
        params = {
            "start_date_min": self.to_iso_utc(start_dt),
            "start_date_max": self.to_iso_utc(end_dt),
            "active": "true",          # 只取活跃的
            "closed": "false",
            "limit": 500,             # 单次最大
        }

        all_events: List[Dict[str, Any]] = []
        all_series: List[Dict[str, Any]] = []

        while True:
            data = self / {
                "url": "/events",
                "params": params
            }
            # r.raise_for_status()
            
            if not data:
                break
            all_events.extend(data)
            self.logger.success(f"Polymarket: Fetched {len(all_events)} events")
            
            # 提取 series 信息（去重）
            

            # 分页：Polymarket 用 createdAt 升序，取最后一条的 createdAt 作为下页起点
            last = len(all_events)
            params["offset"] = last
            if len(data) ==0:
                break
            time.sleep(0.2)  # 简单限速


        for i in all_events:
            pe = PolymarketEvent.from_exchange(i)
            if "markets"   in i:
                # raise ValueError("No markets in event: {}".format(i))
                for m in i["markets"]:
                    mi = PolymarketItem.from_exchange(m)
                    pe.add_item(mi)
            es.append(pe)
            
        return es
    # def get_market(self, market_id: str, user_config: ExchangeRawConfig=None) -> Market:
    #     """
    #     In Polymarket's terminology, a 'market' and an 'event' are often the same.
    #     This method is an alias for get_event.
    #     """

    #     return  Market.model_validate(self/ {
    #         "url": f"/markets/{market_id}",
    #     })

    # def get_markets(self, user_config: ExchangeRawConfig=None) -> List[Market]:
    #     """Fetches a list of all active markets."""
    #     response = self / {
    #             "url": "/markets"
    #         }
    #     ms = []

    #     # Handle different response formats
    #     if isinstance(response, list):
    #         for m in response:
    #             if isinstance(m, dict):
    #                 try:
    #                     ms.append(Market.model_validate(m))
    #                 except Exception as e:
    #                     print(f"Error validating market: {e}")
    #                     continue
    #     elif isinstance(response, dict):
    #         # If response is a dict, look for markets in common keys
    #         markets_data = response.get('markets', response.get('data', []))
    #         if isinstance(markets_data, list):
    #             for m in markets_data:
    #                 if isinstance(m, dict):
    #                     try:
    #                         ms.append(Market.model_validate(m))
    #                     except Exception as e:
    #                         print(f"Error validating market: {e}")
    #                         continue

    #     return ms

    def search(self, query: str, user_config: ExchangeRawConfig=None) -> List[Event]:
        """Searches for markets/events by query."""
        results = self / {
            "url": "/public-search",
            "params": {
                "q": query
            }
        }
        # Convert results to Market objects
        markets = []
        if isinstance(results, list):
            for result in results:
                markets.append(Event.model_validate(result))
        return markets

    # def get_account(self, user_config: ExchangeRawConfig=None) -> Optional[Dict[str, Any]]:
    #     """Fetches the authenticated user's account/portfolio information."""
    #     auth_headers = self._get_auth_headers()
    #     if not auth_headers:
    #         print("Cannot fetch account: No authentication credentials provided.")
    #         return None
        
    #     # Temporarily set auth headers for the transport
    #     original_headers = self._transport.headers
    #     self._transport.headers = auth_headers
        
    #     get_portfolio_query = gql("""
    #         query GetPortfolio {
    #             getPortfolio {
    #                 address
    #                 totalValue
    #                 totalMargin
    #                 totalPnl
    #                 positions {
    #                     market {
    #                         id
    #                         question
    #                         outcomes
    #                     }
    #                     outcome
    #                     balance
    #                     averagePrice
    #                 }
    #             }
    #         }
    #     """)
    #     try:
    #         result = self._client.execute(get_portfolio_query)
    #         return result.get("getPortfolio")
    #     except Exception as e:
    #         print(f"Error fetching account information: {e}")
    #         return None
    #     finally:
    #         # Restore original headers
    #         self._transport.headers = original_headers

    # def get_order(self, order_id: str, user_config: ExchangeRawConfig=None) -> Optional[Dict[str, Any]]:
    #     """
    #     Note: Polymarket's public API does not seem to have a direct query for a single order
    #     by its ID. Order information is typically part of the user's transaction history or portfolio.
    #     This method is a placeholder based on the available API capabilities.
    #     """
    #     print(f"Warning: Polymarket API does not have a public 'getOrder' field. Fetching from transaction history instead.")
        
    #     auth_headers = self._get_auth_headers()
    #     if not auth_headers:
    #         return None

    #     self._transport.headers = auth_headers

    #     # This is a hypothetical query. A real implementation would require knowing the exact schema.
    #     # Often, you'd fetch transactions and filter by a hash or ID.
    #     get_transactions_query = gql("""
    #         query GetTransactions {
    #             getTransactions {
    #                 id # This might be a transaction hash, not an order ID
    #                 type
    #                 timestamp
    #                 amount
    #                 asset {
    #                     id
    #                     symbol
    #                 }
    #             }
    #         }
    #     """)
    #     try:
    #         result = self._client.execute(get_transactions_query)
    #         transactions = result.get("getTransactions", [])
    #         # Filter for the specific order_id if it exists in the transaction data
    #         for tx in transactions:
    #             if tx.get("id") == order_id:
    #                 return tx
    #         return None # Not found
    #     except Exception as e:
    #         print(f"Error fetching order {order_id}: {e}")
    #         return None
    #     finally:
    #         self._transport.headers = {}
