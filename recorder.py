import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import threading
import time
from tqdm import tqdm

R   = "\033[91m"
G   = "\033[92m"
Y   = "\033[93m"
C   = "\033[96m"
P   = "\033[95m"
W   = "\033[97m"
DIM = "\033[2m"
RST = "\033[0m"
BOLD = "\033[1m"

def record_until_enter():
    fs = 44100
    audio_chunks = []

    def callback(indata, frames, time, status):
        audio_chunks.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        input("")

    if not audio_chunks:
        print(f"  {R}Error: No audio captured.{RST}")
        return

    recording = np.concatenate(audio_chunks, axis=0)
    temp_filename = "output_temp.wav"
    write(temp_filename, fs, recording)

    print(f"\n  {P}●{RST} {W}{'Status':<8}{RST}  {Y}TRANSCRIBING{RST}")

    audio_duration_sec = len(recording) / fs
    estimated_process_sec = max(5, audio_duration_sec / 8)

    result_holder = {}
    error_holder = {}

    def run_whisper():
        try:
            model = whisper.load_model("base")
            result_holder["result"] = model.transcribe(temp_filename, fp16=False)
        except Exception as e:
            error_holder["error"] = e

    whisper_thread = threading.Thread(target=run_whisper, daemon=True)
    whisper_thread.start()

    bar_format = f"  {DIM}{{l_bar}}{{bar}}| {{n_fmt}}/{{total_fmt}} [{{elapsed}}<{{remaining}}]{RST}"
    with tqdm(total=100, desc="  Whisper AI", bar_format=bar_format) as pbar:
        filled = 0
        tick = 0.2
        steps_to_95 = estimated_process_sec / tick
        step_size = 95.0 / steps_to_95

        while whisper_thread.is_alive():
            time.sleep(tick)
            increment = min(step_size, 95 - filled)
            if increment > 0:
                pbar.update(increment)
                filled += increment

        whisper_thread.join()
        remaining = 100 - filled
        if remaining > 0:
            pbar.update(remaining)

    if "error" in error_holder:
        print(f"  {R}Whisper error: {error_holder['error']}{RST}")
        return

    transcript = result_holder["result"]["text"].strip()
    with open("notes.txt", "w") as f:
        f.write(transcript)

    print(f"  {DIM}Transcription saved to notes.txt{RST}")

if __name__ == "__main__":
    record_until_enter()