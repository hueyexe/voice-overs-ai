"""
Configuration and constants for AI Voice Narrator.
"""

# Voice style presets optimized for war narratives
VOICE_PRESETS = {
    "neutral": {"exaggeration": 0.5, "cfg_weight": 0.5},
    "calm": {"exaggeration": 0.3, "cfg_weight": 0.7},
}

# Default voice style patterns for auto-ingestion
DEFAULT_VOICE_PATTERN = ["neutral", "calm", "neutral"]

# Default settings for text processing
DEFAULT_SEGMENT_LENGTH = 250
DEFAULT_OUTPUT_DIR = "voice_output"
DEFAULT_PAUSE_DURATION = 0.5

# TTS Model settings
DEFAULT_DEVICE = "cuda"
MODEL_NAME = "chatterbox-tts"

# File extensions and formats
SUPPORTED_TEXT_FORMATS = [".txt", ".md"]
AUDIO_FORMAT = "wav"
JSON_FORMAT = "json"
