
from fastapi import APIRouter, HTTPException, status
import asyncio
import uuid
from digital_life.redis_ import get_value
from digital_life.core import BiographyGenerate
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel



class MemoryCard_biograph(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    time: str = Field(..., description="卡片记录事件的发生时间")
    theme_id: str = Field(None, description="theme_id")


class BiographyRequest(BaseModel):
    """
    请求传记生成的数据模型。
    """

    user_name: str = Field(None, description="用户名字")
    vitae: str = Field(None, description="用户简历")
    memory_cards: list[MemoryCard_biograph] = Field(..., description="记忆卡片列表")
    # 可以在这里添加更多用于生成传记的输入字段


class BiographyResult(BaseModel):
    """
    传记生成结果的数据模型。
    """

    task_id: str = Field(..., description="任务的唯一标识符。")
    status: str = Field(
        ...,
        description="任务的当前状态 (e.g., 'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED').",
    )
    biography_title: Optional[str] = Field(None, description="传记标题")

    biography_brief: Optional[str] = Field(
        None, description="生成的传记简介，仅在状态为 'COMPLETED' 时存在。"
    )
    biography_json: dict | None = Field(
        None, description="生成的传记文本，仅在状态为 'COMPLETED' 时存在。"
    )
    biography_name: list[str] | None = Field(
        None, description="生成的传记文本中的人名，仅在状态为 'COMPLETED' 时存在。"
    )
    biography_place: list[str] | None = Field(
        None, description="生成的传记文本中的地名，仅在状态为 'COMPLETED' 时存在。"
    )
    error_message: Optional[str] = Field(
        None, description="错误信息，仅在状态为 'FAILED' 时存在。"
    )
    progress: float = Field(
        0.0, ge=0.0, le=1.0, description="任务处理进度，0.0到1.0之间。"
    )


bg = BiographyGenerate(model_name = "doubao-1-5-pro-32k-250115")# TODO 1
# bg = BiographyGenerate(model_name = "doubao-1-5-pro-256k-250115")

router = APIRouter(tags=["biography"])

# 免费版传记优化
@router.post("/generate_biography_free", summary="提交传记生成请求")
async def generate_biography(request: BiographyRequest):
    """
    提交一个传记生成请求。

    此接口会立即返回一个任务ID，客户端可以使用此ID查询生成进度和结果。
    实际的生成过程会在后台异步执行。
    """
    try:
        memory_cards = request.model_dump()["memory_cards"]
        result = await bg.agenerate_biography_free(
            user_name=request.user_name,
            memory_cards=memory_cards,
            vitae=request.vitae,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )


@router.post(
    "/generate_biography", response_model=BiographyResult, summary="提交传记生成请求"
)
async def generate_biography(request: BiographyRequest):
    """
    提交一个传记生成请求。

    此接口会立即返回一个任务ID，客户端可以使用此ID查询生成进度和结果。
    实际的生成过程会在后台异步执行。
    """
    try:

        task_id = str(uuid.uuid4())
        memory_cards = request.model_dump()["memory_cards"]
        vitae = request.vitae
        user_name = request.user_name
        asyncio.create_task(bg._generate_biography(task_id, 
                                                   memory_cards = memory_cards,
                                                   vitae = vitae,
                                                   user_name = user_name
                                                   ))
        return BiographyResult(task_id=task_id, status="PENDING", progress=0.0)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )

@router.get(
    "/get_biography_result/{task_id}",
    response_model=BiographyResult,
    summary="查询传记生成结果",
)
async def get_biography_result(task_id: str):
    """
    根据任务ID查询传记生成任务的状态和结果。
    """
    try:
        task_info = get_value(bg.biograph_redis,task_id)
        if not task_info:
            raise HTTPException(
                status_code=404, detail=f"Task with ID '{task_id}' not found."
            )
        return BiographyResult(
            task_id=task_info["task_id"],
            status=task_info["status"],
            biography_title=task_info.get("biography_title", "未知"),
            biography_brief=task_info.get("biography_brief", "未知"),
            biography_json=task_info.get("biography_json", {}),
            biography_name=task_info.get("biography_name", []),
            biography_place=task_info.get("biography_place", []),
            error_message=task_info.get("error_message"),
            progress=task_info.get("progress", 0.0),
        )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )



