from openai import OpenAI
from mcp_client import discover_tools
from mcp import ClientSession, StdioServerParameters
from agent import run_agent_loop
from memory import retrieve_memory,judge_memory,extract_memory,save_memory
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
# from pprint import pprint

load_dotenv()

class Assistant:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.previous_response_id = None
        self.session = None
        self.tools = None

    # async def initialize(self):

    async def chat(self):
        server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )
        async with stdio_client(server_params) as (read,write):
            async with ClientSession(read,write) as session:
                self.session = session
                await self.session.initialize()
                # self.tools = await self.session.list_tools()
                self.tools = await discover_tools(self.session)
                while True:
                    user = input("> ")    
                    if user.lower() == "end":
                        break
                    memory = retrieve_memory(user,self.client)
                    self.messages.append({"role": "user", "content": user})
                    # pprint(self.tools)
                    response =await run_agent_loop(conversation = self.messages,memories = memory,previous_response_id=self.previous_response_id,session = self.session,tools = self.tools,client = self.client)
                    if judge_memory(response,self.client):
                        memory = extract_memory(response,self.client)
                        save_memory(memory)

                    print(response.output_text)   
        #get user input
        #retrieve memories
        # run agent loop
        # print final response
        # judge memory
        # extract memory
        # save memory

async def main():
    assistant = Assistant()
    await assistant.chat()

    #initilaize openi 
    #connect to mcp 
    #iscovers tools 
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())    

