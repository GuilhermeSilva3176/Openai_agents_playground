from agents import Agent, Runner
from pydantic import BaseModel
from .prompts.redirect_agent import PROMPT_MAIN_AGENT

class RedirectAnswer(BaseModel):
    agent_name: str
    user_message: str
    
redirect_agent = Agent(
    name="redirect_agent",
    instructions=PROMPT_MAIN_AGENT,
    model="gpt-4.1-nano",
    output_type=RedirectAnswer
)


async def redirect_message(data: str) -> dict:
    redirect = await Runner.run(redirect_agent, data)
        
    return redirect.dict()