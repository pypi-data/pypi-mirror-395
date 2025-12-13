"""
调度器模块统一入口

提供统一的调度器接口和便捷函数
"""
from .scheduler import BaseScheduler
from .base_task import BaseTask, TaskRegistryMeta
from ..struct.schedule import ScheduleConf

# 导出主要类和函数
__all__ = [
    'BaseScheduler',
    'BaseTask',
    'TaskRegistryMeta',
    'ScheduleConf',
    'create_scheduler',
    'create_simple_task',
    'get_registered_tasks',
    'quick_start_scheduler'
]


def create_scheduler() -> BaseScheduler:
    """
    创建调度器实例

    Returns:
        BaseScheduler: 调度器实例
    """
    return BaseScheduler()


def create_simple_task(task_class_name: str,
                      interval_seconds: int = 60,
                      enabled: bool = False,
                      max_executions: int = -1,
                      **kwargs) -> tuple[ScheduleConf, dict]:
    """
    创建简单任务配置

    Args:
        task_class_name: 任务类名
        interval_seconds: 执行间隔（秒）
        enabled: 是否启用
        max_executions: 最大执行次数（-1为无限）
        **kwargs: 其他配置参数

    Returns:
        tuple[ScheduleConf, dict]: (配置对象, 任务参数)
    """
    config = ScheduleConf(
        name=task_class_name,
        interval_seconds=interval_seconds,
        enabled=enabled,
        max_executions=max_executions,
        **kwargs
    )

    task_params = {
        'task_name': task_class_name,
        'config': config
    }

    return config, task_params


def get_registered_tasks():
    """
    获取所有已注册的任务类

    Returns:
        Dict[str, Type]: 任务名称到任务类的映射
    """
    return TaskRegistryMeta.get_registered_tasks()


def quick_start_scheduler(task_configs: list[tuple[str, ScheduleConf, dict]]) -> BaseScheduler:
    """
    快速启动调度器并添加多个任务

    Args:
        task_configs: 任务配置列表，格式为 [(task_name, config, kwargs), ...]

    Returns:
        BaseScheduler: 已启动的调度器实例
    """
    scheduler = create_scheduler()

    for task_name, config, kwargs in task_configs:
        success = scheduler.add_task(task_name, config, **kwargs)
        if not success:
            print(f"警告: 添加任务 {task_name} 失败")

    # 启动所有启用的任务
    results = scheduler.start_all_tasks()
    print(f"任务启动结果: {results}")

    return scheduler


# 示例使用代码
if __name__ == "__main__":
    # 示例：创建调度器并查看信息
    scheduler = create_scheduler()

    print("调度器信息:")
    info = scheduler.get_scheduler_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    print("\n已注册的任务类:")
    registered = get_registered_tasks()
    for name, task_class in registered.items():
        print(f"  {name}: {task_class}")