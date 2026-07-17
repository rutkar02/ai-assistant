import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPManager:
    def __init__(self):
        self.sessions = []
        self.tool_mapping = {}

    async def connect_server(self,server_name):
        server_params = StdioServerParameters(
        command="python",
        args=[f"{server_name}.py"]
    )
        async with stdio_client(server_params) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                self.sessions.append(session)

    async def discover_tools(self):
        openai_tools = []
        for session in self.sessions:
            tools = await session.list_tools()
            # pprint(tools.tools[0])
            # pprint(tools.tools[0].model_dump())
            for tool in tools.tools:
                tool_dict = tool.model_dump()
                openai_tool = {
                    "type": "function",
                    "name": tool_dict["name"],
                    "description": tool_dict["description"],
                    "parameters": tool_dict["inputSchema"],
                }
                openai_tools.append(openai_tool)
                self.tool_mapping[openai_tool["name"]] = session

        return openai_tools

    async def call_tool(self,tool_name, arguments):
        # if arguments is str:
        session = self.tool_mapping[tool_name]
        arguments_json = json.loads(arguments)
        result = await session.call_tool(tool_name, arguments=arguments_json)
        return result
