
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import argparse
import uvicorn
from contextlib import asynccontextmanager, AsyncExitStack
from serverz.server.scheduler_task import perform_shutdown_tasks, perform_startup_tasks
from serverz.server.models import *
from serverz.server.routers import chat_router
import os

from pro_craft.server.router.prompt import create_router
from serverz import logger

default=8008

@asynccontextmanager
async def lifespan(app: FastAPI):
    """_summary_

    Args:
        app (FastAPI): _description_
    """
    # mcp 服务
    await perform_startup_tasks()
    yield
    await perform_shutdown_tasks()


app = FastAPI(
    title="LLM Service",
    description="custom large language models.",
    version="2.0.1",
    lifespan=lifespan,
)

# --- Configure CORS ---
origins = [
    "*", # Allows all origins (convenient for development, insecure for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the allowed origins
    allow_credentials=True, # Allows cookies/authorization headers
    allow_methods=["*"],    # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],    # Allows all headers (Content-Type, Authorization, etc.)
)
# --- End CORS Configuration ---


database_url = os.getenv("database_url")
test_database_url = os.getenv("test_database_url")
product_database_url = os.getenv("product_database_url")


prompt_router = create_router(database_url=database_url,
                              test_database_url = test_database_url,
                              product_database_url = product_database_url,
                                model_name="doubao-1-5-pro-32k-250115",
                                logger=logger)



# app.include_router(chat_router,prefix="/v1") # TODO 一加这个服务就无法再服务器上运行
app.include_router(prompt_router, prefix="/prompt")


@app.get("/")
async def root():
    """ x """
    return {"message": "LLM Service is running."}



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Start a simple HTTP server similar to http.server."
    )
    parser.add_argument(
        "port",
        metavar="PORT",
        type=int,
        nargs="?",  # 端口是可选的
        default=default,
        help=f"Specify alternate port [default: {default}]",
    )
    # 创建一个互斥组用于环境选择
    group = parser.add_mutually_exclusive_group()

    # 添加 --dev 选项
    group.add_argument(
        "--dev",
        action="store_true",  # 当存在 --dev 时，该值为 True
        help="Run in development mode (default).",
    )

    # 添加 --prod 选项
    group.add_argument(
        "--prod",
        action="store_true",  # 当存在 --prod 时，该值为 True
        help="Run in production mode.",
    )
    args = parser.parse_args()

    if args.prod:
        env = "prod"
    else:
        # 如果 --prod 不存在，默认就是 dev
        env = "dev"

    port = args.port

    if env == "dev":
        port += 100
        reload = True
        app_import_string = (
            f"{__package__}.__main__:app"  # <--- 关键修改：传递导入字符串
        )
    elif env == "prod":
        reload = False
        app_import_string = app
    else:
        reload = False
        app_import_string = app

    # 使用 uvicorn.run() 来启动服务器
    # 参数对应于命令行选项
    uvicorn.run(
        app_import_string, host="0.0.0.0", port=port, reload=reload  # 启用热重载
    )
