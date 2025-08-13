import pyaudio
import webrtcvad
import collections
import sys
import signal
import os

RATE = 16000
CHANNELS = 1
FRAME_DURATION = 30
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
VAD_AGGRESSIVENESS = 2
MAX_SILENCE_DURATION = 2 
FRAMES_PER_CHUNK = 3

vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
pa = pyaudio.PyAudio()

stream = pa.open(format=pyaudio.paInt16,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=FRAME_SIZE)

print("Iniciando gravação de áudio. Pressione Ctrl+C para parar.")

def audio_recording_in_chunks():
    speaking = False
    silence_counter = 0
    temp_frames = []
    
    try:
        while True:
            audio_data = stream.read(FRAME_SIZE, exception_on_overflow=False)
            is_voice = vad.is_speech(audio_data, RATE)

            if is_voice:
                temp_frames.append(audio_data)
                silence_counter = 0
                
                if not speaking:
                    speaking = True
                    print("Início da fala detectado")
                    
                if len(temp_frames) >= FRAMES_PER_CHUNK:
                    chunk_data = b''.join(temp_frames)
                    temp_frames = []
                    print(f"Detectando chunks")
                    yield chunk_data, False
                    
            else:
                if speaking:
                    silence_counter += 1
                    temp_frames.append(audio_data)

                    if silence_counter > MAX_SILENCE_DURATION:
                        
                        if temp_frames:
                            chunk_data = b''.join(temp_frames)
                            temp_frames = []
                            print(f"Detectando chunk final")
                            yield chunk_data, True

                        silence_counter = 0
                        speaking = False
                        print("Fim da fala detectado")
                else:
                    silence_counter = 0
                    temp_frames = []
    except KeyboardInterrupt:
        print("Gravação interrompida.")
        stream.stop_stream()
        stream.close()
        pa.terminate()

# def gravar_pcm24(rate=24000, channels=1, chunk=1024, record_seconds=5):
#     FORMAT = pyaudio.paInt16
#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT, channels=channels,
#                     rate=rate, input=True, frames_per_buffer=chunk)
#     print(f"Gravando {record_seconds}s em {rate}Hz mono PCM16...")
#     frames = []
#     for _ in range(0, int(rate / chunk * record_seconds)):
#         data = stream.read(chunk)
#         frames.append(data)
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     pcm_data = b''.join(frames)
#     return pcm_data