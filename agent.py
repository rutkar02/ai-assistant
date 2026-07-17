from model import call_model
# from mcp_client import call_tool
from mcp_manager import MCPManager
# from pprint import pprint

async def run_agent_loop(messages,previous_response_id,manager,client):
    tools = manager.discover_tools()
    while True:
        response = call_model(messages,previous_response_id,tools,client)
        tool_calls = False
        previous_response_id = response.id
        for item in response.output:
            if item.type=="function_call":
                tool_calls=True
                result = await manager.call_tool(item.name,item.arguments)
                # pprint(result)
                # pprint(type(result))
                messages.append({
                    "type": "function_call_output",
                    "call_id":item.call_id,
                    "output": result.content[0].text             
                })    
        if not tool_calls:
            return response    

        #call model
        # if tool calls
        # execute tool
        # if no tool calls
        # return answer