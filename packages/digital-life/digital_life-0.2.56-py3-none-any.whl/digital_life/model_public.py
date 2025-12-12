
# server
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel
import re


class MemoryCard(BaseModel):
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    time: str = Field(None, description="卡片记录事件的发生时间")
    tag: str = Field(None, description="标签1,max_length=4")
