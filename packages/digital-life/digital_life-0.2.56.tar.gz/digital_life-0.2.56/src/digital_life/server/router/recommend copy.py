# server
# 推荐算法
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel
from digital_life import logger
from digital_life.core import Recommend

router = APIRouter(tags=["recommend"])

rep = Recommend()

class UpdateItem(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="要更新的文本内容。")
    id: str = Field(..., min_length=1, max_length=100, description="与文本关联的唯一ID。")
    type: int = Field(..., description="上传的类型")

@router.post(
    "/update",  # 推荐使用POST请求进行数据更新
    summary="更新或添加文本嵌入",
    description="将给定的文本内容与一个ID关联并更新到Embedding池中。",
    response_description="表示操作是否成功。",
)
def recommended_update(item: UpdateItem):
    try:
        if item.type in [0, 1, 2]:  # 上传的是卡片
            rep.update(text=item.text, id=item.id, type=item.type)
        else:
            logger.error(f'{e} & Error updating EmbeddingPool for ID &  {item.id}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update embedding for ID '{item.id}': {e}",
            )

        return {"status": "success", "message": f"ID '{item.id}' updated successfully."}

    except ValueError as e:  # 假设EmbeddingPool.update可能抛出ValueError
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )


class DeleteRequest(BaseModel):
    id: str

@router.post("/delete", response_model=None, description="delete")
async def delete_server(request: DeleteRequest):
    try:
        rep.delete(id=request.id)  # 包裹的内核函数
        return {"status":"success"}

    except ValueError as e:  # 假设EmbeddingPool.update可能抛出ValueError
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )


class QueryItem(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=500, description="user_id")
    timestamp: str = Field(..., min_length=1, max_length=500, description="timestamp")
    current: int
    size: int

@router.post(
    "/search_biographies_and_cards",
    summary="搜索传记和记忆卡片",
    description="搜索传记和记忆卡片",
    response_description="搜索结果列表。",
)
async def recommended_biographies_and_cards(query_item: QueryItem):
    try:
        
        clear_result = await rep.recommended_biographies_and_cards(user_id = query_item.user_id,
                                                                   timestamp=query_item.timestamp,
                                                                   current=query_item.current,
                                                                    size=query_item.size,
             )

        return {
            "status": "success",
            "result": clear_result,
            "query": query_item.user_id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )



@router.post(
    "/search_figure_person",
    description="搜索数字分身的",
)
async def recommended_figure_person(query_item: QueryItem):
    try:

        clear_result = await rep.recommended_figure_person(user_id = query_item.user_id,
                                                           timestamp = query_item.timestamp,
                                                           current=query_item.current,
                                                           size=query_item.size,
             )
        return {
            "status": "success",
            "result": clear_result,
            "query": query_item.user_id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error Info: {e}",
        )

