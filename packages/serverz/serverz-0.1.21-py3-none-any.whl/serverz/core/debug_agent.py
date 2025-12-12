from typing import List
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.function import UserInputField
from agno.tools.user_control_flow import UserControlFlowTools
from agno.tools.memory import MemoryTools
from agno.tools.reasoning import ReasoningTools
from agno.utils import pprint
from agno.db.sqlite import SqliteDb


class Work():
    def __init__(self):
        db = SqliteDb(db_file="tmp/agents.db")

        self.agent = Agent(
            model=OpenAILike(
                    id="gemini-2.5-flash-preview-05-20-thinking",
                    name="Agno Agent",
                    # id="gpt-5-mini",
                    api_key="sk-XlROm9i34xEkNhOjueapJRgdRBsS2jsTqMrYY1S6WLmkEpyi",
                    base_url="https://api.bianxieai.com/v1",
                    reasoning_effort="low",
                ),
            session_state={"shopping_list": []},
            db=db,
            # tools=[get_weather,add_item, HackerNewsTools()],# tools=[MCPTools(transport="streamable-http", url="https://docs.agno.com/mcp")],
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
            # instructions=None,
            markdown=True,
            
            # reasoning_model = reasoning_model,
            add_history_to_context=True, # 控制是否携带上下文
            # debug_mode = True,
            
        )

    def run(self, message):

        run_response = self.agent.run(message)


        # We use a while loop to continue the running until the agent is satisfied with the user input
        while run_response.is_paused:
            for tool in run_response.tools_requiring_user_input:
                input_schema: List[UserInputField] = tool.user_input_schema

                for field in input_schema:
                    # Display field information to the user
                    print(f"\nField: {field.name} ({field.field_type.__name__}) -> {field.description}")

                    # Get user input (if the value is not set, it means the user needs to provide the value)
                    if field.value is None:
                        user_value = input(f"Please enter a value for {field.name}: ")
                        field.value = user_value
                    else:
                        print(f"Value provided by the agent: {field.value}")

            run_response = self.agent.continue_run(run_response=run_response)

            # If the agent is not paused for input, we are done
            if not run_response.is_paused:
                print(11)
                print(run_response.content)

                break
        print(run_response.content)
        print(22)
