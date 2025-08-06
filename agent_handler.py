from agents.realtime import RealtimeAgent, RealtimeRunner


agent = RealtimeAgent(
    name="Audio Agent",
    instructions="Você é um agente que responde o usuário em português brasileiro."
)

runner = RealtimeRunner(
    starting_agent=agent,
    config={
        "model_settings": {
            "model_name": "gpt-4o-realtime-preview",
            "voice": "alloy",
            "modalities": ["text"],
        }
    }
)

session = None

async def enter_session():
    global session
    session = await runner.run()
    await session.enter()
    if session:
        return True
    
    return False

async def exit_session():
    global session
    if session:
        await session.close()
        session = None
        return True
    
    return False

async def send_audio(audio_data):
    global session
    if not session:
        await enter_session()

    if session:
        await session.send_audio(audio_data)
            
        async for event in session:
            if event.type == "raw_model_event":
                if hasattr(event.data, "item") and hasattr(event.data.item, "role") and event.data.item.role == "assistant":
                    if event.data.item.content:
                        for content in event.data.item.content:
                            return content.text

    return False