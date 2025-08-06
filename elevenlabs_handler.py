from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from config import ELEVEN_KEY

elevenlabs = ElevenLabs(api_key=ELEVEN_KEY)

async def text_to_speech(text: str):
    try:
        audio_stream = elevenlabs.text_to_speech.stream(
            text=text,
            voice_id="lWq4KDY8znfkV0DrK8Vb",
            model_id="eleven_flash_v2_5"
        )
        
        stream(audio_stream)
    except Exception as e:
        print(f"Error in text_to_speech: {e}")