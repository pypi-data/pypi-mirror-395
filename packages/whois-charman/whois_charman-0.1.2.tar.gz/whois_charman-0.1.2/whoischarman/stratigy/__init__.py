from .base_task import BaseTask, TaskRegistryMeta
from .scheduler import BaseScheduler
from .schdule import get_registered_tasks

# 自动载入自定义Task类
try:
    from .auto_loader import load_custom_tasks, get_custom_tasks_info

    # 载入自定义Task类
    custom_tasks = load_custom_tasks()

    # 将自定义Task类注册到TaskRegistryMeta
    for task_name, task_class in custom_tasks.items():
        # 手动注册到TaskRegistryMeta的registry中
        if task_name not in TaskRegistryMeta.registry:
            TaskRegistryMeta.registry[task_name] = task_class
            print(f"✓ 注册自定义Task类: {task_name}")

except ImportError as e:
    print(f"⚠️  自动载入模块导入失败: {e}")
except Exception as e:
    print(f"⚠️  载入自定义Task类时出错: {e}")