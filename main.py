from agent_handler import exit_session, send_audio
from elevenlabs_handler import text_to_speech
from audio_record import gravar_pcm24
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    try:
        while True:
            pcm_data = gravar_pcm24(record_seconds=5)
            print(f"Enviando {len(pcm_data)} bytes de PCM cru")
            openai_response = await send_audio(pcm_data)

            if openai_response:
                print(f"Resposta do OpenAI: {openai_response}")
                await text_to_speech(openai_response)

    except KeyboardInterrupt:
        print("Sessão encerrada pelo usuário.")
        await exit_session()    
    
    except Exception as e:
        print(f"Erro: {e}")
                  
asyncio.run(main())