

from fastapi import APIRouter
from pro_craft import Intel,AsyncIntel
from pro_craft.utils import create_async_session
from fastapi import FastAPI, HTTPException
from .models import *
from fastapi import APIRouter, Depends, HTTPException, status, Header
import os


def create_router(database_url: str,
                  model_name: str,
                  test_database_url: str = None,
                  product_database_url: str = None,
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


    head = "mysql+aiomysql://"
    test_database_url = head + test_database_url
    product_database_url = head + product_database_url


    intels = AsyncIntel(
        database_url=database_url,
        model_name=model_name,
        logger=logger
        )

    async def verify_api_key(authorization: Optional[str] = Header(None)):
        # if not authorization:
        #     raise HTTPException(status_code=401, detail="Invalid authorization scheme")
        # if not authorization.startswith("Bearer "):
        #     raise HTTPException(status_code=401, detail="Invalid authorization scheme")
        
        # token = authorization.split(" ")[1]
        authorization = authorization or "123578"
        
        key = os.getenv("prompt_api_key")

        if authorization != key:
            raise HTTPException(status_code=401, detail="Error Server Position2")

    router = APIRouter(
        tags=["prompt"], # 这里使用 Depends 确保每次请求都验证
        dependencies = [Depends(verify_api_key)]
    )

    # 自动修改
    @router.post("/push_order",
                description="可选 train,inference,summary,finetune,patch",
                response_model=PromptResponse,
                )
    async def push_order(request: PushOrderRequest):
        try:
            result = await intels.push_action_order(
                demand=request.demand,
                prompt_id=request.prompt_id,
                action_type=request.action_type
            )
            return PromptResponse(msg = "success",content=result)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )

    # 人为干预

    @router.get("/registered_prompt",
                description="获取已注册的提示词",
                response_model=PromptResponse)
    async def registered_prompt():
        try:
            async with create_async_session(intels.engine) as session:
                result = await intels.get_all_prompt_id(session)
            # result = ["memorycard-format",
            # "memorycard-polish",
            # "memorycard-merge",
            # "memorycard-score",
            # "memorycard-generate-content",
            # "user-overview",
            # "user-relationship-extraction",
            # "avatar-brief",
            # "avatar-personality-extraction",
            # "avatar-desensitization",
            # ""
            # "biograph-free-writer",
            # "biograph-paid-title",
            # "biograph-outline",
            # "biograph-brief",
            # "biograph-extract-person-name",
            # "biograph-extract-place",
            # "biograph-extract-material",
            # "biograph_material_add",
            # "biograph_material_init",
            # "biograph-writer"]

            return PromptResponse(msg = "success",content=result)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
        
    @router.post("/get_prompt",
                description="获得现行提示词",
                response_model=PromptResponse)
    async def get_prompt(request: GetPromptRequest):
        try:
            async with create_async_session(intels.engine) as session:
                result = await intels.get_prompt(
                    prompt_id=request.prompt_id,
                    version = request.version,
                    session=session
                )
            return PromptResponse(msg = "success",content={"prompt": result.prompt, "version": result.version})
    
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
        
    @router.post("/update_prompt",
                description="更新现行提示词",
                response_model=PromptResponse)
    async def update_prompt(request: UpdatePromptRequest):
        try:
            async with create_async_session(intels.engine) as session:
                await intels.save_prompt(
                                prompt_id = request.prompt_id,
                                new_prompt = request.prompt,
                                use_case = "",
                                action_type = "inference",
                                demand = "上传",
                                score = 70,
                                session = session)
                return PromptResponse(msg = "success",content="")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )

    @router.post("/rollback_prompt",
                description="回滚现行提示词",
                response_model=PromptResponse)
    async def roll_back(request: RollBackPromptRequest):
        try:
            async with create_async_session(intels.engine) as session:
                result = await intels.get_prompt(
                    prompt_id=request.prompt_id,
                    version = request.version,
                    session=session
                )
                assert result.version == request.version
                await intels.save_prompt(
                                prompt_id = request.prompt_id,
                                new_prompt = result.prompt,
                                use_case = result.use_case,
                                action_type = "inference",
                                demand = "",
                                score = 61,
                                session = session)
            return PromptResponse(msg = "success",content="")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
        
    @router.post("/update_logs",
                description="上传日志",
                response_model=PromptResponse)
    async def update_logs(request: UpdateLogsRequest):
        try:
            async with create_async_session(intels.engine) as session:

                await intels.save_prompt(
                                prompt_id = request.prompt_id,
                                new_prompt = result.prompt,
                                use_case = result.use_case,
                                action_type = "inference",
                                demand = "",
                                score = 61,
                                session = session)
            return PromptResponse(msg = "success",content="")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
    #系统级别服务

    @router.get("/sync_log")
    async def sync_log():
        try:
            database_url = "mysql+aiomysql://"+ os.getenv("log_database_url")
            log_path = os.getenv("log_file_path")
            result = await intels.sync_log(log_path,database_url=database_url)
            return PromptResponse(msg = "success",content="")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
    
    @router.post("/sync_test_database",
                 description="同步到测试数据库",
                response_model=PromptResponse)
    async def sync_test_database():
        try:
            result = await intels.sync_production_database(test_database_url)
            return PromptResponse(msg = "success",content="")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )
    
    @router.post("/sync_product_database",
                 description="同步到生产数据库",
                response_model=PromptResponse)
    async def sync_product_database():
        try:
            result = await intels.sync_production_database(product_database_url)
            return PromptResponse(msg = "success",content="")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"{e}"
            )

    return router
