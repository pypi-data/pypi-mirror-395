from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "vspell"
CONFIG_FILE = CONFIG_DIR / "vspell_config.json"
AUDIO_FILE = CONFIG_DIR / "input.wav"

MODEL_CACHE_DIR = Path.home() / ".cache" / "huggingface" / "hub"
