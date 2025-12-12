from pydantic import BaseModel, Field
from digital_life.log import log_func
from digital_life import logger
from pro_craft_infer.core import AsyncIntel

class ContentVer(BaseModel):
    content: str = Field(..., description="内容")

class BriefResponse(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    tags: list[str] = Field(..., description='["标签1","标签2"]')

class DigitalAvatar:
    def __init__(self,model_name = "doubao-1-5-pro-256k-250115"):
        self.inters = AsyncIntel(model_name = model_name)

    @log_func(logger)
    async def desensitization(self, memory_cards: list[str]) -> list[str]:
        """
        数字分身脱敏 0100
        0100
        """
        results = await self.inters.inference_format_gather(
            input_datas=memory_cards,
            prompt_id="avatar-desensitization",
            version=None,
            OutputFormat=ContentVer,
        )

        for i, memory_card in enumerate(memory_cards):
            memory_card["content"] = results[i].get("content")
        return memory_cards
    
    @log_func(logger)
    async def personality_extraction(self, memory_cards: list[dict],action:str,old_character:str) -> str:

        result = await self.inters.inference_format(
                                    input_data={
                                                "action": action,
                                                "old_character": old_character,
                                                "memory_cards": memory_cards
                                            },
                                    prompt_id ="avatar-personality-extraction",
                                    version = None,
                                    OutputFormat=None,
                                    )
        
        return result

    @log_func(logger)
    async def abrief(self, memory_cards: list[dict]) -> dict:

        result = await self.inters.inference_format(
                                input_data={
                                    "memory_cards": memory_cards
                                },
                                prompt_id="avatar-brief",
                                version = None,
                                OutputFormat = BriefResponse,
                                 )
        return result



