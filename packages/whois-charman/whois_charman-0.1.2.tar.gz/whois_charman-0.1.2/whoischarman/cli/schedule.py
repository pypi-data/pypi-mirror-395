#!/usr/bin/env python3
"""
FastAPI 调度系统
提供Web界面和API接口来管理调度任务
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import os
from pathlib import Path

from whoischarman.stratigy.scheduler import BaseScheduler
from whoischarman.struct.schedule import ScheduleConf
from whoischarman.exchangers import ExchangeConfig
from whoischarman.ai import AIConfig
from whoischarman.cli.schedule_temp import HTML_TEMPLATE
from whoischarman.cli.schedule_man_temp import SCRIPT_MANAGEMENT_TEMPLATE
from whoischarman.stratigy.auto_loader import (
    get_all_task_parameters,
    list_scripts,
    install_script,
    create_script_template,
    ScriptValidator,
    reload_custom_tasks
)

# Pydantic models for API request/response
class ExchangeConfigRequest(BaseModel):
    exchange_name: str = Field(..., description="交易所名称")
    proxy: Optional[str] = Field(None, description="代理地址")


class AIConfigRequest(BaseModel):
    model: str = Field("qwen3-4b", description="模型名称")
    api_key: str = Field("sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", description="API密钥")
    api: str = Field("https://xxx.xx.x.x:12341", description="API地址")
    temperature: float = Field(0.3, description="温度")
    max_tokens: int = Field(31024, description="最大token数")
    max_retries: int = Field(3, description="最大重试次数")
    timeout: int = Field(60, description="超时时间")


class TaskCreateRequest(BaseModel):
    name: str = Field(..., description="任务名称")
    task_type: str = Field(..., description="任务类型")
    interval_seconds: int = Field(60, description="执行间隔（秒）")
    enabled: bool = Field(False, description="是否启用")
    max_executions: int = Field(-1, description="最大执行次数，-1表示无限")
    log_level: str = Field("INFO", description="日志级别")
    log_file: Optional[str] = Field(None, description="日志文件路径")
    log_file_root: Optional[str] = Field("/tmp/logs", description="日志文件根路径")
    continue_on_error: bool = Field(True, description="出错时是否继续执行")
    exchange_configs: List[ExchangeConfigRequest] = Field(default_factory=list, description="交易所配置列表")
    ai_configs: List[AIConfigRequest] = Field(default_factory=list, description="AI配置列表")
    params: Dict[str, Any] = Field(default_factory=dict, description="自定义参数")


class TaskUpdateRequest(BaseModel):
    interval_seconds: Optional[int] = Field(None, description="执行间隔（秒）")
    enabled: Optional[bool] = Field(None, description="是否启用")
    max_executions: Optional[int] = Field(None, description="最大执行次数")
    log_level: Optional[str] = Field(None, description="日志级别")
    continue_on_error: Optional[bool] = Field(None, description="出错时是否继续执行")
    exchange_configs: Optional[List[ExchangeConfigRequest]] = Field(None, description="交易所配置列表")
    ai_configs: Optional[List[AIConfigRequest]] = Field(None, description="AI配置列表")
    params: Optional[Dict[str, Any]] = Field(None, description="自定义参数")


class TaskResponse(BaseModel):
    name: str
    status: str
    running: bool
    execution_count: int
    error_count: int
    start_time: Optional[str]
    end_time: Optional[str]
    last_error: Optional[str]
    log_file: str
    config: Dict[str, Any]


class SchedulerInfoResponse(BaseModel):
    total_tasks: int
    running_tasks: int
    enabled_tasks: int
    available_task_classes: List[str]
    configured_tasks: List[str]
    tasks_status: Dict[str, TaskResponse]
    task_parameters: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="任务参数信息")


# Script Management Pydantic models
class ScriptCreateRequest(BaseModel):
    script_name: str = Field(..., description="脚本名称")


class ScriptValidateRequest(BaseModel):
    script_name: str = Field(..., description="脚本名称")


class ScriptInfoResponse(BaseModel):
    name: str
    path: str
    size: int
    modified_time: float
    task_classes: List[str]
    valid: bool
    errors: List[str]
    warnings: List[str]
    security_issues: int


class ScriptsListResponse(BaseModel):
    scripts_dir: str
    exists: bool
    scripts: List[ScriptInfoResponse]
    total_count: int
    task_classes_count: int


class ScriptValidationResponse(BaseModel):
    validation_result: Dict[str, Any]


class ScriptOperationResponse(BaseModel):
    success: bool
    message: str
    validation_result: Optional[Dict[str, Any]] = None
    installed_path: Optional[str] = None


# FastAPI 应用初始化
app = FastAPI(
    title="调度管理系统",
    description="基于FastAPI的调度任务管理系统",
    version="1.0.0"
)

# 全局调度器实例
scheduler = BaseScheduler()

# 临时文件跟踪字典
temp_files_tracker = {}

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML 模板（内嵌）


# API 路由定义
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页HTML"""
    return HTML_TEMPLATE


@app.get("/scheduler/info", response_model=SchedulerInfoResponse)
async def get_scheduler_info():
    """获取调度器整体信息"""
    try:
        info = scheduler.get_scheduler_info()

        # 获取任务参数信息
        task_parameters = get_all_task_parameters()

        # 转换任务状态为响应模型
        tasks_status = {}
        for task_name, task_info in info['tasks_status'].items():
            tasks_status[task_name] = TaskResponse(**task_info)

        return SchedulerInfoResponse(
            total_tasks=info['total_tasks'],
            running_tasks=info['running_tasks'],
            enabled_tasks=info['enabled_tasks'],
            available_task_classes=info['available_task_classes'],
            configured_tasks=info['configured_tasks'],
            tasks_status=tasks_status,
            task_parameters=task_parameters
        )
    except Exception as e:
        logger.error(f"获取调度器信息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks", response_model=Dict[str, TaskResponse])
async def get_all_tasks():
    """获取所有任务状态"""
    try:
        all_tasks = scheduler.get_all_tasks_status()

        # 转换为响应模型
        response = {}
        for task_name, task_info in all_tasks.items():
            response[task_name] = TaskResponse(**task_info)

        return response
    except Exception as e:
        logger.error(f"获取任务列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks")
async def create_task(task_data: TaskCreateRequest):
    """创建新任务"""
    try:
        # 验证任务类型是否存在
        available_tasks = scheduler.get_registered_task_classes()
        if task_data.task_type not in available_tasks:
            raise HTTPException(
                status_code=400,
                detail=f"任务类型 '{task_data.task_type}' 不存在。可用类型: {list(available_tasks.keys())}"
            )

        # 验证任务名称是否已存在
        if task_data.name in scheduler.task_configs:
            raise HTTPException(
                status_code=400,
                detail=f"任务名称 '{task_data.name}' 已存在，请使用不同的名称"
            )

        # 转换交易所配置
        exchange_configs = []
        for ec in task_data.exchange_configs:
            exchange_configs.append(ExchangeConfig(
                exchange_name=ec.exchange_name,
                proxy=ec.proxy
            ))

        # 转换AI配置
        ai_configs = []
        for ac in task_data.ai_configs:
            ai_config = AIConfig(
                model=ac.model,
                api_key=ac.api_key,
                api=ac.api,
                temperature=ac.temperature,
                max_tokens=ac.max_tokens,
                max_retries=ac.max_retries,
                timeout=ac.timeout
            )
            ai_config.using = False
            ai_configs.append(ai_config)

        # 创建调度配置
        schedule_config = ScheduleConf(
            name=task_data.name,
            enabled=task_data.enabled,
            interval_seconds=task_data.interval_seconds,
            max_executions=task_data.max_executions,
            log_level=task_data.log_level,
            log_file=task_data.log_file,
            log_file_root=task_data.log_file_root,
            continue_on_error=task_data.continue_on_error,
            exchange_user_configs=exchange_configs,
            ai_configs=ai_configs,
            params=task_data.params
        )

        # 添加任务到调度器 - 需要手动处理任务类型和任务名称
        try:
            # 检查任务类型是否存在
            available_tasks = scheduler.get_registered_task_classes()
            if task_data.task_type not in available_tasks:
                raise ValueError(f"任务类型 '{task_data.task_type}' 不存在")

            # 检查任务名称是否已存在
            if task_data.name in scheduler.task_configs:
                raise ValueError(f"任务名称 '{task_data.name}' 已存在")

            # 手动创建任务实例
            from whoischarman.stratigy.base_task import TaskRegistryMeta
            task_class = TaskRegistryMeta.get_task_class(task_data.task_type)
            if not task_class:
                raise ValueError(f"未找到任务类: {task_data.task_type}")

            # 创建任务实例
            task_instance = task_class(schedule_config, **task_data.params)

            # 手动添加到调度器
            scheduler.task_configs[task_data.name] = schedule_config
            scheduler.tasks[task_data.name] = task_instance

            logger.info(f"任务 '{task_data.name}' 创建成功，类型: {task_data.task_type}")
            success = True

        except Exception as e:
            logger.error(f"手动添加任务失败: {e}")
            success = False

        if success:
            return {"message": f"任务 '{task_data.name}' 创建成功", "task_name": task_data.name, "task_type": task_data.task_type}
        else:
            raise HTTPException(status_code=400, detail="任务创建失败")

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"创建任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/tasks/{task_name}")
async def update_task(task_name: str, task_data: TaskUpdateRequest):
    """更新任务配置"""
    try:
        # 获取现有任务配置
        if task_name not in scheduler.task_configs:
            raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 不存在")

        existing_config = scheduler.task_configs[task_name]

        # 更新配置字段
        update_data = task_data.dict(exclude_unset=True)

        if 'exchange_configs' in update_data:
            exchange_configs = []
            for ec in update_data['exchange_configs']:
                exchange_configs.append(ExchangeConfig(
                    exchange_name=ec.exchange_name,
                    proxy=ec.proxy
                ))
            update_data['exchange_user_configs'] = exchange_configs
            del update_data['exchange_configs']

        if 'ai_configs' in update_data:
            ai_configs = []
            for ac in update_data['ai_configs']:
                ai_config = AIConfig(
                    model=ac.model,
                    api_key=ac.api_key,
                    api=ac.api,
                    temperature=ac.temperature,
                    max_tokens=ac.max_tokens,
                    max_retries=ac.max_retries,
                    timeout=ac.timeout
                )
                ai_config.using = False
                ai_configs.append(ai_config)
            update_data['ai_configs'] = ai_configs

        # 创建新的配置对象
        for field, value in update_data.items():
            if hasattr(existing_config, field):
                setattr(existing_config, field, value)

        # 更新任务配置
        success = scheduler.update_task_config(task_name, existing_config)

        if success:
            return {"message": f"任务 '{task_name}' 更新成功"}
        else:
            raise HTTPException(status_code=400, detail="任务更新失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/tasks/{task_name}")
async def delete_task(task_name: str):
    """删除任务"""
    try:
        success = scheduler.remove_task(task_name)

        if success:
            return {"message": f"任务 '{task_name}' 删除成功"}
        else:
            raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 不存在")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks/{task_name}/start")
async def start_task(task_name: str):
    """启动任务"""
    try:
        success = scheduler.start_task(task_name)

        if success:
            return {"message": f"任务 '{task_name}' 启动成功"}
        else:
            raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 不存在或启动失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"启动任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks/{task_name}/stop")
async def stop_task(task_name: str):
    """停止任务"""
    try:
        success = scheduler.stop_task(task_name)

        if success:
            return {"message": f"任务 '{task_name}' 停止成功"}
        else:
            raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 不存在或停止失败")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"停止任务失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_name}/status", response_model=TaskResponse)
async def get_task_status(task_name: str):
    """获取任务详细状态"""
    try:
        task_info = scheduler.get_task_status(task_name)

        if task_info is None:
            raise HTTPException(status_code=404, detail=f"任务 '{task_name}' 不存在")

        return TaskResponse(**task_info)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_name}/logs")
async def get_task_logs(task_name: str, lines: int = 100):
    """获取任务日志"""
    try:
        logs = scheduler.get_task_logs(task_name, lines)
        return logs

    except Exception as e:
        logger.error(f"获取任务日志失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events")
async def event_stream():
    """实时事件流 (Server-Sent Events)"""
    async def event_generator():
        try:
            while True:
                # 获取调度器信息
                info = scheduler.get_scheduler_info()

                # 简化信息用于传输
                simplified_info = {
                    'total_tasks': info['total_tasks'],
                    'running_tasks': info['running_tasks'],
                    'enabled_tasks': info['enabled_tasks'],
                    'available_task_classes': info['available_task_classes'],
                    'timestamp': datetime.now().isoformat()
                }

                # 发送SSE格式数据
                yield f"data: {json.dumps(simplified_info)}\\n\\n"

                # 每5秒更新一次
                await asyncio.sleep(5)

        except asyncio.CancelledError:
            logger.info("SSE connection cancelled")
        except Exception as e:
            logger.error(f"SSE error: {e}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


# Script Management Routes
@app.get("/scripts-management", response_class=HTMLResponse)
async def scripts_management_page():
    """返回脚本管理页面HTML"""
    return SCRIPT_MANAGEMENT_TEMPLATE


@app.get("/scripts", response_model=ScriptsListResponse)
async def get_scripts_list():
    """获取所有脚本列表"""
    try:
        result = list_scripts()

        # 转换脚本信息为响应模型
        scripts = []
        for script_info in result.get('scripts', []):
            scripts.append(ScriptInfoResponse(**script_info))

        return ScriptsListResponse(
            scripts_dir=result['scripts_dir'],
            exists=result['exists'],
            scripts=scripts,
            total_count=result['total_count'],
            task_classes_count=result['task_classes_count']
        )
    except Exception as e:
        logger.error(f"获取脚本列表失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scripts/create")
async def create_script(script_data: ScriptCreateRequest):
    """创建新的脚本模板到临时目录"""
    try:
        import tempfile
        import os
        import uuid
        import time
        from pathlib import Path

        # 创建临时目录，使用UUID确保唯一性
        unique_id = str(uuid.uuid4())[:8]
        temp_dir = tempfile.mkdtemp(prefix=f"schedule_script_{unique_id}_")

        # 获取脚本内容
        from whoischarman.stratigy.auto_loader import TaskAutoLoader
        auto_loader = TaskAutoLoader()
        script_content = auto_loader.create_script(script_data.script_name)

        # 创建临时脚本文件
        script_name = f"{script_data.script_name}.py"
        temp_script_path = os.path.join(temp_dir, script_name)

        with open(temp_script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # 跟踪临时文件，设置1小时过期时间
        temp_files_tracker[unique_id] = {
            "temp_dir": temp_dir,
            "script_path": temp_script_path,
            "script_name": script_name,
            "created_at": time.time(),
            "expires_at": time.time() + 3600  # 1小时后过期
        }

        logger.info(f"脚本创建到临时目录: {temp_script_path}")

        return {
            "message": f"脚本创建成功",
            "script_name": script_name,
            "temp_path": temp_script_path,
            "temp_dir": temp_dir,
            "download_url": f"/scripts/download/{unique_id}/{script_name}",
            "content": script_content,
            "download_ready": True,
            "unique_id": unique_id
        }
    except Exception as e:
        logger.error(f"创建脚本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scripts/download/{unique_id}/{script_name}")
async def download_script(unique_id: str, script_name: str):
    """下载临时脚本文件"""
    try:
        import time
        import shutil
        from pathlib import Path

        # 检查文件是否在跟踪器中
        if unique_id not in temp_files_tracker:
            raise HTTPException(status_code=404, detail="临时文件不存在或已过期")

        file_info = temp_files_tracker[unique_id]

        # 检查是否过期
        current_time = time.time()
        if current_time > file_info["expires_at"]:
            # 清理过期的临时文件
            try:
                shutil.rmtree(file_info["temp_dir"])
                del temp_files_tracker[unique_id]
            except:
                pass
            raise HTTPException(status_code=404, detail="临时文件已过期")

        # 检查脚本名称是否匹配
        if file_info["script_name"] != script_name:
            raise HTTPException(status_code=400, detail="脚本名称不匹配")

        # 检查文件是否存在
        script_path = Path(file_info["script_path"])
        if not script_path.exists():
            raise HTTPException(status_code=404, detail="脚本文件不存在")

        # 读取文件内容
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()

        # 返回文件下载响应
        from fastapi.responses import Response
        return Response(
            content=script_content,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename=\"{script_name}\""
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下载脚本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scripts/install")
async def install_script_endpoint(script_file: UploadFile = File(...), force_install: bool = False):
    """安装脚本文件"""
    try:
        # 检查文件类型
        if not script_file.filename.endswith('.py'):
            raise HTTPException(status_code=400, detail="只能上传Python文件 (.py)")

        # 保存临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.py', delete=False) as temp_file:
            content = await script_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # 安装脚本
            result = install_script(temp_file_path, force=force_install)

            if result['success']:
                # 清理临时文件
                os.unlink(temp_file_path)
                return ScriptOperationResponse(**result)
            else:
                # 清理临时文件
                os.unlink(temp_file_path)
                raise HTTPException(status_code=400, detail=result['message'])

        except Exception as e:
            # 确保清理临时文件
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"安装脚本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scripts/validate")
async def validate_script_endpoint(script_data: ScriptValidateRequest):
    """验证脚本"""
    try:
        scripts_dir = Path(os.path.expanduser("~/.schedule_scripts/"))
        script_path = scripts_dir / f"{script_data.script_name}"
        logger.warning(f"{script_path} validating")
        if not script_path.exists():
            raise HTTPException(status_code=404, detail=f"脚本 '{script_data.script_name}' 不存在")

        validator = ScriptValidator()
        validation_result = validator.validate_script(str(script_path))

        return ScriptValidationResponse(validation_result=validation_result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"验证脚本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/scripts/{script_name}")
async def delete_script_endpoint(script_name: str):
    """删除脚本"""
    try:
        scripts_dir = Path(os.path.expanduser("~/.schedule_scripts/"))
        script_path = scripts_dir / f"{script_name}"

        if not script_path.exists():
            raise HTTPException(status_code=404, detail=f"脚本 '{script_name}' 不存在")

        # 删除文件
        os.remove(script_path)

        return {"message": f"脚本 '{script_name}' 删除成功"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除脚本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scripts/reload")
async def reload_scripts_endpoint():
    """重新加载所有脚本"""
    try:
        # 清理过期的临时文件
        cleanup_expired_temp_files()

        # 重新加载自定义任务
        reloaded_tasks = reload_custom_tasks()

        # 获取脚本信息
        result = list_scripts()

        return {
            "message": f"脚本重新加载成功，加载了 {len(reloaded_tasks)} 个Task类",
            "reloaded_tasks": len(reloaded_tasks),
            "task_classes": list(reloaded_tasks.keys())
        }

    except Exception as e:
        logger.error(f"重新加载脚本失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def cleanup_expired_temp_files():
    """清理过期的临时文件"""
    try:
        import time
        import shutil
        current_time = time.time()
        expired_keys = []

        for unique_id, file_info in temp_files_tracker.items():
            if current_time > file_info["expires_at"]:
                expired_keys.append(unique_id)
                try:
                    shutil.rmtree(file_info["temp_dir"])
                    logger.info(f"清理过期的临时目录: {file_info['temp_dir']}")
                except Exception as e:
                    logger.warning(f"清理临时目录失败: {e}")

        # 从跟踪器中删除过期的条目
        for key in expired_keys:
            del temp_files_tracker[key]

        if expired_keys:
            logger.info(f"清理了 {len(expired_keys)} 个过期的临时文件")

    except Exception as e:
        logger.error(f"清理过期临时文件时出错: {e}")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "内部服务器错误"},
    )


def start_server(host: str = "0.0.0.0", port: int = 38000, debug: bool = False):
    """启动FastAPI服务器"""
    logger.info(f"Starting scheduler web server on {host}:{port}")

    # 创建一些示例任务（如果不存在任务）
    if not scheduler.get_all_tasks_status():
        logger.info("No tasks found, creating example tasks...")

        # 创建示例交易所配置
        example_exchange_config = ScheduleConf(
            name="ExchangePullTasks",
            interval_seconds=600,  # 10分钟执行一次
            enabled=False,  # 默认禁用，避免立即执行
            max_executions=-1,
            exchange_user_configs=[
                ExchangeConfig(exchange_name="PolymarketExchange", proxy="socks5h://127.0.0.1:1091"),
                ExchangeConfig(exchange_name="KalshiExchange", proxy="socks5h://127.0.0.1:1091")
            ],
            log_level="INFO",
            log_file_root="/tmp/logs"
        )

        # 添加示例任务
        scheduler.add_task("ExchangePullTasks", example_exchange_config)
        logger.info("Example task 'ExchangePullTasks' created")

    # 启动uvicorn服务器 - 修复reload警告
    if debug:
        # 开发模式 - 使用字符串导入方式支持reload
        uvicorn.run(
            "whoischarman.cli.schedule:app",
            host=host,
            port=port,
            reload=True,
            access_log=True
        )
    else:
        # 生产模式 - 直接使用应用实例
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,
            access_log=False
        )

def main():
    import argparse
    parser = argparse.ArgumentParser(description="FastAPI 调度管理系统")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--host", default="0.0.0.0", help="监听的主机地址")
    parser.add_argument("--port", type=int, default=38000, help="监听的端口号")
    parser.add_argument("-n", "--new", type=str, default=None, help="新建一个脚本模板")
    parser.add_argument("-i", "--install", type=str, default=None, help="安装脚本文件到~/.schedule_scripts/")
    parser.add_argument("-u", "--uninstall", type=str, default=None, help="安装脚本文件到~/.schedule_scripts/")
    parser.add_argument("--force", action="store_true", help="强制安装（覆盖已存在的文件）")
    parser.add_argument("-l", "--list", action="store_true", default=False, help="显示所有已安装的脚本")
    parser.add_argument("--validate", type=str, default=None, help="验证脚本文件但不安装")
    # parser.add_argument("--no-server", action="store_true", help="只执行CLI操作，不启动Web服务器")

    args = parser.parse_args()

    # 处理CLI命令
    if args.new:
        try:
            from whoischarman.stratigy.auto_loader import create_script_template
            script_path = create_script_template(args.new)
            print(f"✅ 脚本模板创建成功: {script_path}")
            print("💡 请编辑脚本文件实现你的任务逻辑")
            print(f"📝 编辑完成后，使用以下命令安装: python -m whoischarman.cli.schedule -i {script_path}")
            return
        except Exception as e:
            print(f"❌ 创建脚本模板失败: {e}")
            return

    elif args.install:
        try:
            from whoischarman.stratigy.auto_loader import install_script

            result = install_script(args.install, force=args.force)

            if result['success']:
                print(f"✅ {result['message']}")

                # 显示验证详情
                if result['validation_result']:
                    v = result['validation_result']

                    if v['task_classes']:
                        print(f"📋 发现Task类: {', '.join(v['task_classes'])}")

                    if v['warnings']:
                        print(f"⚠️  警告: {'; '.join(v['warnings'])}")

                    if v['security_issues']:
                        security_warnings = [issue['message'] for issue in v['security_issues']
                                          if issue['severity'] == 'warning']
                        if security_warnings:
                            print(f"🔒 安全提醒: {'; '.join(security_warnings)}")

                print("💡 安装完成后，重启服务器以加载新的Task类")

            else:
                print(f"❌ 安装失败: {result['message']}")

                # 显示详细错误信息
                if result['validation_result']:
                    v = result['validation_result']

                    if v['errors']:
                        print("🔍 详细错误:")
                        for error in v['errors']:
                            print(f"   - {error}")

                    if v['security_issues']:
                        critical_issues = [issue for issue in v['security_issues']
                                        if issue['severity'] == 'critical']
                        if critical_issues:
                            print("🚨 安全问题:")
                            for issue in critical_issues:
                                print(f"   - {issue['message']}")
            return
        except Exception as e:
            print(f"❌ 安装过程中出错: {e}")
        return

    elif args.validate:
        try:
            from whoischarman.stratigy.auto_loader import ScriptValidator

            validator = ScriptValidator()
            result = validator.validate_script(args.validate)

            print(f"📄 验证脚本: {args.validate}")
            print("=" * 50)

            if result['valid']:
                print("✅ 脚本验证通过")
            else:
                print("❌ 脚本验证失败")

            if result['task_classes']:
                print(f"📋 发现Task类: {', '.join(result['task_classes'])}")

            if result['errors']:
                print("\n🚨 错误:")
                for error in result['errors']:
                    print(f"   - {error}")

            if result['warnings']:
                print("\n⚠️  警告:")
                for warning in result['warnings']:
                    print(f"   - {warning}")

            if result['security_issues']:
                print("\n🔒 安全检查:")
                for issue in result['security_issues']:
                    severity_icon = "🚨" if issue['severity'] == 'critical' else "⚠️"
                    print(f"   {severity_icon} {issue['message']}")
            return
        except Exception as e:
            print(f"❌ 验证过程中出错: {e}")
        return

    elif args.list:
        try:
            from whoischarman.stratigy.auto_loader import list_scripts

            result = list_scripts()

            print(f"📁 脚本目录: {result['scripts_dir']}")

            if not result['exists']:
                print("❌ 脚本目录不存在")
                return

            print(f"📊 总脚本数: {result['total_count']}")
            print(f"🔧 总Task类数: {result['task_classes_count']}")
            print("=" * 60)

            if not result['scripts']:
                print("📭 未发现任何脚本")
                print("💡 使用 -n 参数创建新的脚本模板")
            else:
                for i, script in enumerate(result['scripts'], 1):
                    status = "✅" if script['valid'] else "❌"
                    security_icon = "🔒" if script['security_issues'] > 0 else "✅"

                    print(f"{i:2d}. {status} {script['name']}")
                    print(f"     📁 路径: {script['path']}")
                    print(f"     📏 大小: {script['size']} bytes")
                    print(f"     🔧 Task类: {len(script['task_classes'])} 个 {script['task_classes']}")
                    print(f"     {security_icon} 安全问题: {script['security_issues']} 个")

                    if script['errors']:
                        print(f"     ❌ 错误: {'; '.join(script['errors'])}")

                    if script['warnings']:
                        print(f"     ⚠️  警告: {'; '.join(script['warnings'])}")

                    print()
            return
        except Exception as e:
            print(f"❌ 列出脚本时出错: {e}")
        return

    # 如果没有指定CLI操作，启动Web服务器
    
    start_server(debug=args.debug, host=args.host, port=args.port)
    

if __name__ == "__main__":
    print("🚀 启动 FastAPI 调度管理系统...")
    print("📱 Web界面: http://localhost:38000")
    print("📚 API文档: http://localhost:38000/docs")
    print("⚡ 按 Ctrl+C 停止服务器")
    start_server(debug=True)