from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel
import re

class PushOrderRequest(BaseModel):
    demand: str = Field(None, description="信息")
    prompt_id: str = Field(..., description="提示词id")
    action_type: str = Field(..., description="执行动作",min_length=1, max_length=10)

    @field_validator('action_type')
    @classmethod
    def validate_action_type(cls, v: str) -> str:
        if v in ['train','inference','summary','finetune','patch']:
            return v
        else:
            raise ValueError(f"无效action_type: {v}")

class GetPromptRequest(BaseModel):
    prompt_id: str = Field(..., description="提示词id")

class UpdatePromptRequest(BaseModel):
    prompt_id: str = Field(..., description="提示词id")
    prompt: str = Field(..., description="新的提示词")

class RollBackPromptRequest(BaseModel):
    prompt_id: str = Field(..., description="提示词id")
    version: str = Field(..., description="版本号")

class SyncDataBaseRequest(BaseModel):
    slave_database_url: str = Field(None, description="从属数据库url")
    

class PromptResponse(BaseModel):
    msg: str = Field(..., description="信息")
    content: str = None
