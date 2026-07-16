import json


async def discover_tools(session):
    tools = await session.list_tools()
    # pprint(tools.tools[0])
    # pprint(tools.tools[0].model_dump())
    openai_tools = []
    for tool in tools.tools:
        tool_dict = tool.model_dump()
        openai_tool = {
            "type": "function",
            "name": tool_dict["name"],
            "description": tool_dict["description"],
            "parameters": tool_dict["inputSchema"],
        }
        openai_tools.append(openai_tool)

    return openai_tools


async def call_tool(session, tool_name, arguments):
    # if arguments is str:
    arguments_json = json.loads(arguments)
    result = await session.call_tool(tool_name, arguments=arguments_json)
    return result
