""" core 需要修改"""
from typing import Dict, Any
from modusched.core import Adapter
from serverz.core.tools import get_mcp_tools
from serverz.core.tools.fc import add_func



class ChatBox():
    """ chatbox """
    def __init__(self) -> None:
        self.ada = Adapter()
        self.model_list = ["Gemini2.5","BaseAgent"]
        self.agent = None

    async def init_chatbox(self):
        
        # build BaseAgent
        research_instructions = """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.
        You have access to an internet search tool as your primary means of gathering information.

        ## `add_func`

        Use this to add two numbers.

        ## `weather`

        Use this to get the weather.
        """

        # tools = await get_mcp_tools(
        #     {
        #         # "math": {
        #         #     "command": "python",
        #         #     # Make sure to update to the full absolute path to your
        #         #     # math_server.py file
        #         #     "args": ["/path/to/math_server.py"],
        #         #     "transport": "stdio",
        #         # },
        #         "weather": {
        #             "url": "http://localhost:8106/mcp_server/mcp",
        #             "transport": "streamable_http",
        #         }
        #     }
        # )
        tools = [add_func]
        self.agent = Adapter(type = "agent",
                             tools = tools,
                             system_prompt = research_instructions,
                             )

    async def aproduct(self,messages: str, model: str) -> str:
        """ 同步生成, 搁置 """
        print(messages,'messages')
        assert model in self.model_list
        if model == "Gemini2.5":
            result = await self.ada.apredict(messages=messages)
        elif model == "BaseAgent":
            result = await self.agent.apredict(messages=messages)
        else:
            result = "model name is None"
        print(result,'result')

        return result

    async def astream_product(self,messages: list[dict], model: str) -> Any:
        """
        # 只需要修改这里
        """
        assert model in self.model_list
        if model == "Gemini2.5":
            async for word in self.ada.astream(messages=messages):
                yield word

        elif model == "BaseAgent":
            async for word in self.agent.astream(messages=messages):
                yield word

        else:
            yield 'pass'


