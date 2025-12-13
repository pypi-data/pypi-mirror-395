from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Union, Callable,List
from enum import Enum
import time
from whoischarman.exchangers import ExchangeConfig
from abc import abstractmethod

class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 正在运行
    STOPPED = "stopped"      # 已停止
    ERROR = "error"         # 执行出错
    COMPLETED = "completed" # 执行完成

class AIRawConfig(BaseModel):
    """AI配置类"""
    
    model: str = Field("qwen3-4b", description="模型名称")
    api_key: str = Field("sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", description="API密钥")
    api: str = Field("https://xxx.xx.x.x:12341/v1/completions", description="API地址")
    temperature: float = Field(0.3, description="温度")
    max_tokens: int = Field(31024, description="最大token数")
    max_retries: int = Field(3, description="最大重试次数")
    timeout: int = Field(60, description="超时时间")

    using: bool = Field(False, description="是否正在使用AI")

    @abstractmethod
    def get_instance(self) -> Callable:
        raise NotImplementedError("请实现get_instance方法")
    
class ScheduleConf(BaseModel):
    """调度任务配置类"""

    # 基础配置
    name: str = Field(..., description="任务名称")
    enabled: bool = Field(False, description="是否启用任务")

    # 调度配置 - 为了兼容性，同时支持interval和interval_seconds
    interval_seconds: int = Field(60, description="执行间隔（秒）")
    interval: Optional[float] = Field(None, description="执行间隔（秒），优先使用interval_seconds")
    repeat_count: Optional[int] = Field(None, description="重复次数，None表示无限重复")
    max_executions: int = Field(-1, description="最大执行次数，-1表示无限")
    delay: float = Field(0.0, description="首次执行延迟（秒）")

    # 时间配置
    start_time: Optional[float] = Field(None, description="开始执行时间戳")
    end_time: Optional[float] = Field(None, description="结束执行时间戳")

    # 日志配置
    log_level: str = Field("INFO", description="日志级别")
    log_file: Optional[str] = Field(None, description="日志文件路径，None表示使用默认路径")
    log_file_root: Optional[str] = Field(None, description="日志文件根路径，None表示使用默认路径 (./logs)")

    # 错误处理配置
    continue_on_error: bool = Field(True, description="出错时是否继续执行")

    # 自定义参数
    params: Dict[str, Any] = Field(default_factory=dict, description="传递给任务的自定义参数")

    # 回调函数
    callback: Optional[Callable] = Field(None, description="任务回调函数")

    # User 配置
    exchange_user_configs: List[ExchangeConfig] = Field([], description="交易所用户配置列表")

    # AI 配置
    ai_configs: List[AIRawConfig] = Field([], description="AI 配置列表")

    def __init__(self, **data):
        """初始化时处理interval字段兼容性"""
        if 'interval' in data and 'interval_seconds' not in data:
            data['interval_seconds'] = int(data['interval'])
        super().__init__(**data)

    class Config:
        use_enum_values = True

    def __post_init__(self):
        """验证配置"""
        if self.interval is not None and self.interval <= 0:
            raise ValueError("interval must be greater than 0")

        if self.repeat_count is not None and self.repeat_count <= 0:
            raise ValueError("repeat_count must be greater than 0")

        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValueError("start_time must be less than end_time")

    def should_execute_at(self, current_time: float) -> bool:
        """判断是否应该在指定时间执行"""
        # 检查是否启用
        if not self.enabled:
            return False

        # 检查时间范围
        if self.start_time is not None and current_time < self.start_time:
            return False

        if self.end_time is not None and current_time > self.end_time:
            return False

        return True

    def get_log_file_path(self, default_log_dir: str = "logs") -> str:
        """获取日志文件路径"""
        if self.log_file:
            return self.log_file

        # 生成默认日志文件路径
        timestamp = int(time.time())
        return f"{default_log_dir}/{self.name}_{timestamp}.log"