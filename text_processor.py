"""
Text processing utilities for AI Voice Narrator.
Handles text cleaning, intelligent segmentation, and auto-ingestion.
"""

import re
import json
from pathlib import Path
from typing import Dict, List
from config import DEFAULT_VOICE_PATTERN, DEFAULT_SEGMENT_LENGTH


class TextProcessor:
    """Handles text processing and auto-ingestion for the AI Voice Narrator."""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text for TTS processing."""
        # Remove excessive whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)  # Limit consecutive newlines
        text = re.sub(r" {2,}", " ", text)  # Remove multiple spaces

        # Handle quotation marks for better TTS
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(""", "'").replace(""", "'")

        # Clean up common formatting issues
        text = re.sub(r"\s+([.!?])", r"\1", text)  # Remove space before punctuation

        return text.strip()

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting - can be improved with nltk if needed
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def intelligent_text_splitting(
        text: str, target_length: int = DEFAULT_SEGMENT_LENGTH
    ) -> List[str]:
        """
        Split text intelligently into segments of approximately target_length characters.

        Args:
            text: The text to split
            target_length: Target length per segment in characters

        Returns:
            List of text segments
        """
        # Clean up the text
        text = TextProcessor.clean_text(text)

        # Split into paragraphs first
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        segments = []
        current_segment = ""

        for paragraph in paragraphs:
            # If paragraph is very long, split it by sentences
            if len(paragraph) > target_length * 1.5:
                sentences = TextProcessor.split_into_sentences(paragraph)

                for sentence in sentences:
                    # If adding this sentence exceeds target length, start new segment
                    if (
                        len(current_segment) + len(sentence) > target_length
                        and current_segment
                    ):
                        segments.append(current_segment.strip())
                        current_segment = sentence + " "
                    else:
                        current_segment += sentence + " "
            else:
                # If adding this paragraph exceeds target length, start new segment
                if (
                    len(current_segment) + len(paragraph) > target_length
                    and current_segment
                ):
                    segments.append(current_segment.strip())
                    current_segment = paragraph + "\n\n"
                else:
                    current_segment += paragraph + "\n\n"

        # Add any remaining content
        if current_segment.strip():
            segments.append(current_segment.strip())

        return segments

    @staticmethod
    def auto_ingest_text_file(
        text_file_path: str,
        title: str = None,
        description: str = None,
        target_segment_length: int = DEFAULT_SEGMENT_LENGTH,
        voice_style_pattern: List[str] = None,
        global_audio_prompt: str = None,
        output_json_path: str = None,
    ) -> Dict:
        """
        Automatically convert a large text file into a structured story JSON.

        Args:
            text_file_path: Path to the text file to convert
            title: Title for the story (defaults to filename)
            description: Description of the story
            target_segment_length: Target character length per segment
            voice_style_pattern: List of voice styles to cycle through
            global_audio_prompt: Path to reference audio file
            output_json_path: Path to save the generated JSON (optional)

        Returns:
            Dictionary containing the generated story structure
        """
        text_path = Path(text_file_path)

        if not text_path.exists():
            raise FileNotFoundError(f"Text file not found: {text_file_path}")

        # Read the text file
        print(f"📖 Reading text file: {text_path.name}")
        with open(text_path, "r", encoding="utf-8") as f:
            text_content = f.read()

        # Set defaults
        if title is None:
            title = text_path.stem.replace("-", " ").replace("_", " ").title()

        if voice_style_pattern is None:
            voice_style_pattern = DEFAULT_VOICE_PATTERN.copy()

        # Split text into segments
        print(
            f"✂️  Splitting text into segments (target length: {target_segment_length} chars)"
        )
        segments = TextProcessor.intelligent_text_splitting(
            text_content, target_segment_length
        )

        # Create segments with voice variation
        story_segments = []
        voice_cycle_index = 0

        for i, segment_text in enumerate(segments):
            # Determine voice style
            voice_style = voice_style_pattern[
                voice_cycle_index % len(voice_style_pattern)
            ]
            voice_cycle_index += 1

            # Create segment object
            segment = {"text": segment_text.strip()}

            # Add voice style if not neutral
            if voice_style != "neutral":
                segment["voice_style"] = voice_style

            story_segments.append(segment)

        # Build the complete story structure
        story_data = {
            "title": title,
            "description": description or f"Auto-generated from {text_path.name}",
            "settings": {"voice_style": "neutral"},
            "create_full_audio": True,
            "segments": story_segments,
        }

        # Add global audio prompt if provided
        if global_audio_prompt:
            story_data["settings"]["audio_prompt"] = global_audio_prompt

        print(f"✅ Generated {len(story_segments)} segments from text")

        # Save JSON if path provided
        if output_json_path:
            output_path = Path(output_json_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(story_data, f, indent=4, ensure_ascii=False)
            print(f"💾 Saved JSON to: {output_path}")

        return story_data

    @staticmethod
    def load_story_from_json(json_path: str) -> Dict:
        """Load story data from JSON file."""
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
