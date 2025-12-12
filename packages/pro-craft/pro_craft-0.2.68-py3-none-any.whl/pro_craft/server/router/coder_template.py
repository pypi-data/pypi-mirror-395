
from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, Depends, HTTPException, status, Header

import os
from pro_craft.utils import create_async_session
from .models import PromptResponse, BaseModel

from pro_craft.code.tp_code_agent import agent
from typing import Optional
from pro_craft.code.write_code import write_code


def create_router(database_url: str,
                  slave_database_url: str,
                  model_name: str,
                  logger = None):
    """
    # TODO 整理改为异步
    创建一个包含 ProCraft 路由的 FastAPI APIRouter 实例。

    Args:
        database_url (str): 数据库连接字符串。
        model_name (str): 用于 Intel 实例的模型名称。
        api_key_secret (str, optional): 用于验证 API Key 的秘密字符串。
                                        如果提供，它将覆盖环境变量 PRO_CRAFT_API_KEY。
                                        如果都不提供，会使用硬编码的 'your_default_secret_key'。
    Returns:
        APIRouter: 配置好的 FastAPI APIRouter 实例。
    """
    class ChatInfo(BaseModel):
        content: str


    router = APIRouter(
        tags=["code_template"], # 这里使用 Depends 确保每次请求都验证
    )

    # 自动修改
    @router.post("/chat_with_agent",
                description="与agent 进行聊天",
                response_model=PromptResponse,
                )
    async def chat_with_agent(request: ChatInfo):
        try:
            result = agent.invoke({"messages": [{"role": "user", "content": request.content}]})
            print(result["messages"][-1].content)
            content = result["messages"][-1].content
            result = write_code(content)
            return PromptResponse(msg = "success",content=result)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
