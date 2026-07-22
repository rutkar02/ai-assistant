from openai import OpenAI
from agent import run_agent_loop
from memory import retrieve_memory,judge_memory,extract_memory,save_memory
from dotenv import load_dotenv
from context import build_context
from knowledge import retrieve_knowledge
from commands import handle_command
from mcp_manager import MCPManager
from config import server
# from pprint import pprint

load_dotenv()

class Assistant:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []
        self.previous_response_id = None
        self.manager = MCPManager()   

    async def initialize(self):
        result = await self.manager.initialize(server)
        if not result.success:
            print("Some Mcp servers failed to initialize")     

    async def chat(self):
        while True:
            user = input("> ")    
            # ✅ Allow multiple exit keywords
            if user.lower().strip() in ["end", "exit", "quit", "q"]:
                print("Goodbye!")
                await self.manager.close()  # Cleanly close MCP sessions!
                break
            result = handle_command(user,self.client)
            if(result.handled):
                print(result.message)
                continue
            memory = retrieve_memory(user,self.client)
            knowledge = retrieve_knowledge(user,self.client)
            self.messages.append({"role": "user", "content": user})
            prompt = build_context(self.messages,memory,knowledge)
            response =await run_agent_loop(prompt,previous_response_id=self.previous_response_id,manager = self.manager,client = self.client)
            self.previous_response_id = response.id
            if judge_memory(response,self.client):
                memory = extract_memory(response,self.client)
                save_memory(memory)

            print(response.output_text)   
            self.messages.append({
                "role": "assistant",
                "content": response.output_text
            })

async def main():
    assistant = Assistant()
    await assistant.initialize()
    await assistant.chat()
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())    

