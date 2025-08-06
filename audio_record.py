import pyaudio

def gravar_pcm24(rate=24000, channels=1, chunk=1024, record_seconds=5):
    FORMAT = pyaudio.paInt16
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=channels,
                    rate=rate, input=True, frames_per_buffer=chunk)
    print(f"Gravando {record_seconds}s em {rate}Hz mono PCM16...")
    frames = []
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    pcm_data = b''.join(frames)
    return pcm_data