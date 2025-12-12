# 1 日志不打在server中 不打在工具中, 只打在core 中
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel
import re
import os
from digital_life import logger
from digital_life.log import log_func
from datetime import datetime
from pro_craft_infer.core import AsyncIntel
from digital_life.model_public import MemoryCard

from tqdm import tqdm

class AIServerInputError(Exception):
    pass

class MemoryCardScore(BaseModel):
    score: int = Field(..., description="得分")
    reason: str = Field(..., description="给分理由")

class MemoryCardArticle(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")

class MemoryCardGenerate(BaseModel):
    title: str = Field(..., description="标题",min_length=1, max_length=30)
    content: str = Field(..., description="内容",min_length=1,max_length=1000)
    score: int = Field(..., description="卡片得分", ge=0, le=10)
    tag: str = Field(..., description="标签1, max_length=4")
    time: str = Field(..., description="日期格式,YYYY年MM月DD日,其中YYYY可以是4位数字或4个下划线,MM可以是2位数字或2个--,DD可以是2位数字或2个--。年龄范围 输出对应的文字描述, 比如:而立, 不惑")
    topic: int = Field(..., description="主题1-5",ge=0, le=5)


class MemoryCardsGenerate(BaseModel):
    memory_cards: list[MemoryCardGenerate] = Field(..., description="记忆卡片列表")


# 1. 定义记忆卡片模型 (Chapter)
class Chapter(BaseModel):
    """
    表示文档中的一个记忆卡片（章节）。
    """
    title: str = Field(..., description="记忆卡片的标题")
    content: str = Field(..., description="记忆卡片的内容")

class Chapters(BaseModel):
    chapters: List[Chapter] = Field(..., description="记忆卡片列表")




class TimeCheck_time(BaseModel):
    """
    注意, 如果有多个时间阶段, 只保留最早的一个
    """
    time: str = Field(...,description="----年--月--日")
    reason: str = Field(...,description="推理原因")

    @field_validator('time')
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        combined_regex = r"^(?:(\d{4}|-{4}|-{2})年(\d{2}|-{2})月(\d{2}|-{2})日)"
        match = re.match(combined_regex, v)
        if match:
            return v
        else:
            raise ValueError("时间无效")
        
class TimeCheck_timeline(BaseModel):
    """
    注意, 如果有多个时间阶段, 只保留最早的一个
    """
    stage: str = Field(...,description="根据发生的事件推测其发生的阶段")
    reason: str = Field(...,description="推理原因")
    @field_validator('stage')
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        if v in ["稚龄","少年","弱冠","而立","不惑","知天命","耳顺","古稀","耄耋","鲐背","期颐"]:
            return v
        else:
            raise ValueError("时间无效")

class MemoryCardManager:
    def __init__(self,model_name  = ""):
        self.inters = AsyncIntel(model_name = model_name,logger = logger)

    @log_func(logger)
    async def ascore_from_memory_card(self, memory_cards: list[str]) -> list[int]:
        result = await self.inters.inference_format_gather(
            input_datas=memory_cards,
            prompt_id = "memorycard-score",
            version = None,
            OutputFormat = MemoryCardScore,
        )
        return result

    @log_func(logger) # 函数 输入, 输出
    async def amemory_card_merge(self, memory_cards: list[str],birthday: str, age: str):
        result = await self.inters.inference_format(
            input_data=memory_cards,
            prompt_id = "memorycard-merge",
            version = None,
            OutputFormat = MemoryCard,
        )
        time = await self.get_time(content = result.get("content"), birthday = birthday, age = age)
        result.update({"time":time})
        return result

    @log_func(logger)
    async def amemory_card_polish(self, memory_card: dict) -> dict:
        result = await self.inters.inference_format(
            input_data=memory_card,
            prompt_id = "memorycard-polish",
            version = None,
            OutputFormat = MemoryCardArticle,
        )
        return result

    async def get_time(self,content,birthday = '',age = ''):
        doc = {"稚龄":"0到10岁",
                "少年":"11到20岁",
                "弱冠":"21到30岁",
                "而立":"31到40岁",
                "不惑":"41到50岁",
                "知天命":"51到60岁",
                "耳顺":"61到70岁",
                "古稀":"71到80岁",
                "耄耋":"81到90岁",
                "鲐背":"91到100岁",
                "期颐":"101到110岁"} 
        
        result_time = "----年--月--日"

        # 先做一个年月日格式的生成
        now_str = datetime.now().strftime("%Y年%m月%d日")

        datetime_output = await self.inters.inference_format(
            input_data={
                            "出生时间": birthday,
                            "now_time": now_str,
                            "content": content
                        },
            prompt_id = "memorycard-get-time",
            version=None,
            OutputFormat=TimeCheck_time,
            )
        result_time = datetime_output.get("time","----年--月--日")

        if "--年--月--日" in result_time: 
            # 说明没有检测出具体的时间 则寻找时间段
            ai_result_time = await self.inters.inference_format(
                input_data={
                            "当前年龄": age,
                            "content": content
                        },
                prompt_id = "memorycard-get-timeline",
                version=None,
                OutputFormat= TimeCheck_timeline,
                )
            stage = ai_result_time.get("stage","而立")
            result_time = doc[stage]

        return result_time

    @log_func(logger)
    async def agenerate_memory_card_by_text(self, chat_history_str: str, birthday: str, age : str):
        weight=int(os.getenv("card_weight",1000))
        number_ = len(chat_history_str) // weight + 1

        result_dict = await self.inters.inference_format(
            input_data={"建议输出卡片数量":  number_, "chat_history_str": chat_history_str},
            prompt_id = "memorycard-generate-content",
            version=None,
            OutputFormat= Chapters,
            )
        
        chapters = result_dict["chapters"]

        if [chapter.get("content") for chapter in chapters] == [""]:
            raise AIServerInputError("没有记忆卡片生成")
        
        chapters_with_tags = await self.inters.inference_format_gather(
                input_datas=[chapter for chapter in chapters],
                prompt_id = "memorycard-format",
                version = None,
                OutputFormat = MemoryCardGenerate,
            )

        for chapter_with_tag in tqdm(chapters_with_tags):
            time = await self.get_time(content = chapter_with_tag.get("content"), birthday = birthday, age = age)
            chapter_with_tag.update({"time":time})

        return chapters_with_tags
    
    def _generate_check(self,chat_history_str):
        if "human" not in chat_history_str:
            raise AIServerInputError("聊天历史生成记忆卡片时, 必须要有用户的输入信息")
        
        if "ai" in chat_history_str:
            chat_history_str = "human" + chat_history_str.split("human",1)[-1]
            chat_history_str = chat_history_str.rsplit("ai:",1)[0]
        return chat_history_str
    
    async def agenerate_memory_card(self, chat_history_str: str,birthday: str, age : str):
        chat_history_str = self._generate_check(chat_history_str)
        result = await self.agenerate_memory_card_by_text(chat_history_str = chat_history_str, birthday = birthday, age = age)
        return result


# ----年11月--日至次年02月--日