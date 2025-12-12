# 代码生成(模板)
from agno.agent import Agent
from agno.tools.function import UserInputField
from agno.models.openai import OpenAIChat
from agno.models.openai.like import OpenAILike
from agno.tools import tool
from agno.tools.toolkit import Toolkit
from agno.tools.user_control_flow import UserControlFlowTools
from agno.utils import pprint
from agno.db.sqlite import SqliteDb
from agno.run import RunContext
from agno.os import AgentOS
from typing import List,Dict,Any
from pro_craft.code.manager import GenerateCodeByTemplate


research_instructions = """你是一个高级代码生成助手 Agent，你的主要职责是帮助用户通过模板快速生成代码。

**你的目标是：**
1.  **精确理解用户对代码功能和结构的自然语言描述。**
2.  **在现有模板库中，智能地找到最符合用户需求的模板。**
3.  **如果找不到高匹配度的模板，提示用户创建新模板。**
4.  **基于选定的模板和用户需求，生成一个结构化、可执行的 `REQUEST_START/END` 指令文件，用于后续的代码生成。**
5.  **在必要时与用户进行交互，澄清需求或提供建议。**
6.  **结合代码生成指导和模板, 生成代码**


**你的工作流程:**

1.  **接收用户需求：** 用户会提供一个自然语言描述。
2.  **初步理解与模板搜索：**
    *   首先使用 `search_template_by_demand` 工具，以用户需求的概要作为 `query`，找到最相关的模板。
    *   分析搜索结果中的 `match_score` 和 `description`，评估匹配度。
3.  **决策点 - 模板匹配：**
    *   **高匹配度：** 如果存在一个或少数几个模板的 `match_score` 显著高，且 `description` 与用户需求高度吻合：
        *   使用 `get_template_details` 获取该模板的完整信息。
        *   进入 **需求细化与指令生成** 阶段。
    *   **中等匹配度 / 多个相似匹配：** 如果有多个模板得分接近，或没有一个模板完美匹配：
        *   根据用户反馈，决定是选择一个模板还是引导用户创建新模板。
    *   **低匹配度 / 无匹配：** 如果没有找到任何合适的模板（例如，所有 `match_score` 都很低）：
        *   告知用户未能找到合适的模板，并询问用户是否希望提供多个示例代码，或者用户选定模板。
        *   如果用户没有模板, 则退出流程。
4.  **需求细化与指令生成 (基于选定模板):**
    *   一旦确定了模板，仔细解析用户需求的每个细节，并将其映射到选定模板中的 `BLOCK` 和 `PLACEHOLDER`。
    *   如果用户需求与模板的某个 `BLOCK` 或 `PLACEHOLDER` 不兼容，或用户没有提供足够的细节来填充某个区域，向用户提问。
    *   当所有必要信息都已获取且明确无误时，使用 `generate_request_file` 工具生成最终的 `REQUEST_START/END` 指令文件。
5.  **输出最终指令：** 将 `generate_request_file` 的输出返回给系统，以便进行下一步的代码生成。
6   ** 使用 generate_code_by_request 生成代码

**交互约束:**
*   除非使用工具，否则不要直接与用户对话。
*   始终以使用工具作为首选行动。
*   保持你的回复简洁、直接，聚焦于完成任务。

"""


agent = Agent(
    name="Code_Template",
    model=OpenAILike(
        # id="gemini-2.5-flash-preview-05-20-thinking",
        name="Agno Agent",
        id = "gpt-5.1",
        api_key="sk-XlROm9i34xEkNhOjueapJRgdRBsS2jsTqMrYY1S6WLmkEpyi",
        base_url="https://api.bianxieai.com/v1",
    ),
    instructions=[research_instructions],
    tools = [GenerateCodeByTemplate(database_url = "ai:ai@192.168.1.165:5432/ai",
                                    q_collection = "template_collection",
                                    q_host = "192.168.1.165",
                                    q_port = 6333,
                                    embed_model_name = "doubao-embedding-text-240715",
                                    embed_api_key = "39ad310a-c6f7-4d66-962e-1fbfa7e6edf1",
                      ),
             UserControlFlowTools()],
    markdown=True,
)


from agno.os import AgentOS
agent_os = AgentOS(
    id="code_template_01",
    description="一个写代码的agent",
    agents=[agent],
    # teams=[basic_team],
    # workflows=[basic_workflow]
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app=f"{__package__}.{__file__.split('/')[-1].split(".")[0]}:app",port = 7781, reload=True)