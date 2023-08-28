import os
import pygame
import sounddevice as sd
import soundfile as sf
import threading
import time

def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()


def record_audio(recording_file, duration):
    sample_rate = 44100  # Adjust this to match your desired sample rate
    frames = int(duration * sample_rate)
    sd.default.device = 1

    audio = sd.rec(frames, channels=2, dtype='float32')
    sd.wait()

    sf.write(recording_file, audio, sample_rate)


def process_audio(audio_file, recording_file):
    print(f"Playing and recording: {audio_file} -> {recording_file}")

    playback_thread = threading.Thread(target=play_audio, args=(audio_file,))
    recording_thread = threading.Thread(target=record_audio, args=(recording_file, 6.0))  # 6-second recording duration
 
    playback_thread.start()
    recording_thread.start()

    playback_thread.join()
    recording_thread.join()


if __name__ == "__main__":
    input_folder = r"C:\Users\medag\OneDrive\Documents\Python Projects\Binaural _Hearing\Cubase_Recordings"
    output_folder = "C:\\Users\\medag\\PYTHON_OUTPUT"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".wav"):
                audio_file = os.path.join(root, file)
                recording_file = os.path.join(output_folder, file.replace(".wav", "_pr.wav"))

                process_audio(audio_file, recording_file)

    print("Playback and recording started for all files.")