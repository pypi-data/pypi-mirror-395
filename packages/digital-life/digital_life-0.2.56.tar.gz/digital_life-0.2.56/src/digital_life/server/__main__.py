# server
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel
from digital_life import logger
from .router import biography_router, chat_router, avatar_router, memory_card_router, user_router, recommended_router

from pro_craft_infer.log_router import create_router
import inspect
import math
import os

app = FastAPI(
    title="digital_life server",
    description="数字人生服务",
    version="1.0.1",
)

# --- Configure CORS ---
origins = [
    "*", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specifies the allowed origins
    allow_credentials=True,  # Allows cookies/authorization headers
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers (Content-Type, Authorization, etc.)
)
# --- End CORS Configuration ---

default = 8007
DATABASE = os.getenv("database_url")
LOG_DATABASE = os.getenv("log_database_url")
LOGFILE_PATH = os.getenv("log_file_path")


# check

import time
import os
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse, ResponseHandlingException
from requests.exceptions import ConnectionError, Timeout

def check_qdrant_availability(
    host: str, 
    port: int = 6333, 
    api_key: str = None, 
    timeout: int = 5, 
    max_retries: int = 5, 
    retry_delay: int = 5
) -> bool:
    """
    检测 Qdrant 服务是否可用。

    Args:
        host (str): Qdrant 服务的地址。
        port (int): Qdrant 服务的端口，默认为 6333。
        api_key (str, optional): Qdrant 服务的 API 密钥。默认为 None。
        timeout (int): 每次连接尝试的超时时间（秒）。
        max_retries (int): 最大重试次数。
        retry_delay (int): 每次重试之间的等待时间（秒）。

    Returns:
        bool: 如果 Qdrant 服务可用，返回 True；否则返回 False。
    """
    print(f"尝试连接到 Qdrant 服务: {host}:{port}")
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"尝试连接 (第 {attempt}/{max_retries} 次)...")
            client = QdrantClient(
                host=host, 
                port=port, 
                api_key=api_key, 
                timeout=timeout # 设置客户端级别的超时
            )
            
            # 尝试执行一个轻量级操作来验证连接，例如检查一个不存在的 collection
            # 如果连接成功但 Qdrant 服务本身有问题，这个操作可能会失败并抛出异常
            client.get_collections() 
            
            print(f"成功连接到 Qdrant 服务: {host}:{port}")
            return True
        except (ConnectionError, Timeout, ResponseHandlingException, UnexpectedResponse) as e:
            print(f"连接 Qdrant 失败: {e}")
            if attempt < max_retries:
                print(f"将在 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
            else:
                print(f"达到最大重试次数 ({max_retries})，无法连接到 Qdrant 服务。")
                return False
        except Exception as e:
            # 捕获其他未知错误
            print(f"连接 Qdrant 时发生未知错误: {e}")
            if attempt < max_retries:
                print(f"将在 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
            else:
                print(f"达到最大重试次数 ({max_retries})，无法连接到 Qdrant 服务。")
                return False

QDRANT_HOST = os.getenv("host", "localhost")  # 默认使用 localhost
QDRANT_PORT = int(os.getenv("port", 6333))    # 默认使用 6333

if check_qdrant_availability(QDRANT_HOST, QDRANT_PORT):
    print("\nQdrant 服务已准备就绪，可以继续启动应用程序。")
    # 在这里可以放置你的应用程序启动逻辑
    # 例如：
    # from my_app import start_application
    # start_application()
else:
    print("\nQdrant 服务不可用，应用程序将退出或进入维护模式。")
    # 在这里可以决定是退出程序，还是进入一个等待状态，或者降级服务
    exit(1) # 通常在核心服务不可用时直接退出





                             
prompt_router = create_router(database_url_no_protocol=DATABASE,
                                model_name="doubao-1-5-pro-32k-250115",
                                log_database_url_no_protocol = LOG_DATABASE,
                                log_path = LOGFILE_PATH,
                                logger=logger)

app.include_router(avatar_router,      prefix="/digital_avatar")
app.include_router(memory_card_router, prefix="/memory_card")
app.include_router(recommended_router, prefix="/recommended")
app.include_router(prompt_router,      prefix="/prompt")
app.include_router(chat_router,        prefix="/v1")
app.include_router(biography_router,   prefix = "")
app.include_router(user_router,        prefix = "")


async def get_score_overall(
    S: list[int], total_score: int = 0, epsilon: float = 0.001, K: float = 0.8
) -> float:
    """
    计算 y = sqrt(1/600 * x) 的值。
    计算人生总进度
    """
    x = sum(S)
    
    S_r = [math.sqrt((1/101) * i)/5 for i in S]
    return sum(S_r) * 100

    # return math.sqrt((1/601) * x)  * 100


async def get_score(
    S: list[int], total_score: int = 0, epsilon: float = 0.001, K: float = 0.01
) -> float:
    # 人生主题分值计算
    # 一个根据 列表分数 计算总分数的方法 如[1,4,5,7,1,5] 其中元素是 1-10 的整数
    # 一个非常小的正数，确保0分也有微弱贡献，100分也不是完美1
    # 调整系数，0 < K <= 1。K越大，总分增长越快。

    for score in S:
        normalized_score = (score + epsilon) / (10 + epsilon)
        total_score = total_score + (100 - total_score) * normalized_score * K
        if total_score >= 100 - 1e-9:  
            total_score = 100 - 1e-9
            break 

    return total_score



@app.get("/")
async def root():
    """server run"""
    envs = {
        "server":os.getenv("server_name",'default'),
        "collection_name":os.getenv("collection_name"),
        "log_file_path":os.getenv("log_file_path",''),
        "info":"hello_world",
        "test":"这是一个新的改变",
    }

    return {"message": "LLM Service is running.",
            "envs":envs}

class LifeTopicScoreRequest(BaseModel):
    S_list: List[int] = Field(..., description="List of scores, each between 1 and 10.")
    K: float = Field(0.8, description="Weighting factor K.")
    total_score: int = Field(0, description="Initial total score.")
    epsilon: float = Field(0.001, description="Epsilon value for calculation.")

    @model_validator(mode="after")
    def validate_s_list(self):
        if not all(0 <= x <= 10 for x in self.S_list):
            raise ValueError(
                "All elements in 'S_list' must be integers between 1 and 10 (inclusive)."
            )
        return self


@app.post("/life_topic_score")
async def life_topic_score_server(request: LifeTopicScoreRequest):
    try:
        result = await get_score(
            S=request.S_list,
            total_score=request.total_score,
            epsilon=request.epsilon,
            K=request.K,
        )
        return {
            "message": "Life topic score calculated successfully",
            "result": int(result),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Function name: {e}",
        )


class ScoreRequest(BaseModel):
    S_list: List[float] = Field(
        ...,
        description="List of string representations of scores, each between 1 and 10.",
    )
    K: float = Field(0.3, description="Coefficient K for score calculation.")
    total_score: int = Field(0, description="Total score to be added.")
    epsilon: float = Field(0.0001, description="Epsilon value for score calculation.")

    @model_validator(mode="after")
    def check_s_list_values(self):
        for s_val in self.S_list:
            try:
                int_s_val = float(s_val)
                if not (0 <= int_s_val <= 100):
                    raise ValueError(
                        "Each element in 'S_list' must be an integer between 1 and 10."
                    )
            except ValueError:
                raise ValueError(
                    "Each element in 'S_list' must be a valid integer string."
                )
        return self


@app.post("/life_aggregate_scheduling_score")
async def life_aggregate_scheduling_score_server(request: ScoreRequest):
    try:
        result = await get_score_overall(
            request.S_list,
            total_score=request.total_score,
            epsilon=request.epsilon,
            K=request.K,
        )
        return {
            "message": "life aggregate scheduling score successfully",
            "result": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        frame = inspect.currentframe()
        info = inspect.getframeinfo(frame)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Function name: {info.function} : {e}",
        )


if __name__ == "__main__":
    import argparse
    import uvicorn
    
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
