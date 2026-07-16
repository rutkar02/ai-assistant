from openai import OpenAI
from mcp_client import discover_tools
from mcp import ClientSession, StdioServerParameters
from agent import run_agent_loop
from memory import retrieve_memory,judge_memory,extract_memory,save_memory
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from prompt import build_prompt
from knowledge import retrieve_knowledge,ingest_document
from config import PDF_PATH
from commands import handle_command
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
                ingest_document(PDF_PATH,self.client)

                while True:
                    user = input("> ")    
                    if user.lower() == "end":
                        break
                    if(handle_command(user,self.client)):
                        continue
                    memory = retrieve_memory(user,self.client)
                    knowledge = retrieve_knowledge(user,self.client)
                    self.messages.append({"role": "user", "content": user})
                    prompt = build_prompt(self.messages,memory,knowledge)
                    response =await run_agent_loop(prompt,previous_response_id=self.previous_response_id,session = self.session,tools = self.tools,client = self.client)
                    self.previous_response_id = response.id
                    if judge_memory(response,self.client):
                        memory = extract_memory(response,self.client)
                        save_memory(memory)

                    print(response.output_text)   
                    self.messages.append({
                        "role": "assistant",
                        "content": response.output_text
                    })
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

