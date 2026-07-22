import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dataclasses import dataclass
from contextlib import AsyncExitStack

class MCPManager:
    def __init__(self):
        self.sessions = {}
        self.tool_mapping = {}
        self.exit_stack = AsyncExitStack()
        self.tools = []

    @dataclass
    class ConnectionResult:
        success: bool
        message: list[str]

    async def initialize(self,server_list):
        message = []
        success = True
        for server in server_list:
            connected = await self.connect_server(server)
            if connected:
                message.append(f"Connected: {server}")
            else:
                message.append(f"Failed: {server}")
                success = False
        if not success:
            return self.ConnectionResult(False,message) 
        await self.discover_tools()
        self.get_tools()
        return self.ConnectionResult(True,message)  
    
    async def connect_server(self,server):
        server_params = StdioServerParameters(
        command=server["command"],
        args=server["args"]
    )
        (read,write) = await self.exit_stack.enter_async_context(stdio_client(server_params))
        session = await self.exit_stack.enter_async_context(ClientSession(read,write))
        try:
            await session.initialize()
            self.sessions[server["name"]]=session
            return True
        except Exception as e:
            print(e)
            return False    

    async def discover_tools(self):
        openai_tools = []
        for session in self.sessions.values():
            tools = await session.list_tools()
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

        self.tools = openai_tools

    def get_tools(self):
        return self.tools

    async def call_tool(self,tool_name, arguments):
        # if arguments is str:
        session = self.tool_mapping[tool_name]
        arguments_json = json.loads(arguments)
        result = await session.call_tool(tool_name, arguments=arguments_json)
        return result
    
    async def close(self):
        await self.exit_stack.aclose()
