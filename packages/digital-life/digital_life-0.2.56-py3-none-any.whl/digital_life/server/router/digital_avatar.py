
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from digital_life.model_public import MemoryCard
from digital_life.core import DigitalAvatar

router = APIRouter(tags=["digital_avatar"])
da = DigitalAvatar(model_name = "doubao-seed-1-6-flash-250828")


class BriefResponse(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    tags: list[str] = Field(..., description='["标签1","标签2"]')


class MemoryCards(BaseModel):
    memory_cards: list[MemoryCard] = Field(..., description="记忆卡片列表")


@router.post(
    "/brief", response_model=BriefResponse, description="数字分身介绍"
)
async def brief_server(request: MemoryCards):
    try:
        result = await da.abrief(memory_cards=request.model_dump()["memory_cards"])
        return BriefResponse(
                title=result.get("title"),
                content=result.get("content"),
                tags=result.get("tags")[:2],
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )

class AvatarXGRequests(BaseModel):
    action: str
    old_character: str
    memory_cards: list[MemoryCard]
    

@router.post("/personality_extraction")
async def digital_avatar_personality_extraction(request: AvatarXGRequests):
    """数字分身性格提取"""
    try:
        result = await da.personality_extraction(memory_cards=request.model_dump()["memory_cards"],
                                                 action = request.action,
                                                 old_character = request.old_character)
        return {"text": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )


@router.post("/desensitization",response_model=MemoryCards)
async def digital_avatar_desensitization(request: MemoryCards):
    """
    数字分身脱敏
    """
    try:
        result = await da.desensitization(memory_cards=request.model_dump()["memory_cards"])
        return MemoryCards(memory_cards = result)
    except Exception as e:
        # frame = inspect.currentframe()
        # info = inspect.getframeinfo(frame)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )