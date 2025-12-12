from langchain_mcp_adapters.client import MultiServerMCPClient  
import asyncio
async def get_mcp_tools(conn_dict = {}):
    client = MultiServerMCPClient(conn_dict)
    tools = await client.get_tools()
    return tools

if __name__ == "__main__":
    async def main():
        res = await get_mcp_tools(
            {
                # "math": {
                #     "command": "python",
                #     # Make sure to update to the full absolute path to your
                #     # math_server.py file
                #     "args": ["/path/to/math_server.py"],
                #     "transport": "stdio",
                # },
                "weather": {
                    "url": "http://localhost:8106/mcp_server/mcp",
                    "transport": "streamable_http",
                }
            }
        )
        return res
    
    x = asyncio.run(main())
    print(x,'xxx')
