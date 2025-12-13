"""
调度器模块

提供多线程任务调度和管理功能
"""
import logging
import threading
from typing import Any, Dict, List, Optional, Type

from .base_task import BaseTask, TaskRegistryMeta
from ..struct.schedule import ScheduleConf


class BaseScheduler:
    """调度器基类

    负责管理多个定时任务的生命周期
    """

    def __init__(self):
        """初始化调度器"""
        self.tasks: Dict[str, BaseTask] = {}
        self.task_configs: Dict[str, ScheduleConf] = {}
        self._lock = threading.RLock()  # 使用可重入锁

        # 设置调度器日志
        self.logger = self._setup_logger()

        # 自动发现并注册任务
        self._auto_discover_tasks()

    def _setup_logger(self) -> logging.Logger:
        """设置调度器日志记录器"""
        logger = logging.getLogger("scheduler")
        if not logger.handlers:
            # 创建logs目录
            import os
            os.makedirs("logs", exist_ok=True)

            log_file = "logs/scheduler.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO)

        return logger

    def _auto_discover_tasks(self):
        """自动发现所有继承BaseTask的任务类"""
        self.logger.info("开始自动发现任务类...")
        registered_tasks = TaskRegistryMeta.get_registered_tasks()

        if not registered_tasks:
            self.logger.info("未发现任何任务类")
            return

        self.logger.info(f"发现 {len(registered_tasks)} 个任务类: {list(registered_tasks.keys())}")

        # 为每个发现的任务类创建默认配置
        for task_name, task_class in registered_tasks.items():
            if task_name not in self.task_configs:
                # 创建默认配置
                default_config = ScheduleConf(
                    name=task_name,
                    interval_seconds=60,  # 默认60秒间隔
                    enabled=False,  # 默认禁用
                    max_executions=-1  # 无限执行
                )
                self.task_configs[task_name] = default_config
                self.logger.info(f"为任务 {task_name} 创建默认配置")

    def add_task(self, task_name: str, config: ScheduleConf, **kwargs) -> bool:
        """
        添加任务到调度器

        Args:
            task_name: 任务名称
            config: 任务配置
            **kwargs: 任务自定义参数

        Returns:
            bool: 添加是否成功
        """
        with self._lock:
            try:
                # 检查任务是否已存在
                if task_name in self.tasks:
                    self.logger.warning(f"任务 {task_name} 已存在，将被替换")
                    self.stop_task(task_name)

                # 保存配置
                self.task_configs[task_name] = config

                # 创建任务实例
                task = TaskRegistryMeta.create_task_instance(task_name, config, **kwargs)
                self.tasks[task_name] = task

                self.logger.info(f"成功添加任务: {task_name}")
                return True

            except Exception as e:
                self.logger.error(f"添加任务 {task_name} 失败: {e}")
                return False

    def remove_task(self, task_name: str) -> bool:
        """
        移除任务

        Args:
            task_name: 任务名称

        Returns:
            bool: 移除是否成功
        """
        with self._lock:
            try:
                if task_name in self.tasks:
                    # 先停止任务
                    self.stop_task(task_name)
                    # 移除任务
                    del self.tasks[task_name]
                    # 移除配置
                    if task_name in self.task_configs:
                        del self.task_configs[task_name]

                    self.logger.info(f"成功移除任务: {task_name}")
                    return True
                else:
                    self.logger.warning(f"任务 {task_name} 不存在")
                    return False

            except Exception as e:
                self.logger.error(f"移除任务 {task_name} 失败: {e}")
                return False

    def start_task(self, task_name: str) -> bool:
        """
        启动指定任务

        Args:
            task_name: 任务名称

        Returns:
            bool: 启动是否成功
        """
        with self._lock:
            if task_name not in self.tasks:
                self.logger.error(f"任务 {task_name} 不存在")
                return False

            try:
                self.tasks[task_name].start()
                self.logger.info(f"任务 {task_name} 启动成功")
                return True

            except Exception as e:
                self.logger.error(f"启动任务 {task_name} 失败: {e}")
                return False

    def stop_task(self, task_name: str) -> bool:
        """
        停止指定任务

        Args:
            task_name: 任务名称

        Returns:
            bool: 停止是否成功
        """
        with self._lock:
            if task_name not in self.tasks:
                self.logger.error(f"任务 {task_name} 不存在")
                return False

            try:
                self.tasks[task_name].stop()
                self.logger.info(f"任务 {task_name} 停止成功")
                return True

            except Exception as e:
                self.logger.error(f"停止任务 {task_name} 失败: {e}")
                return False

    def start_all_tasks(self) -> Dict[str, bool]:
        """
        启动所有已启用的任务

        Returns:
            Dict[str, bool]: 任务名称到启动结果的映射
        """
        results = {}
        with self._lock:
            for task_name, config in self.task_configs.items():
                if config.enabled:
                    results[task_name] = self.start_task(task_name)
                else:
                    self.logger.info(f"任务 {task_name} 已禁用，跳过启动")
                    results[task_name] = True

        return results

    def stop_all_tasks(self) -> Dict[str, bool]:
        """
        停止所有任务

        Returns:
            Dict[str, bool]: 任务名称到停止结果的映射
        """
        results = {}
        with self._lock:
            for task_name in self.tasks.keys():
                results[task_name] = self.stop_task(task_name)

        return results

    def get_task_status(self, task_name: str) -> Optional[Dict[str, Any]]:
        """
        获取任务状态

        Args:
            task_name: 任务名称

        Returns:
            Optional[Dict[str, Any]]: 任务状态信息
        """
        with self._lock:
            if task_name in self.tasks:
                return self.tasks[task_name].stats
            return None

    def get_all_tasks_status(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有任务状态

        Returns:
            Dict[str, Dict[str, Any]]: 任务名称到状态信息的映射
        """
        with self._lock:
            return {name: task.stats for name, task in self.tasks.items()}

    def get_task_logs(self, task_name: str, lines: int = 100) -> List[str]:
        """
        获取任务日志

        Args:
            task_name: 任务名称
            lines: 返回的日志行数

        Returns:
            List[str]: 日志行列表
        """
        with self._lock:
            if task_name in self.tasks:
                return self.tasks[task_name].get_logs(lines)
            return []

    def get_registered_task_classes(self) -> Dict[str, Type]:
        """
        获取所有已注册的任务类

        Returns:
            Dict[str, Type]: 任务名称到任务类的映射
        """
        return TaskRegistryMeta.get_registered_tasks()

    def update_task_config(self, task_name: str, config: ScheduleConf) -> bool:
        """
        更新任务配置

        Args:
            task_name: 任务名称
            config: 新的配置

        Returns:
            bool: 更新是否成功
        """
        with self._lock:
            try:
                if task_name in self.tasks:
                    # 如果任务正在运行，先停止
                    was_running = self.tasks[task_name].running
                    if was_running:
                        self.stop_task(task_name)

                    # 更新配置
                    self.task_configs[task_name] = config

                    # 重新创建任务实例
                    task = TaskRegistryMeta.create_task_instance(task_name, config)
                    self.tasks[task_name] = task

                    # 如果之前在运行，重新启动
                    if was_running and config.enabled:
                        self.start_task(task_name)

                    self.logger.info(f"任务 {task_name} 配置更新成功")
                    return True
                else:
                    self.logger.warning(f"任务 {task_name} 不存在")
                    return False

            except Exception as e:
                self.logger.error(f"更新任务 {task_name} 配置失败: {e}")
                return False

    def enable_task(self, task_name: str) -> bool:
        """启用任务"""
        if task_name in self.task_configs:
            self.task_configs[task_name].enabled = True
            self.logger.info(f"任务 {task_name} 已启用")
            return True
        return False

    def disable_task(self, task_name: str) -> bool:
        """禁用任务"""
        if task_name in self.task_configs:
            self.task_configs[task_name].enabled = False
            self.logger.info(f"任务 {task_name} 已禁用")
            # 如果任务正在运行，停止它
            if task_name in self.tasks and self.tasks[task_name].running:
                self.stop_task(task_name)
            return True
        return False

    def get_scheduler_info(self) -> Dict[str, Any]:
        """
        获取调度器信息

        Returns:
            Dict[str, Any]: 调度器状态信息
        """
        with self._lock:
            total_tasks = len(self.tasks)
            running_tasks = sum(1 for task in self.tasks.values() if task.running)
            enabled_tasks = sum(1 for config in self.task_configs.values() if config.enabled)

            return {
                'total_tasks': total_tasks,
                'running_tasks': running_tasks,
                'enabled_tasks': enabled_tasks,
                'available_task_classes': list(self.get_registered_task_classes().keys()),
                'configured_tasks': list(self.task_configs.keys()),
                'tasks_status': {name: task.stats for name, task in self.tasks.items()}
            }

    def cleanup(self):
        """清理调度器资源"""
        self.logger.info("开始清理调度器资源...")
        self.stop_all_tasks()
        self.logger.info("调度器资源清理完成")