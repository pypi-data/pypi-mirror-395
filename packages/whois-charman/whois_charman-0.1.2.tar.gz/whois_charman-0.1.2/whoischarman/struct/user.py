from pydantic import BaseModel
from typing import Optional, Callable
from abc import abstractmethod
class ExchangeRawConfig(BaseModel):
    """
    User configuration for a market.
    """
    exchange_name : str
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    api_passphrase: Optional[str] = None

    endpoint: Optional[str] = None
    api_rest_endpoint: Optional[str] = None
    api_stream_endpoint: Optional[str] = None


    proxy: Optional[str] = None

    @abstractmethod
    def get_instance(self) -> Callable:
        raise NotImplementedError("请实现get_instance方法")