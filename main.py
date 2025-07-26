from fastapi import FastAPI
from openai_agents.redirect_agent import redirect_message
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()
app = FastAPI()

class MessageRequest(BaseModel):
    msg: str

@app.post("/agent")
async def messager_sender(request: MessageRequest):
    print(request)
    return await redirect_message(request.msg)