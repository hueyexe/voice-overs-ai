"""
Audio generation utilities for AI Voice Narrator.
Handles TTS model interaction and audio processing.
"""

from typing import Dict, List, Optional
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from config import VOICE_PRESETS, DEFAULT_PAUSE_DURATION


class AudioGenerator:
    """Handles audio generation using Chatterbox TTS."""

    def __init__(self, device: str = "cuda"):
        """
        Initialize the audio generator.

        Args:
            device: Device to run the model on ("cuda" or "cpu")
        """
        self.device = device

        # Initialize the TTS model
        print("Loading Chatterbox TTS model...")
        self.model = ChatterboxTTS.from_pretrained(device=device)
        print("Model loaded successfully!")

    def generate_segment_audio(
        self,
        text: str,
        voice_style: str = "neutral",
        audio_prompt_path: Optional[str] = None,
        custom_params: Optional[Dict] = None,
    ) -> torch.Tensor:
        """
        Generate audio for a single text segment.

        Args:
            text: Text to convert to speech
            voice_style: Predefined voice style ("neutral", "calm")
            audio_prompt_path: Path to audio file for voice cloning
            custom_params: Custom TTS parameters to override defaults

        Returns:
            Generated audio tensor
        """
        # Get base parameters from voice style
        params = VOICE_PRESETS.get(voice_style, VOICE_PRESETS["neutral"]).copy()

        # Override with custom parameters if provided
        if custom_params:
            params.update(custom_params)

        # Generate audio
        if audio_prompt_path:
            wav = self.model.generate(
                text, audio_prompt_path=audio_prompt_path, **params
            )
        else:
            wav = self.model.generate(text, **params)

        return wav

    def concatenate_segments(
        self,
        audio_files: List[str],
        output_path: str,
        pause_duration: float = DEFAULT_PAUSE_DURATION,
    ):
        """
        Concatenate multiple audio segments into a single file.

        Args:
            audio_files: List of audio file paths to concatenate
            output_path: Path for the output file
            pause_duration: Duration of pause between segments in seconds
        """
        print(f"Concatenating {len(audio_files)} segments...")

        # Load all audio files
        audio_tensors = []
        for file_path in audio_files:
            audio, _ = ta.load(file_path)
            audio_tensors.append(audio)

            # Add pause between segments (except after the last one)
            if file_path != audio_files[-1]:
                pause_samples = int(pause_duration * self.model.sr)
                pause = torch.zeros(1, pause_samples)
                audio_tensors.append(pause)

        # Concatenate all audio
        combined_audio = torch.cat(audio_tensors, dim=1)

        # Save combined audio
        ta.save(output_path, combined_audio, self.model.sr)
        print(f"Complete audio saved: {output_path}")

    def save_audio(self, audio_tensor: torch.Tensor, file_path: str):
        """
        Save audio tensor to file.

        Args:
            audio_tensor: The audio data to save
            file_path: Path where to save the audio file
        """
        ta.save(file_path, audio_tensor, self.model.sr)
