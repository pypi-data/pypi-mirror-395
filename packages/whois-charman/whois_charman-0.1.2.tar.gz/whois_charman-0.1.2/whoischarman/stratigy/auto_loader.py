"""
自动载入模块

自动扫描并载入 ~/.schedule_scripts/ 目录下的Python文件中的Task类
"""
import os
import sys
import importlib.util
import inspect
from typing import Dict, List, Type, Any, Optional
from pathlib import Path
import json

from .base_task import BaseTask


class TaskAutoLoader:
    """Task类自动载入器"""

    def __init__(self, scripts_dir: str = None):
        """
        初始化自动载入器

        Args:
            scripts_dir: 脚本目录路径，默认为 ~/.schedule_scripts/
        """
        if scripts_dir is None:
            scripts_dir = os.path.expanduser("~/.schedule_scripts/")

        self.scripts_dir = Path(scripts_dir)
        self.loaded_modules: Dict[str, Any] = {}
        self.loaded_task_classes: Dict[str, Type[BaseTask]] = {}
        self.task_parameters: Dict[str, Dict[str, Any]] = {}  # 存储Task类的参数信息

        # 确保目录存在
        self._ensure_scripts_directory()

    def _ensure_scripts_directory(self):
        """确保脚本目录存在，不存在则创建"""
        try:
            self.scripts_dir.mkdir(parents=True, exist_ok=True)
            print(f"✓ 脚本目录已准备: {self.scripts_dir}")

            # 创建示例文件如果目录为空
            if not any(self.scripts_dir.iterdir()):
                self._create_example_script()

        except Exception as e:
            print(f"⚠️  创建脚本目录失败: {e}")

    def _create_example_script(self):
        """创建示例脚本文件"""
        example_content = '''"""
示例自定义任务

这是一个示例文件，展示如何创建自定义任务类
"""
from whoischarman.stratigy.base_task import BaseTask
from whoischarman.struct.schedule import ScheduleConf
from typing import Any, Dict


class CustomWeatherTask(BaseTask):
    """自定义天气任务示例"""

    def __init__(self, config: ScheduleConf, **kwargs):
        super().__init__(config, **kwargs)
        self.city = kwargs.get('city', 'Beijing')
        self.logger.info(f"自定义天气任务初始化，城市: {self.city}")

    def execute(self) -> Dict[str, Any]:
        """执行天气查询任务"""
        import random

        # 模拟天气数据
        weather_data = {
            'city': self.city,
            'temperature': random.randint(10, 30),
            'humidity': random.randint(30, 80),
            'timestamp': self._get_timestamp()
        }

        self.logger.info(f"{self.city} 天气: {weather_data}")
        return weather_data

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


class DataCollectorTask(BaseTask):
    """数据收集任务示例"""

    def __init__(self, config: ScheduleConf, **kwargs):
        super().__init__(config, **kwargs)
        self.data_source = kwargs.get('data_source', 'default')
        self.logger.info(f"数据收集任务初始化，数据源: {self.data_source}")

    def execute(self) -> Dict[str, Any]:
        """执行数据收集任务"""
        import random

        collected_data = {
            'source': self.data_source,
            'records_count': random.randint(1, 100),
            'status': 'success',
            'timestamp': self._get_timestamp()
        }

        self.logger.info(f"收集到数据: {collected_data}")
        return collected_data

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
'''

        example_file = self.scripts_dir / "example_tasks.py"
        try:
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(example_content)
            print(f"✓ 已创建示例脚本: {example_file}")
        except Exception as e:
            print(f"⚠️  创建示例脚本失败: {e}")
    
    def create_script(self, name: str):
        """创建示例脚本文件"""
        n = name.capitalize()
        example_content = f'''"""
示例自定义任务

这是一个示例文件，展示如何创建自定义任务类
"""
from whoischarman import BaseTask
from whoischarman import DBModel
from whoischarman import ScheduleConf
from typing import Any, Dict

class {n}Table(DBModel):
    """自定义{n}数据表"""
    name: str = "test_name"
    userid: str = "test_userid"
    status: bool = false
    num: int = 0

    _ALIAS = {{
        "userid": "id",
    }}
    


class {n}Task(BaseTask):
    """自定义{n}任务示例"""

    def __init__(self, config: ScheduleConf,user_id: str ,**kwargs):
        super().__init__(config, **kwargs)
        {n}Table.create_table()
        self.user_id = user_id

    def execute(self) -> Dict[str, Any]:
        """执行天气查询任务"""
        import random

        # 模拟天气数据
        all_ids = {n}Table.get_all_ids()
        
        

        self.logger.info(f"🔍 正在执行...{n} Task \n {{all_ids}}")
        new_t = {n}Table(user_id=self.user_id, num=random.randint(0, 100))
        new_t.save()
        return '{n}'
'''

        return example_content

    def scan_and_load_tasks(self) -> Dict[str, Type[BaseTask]]:
        """
        扫描并载入所有Python文件中的Task类

        Returns:
            Dict[str, Type[BaseTask]]: 载入的Task类字典
        """
        self.loaded_task_classes.clear()

        if not self.scripts_dir.exists():
            print(f"⚠️  脚本目录不存在: {self.scripts_dir}")
            return {}

        # 扫描Python文件
        python_files = list(self.scripts_dir.glob("*.py"))

        if not python_files:
            print(f"📂 脚本目录为空: {self.scripts_dir}")
            return {}

        print(f"🔍 扫描脚本目录: {self.scripts_dir}")
        print(f"📄 发现 {len(python_files)} 个Python文件")

        for py_file in python_files:
            if py_file.name.startswith("__"):
                continue  # 跳过__init__.py等文件

            try:
                task_classes = self._load_tasks_from_file(py_file)
                self.loaded_task_classes.update(task_classes)

            except Exception as e:
                print(f"❌ 载入文件失败 {py_file}: {e}")

        if self.loaded_task_classes:
            print(f"✅ 成功载入 {len(self.loaded_task_classes)} 个Task类:")
            for name in self.loaded_task_classes.keys():
                print(f"   - {name}")
        else:
            print("📭 未发现任何Task类")

        return self.loaded_task_classes

    def _load_tasks_from_file(self, py_file: Path) -> Dict[str, Type[BaseTask]]:
        """
        从单个Python文件中载入Task类

        Args:
            py_file: Python文件路径

        Returns:
            Dict[str, Type[BaseTask]]: 该文件中的Task类字典
        """
        # 获取项目根目录路径
        project_root = Path(__file__).parent.parent.parent.parent  # 从 whoischarman/stratigy/ 回到项目根目录

        # 临时添加项目根目录到 sys.path
        original_path = sys.path[:]
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        try:
            # 构建模块名
            module_name = f"schedule_scripts.{py_file.stem}"

            # 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"无法创建模块规范: {py_file}")

            module = importlib.util.module_from_spec(spec)

            # 将模块添加到sys.modules中，以支持相对导入
            sys.modules[module_name] = module

            # 设置模块的__package__属性以支持相对导入
            module.__package__ = "whoischarman.stratigy"

            spec.loader.exec_module(module)
        except Exception as e:
            raise ImportError(f"执行模块失败: {e}")
        finally:
            # 恢复原始 sys.path
            sys.path[:] = original_path

        # 保存模块引用
        self.loaded_modules[module_name] = module

        # 扫描模块中的Task类
        task_classes = {}

        for name, obj in inspect.getmembers(module, inspect.isclass):
            # 检查是否是BaseTask的子类，但不是BaseTask本身
            if (hasattr(obj, '__bases__') and
                any(base.__name__ == 'BaseTask' for base in obj.__bases__) and
                obj.__name__ != 'BaseTask'):

                task_classes[name] = obj
                print(f"   ✓ 发现Task类: {name} (来自 {py_file.name})")

                # 检测并存储Task类的参数信息
                parameters = self._detect_task_parameters(obj)
                self.task_parameters[name] = parameters

                if parameters:
                    print(f"      🔧 参数: {list(parameters.keys())}")
                    for param_name, param_info in parameters.items():
                        required_text = "必需" if param_info['required'] else f"可选(默认: {param_info['default']})"
                        print(f"         - {param_name}: {param_info['type']} ({required_text})")

        return task_classes

    def _detect_task_parameters(self, task_class: Type[BaseTask]) -> Dict[str, Any]:
        """
        检测Task类的__init__方法参数

        Args:
            task_class: Task类

        Returns:
            Dict[str, Any]: 参数信息字典
        """
        try:
            # 获取__init__方法的签名
            init_method = task_class.__init__
            sig = inspect.signature(init_method)

            parameters = {}

            for param_name, param in sig.parameters.items():
                # 跳过self和config参数，这些是BaseTask必需的
                if param_name in ['self', 'config']:
                    continue

                param_info = {
                    'name': param_name,
                    'type': str(param.annotation) if param.annotation != param.empty else 'Any',
                    'default': None,
                    'required': param.default == param.empty,
                    'description': f'Parameter {param_name}'
                }

                # 处理默认值
                if param.default != param.empty:
                    # 尝试序列化默认值，如果失败则转为字符串
                    try:
                        param_info['default'] = json.loads(json.dumps(param.default, default=str))
                    except:
                        param_info['default'] = str(param.default)

                # 处理特殊类型注解
                if param.annotation != param.empty:
                    origin = getattr(param.annotation, '__origin__', None)
                    if origin is not None:
                        # 处理泛型类型如 List[str], Dict[str, int] 等
                        param_info['type'] = f"{origin.__name__}{getattr(param.annotation, '__args__', '')}"

                parameters[param_name] = param_info

            return parameters

        except Exception as e:
            print(f"⚠️  检测 {task_class.__name__} 参数失败: {e}")
            return {}

    def reload_tasks(self) -> Dict[str, Type[BaseTask]]:
        """
        重新载入所有Task类

        Returns:
            Dict[str, Type[BaseTask]]: 重新载入的Task类字典
        """
        print("🔄 重新载入自定义Task类...")

        # 清除已载入的模块
        for module_name in list(self.loaded_modules.keys()):
            if module_name in sys.modules:
                del sys.modules[module_name]

        self.loaded_modules.clear()
        self.loaded_task_classes.clear()
        self.task_parameters.clear()

        # 重新扫描和载入
        return self.scan_and_load_tasks()

    def get_loaded_tasks(self) -> Dict[str, Type[BaseTask]]:
        """
        获取已载入的Task类

        Returns:
            Dict[str, Type[BaseTask]]: 已载入的Task类字典
        """
        return self.loaded_task_classes.copy()

    def get_task_parameters(self, task_name: str) -> Dict[str, Any]:
        """
        获取指定Task类的参数信息

        Args:
            task_name: Task类名

        Returns:
            Dict[str, Any]: 参数信息字典
        """
        return self.task_parameters.get(task_name, {})

    def get_all_task_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有Task类的参数信息

        Returns:
            Dict[str, Dict[str, Any]]: 所有Task类的参数信息
        """
        return self.task_parameters.copy()

    def get_scripts_info(self) -> Dict[str, Any]:
        """
        获取脚本目录信息

        Returns:
            Dict[str, Any]: 脚本目录信息
        """
        return {
            'scripts_directory': str(self.scripts_dir),
            'exists': self.scripts_dir.exists(),
            'python_files': len(list(self.scripts_dir.glob("*.py"))) if self.scripts_dir.exists() else 0,
            'loaded_modules': len(self.loaded_modules),
            'loaded_task_classes': len(self.loaded_task_classes),
            'task_class_names': list(self.loaded_task_classes.keys()),
            'task_parameters': {name: list(params.keys()) for name, params in self.task_parameters.items()}
        }


# 全局自动载入器实例
_auto_loader = None


def get_auto_loader() -> TaskAutoLoader:
    """
    获取全局自动载入器实例

    Returns:
        TaskAutoLoader: 自动载入器实例
    """
    global _auto_loader
    if _auto_loader is None:
        _auto_loader = TaskAutoLoader()
    return _auto_loader


def load_custom_tasks() -> Dict[str, Type[BaseTask]]:
    """
    载入自定义Task类

    Returns:
        Dict[str, Type[BaseTask]]: 载入的Task类字典
    """
    return get_auto_loader().scan_and_load_tasks()


def reload_custom_tasks() -> Dict[str, Type[BaseTask]]:
    """
    重新载入自定义Task类

    Returns:
        Dict[str, Type[BaseTask]]: 重新载入的Task类字典
    """
    return get_auto_loader().reload_tasks()


def get_custom_tasks_info() -> Dict[str, Any]:
    """
    获取自定义Task信息

    Returns:
        Dict[str, Any]: 自定义Task信息
    """
    return get_auto_loader().get_scripts_info()


def get_task_parameters(task_name: str) -> Dict[str, Any]:
    """
    获取指定Task类的参数信息

    Args:
        task_name: Task类名

    Returns:
        Dict[str, Any]: 参数信息字典
    """
    return get_auto_loader().get_task_parameters(task_name)


def get_all_task_parameters() -> Dict[str, Dict[str, Any]]:
    """
    获取所有Task类的参数信息

    Returns:
        Dict[str, Dict[str, Any]]: 所有Task类的参数信息
    """
    return get_auto_loader().get_all_task_parameters()


class ScriptValidator:
    """脚本验证器"""

    def __init__(self):
        self.required_imports = [
            'BaseTask',
            'ScheduleConf'
        ]
        self.forbidden_patterns = [
            'os.system',
            'subprocess.call',
            'subprocess.run',
            'eval(',
            'exec(',
            '__import__',
            'open(',
            'file('
        ]

    def validate_script(self, script_path: str) -> Dict[str, Any]:
        """
        验证脚本文件

        Args:
            script_path: 脚本文件路径

        Returns:
            Dict[str, Any]: 验证结果
        """
        result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'task_classes': [],
            'security_issues': []
        }

        try:
            script_path = Path(script_path)

            # 检查文件是否存在
            if not script_path.exists():
                result['errors'].append(f"文件不存在: {script_path}")
                return result

            # 检查文件扩展名
            if script_path.suffix != '.py':
                result['errors'].append("文件必须是Python文件 (.py)")
                return result

            # 读取文件内容
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                result['errors'].append(f"无法读取文件: {e}")
                return result

            # 基本语法检查
            try:
                compile(content, str(script_path), 'exec')
            except SyntaxError as e:
                result['errors'].append(f"语法错误: {e}")
                return result

            # 安全检查
            security_issues = self._check_security(content)
            result['security_issues'] = security_issues

            # 检查必要的导入
            import_issues = self._check_imports(content)
            result['warnings'].extend(import_issues)

            # 尝试加载并检查Task类
            try:
                task_classes = self._check_task_classes(script_path)
                result['task_classes'] = task_classes

                if not task_classes:
                    result['warnings'].append("未发现任何继承自BaseTask的类")

            except Exception as e:
                result['errors'].append(f"加载Task类时出错: {e}")
                return result

            # 如果有严重安全问题，拒绝安装
            critical_issues = [issue for issue in security_issues if issue['severity'] == 'critical']
            if critical_issues:
                result['errors'].append("发现严重安全问题，拒绝安装")
                for issue in critical_issues:
                    result['errors'].append(f"  - {issue['message']}")
                return result

            # 如果有Task类且没有严重错误，则认为有效
            if task_classes and not result['errors']:
                result['valid'] = True

        except Exception as e:
            result['errors'].append(f"验证过程中出错: {e}")

        return result

    def _check_security(self, content: str) -> List[Dict[str, Any]]:
        """检查安全性问题"""
        issues = []

        for pattern in self.forbidden_patterns:
            if pattern in content:
                severity = 'critical' if pattern in ['eval(', 'exec(', '__import__'] else 'warning'
                issues.append({
                    'pattern': pattern,
                    'message': f"发现潜在危险的函数调用: {pattern}",
                    'severity': severity
                })

        # 检查网络访问
        network_patterns = ['requests.', 'urllib.', 'http.', 'socket.']
        for pattern in network_patterns:
            if pattern in content:
                issues.append({
                    'pattern': pattern,
                    'message': f"发现网络访问代码: {pattern}",
                    'severity': 'warning'
                })

        # 检查文件系统操作
        file_patterns = ['shutil.', 'os.remove', 'os.rmdir', 'os.mkdir']
        for pattern in file_patterns:
            if pattern in content:
                issues.append({
                    'pattern': pattern,
                    'message': f"发现文件系统操作: {pattern}",
                    'severity': 'warning'
                })

        return issues

    def _check_imports(self, content: str) -> List[str]:
        """检查必要的导入"""
        issues = []

        has_basetask = 'BaseTask' in content
        has_scheduleconf = 'ScheduleConf' in content

        if not has_basetask:
            issues.append("建议导入 BaseTask 类")

        if not has_scheduleconf:
            issues.append("建议导入 ScheduleConf 类")

        return issues

    def _check_task_classes(self, script_path: Path) -> List[str]:
        """检查Task类"""
        task_classes = []

        try:
            # 创建临时模块名
            module_name = f"temp_validation_{script_path.stem}"
            spec = importlib.util.spec_from_file_location(module_name, script_path)

            if spec is None or spec.loader is None:
                return task_classes

            module = importlib.util.module_from_spec(spec)

            # 临时添加到sys.modules
            sys.modules[module_name] = module

            try:
                spec.loader.exec_module(module)

                # 查找Task类
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if (hasattr(obj, '__bases__') and
                        any(base.__name__ == 'BaseTask' for base in obj.__bases__) and
                        obj.__name__ != 'BaseTask'):
                        task_classes.append(name)

            finally:
                # 清理临时模块
                if module_name in sys.modules:
                    del sys.modules[module_name]

        except Exception:
            # 忽略加载错误，由调用者处理
            pass

        return task_classes


def install_script(script_path: str, force: bool = False) -> Dict[str, Any]:
    """
    安装脚本到 ~/.schedule_scripts/ 目录

    Args:
        script_path: 源脚本路径
        force: 是否强制安装（覆盖已存在的文件）

    Returns:
        Dict[str, Any]: 安装结果
    """
    result = {
        'success': False,
        'message': '',
        'validation_result': None,
        'installed_path': None
    }

    try:
        script_path = Path(script_path)

        # 验证脚本
        validator = ScriptValidator()
        validation_result = validator.validate_script(script_path)
        result['validation_result'] = validation_result

        if not validation_result['valid']:
            result['message'] = "脚本验证失败，无法安装"
            if validation_result['errors']:
                result['message'] += f": {'; '.join(validation_result['errors'])}"
            return result

        # 目标目录
        target_dir = Path(os.path.expanduser("~/.schedule_scripts/"))
        target_dir.mkdir(parents=True, exist_ok=True)

        # 目标文件路径
        target_file = target_dir / script_path.name

        # 检查文件是否已存在
        if target_file.exists() and not force:
            result['message'] = f"目标文件已存在: {target_file} (使用 --force 强制覆盖)"
            return result

        # 复制文件
        import shutil
        shutil.copy2(script_path, target_file)

        result['success'] = True
        result['installed_path'] = str(target_file)
        result['message'] = f"脚本安装成功: {target_file}"

        # 显示发现的Task类
        if validation_result['task_classes']:
            result['message'] += f" (包含Task类: {', '.join(validation_result['task_classes'])})"

        # 显示警告信息
        if validation_result['warnings']:
            result['message'] += f" [警告: {'; '.join(validation_result['warnings'])}]"

        # 显示安全问题
        if validation_result['security_issues']:
            security_warnings = [issue['message'] for issue in validation_result['security_issues']
                               if issue['severity'] == 'warning']
            if security_warnings:
                result['message'] += f" [安全提醒: {'; '.join(security_warnings)}]"

    except Exception as e:
        result['message'] = f"安装失败: {e}"

    return result


def list_scripts() -> Dict[str, Any]:
    """
    列出 ~/.schedule_scripts/ 目录中的所有脚本

    Returns:
        Dict[str, Any]: 脚本列表信息
    """
    result = {
        'scripts_dir': str(Path(os.path.expanduser("~/.schedule_scripts/"))),
        'exists': False,
        'scripts': [],
        'total_count': 0,
        'task_classes_count': 0
    }

    try:
        scripts_dir = Path(result['scripts_dir'])
        result['exists'] = scripts_dir.exists()

        if not scripts_dir.exists():
            return result

        # 扫描Python文件
        script_files = list(scripts_dir.glob("*.py"))
        result['total_count'] = len(script_files)

        validator = ScriptValidator()
        total_task_classes = 0

        for script_file in script_files:
            if script_file.name.startswith("__"):
                continue

            # 验证脚本
            validation_result = validator.validate_script(script_file)

            script_info = {
                'name': script_file.name,
                'path': str(script_file),
                'size': script_file.stat().st_size,
                'modified_time': script_file.stat().st_mtime,
                'task_classes': validation_result['task_classes'],
                'valid': validation_result['valid'],
                'errors': validation_result['errors'],
                'warnings': validation_result['warnings'],
                'security_issues': len(validation_result['security_issues'])
            }

            result['scripts'].append(script_info)
            total_task_classes += len(validation_result['task_classes'])

        result['task_classes_count'] = total_task_classes

    except Exception as e:
        result['error'] = str(e)

    return result


def create_script_template(script_name: str) -> str:
    """
    创建脚本模板

    Args:
        script_name: 脚本名称

    Returns:
        str: 创建的脚本路径
    """
    scripts_dir = Path(os.path.expanduser("~/.schedule_scripts/"))
    scripts_dir.mkdir(parents=True, exist_ok=True)

    script_path = scripts_dir / f"{script_name}.py"

    template = f'''"""
{script_name} - 自定义任务脚本

使用说明:
1. 继承 BaseTask 类创建自定义任务
2. 实现 execute() 方法定义任务逻辑
3. 使用 self.logger 记录日志
4. 通过 kwargs 传递自定义参数
"""
import sys
import os
from datetime import datetime
from typing import Dict, Any

# 添加项目路径到sys.path
project_path = os.path.expanduser("/Users/mroy/Codes/Go/src/git.me/dr/whois-charman")
if project_path not in sys.path:
    sys.path.append(project_path)

from whoischarman.stratigy.base_task import BaseTask
from whoischarman.struct.schedule import ScheduleConf


class {script_name.title().replace('_', '')}Task(BaseTask):
    """
    自定义任务类

    在execute()方法中实现你的任务逻辑
    """

    def __init__(self, config: ScheduleConf, **kwargs):
        super().__init__(config, **kwargs)

        # 从kwargs中获取自定义参数
        self.custom_param = kwargs.get('custom_param', 'default_value')

        self.logger.info(f"{{self.__class__.__name__}} 任务初始化完成")
        self.logger.info(f"自定义参数: {{self.custom_param}}")

    def execute(self) -> Dict[str, Any]:
        """
        执行任务逻辑

        Returns:
            Dict[str, Any]: 任务执行结果
        """
        self.logger.info("开始执行任务...")

        try:
            # TODO: 在这里实现你的任务逻辑
            result = {{
                'task_name': self.__class__.__name__,
                'custom_param': self.custom_param,
                'execution_time': datetime.now().isoformat(),
                'status': 'completed',
                'message': '任务执行成功'
            }}

            self.logger.info(f"任务执行完成: {{result}}")
            return result

        except Exception as e:
            self.logger.error(f"任务执行失败: {{e}}")
            raise


# 你可以在这个文件中定义多个Task类
class AnotherCustomTask(BaseTask):
    """另一个自定义任务示例"""

    def execute(self) -> Dict[str, Any]:
        """简单示例任务"""
        return {{
            'message': '这是另一个自定义任务',
            'timestamp': datetime.now().isoformat()
        }}
'''

    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(template)

        return str(script_path)

    except Exception as e:
        raise Exception(f"创建脚本模板失败: {e}")