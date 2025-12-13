
# FastAPI 应用初始化
from schedule_temp import HTML_TEMPLATE
from schedule_man_temp import SCRIPT_MANAGEMENT_TEMPLATE
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi import FastAPI
import uvicorn
import logging

app = FastAPI(
    title="调度管理系统",
    description="基于FastAPI的调度任务管理系统",
    version="1.0.0"
)

# 全局调度器实例
# scheduler = BaseScheduler()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML 模板（内嵌）


# API 路由定义
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页HTML"""
    return HTML_TEMPLATE

@app.get("/2", response_class=HTMLResponse)
async def read_root():
    """返回主页HTML"""
    return SCRIPT_MANAGEMENT_TEMPLATE


def start_server(host: str = "0.0.0.0", port: int = 38003, debug: bool = False):
    """启动FastAPI服务器"""
    logger.info(f"Starting scheduler web server on {host}:{port}")

    
        # 开发模式 - 使用字符串导入方式支持reload
    uvicorn.run(
        "test:app",
        host=host,
        port=port,
        reload=True,
        access_log=True
    )

if __name__ == "__main__":
    start_server()