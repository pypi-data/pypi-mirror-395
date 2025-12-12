import sounddevice as sd
from scipy.io.wavfile import write, read
from faster_whisper import WhisperModel
import pyperclip
import os
import time
import numpy as np
import json
import argparse
import string
from .constants import CONFIG_DIR,CONFIG_FILE, MODEL_CACHE_DIR, AUDIO_FILE
from .utils.spinner import Spinner

# ---------------------------
# Configuration
# ---------------------------
def save_config(threshold):
    config = {"silence_threshold": threshold}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print(f"Saved silence threshold: {threshold:.6f} → {CONFIG_FILE}")

def load_config(default_threshold=0.003):
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("silence_threshold", default_threshold)
        except Exception:
            pass
    return default_threshold


# ---------------------------
# Audio
# ---------------------------
def record_audio(filename=AUDIO_FILE, duration=2, samplerate=16000):
    spinner = Spinner(f"Listening for {int(duration)} seconds...")
    spinner.start()
    audio = sd.rec(int(duration*samplerate), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()
    write(filename, samplerate, audio)
    spinner.stop()
    return filename, audio

def is_silent(audio):
    threshold = load_config()
    return np.max(np.abs(audio)) < threshold

# ---------------------------
# Calibration
# ---------------------------
def calibrate_noise(duration=2, samplerate=16000):
    print("Starting calibration…")
    print(f"Remain silent for {duration} seconds.")

    spinner = Spinner("Calibrating ambient noise…")
    spinner.start()
    audio = sd.rec(int(duration*samplerate), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()
    spinner.stop()

    noise_level = float(np.max(np.abs(audio)))
    threshold = noise_level * 2.5
    print(f"\nMeasured ambient noise: {noise_level:.6f}")
    print(f"Recommended threshold: {threshold:.6f}\n")
    save_config(threshold)
    print("Calibration complete.")

# ---------------------------
# Playback
# ---------------------------
def playback_audio(filename=AUDIO_FILE, volume=2.0):
    if not os.path.exists(filename):
        print(f"Audio file {filename} not found!")
        return

    print(f"Playing back recorded audio at {volume}× volume...")
    # Fallback using numpy + sounddevice
    samplerate, data = read(filename)
    data = data * volume  # scale amplitude
    data = np.clip(data, -1.0, 1.0)  # avoid clipping
    sd.play(data, samplerate)
    sd.wait()
        

# ---------------------------
# Model
# ---------------------------

def load_model(model_size="medium"):
    model_exists = any(
        model_size in p for p in os.listdir(MODEL_CACHE_DIR)
    ) if os.path.exists(MODEL_CACHE_DIR) else False

    if not model_exists:
        print("\n==============================")
        print("   Downloading model...")
        print("   This may take a few minutes.")
        print("==============================\n")

    spinner = Spinner("Loading model…")
    spinner.start()

    try:
        start = time.time()

        model = WhisperModel(model_size, device="auto", compute_type="float32")

        end = time.time()

        if not model_exists:
            print(f"Model download complete in {end-start:.1f} seconds!\n")

        return model

    except Exception as e:
        print("\n❌ ERROR: Could not load Whisper model.")
        print(f"Reason: {e}\n")
        return None

    finally:
        spinner.stop()


def transcribe_audio(model, filename):
    segments, _ = model.transcribe(filename)
    text = "".join(segment.text for segment in segments)
    return text.strip()


def remove_punctuation(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

# ---------------------------
# Main CLI
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="VSpell - Voice spelling tool")
    parser.add_argument("--calibrate", action="store_true", help="Calibrate ambient noise threshold")
    parser.add_argument("--punctuate", action="store_true", help="Retain punctuation and original casing in transcribed text")
    parser.add_argument("--playback", type=float, nargs='?', const=1.0,
                    help="Playback recorded audio with optional volume multiplier (default=1.0)")
    parser.add_argument("--duration", type=float, default=2, help="Recording duration in seconds")
    parser.add_argument("--model", type=str, default="medium", help="Whisper model size [tiny, base, small, medium, large] (default=medium)")
    args = parser.parse_args()
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if args.playback:
        playback_audio(volume=args.playback)
        return

    if args.calibrate:
        calibrate_noise(duration=args.duration)
        return

    print(f"Using silence threshold: {load_config():.6f}")

    model = load_model(args.model)
    if not model:
        return

    audio_file, audio = record_audio(duration=args.duration)

    if is_silent(audio):
        print("No speech detected — nothing transcribed.")
        pyperclip.copy("")
        return

    spinner = Spinner("Transcribing…")
    spinner.start()
    text = transcribe_audio(model, audio_file)
    if not args.punctuate:
        text = remove_punctuation(text)
    spinner.stop()

    print(f"Transcribed: {text}")
    pyperclip.copy(text)
    print("Text copied to clipboard.")

if __name__ == "__main__":
    main()
