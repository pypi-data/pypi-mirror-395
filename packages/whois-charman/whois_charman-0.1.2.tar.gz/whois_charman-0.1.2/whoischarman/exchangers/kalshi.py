from typing import List, Dict, ClassVar,Any
from .base import BaseExchange, ExchangeRawConfig,MapArgs
from ..struct.exchange import Event, Item
from datetime import timedelta
import time

class KalshiItem(Item):
    _ALIAS ={
        "ticker": "id",
        "close_ts": "close_time",
        "open_ts": "open_time",
        "yes_sub_title": "name",
        "yes_subtitle": "name",
    }

class KalshiEvent(Event):
    _ALIAS = {
        "ticker": "id",
        "series_ticker": "id",
        "event_title": "desc",
        "series_title": "title",
        "total_volume": "volume",
    }
    Itype: ClassVar[type] = KalshiItem  # 添加对应的Item类型

class KalshiExchange(BaseExchange):
    """
    Kalshi Exchange
    """
    Etype = KalshiEvent
    Itype = KalshiItem
    def init(self, user_config: ExchangeRawConfig = None):
        
        if not self.user_config.endpoint:
            self.user_config.endpoint = "https://api.elections.kalshi.com/trade-api/v2"
    
    def get_items(self, event_or_id):
        ms = []
        
        event_id = event_or_id
        if isinstance(event_or_id, Event):
            event_id = event_or_id.id
        res = self / {
            "url": f"/markets/",
            "params": {
                "series_ticker": event_id,
                "status":"open"
            }
        }
        try:
            for r in res["markets"]:
                i:KalshiItem = KalshiItem.from_exchange(r)
                i.event_id = event_id 
                ms.append(i)
                if isinstance(event_or_id, Event):
                    event_or_id.add_item(i)
        
            return ms
        except KeyError as e:
            self.logger.error(f"Error fetching items for event {event_id}: {res}\n{e}")

    def get_event(self, event_id: str, user_config: ExchangeRawConfig=None) -> KalshiEvent:
        """Fetches a single market/event by its ID."""
        future = self.no_wait(self.get_items, event_id)
        event = KalshiEvent.from_exchange((self / {
            "url": f"/series/{event_id}"
        })['series'])
        items = future.result()
        event.items = items
        return event
    
    def get_events(self,user_config = None) -> List[Event]:
        """Fetches all events exclude exists ids."""

        exists_ids = set(self.Etype.get_all_ids().keys())
        new_series = []
        for raw in (self / {
            "url": "/series",
        })['series']:
            ev = KalshiEvent.from_exchange(raw)
            new_series.append(ev)
            
        
        need_add:List[KalshiEvent] = []
        for ev in new_series:
            if ev.id not in exists_ids:
                need_add.append(ev)
        self.logger.success(f'{len(need_add)}/ {len(new_series)}  new events found. exists ids: {len(exists_ids)}')
        self.map(self.get_items, need_add)
        ok_evs = []
        
        for ev in need_add:
            if len(ev.items) > 0:
                ev.closed = False
            else:
                ev.closed = True
            ok_evs.append(ev)

        return ok_evs
        


        # end_ts   = (self.utc_now() + timedelta(hours=1)).timestamp()
        # # start_ts = int((self.utc_now() - timedelta(days=30)).timestamp())

        # params = {
        #     "min_close_ts": end_ts,   # 官方支持：close_ts > start_ts
        #     "with_nested_markets": "true",
        #     "limit": 200,               # 上限 200
        #     "status": "open",           # 只取未结算，可自行去掉
        # }

        # all_events: List[Dict[str, Any]] = []
        # cursor: str | None = None

        # while True:
        #     if cursor:
        #         params["cursor"] = cursor
        #     else:
        #         params.pop("cursor", None)

        #     data = self / {
        #         "url": "/events",
        #         "params": params,
        #     }
            
        #     events = data.get("events", [])
        #     self.logger.info(f"Got {len(events)} events")
        #     all_events.extend(events)
        #     if len(all_events) >= limit:
        #         break

        #     cursor = data.get("cursor")
        #     if not cursor or len(events) < params["limit"]:
        #         break
        #     time.sleep(0.2)  # 简单限速
        # es = []
        # for event in all_events:
        #     E = KalshiEvent.from_exchange(event)
        #     for market in event.get("markets", []):
        #         M = KalshiItem.from_exchange(market)
        #         E.add_item(M)
        #     es.append(E)
        # return es
    
    def search(self, query="",page_size=100,page=1, user_config = None):
        """
        Docstring for search
        
        :param self: Description
        :param query: Description, when empty, returns lastest events
        :param page_size: Description
        :param page: Description
        :param user_config: Description
        """
        e = self / {
            "url": f"https://api.elections.kalshi.com/v1/search/series?order_by=querymatch&query={query}&page_size={page_size}&fuzzy_threshold=4&with_milestones=true"
        }
        # self.logger.success(f"{e}")
        
        es = []
        for raw_ser in e["current_page"]:
            event =  KalshiEvent.from_exchange(raw_ser)
            for mi in raw_ser["markets"]:
                m = KalshiItem.from_exchange(mi)
                event.add_item(m)
            es.append(event)
        
        # self.map(self.get_items, es)
        next_cursor = e["next_cursor"]
        i = 1
        a = page
        while page > 1:
            self.logger.info(f"pulled {len(es)} events. left page: {page}/{a}")
            e = self / {
                "url": f"https://api.elections.kalshi.com/v1/search/series?order_by=querymatch&query={query}&page_size={page_size}&fuzzy_threshold=4&with_milestones=true&cursor={next_cursor}"
            }
            
            es_tmp = []
            for raw_ser in e["current_page"]:
                event =  KalshiEvent.from_exchange(raw_ser)
                for mi in raw_ser["markets"]:
                    m = KalshiItem.from_exchange(mi)
                    event.add_item(m)
                es_tmp.append(event)
            next_cursor = e["next_cursor"]
            page -= 1
            es.extend(es_tmp)
        return es
