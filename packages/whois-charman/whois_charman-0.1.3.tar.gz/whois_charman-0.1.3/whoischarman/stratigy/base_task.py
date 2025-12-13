"""
任务基类模块

提供基础任务接口和自动注册功能
"""
import asyncio
import logging
import os
import threading
import time
from abc import ABC, ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Callable

from whoischarman.struct.schedule import ScheduleConf


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"      # 等待运行
    RUNNING = "running"      # 正在运行
    STOPPED = "stopped"      # 已停止
    ERROR = "error"         # 错误状态
    COMPLETED = "completed"  # 已完成


class TaskRegistryMeta(ABCMeta):
    """任务注册器元类，自动继承BaseTask的子类"""
    registry: Dict[str, type] = {}

    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)

        # 只注册BaseTask的直接子类，忽略BaseTask本身
        if bases and name != 'BaseTask':
            # 检查是否继承自BaseTask
            for base in bases:
                if base.__name__ == 'BaseTask' or hasattr(base, '__bases__'):
                    # 查找BaseTask在基类中
                    if base.__name__ == 'BaseTask':
                        cls.registry[name] = new_class
                        print(f"注册任务类: {name}")
                        break

        return new_class

    @classmethod
    def get_registered_tasks(cls) -> Dict[str, type]:
        """获取所有已注册的任务类"""
        return cls.registry.copy()

    @classmethod
    def get_task_class(cls, name: str) -> Optional[type]:
        """根据名称获取任务类"""
        return cls.registry.get(name)

    @classmethod
    def create_task_instance(cls, task_name: str, config: ScheduleConf, **kwargs):
        """创建任务实例"""
        task_class = cls.get_task_class(task_name)
        if not task_class:
            raise ValueError(f"未找到任务类: {task_name}")

        return task_class(config, **kwargs)


class BaseTask(ABC, metaclass=TaskRegistryMeta):
    """任务基类

    所有定时任务都需要继承此类并实现execute方法
    """

    def __init__(self, config: ScheduleConf, **kwargs):
        """
        初始化任务

        Args:
            config: 任务配置
            **kwargs: 自定义参数
        """
        # 先创建锁，避免property访问时的冲突
        self._status_lock = threading.Lock()
        self._count_lock = threading.Lock()

        self.config = config
        self.kwargs = kwargs
        self.name = config.name
        self._status = TaskStatus.PENDING  # 直接设置私有变量
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.execution_count = 0
        self.error_count = 0
        self.last_error: Optional[str] = None

        # 初始化日志文件路径
        self.log_file = self.config.log_file
        if self.log_file is None:
            self.logs_dir = "logs" if self.config.log_file_root is None else self.config.log_file_root
            self.log_file = os.path.join(self.logs_dir, f"{self.name}.log")

        # 设置独立的日志记录器
        self.logger = self._setup_logger()

        # 控制任务运行
        self._running = False
        self._stop_event = threading.Event()

    def _setup_logger(self) -> logging.Logger:
        """为任务设置独立的日志记录器"""
        logger_name = f"task.{self.name}"
        logger = logging.getLogger(logger_name)

        # 如果logger没有处理器，则添加文件处理器
        if not logger.handlers:
            # 创建logs目录（如果不存在）
            os.makedirs(self.logs_dir, exist_ok=True)

            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(getattr(logging, self.config.log_level.upper()))

            # 设置日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.setLevel(getattr(logging, self.config.log_level.upper()))

        return logger

    @property
    def status(self) -> TaskStatus:
        """获取任务状态"""
        with self._status_lock:
            return self._status

    @status.setter
    def status(self, value: TaskStatus):
        """设置任务状态"""
        with self._status_lock:
            self._status = value

    @property
    def running(self) -> bool:
        """检查任务是否正在运行"""
        return self._running and not self._stop_event.is_set()

    @property
    def stats(self) -> Dict[str, Any]:
        """获取任务统计信息"""
        return {
            'name': self.name,
            'status': self.status.value,
            'running': self.running,
            'execution_count': self.execution_count,
            'log_file': self.log_file,
            'error_count': self.error_count,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'last_error': self.last_error,
            'config': self.config.dict()
        }

    def start(self):
        """启动任务"""
        if self.running:
            self.logger.warning(f"任务 {self.name} 已在运行中")
            return

        if not self.config.enabled:
            self.logger.info(f"任务 {self.name} 已禁用，跳过启动")
            return

        self.logger.info(f"启动任务: {self.name}")
        self._running = True
        self._stop_event.clear()
        self.status = TaskStatus.PENDING
        self.start_time = datetime.now()

        # 在新线程中运行任务
        thread = threading.Thread(target=self._run_loop, daemon=True)
        thread.start()

    def stop(self):
        """停止任务"""
        if not self.running:
            self.logger.warning(f"任务 {self.name} 未在运行中")
            return

        self.logger.info(f"停止任务: {self.name}")
        self._stop_event.set()
        self._running = False
        self.status = TaskStatus.STOPPED
        self.end_time = datetime.now()

    def _run_loop(self):
        """任务运行主循环"""
        try:
            self.status = TaskStatus.RUNNING

            while self.running and not self._stop_event.is_set():
                try:
                    # 检查是否需要停止
                    if self._stop_event.is_set():
                        break

                    # 执行任务
                    self.execute_single()

                    # 检查执行次数限制
                    if self.config.max_executions > 0 and self.execution_count >= self.config.max_executions:
                        self.logger.info(f"任务 {self.name} 达到最大执行次数限制")
                        break

                    # 等待下次执行
                    if self.running and not self._stop_event.is_set():
                        self._stop_event.wait(self.config.interval_seconds)

                except Exception as e:
                    self._handle_error(e)

                    # 如果配置了遇到错误时停止，则退出循环
                    if not self.config.continue_on_error:
                        break

                    # 错误等待时间
                    if self.running and not self._stop_event.is_set():
                        self._stop_event.wait(self.config.interval_seconds)

        except Exception as e:
            self._handle_error(e)

        finally:
            self._running = False
            self.status = TaskStatus.COMPLETED
            self.end_time = datetime.now()
            self.logger.info(f"任务 {self.name} 结束运行")

    def execute_single(self):
        """执行单次任务"""
        try:
            self.logger.info(f"开始执行任务: {self.name} (第{self.execution_count + 1}次)")

            # 执行具体任务逻辑
            if asyncio.iscoroutinefunction(self.execute):
                # 异步任务
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(self.execute())
                finally:
                    loop.close()
            else:
                # 同步任务
                result = self.execute()

            # 更新执行计数
            with self._count_lock:
                self.execution_count += 1

            self.logger.info(f"任务 {self.name} 执行成功，结果: {result}")
            if self.config.callback is not None and isinstance(self.config.callback, Callable):
                self.config.callback(result)
        except Exception as e:
            self._handle_error(e)
            raise

    def _handle_error(self, error: Exception):
        """处理任务执行错误"""
        error_msg = f"任务 {self.name} 执行出错: {str(error)}"
        self.logger.error(error_msg, exc_info=True)

        with self._count_lock:
            self.error_count += 1

        self.last_error = str(error)
        self.status = TaskStatus.ERROR

    @abstractmethod
    def execute(self) -> Any:
        """
        任务执行逻辑（子类必须实现）

        Returns:
            Any: 任务执行结果

        Raises:
            Exception: 任务执行异常
        """
        pass

    def get_logs(self, lines: int = 100) -> list:
        """获取任务最近的日志"""
        try:
            import os
            # 使用正确的日志文件路径
            log_file = self.log_file
            if not os.path.exists(log_file):
                return []

            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return [line.strip() for line in all_lines[-lines:]]

        except Exception as e:
            self.logger.error(f"读取日志文件失败: {e}")
            return []