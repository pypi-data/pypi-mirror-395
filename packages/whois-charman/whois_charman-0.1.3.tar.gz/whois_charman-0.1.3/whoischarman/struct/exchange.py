import datetime
from typing import Optional
from typing import List
from typing import ClassVar
from pathlib import Path
from .db import DBModel
class BaseExchangeModel(DBModel):
    _DB: ClassVar[Optional[str]] = str(Path("~").expanduser() / ".whois-charman"/"dbs"/ "exchange.db" )  # 数据库文件路径，子类需要指定
    @classmethod
    def from_exchange(cls, data: dict) -> "Event":
        """通用入口：传原始 dict，返回 Event 实例"""
        # 1. 别名 → 标准名
        # print(cls._ALIAS, type(cls._ALIAS))
        data = {cls._ALIAS.get(k, k): v for k, v in data.items()}

        # 2. 特殊值转换（示例）
        if "state" in data:               # Huobi 的 state 转 closed
            data["closed"] = bool(int(data.pop("state")))
        if "enable" in data:              # OKX 的 enable 转 active
            data["active"] = bool(int(data.pop("enable")))

        # 2.5. 应用自动类型转换
        # 创建一个临时实例来使用类型转换功能
        temp_instance = cls.__new__(cls)
        data = temp_instance._convert_types(data)

        # 3. 构造
        return cls(**data)
    

class Item(BaseExchangeModel):
    # 数据库配置 - 默认数据库路径
    event_id: Optional[str] = None
    title: Optional[str] = None
    name: Optional[str] = None
    yes_bid: Optional[float] = None
    yes_ask: Optional[float] = None
    no_bid: Optional[float] = None
    no_ask: Optional[float] = None
    volume : Optional[float] = None
    
    

class Event(BaseExchangeModel):
    # 数据库配置 - 默认数据库路径

    title: Optional[str] = None
    desc: Optional[str] = None
    volume: Optional[float] = 0.0
    category: Optional[str] = None
    items: List[Item] = []
    closed: Optional[bool] = None
    Itype: ClassVar = Item
    def merge_items(self, items:List[Item]):
        self.items = items
        if self.open_time is None :
            for i in items:
                i.event_slug = self.slug
                if i.open_time is not None:
                    self.open_time = i.open_time
                if i.close_time is not None:
                    self.close_time = i.close_time
                if self.open_time is not None:
                    break
        return self

    def add_item(self, item: Item):
        item.title = self.title
        item.event_id = self.id
        self.items.append(item)
        if self.open_time is None and item.open_time is not None:
            self.open_time = item.open_time
        if self.close_time is None and item.close_time is not None:
            self.close_time = item.close_time
        return self