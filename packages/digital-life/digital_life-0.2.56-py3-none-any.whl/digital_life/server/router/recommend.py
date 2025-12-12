from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from digital_life import logger
from digital_life.core import Recommend

router = APIRouter(tags=["recommend"])

rep = Recommend()


# ============================
# Pydantic Models
# ============================

class UpdateItem(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="要更新的文本内容。")
    id: str = Field(..., min_length=1, max_length=100, description="与文本关联的唯一ID。")
    type: int = Field(..., description="上传的类型：例如 0/1/2 表示卡片类型。")


class DeleteRequest(BaseModel):
    id: str = Field(..., min_length=1, max_length=100, description="要删除的文本/嵌入对应的唯一ID。")


class QueryItem(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=500, description="user_id")
    timestamp: str = Field(..., min_length=1, max_length=500, description="时间戳")
    current: int = Field(..., ge=1, description="当前页码（从1开始）。")
    size: int = Field(..., ge=1, le=100, description="每页大小。")


# ============================
# Routes
# ============================

@router.post(
    "/update",
    summary="更新或添加文本嵌入",
    description="将给定的文本内容与一个ID关联并更新到 Embedding 池中。",
    response_description="表示操作是否成功。",
)
def recommended_update(item: UpdateItem):
    if item.type not in (0, 1, 2):
        # 对无效 type 做显式校验，而不是走 try/except
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid type '{item.type}', only 0/1/2 are supported.",
        )

    try:
        rep.update(text=item.text, id=item.id, type=item.type)
        return {"status": "success", "message": f"ID '{item.id}' updated successfully."}
    except ValueError as e:  # 业务/参数错误
        logger.warning(f"Update failed for ID={item.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.exception(f"Unexpected error updating embedding for ID={item.id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating embedding.",
        )


@router.post(
    "/delete",
    summary="删除文本嵌入",
    description="根据 ID 删除对应的文本/嵌入信息。",
    response_description="表示操作是否成功。",
)
async def delete_server(request: DeleteRequest):
    try:
        rep.delete(id=request.id)
        return {"status": "success", "message": f"ID '{request.id}' deleted successfully."}
    except ValueError as e:
        logger.warning(f"Delete failed for ID={request.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.exception(f"Unexpected error deleting embedding for ID={request.id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting embedding.",
        )


@router.post(
    "/search_biographies_and_cards",
    summary="搜索传记和记忆卡片",
    description="根据 user_id、时间戳及分页信息搜索传记和记忆卡片。",
    response_description="搜索结果列表。",
)
async def recommended_biographies_and_cards(query_item: QueryItem):
    try:
        clear_result = await rep.recommended_biographies_and_cards(
            user_id=query_item.user_id,
            timestamp=query_item.timestamp,
            current=query_item.current,
            size=query_item.size,
        )
        return {
            "status": "success",
            "result": clear_result,
            "query": {
                "user_id": query_item.user_id,
                "timestamp": query_item.timestamp,
                "current": query_item.current,
                "size": query_item.size,
            },
        }
    except Exception as e:
        logger.exception(
            "Error in /search_biographies_and_cards",
            extra={"user_id": query_item.user_id},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while searching biographies and cards.",
        )


@router.post(
    "/search_figure_person",
    summary="搜索数字分身",
    description="根据 user_id、时间戳及分页信息搜索数字分身。",
    response_description="搜索结果列表。",
)
async def recommended_figure_person(query_item: QueryItem):
    try:
        clear_result = await rep.recommended_figure_person(
            user_id=query_item.user_id,
            timestamp=query_item.timestamp,
            current=query_item.current,
            size=query_item.size,
        )
        return {
            "status": "success",
            "result": clear_result,
            "query": {
                "user_id": query_item.user_id,
                "timestamp": query_item.timestamp,
                "current": query_item.current,
                "size": query_item.size,
            },
        }
    except Exception as e:
        logger.exception(
            "Error in /search_figure_person",
            extra={"user_id": query_item.user_id},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while searching figure person.",
        )