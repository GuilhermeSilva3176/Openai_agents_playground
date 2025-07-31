from fastapi import FastAPI
from openai_agents.main_agent import session_end, handle_message
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
load_dotenv()


async def main():
    try:
        while True:
            message = input("User: ")
            result = await handle_message(message.encode('utf-8'))

            print(f"bot: {result}")
            
            if message.lower() == "exit":
                break
    except Exception as e:
        print(f"Error starting session: {e}")
    finally:
        await session_end()
        print("Session ended successfully")
        
asyncio.run(main())