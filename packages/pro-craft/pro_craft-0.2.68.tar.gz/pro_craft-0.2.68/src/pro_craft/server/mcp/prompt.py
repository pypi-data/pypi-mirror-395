from mcp.server.fastmcp import FastMCP

from pro_craft import Intel,AsyncIntel
from .models import *

def create_mcp(database_url: str,
                  slave_database_url: str,
                  model_name: str,
                  logger = None):
    # region MCP Weather
    mcp = FastMCP("Prompt")

    intels = AsyncIntel(
        database_url=database_url,
        model_name=model_name,
        logger=logger
        )

    @mcp.tool()
    async def push_order(demand: str, prompt_id: str, action_type: str):
        """
        希望大模型进行哪种模式的调整
        demand: str = Field(None, description="信息")
        prompt_id: str = Field(..., description="提示词id")
        action_type: str = Field(..., description="执行动作",min_length=1, max_length=10)
        """
        try:
            PushOrderRequest(demand=demand,prompt_id=prompt_id,action_type=action_type)
            result = await intels.push_action_order(
                demand=demand,
                prompt_id=prompt_id,
                action_type=action_type
            )
            return PromptResponse(msg = "success",content=result)
        except Exception as e:
            return f"Error : {e}"
        
    @mcp.tool()
    async def get_registered_prompt():
        "获取以注册的可修改的提示词id"
        try:
            result = ["memorycard-format",
            "memorycard-polish",
            "memorycard-merge",
            "memorycard-score",
            "memorycard-generate-content",
            "user-overview",
            "user-relationship-extraction",
            "avatar-brief",
            "avatar-personality-extraction",
            "avatar-desensitization",
            "biograph-free-writer",
            "biograph-paid-title",
            "biograph-outline",
            "biograph-brief",
            "biograph-extract-person-name",
            "biograph-extract-place",
            "biograph-extract-material",
            "biograph-writer"]

            return PromptResponse(msg = "success",content=result)
        except Exception as e:
            return f"Error : {e}"


    @mcp.tool()
    async def sync_database():
        try:
            result = await intels.sync_production_database(slave_database_url)
            return PromptResponse(msg = "success",content=result)
        except Exception as e:
            return f"Error : {e}"

    return mcp

if __name__ == "__main__":
    mcp = create_mcp()
    mcp.run(transport="streamable-http")
