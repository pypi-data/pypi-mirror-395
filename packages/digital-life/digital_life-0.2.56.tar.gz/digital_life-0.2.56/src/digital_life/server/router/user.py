from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from digital_life.model_public import MemoryCard
from digital_life.core import UserInfo

router = APIRouter(tags=["user"])

# 可按需改成依赖注入，但保持与原逻辑一致先用模块级单例
userinfo = UserInfo(model_name="doubao-seed-1-6-flash-250828")


# =========================
# Pydantic Models
# =========================
class UserOverviewRequest(BaseModel):
    action: str = Field(..., description="操作类型，例如 create / update 等")
    old_overview: str = Field(
        ..., description="已有的用户概述文本，用于在此基础上更新或生成"
        )
    memory_cards: List[MemoryCard] = Field(
        default_factory=list,
        description="与用户相关的记忆卡片列表，用于辅助生成概述",
    )


class UserOverviewResponse(BaseModel):
    overview: str = Field(..., description="根据输入生成或更新后的用户概述")


class UserRelationshipExtractionRequest(BaseModel):
    text: str = Field(..., description="需要提取用户关系信息的原始文本")


# class UserRelationshipExtractionResponse(BaseModel):
#     relation: str = Field(..., description="从文本中解析出的用户关系信息")


# =========================
# Routes
# =========================
@router.post(
    "/user_overview",
    response_model=UserOverviewResponse,
    description="根据历史概述和记忆卡片生成 / 更新用户概述",
)
async def user_overview_server(request: UserOverviewRequest) -> UserOverviewResponse:
    """
    用户概述生成接口。

    根据传入的 `action`、`old_overview` 以及 `memory_cards`，
    调用内部的 `userinfo.auser_overview` 核心逻辑生成新的用户概述。
    """
    try:
        result = await userinfo.auser_overview(
            action=request.action,
            old_overview=request.old_overview,
            memory_cards=request.model_dump()["memory_cards"],  # 直接使用字段，避免硬编码 key
        )
        return UserOverviewResponse(overview=result)
    except Exception as e:
        # 这里可以根据你项目的日志方案补充 logger.error
        # logger.error(f"user_overview_server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while generating user overview.",
        ) from e


@router.post(
    "/user_relationship_extraction",
    response_model=None,
    description="用户关系提取",
)
async def user_relationship_extraction_server(
    request: UserRelationshipExtractionRequest,
):
    """
    从给定文本中提取用户之间的关系信息。
    """
    try:
        result = await userinfo.auser_relationship_extraction(text=request.text)
        return {"relation": result}
        # return UserRelationshipExtractionResponse(relation=result)
    except Exception as e:
        # logger.error(f"user_relationship_extraction_server error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while extracting user relationships.",
        ) from e