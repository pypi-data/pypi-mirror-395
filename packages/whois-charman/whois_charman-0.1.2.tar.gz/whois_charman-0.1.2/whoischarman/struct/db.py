import datetime
import time
import sqlite3
import json
import typing
from pathlib import Path
from contextlib import contextmanager
from loguru import logger
from dateutil import parser as date_parser
from typing import Optional 
from typing import Dict 
from typing import Any
from typing import List 
from typing import ClassVar 
from typing import Type 
from typing import TypeVar 
from pydantic import BaseModel

T = TypeVar('T', bound='DBModel')

def parse_datetime(date_str: str) -> datetime.datetime:
    """增强的datetime解析，处理各种时区格式"""
    try:
        # 尝试使用 dateutil 默认解析
        return date_parser.parse(date_str)
    except (ValueError, TypeError):
        # 处理特殊时区格式，如 "2020-11-02 16:31:01+00"
        import re

        # 匹配模式: YYYY-MM-DD HH:MM:SS+HH or +HHMM
        timezone_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})([+-]\d{2})(?::?(\d{2}))?$'
        match = re.match(timezone_pattern, date_str.strip())

        if match:
            base_time_str, timezone_hour, timezone_min = match.groups()

            try:
                # 先解析基础时间部分
                base_time = datetime.datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")

                # 处理时区偏移
                if timezone_hour:
                    hours = int(timezone_hour)
                    minutes = int(timezone_min) if timezone_min else 0

                    # 如果是负时区
                    if hours < 0:
                        minutes = -minutes
                    total_offset_minutes = hours * 60 + minutes

                    # 创建时区
                    import datetime as dt
                    tz = dt.timezone(dt.timedelta(minutes=total_offset_minutes))
                    return base_time.replace(tzinfo=tz)
                else:
                    return base_time

            except ValueError:
                pass

        # 如果还是失败，尝试其他常见格式
        common_formats = [
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
        ]

        for fmt in common_formats:
            try:
                return datetime.datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        # 如果所有尝试都失败，抛出原始异常
        raise ValueError(f"Unable to parse datetime string: {date_str}")
class DBModel(BaseModel):

    _DB: ClassVar[Optional[str]] = str(Path("~").expanduser() / ".whois-charman"/"dbs"/ "cache.db" )  # 数据库文件路径，子类需要指定

    # 数据库连接缓存
    _toggle_create: ClassVar[bool] = False
    _connections: ClassVar[Dict[str, sqlite3.Connection]] = {}
    id: str # 有些事slug 有些是 ticker

    open_time:Optional[datetime.datetime] = None
    close_time: Optional[datetime.datetime] = None

    _ALIAS:ClassVar = { }
    class Config:
        extra = "ignore"  # Allow extra fields from API responses
        validate_by_name = True

    def __init__(self, **data):
        # Apply _ALIAS mapping during initialization
        if hasattr(self.__class__, '_ALIAS') and self.__class__._ALIAS:
            # Create a copy of data to avoid modifying the original
            processed_data = {}
            for key, value in data.items():
                # Map field names using _ALIAS if a mapping exists
                mapped_key = self.__class__._ALIAS.get(key, key)
                processed_data[mapped_key] = value
            data = processed_data

        # Apply automatic type conversion
        data = self._convert_types(data)

        # Apply special value transformations (same as in from_exchange)
        if "state" in data:               # Huobi 的 state 转 closed
            data["closed"] = bool(int(data.pop("state")))
        if "enable" in data:              # OKX 的 enable 转 active
            data["active"] = bool(int(data.pop("enable")))
        try:
            super().__init__(**data)
        except Exception as e:
            # r = json.dumps(data, indent=4)
            logger.warning(f'{data}')
            raise e

    def _convert_types(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """根据目标字段类型自动转换输入数据"""
        if not data:
            return data

        processed_data = data.copy()

        for field_name, field_info in self.__class__.model_fields.items():
            if field_name not in processed_data:
                continue

            value = processed_data[field_name]
            if value is None:
                continue

            target_type = field_info.annotation
            converted_value = self._try_convert_value(value, target_type)
            if converted_value is not None:
                processed_data[field_name] = converted_value

        return processed_data

    def _try_convert_value(self, value: Any, target_type) -> Any:
        """尝试将值转换为目标类型"""
        if value is None:
            return None

        # 处理 Optional 和 Union 类型
        if typing.get_origin(target_type) is typing.Union:
            args = typing.get_args(target_type)
            # 找到非 NoneType 的类型
            for arg_type in args:
                if arg_type is not type(None):
                    try:
                        # 尝试转换到第一个非 None 类型
                        return self._convert_to_type(value, arg_type)
                    except (ValueError, TypeError):
                        continue
            return None

        # 如果类型已经匹配，直接返回
        try:
            if isinstance(value, target_type):
                return value
        except TypeError:
            # target_type 可能是 typing 对象，继续处理
            pass

        # 直接类型转换
        try:
            return self._convert_to_type(value, target_type)
        except (ValueError, TypeError):
            # 转换失败，返回原值让pydantic处理
            return value

    def _convert_to_type(self, value: Any, target_type) -> Any:
        """执行具体的类型转换"""
        type_str = str(target_type).lower()

        # DateTime转换
        if 'datetime' in type_str:
            if isinstance(value, str):
                return self._parse_datetime(value)
            elif isinstance(value, (int, float)):
                return datetime.datetime.fromtimestamp(value)

        # Date转换
        elif 'date' in type_str and 'datetime' not in type_str:
            if isinstance(value, str):
                return self._parse_datetime(value).date()
            elif isinstance(value, (int, float)):
                return datetime.datetime.fromtimestamp(value).date()

        # Time转换
        elif 'time' in type_str and 'datetime' not in type_str:
            if isinstance(value, str):
                return self._parse_datetime(value).time()

        # Float转换
        elif 'float' in type_str:
            return float(value)

        # Int转换
        elif 'int' in type_str:
            return int(value)

        # Bool转换
        elif 'bool' in type_str:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)

        # 其他类型直接返回
        return value

    def _parse_datetime(self, date_str: str) -> datetime.datetime:
        """增强的datetime解析，处理各种时区格式"""
        try:
            # 尝试使用 dateutil 默认解析
            return date_parser.parse(date_str)
        except (ValueError, TypeError):
            # 处理特殊时区格式，如 "2020-11-02 16:31:01+00"
            import re

            # 匹配模式: YYYY-MM-DD HH:MM:SS+HH or +HHMM
            timezone_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})([+-]\d{2})(?::?(\d{2}))?$'
            match = re.match(timezone_pattern, date_str.strip())

            if match:
                base_time_str, timezone_hour, timezone_min = match.groups()

                try:
                    # 先解析基础时间部分
                    base_time = datetime.datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")

                    # 处理时区偏移
                    if timezone_hour:
                        hours = int(timezone_hour)
                        minutes = int(timezone_min) if timezone_min else 0

                        # 如果是负时区
                        if hours < 0:
                            minutes = -minutes
                        total_offset_minutes = hours * 60 + minutes

                        # 创建时区
                        import datetime as dt
                        tz = dt.timezone(dt.timedelta(minutes=total_offset_minutes))
                        return base_time.replace(tzinfo=tz)
                    else:
                        return base_time

                except ValueError:
                    pass

            # 如果还是失败，尝试其他常见格式
            common_formats = [
                "%Y-%m-%d %H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
            ]

            for fmt in common_formats:
                try:
                    return datetime.datetime.strptime(date_str.strip(), fmt)
                except ValueError:
                    continue

            # 如果所有尝试都失败，抛出原始异常
            raise ValueError(f"Unable to parse datetime string: {date_str}")

    @classmethod
    def get_db_path(cls) -> str:
        """获取数据库文件路径"""
        if cls._DB is None:
            raise ValueError(f"{cls.__name__}._DB 未设置，请在子类中指定数据库路径")
        return cls._DB

    @classmethod
    @contextmanager
    def get_db_connection(cls):
        """获取数据库连接（上下文管理器）"""
        db_path = cls.get_db_path()

        # 确保数据库目录存在
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # 使用连接池
        conn_key = f"{cls.__name__}_{db_path}"
        if conn_key not in cls._connections:
            cls._connections[conn_key] = sqlite3.connect(db_path, check_same_thread=False)
            cls._connections[conn_key].row_factory = sqlite3.Row  # 使结果可以通过列名访问

        conn = cls._connections[conn_key]
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            logger.error(f"数据库操作失败: {e} / {db_path}")
            raise
        finally:
            pass  # 不关闭连接，保持连接池

    @classmethod
    def get_table_name(cls) -> str:
        """获取表名（使用类名）"""
        return cls.__name__.lower()

    @classmethod
    def _model_to_sql_type(cls, field_type) -> str:
        """将 Pydantic 字段类型转换为 SQLite 类型"""
        type_str = str(field_type).lower()

        if 'int' in type_str:
            return 'INTEGER'
        elif 'float' in type_str or 'decimal' in type_str:
            return 'REAL'
        elif 'bool' in type_str:
            return 'INTEGER'  # SQLite 没有布尔类型，用 INTEGER 表示
        elif 'datetime' in type_str or 'date' in type_str or 'time' in type_str:
            return 'TEXT'  # 日期时间存储为 TEXT
        elif 'list' in type_str or 'dict' in type_str:
            return 'TEXT'  # 复杂类型序列化为 JSON 存储为 TEXT
        else:
            return 'TEXT'  # 默认为 TEXT

    @classmethod
    def get_create_table_sql(cls) -> str:
        """生成创建表的 SQL 语句"""
        table_name = cls.get_table_name()

        # 获取模型字段
        fields = cls.model_fields
        sql_parts = [f"id TEXT PRIMARY KEY"]  # 添加主键

        for field_name, field_info in fields.items():
            if field_name == 'id':
                continue  # 跳过已定义的 id 字段

            sql_type = cls._model_to_sql_type(field_info.annotation)
            sql_parts.append(f"{field_name} {sql_type}")

        # 添加创建和更新时间（如果没有已存在）
        existing_fields = {field_name for field_name in cls.model_fields.keys()}
        if 'created_at' not in existing_fields:
            sql_parts.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        if 'updated_at' not in existing_fields:
            sql_parts.append("updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(sql_parts)})"

    @classmethod
    def create_table(cls) -> bool:
        """创建数据表"""
        try:
            with cls.get_db_connection() as conn:
                sql = cls.get_create_table_sql()
                conn.execute(sql)
                conn.commit()
                logger.info(f"表 {cls.get_table_name()} 创建成功")
                return True
        except Exception as e:
            logger.error(f"创建表失败: {e}")
            return False

    @classmethod
    def _serialize_value(cls, value: Any) -> Any:
        """序列化值用于数据库存储"""
        if value is None:
            return None
        elif isinstance(value, DBModel):
            # 如果是DBModel实例，递归调用save并返回其ID
            try:
                value.save()  # 先保存嵌套对象
                return value.id  # 存储嵌套对象的ID
            except Exception as e:
                logger.error(f"保存嵌套对象失败: {e}")
                return None
        elif isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False)
        elif isinstance(value, datetime.datetime):
            return value.isoformat()
        elif isinstance(value, (bool,)):
            return int(value)
        else:
            return value

    @classmethod
    def _deserialize_value(cls, value: Any, field_type) -> Any:
        """反序列化数据库值"""
        if value is None:
            return None

        # 检查是否是DBModel类型
        import typing
        if hasattr(field_type, '__origin__') and field_type.__origin__ is list:
            # 处理列表类型
            args = typing.get_args(field_type)
            if len(args) == 1 and isinstance(args[0], type) and issubclass(args[0], DBModel):
                # 如果是DBModel列表，从ID列表重新加载对象
                try:
                    ids = json.loads(value) if isinstance(value, str) else value
                    if isinstance(ids, list):
                        # 尝试使用调用类的子类类型而不是硬编码的基类类型
                        model_type = args[0]

                        # 检查调用类是否有对应的Item子类
                        if hasattr(cls, 'Itype'):
                            model_type = cls.Itype
                        else:
                            # 尝试根据类名推断对应的Item类
                            raise AttributeError(f"Cannot infer Item class for {cls.__name__}. must define Itype!!!")
                        return [model_type.get_by_id(item_id) for item_id in ids if item_id]
                except (json.JSONDecodeError, TypeError, AttributeError):
                    return []
            else:
                # 普通列表，按原逻辑处理
                try:
                    return json.loads(value) if isinstance(value, str) else value
                except (json.JSONDecodeError, TypeError):
                    return value if isinstance(value, list) else []

        # 检查是否是Optional[DBModel]
        if hasattr(field_type, '__origin__') and field_type.__origin__ is typing.Union:
            args = typing.get_args(field_type)
            for arg in args:
                if isinstance(arg, type) and issubclass(arg, DBModel):
                    # 找到DBModel类型，从ID重新加载对象
                    return arg.get_by_id(value)

        elif isinstance(field_type, type) and issubclass(field_type, DBModel):
            # 如果是单个DBModel，从ID重新加载对象
            return field_type.get_by_id(value)

        # 原有的类型处理逻辑
        type_str = str(field_type).lower()

        if 'list' in type_str or 'dict' in type_str:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        elif 'bool' in type_str:
            return bool(value)
        elif 'int' in type_str:
            return int(value) if value is not None else None
        elif 'float' in type_str:
            return float(value) if value is not None else None
        elif 'datetime' in type_str:
            try:
                return datetime.datetime.fromisoformat(value)
            except (ValueError, TypeError):
                return value
        else:
            return value

    def _to_db_dict(self) -> Dict[str, Any]:
        """将模型转换为数据库字典"""
        data = {}

        # 确保有 id 字段
        if hasattr(self, 'id') and self.id:
            data['id'] = self.id
        elif hasattr(self, 'slug') and self.slug:
            data['id'] = self.slug
        else:
            # 生成一个唯一的 ID
            data['id'] = f"{self.__class__.__name__}_{int(time.time())}_{id(self)}"

        # 处理其他字段 - 使用类级别的model_fields访问
        for field_name in self.__class__.model_fields.keys():
            if field_name == 'id':
                continue

            value = getattr(self, field_name, None)
            data[field_name] = self._serialize_value_for_field(value, field_name)

        return data

    def _serialize_value_for_field(self, value: Any, field_name: str) -> Any:
        """为特定字段序列化值，处理嵌套结构"""
        if value is None:
            return None

        # 处理DBModel列表（如items字段）
        elif isinstance(value, list) and value:
            if all(isinstance(item, DBModel) for item in value):
                # 如果列表中所有元素都是DBModel，保存它们并返回ID列表
                ids = []
                for item in value:
                    try:
                        item.save()
                        ids.append(item.id)
                    except Exception as e:
                        logger.error(f"保存嵌套对象列表中的项目失败，字段: {field_name}, 错误: {e}")
                        continue
                return json.dumps(ids, ensure_ascii=False) if ids else None
            else:
                # 普通列表，直接序列化
                return json.dumps([self._serialize_value(item) for item in value], ensure_ascii=False)

        # 处理单个DBModel
        elif isinstance(value, DBModel):
            # 如果是DBModel实例，递归调用save并返回其ID
            try:
                value.save()  # 先保存嵌套对象
                return value.id  # 存储嵌套对象的ID
            except Exception as e:
                logger.error(f"保存嵌套对象失败，字段: {field_name}, 错误: {e}")
                return None

        # 其他情况使用原有的序列化逻辑
        else:
            return self._serialize_value(value)

    @classmethod
    def _from_db_row(cls, row: sqlite3.Row) -> 'DBModel':
        """从数据库行创建模型实例"""
        data = {}

        for field_name, field_info in cls.model_fields.items():
            if field_name in row.keys():
                raw_value = row[field_name]
                data[field_name] = cls._deserialize_value(raw_value, field_info.annotation)

        return cls(**data)

    def save(self) -> bool:
        """保存实例到数据库（插入或更新）"""
        try:
            if not self.__class__._toggle_create:
                self.__class__.create_table()
                self.__class__._toggle_create = True

            with self.get_db_connection() as conn:
                table_name = self.get_table_name()
                data = self._to_db_dict()
                id_value = data['id']

                # 检查记录是否已存在
                cursor = conn.execute(f"SELECT id FROM {table_name} WHERE id = ?", (id_value,))
                exists = cursor.fetchone() is not None

                if exists:
                    # 更新现有记录
                    set_clause = ', '.join([f"{k} = ?" for k in data.keys() if k != 'id'])
                    values = [v for k, v in data.items() if k != 'id'] + [id_value]

                    sql = f"UPDATE {table_name} SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
                    conn.execute(sql, values)
                    logger.debug(f"更新记录 {id_value}")
                else:
                    # 插入新记录
                    columns = ', '.join(data.keys())
                    placeholders = ', '.join(['?'] * len(data))
                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    conn.execute(sql, list(data.values()))
                    logger.debug(f"插入记录 {id_value}")

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"保存记录失败: {e}")
            return False

    @classmethod
    def get_by_id(cls: Type[T], id_value: str) -> Optional[T]:
        """通过 ID 获取记录"""
        try:
            with cls.get_db_connection() as conn:
                cursor = conn.execute(
                    f"SELECT * FROM {cls.get_table_name()} WHERE id = ?",
                    (id_value,)
                )
                row = cursor.fetchone()
                return cls._from_db_row(row) if row else None
        except Exception as e:
            logger.error(f"查询记录失败: {e} | {cls.get_table_name()} ")
            return None
    
    @classmethod
    def get_last(cls: Type[T]) -> Type[T]:
        """获取最后一条记录的 ID"""
        try:
            with cls.get_db_connection() as conn:
                cursor = conn.execute(
                    f"SELECT `id`,`open_time`,`close_time` FROM {cls.get_table_name()} ORDER BY  `open_time` DESC LIMIT 1"
                )
                row = cursor.fetchone()
                if row:
                    return cls._from_db_row(row)
                else:
                    return None
        except Exception as e:
            logger.error(f"查询记录失败: {e} | {cls.get_table_name()} ")
            return None

    @classmethod
    def get_last_id(cls: Type[T]) -> Optional[Dict[str, Any]]:
        """获取最后一条记录的 ID"""
        try:
            with cls.get_db_connection() as conn:
                cursor = conn.execute(
                    f"SELECT `id`,`open_time`,`close_time` FROM {cls.get_table_name()} ORDER BY  `open_time` DESC LIMIT 1"
                )
                row = cursor.fetchone()
                if row:
                    id = row['id']
                    open_time = row['open_time']
                    close_time = row['close_time']
                    o_t = None
                    c_t = None
                    if open_time:
                        o_t = parse_datetime(open_time)
                    if close_time:
                        c_t = parse_datetime(close_time) if close_time else None
                    return {"id": id, "open_time": o_t, "close_time": c_t}
                else:
                    return None
        except Exception as e:
            logger.error(f"查询记录失败: {e} | {cls.get_table_name()} ")
            return None
    
    @classmethod
    def get_all_ids(cls: Type[T], limit: Optional[int] = None) -> Dict[str,Any]:
        """获取所有记录的 ID"""
        try:
            
            
            with cls.get_db_connection() as conn:
                cursor = conn.execute(
                    f"SELECT id,open_time,close_time FROM {cls.get_table_name()} ORDER BY open_time DESC"
                )
                rows = cursor.fetchmany(limit) if limit else cursor.fetchall()
                es = {}
                for row in rows:
                    i = row['id']
                    open_time = row['open_time']
                    close_time = row['close_time']
                    o_t = None
                    c_t = None
                    if open_time:
                        o_t = parse_datetime(open_time)
                    if close_time:
                        c_t = parse_datetime(close_time) if close_time else None
                    es[i] =(o_t, c_t)
                return es
        except Exception as e:
            import traceback
            logger.error(f"失败跟踪:{traceback.format_exc()} ")
            logger.error(f"查询记录失败: {e} | {cls.get_table_name()} ")
            return {}

    @classmethod
    def get_all(cls: Type[T], limit: Optional[int] = None) -> List[T]:
        """获取所有记录"""
        try:
            cls.create_table()
            with cls.get_db_connection() as conn:
                sql = f"SELECT * FROM {cls.get_table_name()} ORDER BY created_at DESC"
                if limit:
                    sql += f" LIMIT {limit}"

                cursor = conn.execute(sql)
                return [cls._from_db_row(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"获取所有记录失败: {e} in {cls.get_table_name()}")
            return []
    

    @classmethod
    def find_by(cls: Type[T], **conditions) -> List[T]:
        """根据条件查询记录"""
        if not conditions:
            return []

        try:
            with cls.get_db_connection() as conn:
                where_clauses = []
                values = []

                for field, value in conditions.items():
                    where_clauses.append(f"{field} = ?")
                    values.append(cls._serialize_value(value))

                sql = f"SELECT * FROM {cls.get_table_name()} WHERE {' AND '.join(where_clauses)}"
                cursor = conn.execute(sql, values)

                return [cls._from_db_row(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"条件查询失败: {e}")
            return []

    @classmethod
    def update(cls: Type[T], id_value: str, **kwargs) -> bool:
        """更新指定记录"""
        if not kwargs:
            return False

        try:
            with cls.get_db_connection() as conn:
                set_clauses = []
                values = []

                for field, value in kwargs.items():
                    if field in cls.model_fields:
                        set_clauses.append(f"{field} = ?")
                        values.append(cls._serialize_value(value))

                if not set_clauses:
                    return False

                values.append(id_value)
                sql = f"UPDATE {cls.get_table_name()} SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
                cursor = conn.execute(sql, values)
                conn.commit()

                success = cursor.rowcount > 0
                if success:
                    logger.debug(f"更新记录 {id_value} 成功")
                else:
                    logger.warning(f"未找到记录 {id_value}")

                return success
        except Exception as e:
            logger.error(f"更新记录失败: {e}")
            return False

    @classmethod
    def delete(cls: Type[T], id_value: str) -> bool:
        """删除指定记录"""
        try:
            with cls.get_db_connection() as conn:
                cursor = conn.execute(
                    f"DELETE FROM {cls.get_table_name()} WHERE id = ?",
                    (id_value,)
                )
                conn.commit()

                success = cursor.rowcount > 0
                if success:
                    logger.debug(f"删除记录 {id_value} 成功")
                else:
                    logger.warning(f"未找到要删除的记录 {id_value}")

                return success
        except Exception as e:
            logger.error(f"删除记录失败: {e}")
            return False

    @classmethod
    def count(cls) -> int:
        """获取记录总数"""
        try:
            with cls.get_db_connection() as conn:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {cls.get_table_name()}")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"获取记录数失败: {e}")
            return 0