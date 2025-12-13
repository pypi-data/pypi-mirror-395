
from abc import ABC, abstractmethod
import concurrent.futures
from typing import List,Any, Generator,Optional
from whoischarman.struct.user import ExchangeRawConfig
from whoischarman.struct.exchange import Event, Item
from typing import Dict, List, Callable
import asyncio
import concurrent
from concurrent.futures import as_completed
from datetime import datetime, timezone, timedelta
import requests
from tqdm import tqdm
from pydantic import BaseModel
from loguru import logger


class RegistryClass:
    """
    Registry class to automatically store all BaseMarket subclasses.
    The _cls dictionary will contain all registered market classes.
    """
    _cls = {}

    @classmethod
    def register(cls, market_class):
        """Register a market class in the registry."""
        cls._cls[market_class.__name__] = market_class

    @classmethod
    def get(cls, class_name):
        """Get a market class by name."""
        return cls._cls.get(class_name)

    @classmethod
    def list_classes(cls):
        """List all registered classes."""
        return list(cls._cls.keys())



class ExchangeRegistryMeta(type):
    """
    Metaclass that automatically registers BaseExchange subclasses in RegistryClass.
    """
    def __new__(mcs, name, bases, namespace):
        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)

        # Register the class if it's a BaseExchange subclass (but not BaseExchange itself)
        if (len(bases) > 0 and any(hasattr(base, '__metaclass__') and base.__metaclass__ == mcs for base in bases)) or \
           (len(bases) > 0 and any(base.__name__ == 'BaseExchange' for base in bases)):
            if name != 'BaseExchange':  # Don't register BaseExchange itself
                RegistryClass.register(cls)

        return cls
    
class MapArgs(BaseModel):
    args: List[Any] = []
    kwargs: Dict = {}
    result :Optional[Any] = None

class BaseExchange(object, metaclass=ExchangeRegistryMeta):
    """
    Base class for all Exchange implementations.
    Subclasses will be automatically registered in RegistryClass._cls
    """
    Etype = Event
    Itype = Item
    
    def __init__(self, user_config:ExchangeRawConfig):
        self.user_config = user_config
        
        # 等待后续在 self.init进行初始化
        self.client = None
        self.req = requests.Session()
        self.init(user_config)
        self.logger = logger
        self.exe = None
        
    @property
    def name(self):
        return self.user_config.exchange_name
    
    def to_iso_utc(self,dt: datetime) -> str:
        """转成 ISO-8601 UTC 字符串（带 Z）"""
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def utc_now(self) -> datetime:
        return datetime.now(timezone.utc)

    @abstractmethod
    def init(self, user_config:ExchangeRawConfig):
        """
        这个方法主要用来初始化一些client 等
        
        
        :param self: Description
        :param user_config: 包含用户的token， api_key，api_secret等
        :type user_config: ExchangeRawConfig
        """

        
    @abstractmethod
    def get_event(self,event_id:str, user_config:ExchangeRawConfig=None) -> Event:
        pass

    @abstractmethod
    def get_events(self, user_config:ExchangeRawConfig=None) -> List[Event]:
        pass


    @abstractmethod
    def get_items(self,event_id:str, user_config:ExchangeRawConfig=None) -> List[Item]:
        pass

    @abstractmethod
    def get_items(self,event_id:Optional[str], user_config:ExchangeRawConfig=None) -> List[Item]:
        pass

    @abstractmethod
    def search(self,query:str,page_size=500,page=0, user_config:ExchangeRawConfig=None) -> List[Event]:
        pass

    def map_by_args(self, func:Callable, func_args: List[MapArgs], workers=10) -> List[MapArgs] : 
        with concurrent.futures.thread.ThreadPoolExecutor(max_workers=workers) as exe:
            _stack = {}
            # if isinstance(func_args, list):
            for id,A in enumerate(func_args):
                args = A.args
                kwargs = A.kwargs
                _stack[exe.submit(func, *args, ** kwargs)] = id
            
            for future in tqdm(as_completed(_stack), desc=f"Map In Threading:{workers}", total=len(func_args)):
                result =  future.result()
                raw_r:MapArgs = func_args[_stack[future]]
                raw_r.result = result
            return func_args

    def map(self, func:Callable, func_args: List[Any], workers=10) -> List[Any] : 
        with concurrent.futures.thread.ThreadPoolExecutor(max_workers=workers) as exe:
            # _stack = {}
            # if isinstance(func_args, list):
            res = []
            for i in tqdm(exe.map(func, func_args), desc=f"Map In Threading:{workers}", total=len(func_args)):
                res.append(i)
            return res

    def no_wait(self, func:Callable, *args, **kwargs) :
        if self.exe is None:
            self.exe = concurrent.futures.thread.ThreadPoolExecutor(max_workers=10)
        return self.exe.submit(func, *args, **kwargs)
    
    @abstractmethod
    def get_account(self, user_config:ExchangeRawConfig=None):
        pass

    @abstractmethod
    def get_order(self,order_id:str, user_config:ExchangeRawConfig=None):
        pass

    def __truediv__(self, req_opt:dict):
        method  = req_opt.pop("method","get")
        headers = req_opt.pop("headers",{
            "Content-Type":"application/json"
        })
        if self.user_config.proxy is not None:
            self.req.proxies = {
                "http":self.user_config.proxy,
                "https":self.user_config.proxy
            }
        end_point = self.user_config.endpoint
        if end_point.endswith("/"):
            end_point = end_point[:-1]
        if "u" in req_opt:
            url = req_opt.pop("u", None)
        elif "url" in req_opt:    
            url = req_opt.pop("url", None)
        else:
            raise Exception("no url or u in {}")
        if not url.startswith("http"):
            url = end_point + url
        
        data = req_opt.pop("data", None)
        
        parms = req_opt.pop("params", None)
        try_time = 4

        while try_time > 0:
            try:
                method_call = getattr(self.req,method)
                if parms is None:
                    c = method_call(url,headers=headers, data=req_opt).json()
                else:
                    c = method_call(url,headers=headers, params=parms).json()
                if c is not None and "error" in c and  c["error"] is not None and "message" in c["error"] and "too many requests" in c["error"]["message"]:
                    import time
                    logger.warning(f"Request Error Waiting 3s try agin (try:{try_time}) : {c['error']}")
                    time.sleep(3)
                    try_time -= 1
                    continue
                return c
                
            except Exception as e:
                if try_time == 0:
                    import traceback
                    logger.warning(f"Error detail : {traceback.format_exc()}")
                    logger.error(f"Error : {e}")
                    raise e
                else:
                    import time
                    logger.warning(f"Network Error Waiting 3s try agin (try:{try_time}) : {e}")
                    time.sleep(3)
                    try_time -= 1

        


class ExchangeConfig(ExchangeRawConfig):
    """
    Base class for all exchange config classes.
    """
    def get_instance(self) -> BaseExchange:
        """
        Get the exchange class from the registry.
        """
        return RegistryClass.get(self.exchange_name)(self)
