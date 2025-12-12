from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.user_control_flow import UserControlFlowTools
from agno.tools.memory import MemoryTools
from agno.tools.reasoning import ReasoningTools
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    id = "debug_agent",
    model=OpenAILike(
            # id="gemini-2.5-flash-preview-05-20-nothinking",
            id="gemini-2.5-flash-preview-05-20-thinking",
            name="Agno Agent",
            # id="gpt-5-mini",
            api_key="sk-XlROm9i34xEkNhOjueapJRgdRBsS2jsTqMrYY1S6WLmkEpyi",
            base_url="https://api.bianxieai.com/v1",
            reasoning_effort="low",
        ),
    session_state={"shopping_list": []},
    db=db,
    tools=[
        ReasoningTools(add_instructions=True,# 许多工具包都带有预先编写的指导，解释如何使用其工具。设置add_instructions=True将这些指令注入代理提示中
                       # ReasoningTools(enable_think=True, enable_analyze=True,
                       add_few_shot=True # 给定几个预编写好的 few - shot
                      ),
        MemoryTools(db=db, 
                    add_instructions=True,
                    add_few_shot=True,
                    enable_analyze=True,
                    enable_think=True,
                      ),
        UserControlFlowTools()
    ],
    # instructions=None,# str system_prompt
    markdown=True,
    add_history_to_context=True, # 控制是否携带上下文
    # debug_mode = True,
)

# 可直接拷贝 - 
from agno.os import AgentOS
agent_os = AgentOS(
    id="debug_01",
    description="一个用于改错和提问",
    agents=[agent],
    # teams=[basic_team],
    # workflows=[basic_workflow]
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app=f"{__package__}.{__file__.split('/')[-1].split(".")[0]}:app",port = 7780, reload=True)