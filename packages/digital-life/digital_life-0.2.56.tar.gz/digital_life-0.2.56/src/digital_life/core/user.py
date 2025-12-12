
from typing import Dict
from pydantic import BaseModel, Field, RootModel
from digital_life.log import log_func
from digital_life import logger
from pro_craft_infer.core import AsyncIntel

class UserInfo:
    def __init__(self,model_name = "doubao-1-5-pro-256k-250115"):
        self.inters = AsyncIntel(model_name = model_name,logger=logger)

    @log_func(logger)
    async def auser_relationship_extraction(self,text: str) -> dict:

        class PersonInfo(BaseModel):
            """
            表示一个人的详细信息。
            """
            relationship: str = Field(..., description="与查询对象的_关系_")
            profession: str = Field(..., description="职业信息")
            birthday: str = Field(..., description="生日信息 (格式可根据实际情况调整)")

        class CharactersData(RootModel[Dict[str, PersonInfo]]):
            """
            表示一个包含多个角色信息的字典，键为角色名称，值为 PersonInfo 模型。
            """
            pass # RootModel 不需要定义额外的字段，它直接代理其泛型类型

        result = await self.inters.inference_format(
                        input_data={"chat_history": text},
                        prompt_id="user-relationship-extraction",
                        version = None,
                        OutputFormat = CharactersData,
                            )
        return result

    @log_func(logger)
    async def auser_overview(self,action: str,old_overview: str, memory_cards: list[dict]) -> str:

        result = await self.inters.inference_format(
                input_data={
                            "action": action,
                            "old_overview": old_overview,
                            "memory_cards": memory_cards
                            },
                prompt_id="user-overview",
                version = None,
                OutputFormat = None,
                    )
        return result

