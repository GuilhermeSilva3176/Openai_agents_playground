from agent_handler import exit_session, send_audio_to_openai
from elevenlabs_handler import text_to_speech
from audio_record import audio_recording_in_chunks
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    try:
        for chunks, is_last in audio_recording_in_chunks():
            await send_audio_to_openai(chunks, is_last)

    except KeyboardInterrupt:
        print("Sessão encerrada pelo usuário.")
        await exit_session()    
    
    except Exception as e:
        print(f"Erro: {e}")
                  
asyncio.run(main())