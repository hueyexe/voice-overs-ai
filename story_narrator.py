"""
Main War Story Narrator class.
Orchestrates text processing and audio generation for AI Voice Narration.
"""

from pathlib import Path
from typing import Dict, List, Optional
from audio_generator import AudioGenerator
from text_processor import TextProcessor
from config import DEFAULT_OUTPUT_DIR


class StoryNarrator:
    """AI Voice Narrator using Chatterbox TTS for generating voiceovers from JSON input."""

    def __init__(self, device: str = "cuda", output_dir: str = DEFAULT_OUTPUT_DIR):
        """
        Initialize the AI Voice Narrator.

        Args:
            device: Device to run the model on ("cuda" or "cpu")
            output_dir: Directory to save generated audio files
        """
        self.device = device
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize the audio generator
        self.audio_generator = AudioGenerator(device=device)

    def load_story_from_json(self, json_path: str) -> Dict:
        """Load story data from JSON file."""
        return TextProcessor.load_story_from_json(json_path)

    def generate_segment_audio(
        self,
        text: str,
        voice_style: str = "neutral",
        audio_prompt_path: Optional[str] = None,
        custom_params: Optional[Dict] = None,
    ):
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
        return self.audio_generator.generate_segment_audio(
            text=text,
            voice_style=voice_style,
            audio_prompt_path=audio_prompt_path,
            custom_params=custom_params,
        )

    def process_war_story(
        self, story_data: Dict, story_name: str = "war_story"
    ) -> List[str]:
        """
        Process a complete war story from JSON data.

        Args:
            story_data: Dictionary containing story segments and metadata
            story_name: Name for the output files

        Returns:
            List of generated audio file paths
        """
        generated_files = []
        segments = story_data.get("segments", [])
        global_settings = story_data.get("settings", {})

        print(f"Processing war story: {story_data.get('title', 'Untitled')}")
        print(f"Generating audio for {len(segments)} segments...")

        # Process each segment
        for i, segment in enumerate(segments):
            segment_text = segment.get("text", "")
            if not segment_text.strip():
                continue

            # Get segment-specific settings
            voice_style = segment.get(
                "voice_style", global_settings.get("voice_style", "neutral")
            )
            audio_prompt = segment.get(
                "audio_prompt", global_settings.get("audio_prompt")
            )
            custom_params = segment.get("tts_params", {})

            print(f"Processing segment {i+1}/{len(segments)}: {voice_style} style")

            # Generate audio for this segment
            wav = self.generate_segment_audio(
                text=segment_text,
                voice_style=voice_style,
                audio_prompt_path=audio_prompt,
                custom_params=custom_params,
            )

            # Save segment audio
            segment_filename = f"{story_name}_segment_{i+1:03d}.wav"
            segment_path = self.output_dir / segment_filename
            self.audio_generator.save_audio(wav, str(segment_path))
            generated_files.append(str(segment_path))

            print(f"Saved: {segment_filename}")

        # Generate concatenated version if requested
        if story_data.get("create_full_audio", True) and generated_files:
            complete_path = str(self.output_dir / f"{story_name}_complete.wav")
            self.audio_generator.concatenate_segments(generated_files, complete_path)

        return generated_files

    def process_story_from_file(self, json_file_path: str) -> List[str]:
        """
        Process a war story directly from a JSON file.

        Args:
            json_file_path: Path to the JSON file containing the story data

        Returns:
            List of generated audio file paths
        """
        # Load story data from JSON
        story_data = self.load_story_from_json(json_file_path)

        # Generate story name from filename
        story_name = Path(json_file_path).stem

        # Process the story
        return self.process_war_story(story_data, story_name)

    def batch_process_stories(self, json_directory: str) -> Dict[str, List[str]]:
        """
        Process multiple war stories from a directory of JSON files.

        Args:
            json_directory: Directory containing JSON story files

        Returns:
            Dictionary mapping story names to their generated audio file paths
        """
        json_dir = Path(json_directory)
        results = {}

        # Find all JSON files in the directory
        json_files = list(json_dir.glob("*.json"))

        if not json_files:
            print(f"No JSON files found in {json_directory}")
            return results

        print(f"Found {len(json_files)} story files to process...")

        # Process each story file
        for json_file in json_files:
            print(f"\n{'='*50}")
            print(f"Processing: {json_file.name}")
            print(f"{'='*50}")

            try:
                generated_files = self.process_story_from_file(str(json_file))
                results[json_file.stem] = generated_files
                print(f"✅ Successfully processed {json_file.name}")
            except Exception as e:
                print(f"❌ Error processing {json_file.name}: {str(e)}")
                results[json_file.stem] = []

        return results

    def auto_ingest_text_file(self, text_file_path: str, **kwargs) -> Dict:
        """
        Automatically convert a large text file into a structured war story JSON.

        Args:
            text_file_path: Path to the text file to convert
            **kwargs: Additional arguments passed to TextProcessor.auto_ingest_text_file

        Returns:
            Dictionary containing the generated story structure
        """
        return TextProcessor.auto_ingest_text_file(text_file_path, **kwargs)

    def process_text_file_directly(
        self, text_file_path: str, story_name: str = None, **kwargs
    ) -> List[str]:
        """
        Convenience method to convert text file to JSON and immediately process it.

        Args:
            text_file_path: Path to the text file
            story_name: Name for the generated audio files
            **kwargs: Additional arguments for auto_ingest_text_file

        Returns:
            List of generated audio file paths
        """
        # Generate JSON from text file
        story_data = self.auto_ingest_text_file(text_file_path, **kwargs)

        # Use filename as story name if not provided
        if story_name is None:
            story_name = Path(text_file_path).stem

        # Process the generated story
        return self.process_war_story(story_data, story_name)
