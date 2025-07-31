from agents.realtime import RealtimeAgent, RealtimeRunner
from .prompts.main_agent import PROMPT_MAIN_AGENT

main_agent = RealtimeAgent(
    name="main_agent",
    instructions=PROMPT_MAIN_AGENT
)

runner = RealtimeRunner(
    starting_agent=main_agent,
    config={
        "model_settings": {
            "model_name": "gpt-4o-mini-realtime-preview",
            "voice": "alloy",
            "modalities": ["text"],
        }
    }
)

session = None

async def session_start():
    global session
    try:
        session = await runner.run()
        await session.enter()
        print("Session started successfully")
        return session
    except Exception as e:
        print(f"Error starting session: {e}")

async def session_end():
    global session
    try:
        if session:
            await session.close()
            print("Session ended successfully")
        else:
            print("No active session to end")
    except Exception as e:
        print(f"Error ending session: {e}")

async def handle_message(content_byte):
    global session
    try:
        if not session:
            session = await session_start()
        if session:
            print("Handling message in session")
            await session.send_message(content_byte)

            full_response = ""
            async for event in session:
                print(f"Event received: {event}")
                
                if event.type == "raw_model_event":
                    data = getattr(event, "data", None)
                    # Captura texto do assistente conforme ele chega
                    if hasattr(data, "item") and hasattr(data.item, "content"):
                        for chunk in data.item.content:
                            if hasattr(chunk, "text") and chunk.text:
                                full_response += chunk.text

                elif event.type == "error":
                    print(f"Error in session: {event.content.text}")
                    return f"Error: {event.content.text}"

                elif event.type == "raw_model_event" and getattr(event.data, "type", None) == "turn_ended":
                    print("Turn ended, exiting loop.")
                    break  # Fim da resposta

            return full_response if full_response else "No response from bot."

    except Exception as e:
        print(f"Error handling message: {e}")
        return None