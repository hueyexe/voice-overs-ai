"""
Utility functions for AI Voice Narrator.
Helper functions for file operations, validation, and formatting.
"""

from pathlib import Path
from typing import List, Optional
from config import SUPPORTED_TEXT_FORMATS


def validate_text_file(file_path: str) -> bool:
    """
    Validate that a text file exists and has a supported format.

    Args:
        file_path: Path to the text file

    Returns:
        True if file is valid, False otherwise
    """
    path = Path(file_path)

    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return False

    if path.suffix.lower() not in SUPPORTED_TEXT_FORMATS:
        print(f"❌ Unsupported file format: {path.suffix}")
        print(f"   Supported formats: {', '.join(SUPPORTED_TEXT_FORMATS)}")
        return False

    return True


def validate_audio_prompt(audio_path: Optional[str]) -> bool:
    """
    Validate that an audio prompt file exists.

    Args:
        audio_path: Path to the audio file (can be None)

    Returns:
        True if file is valid or None, False if invalid
    """
    if audio_path is None:
        return True

    path = Path(audio_path)

    if not path.exists():
        print(f"⚠️  Audio prompt file not found: {audio_path}")
        print("   Proceeding without voice cloning...")
        return False

    return True


def ensure_output_directory(output_dir: str) -> Path:
    """
    Ensure output directory exists and return Path object.

    Args:
        output_dir: Path to output directory

    Returns:
        Path object for the directory
    """
    dir_path = Path(output_dir)
    dir_path.mkdir(exist_ok=True)
    return dir_path


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:.0f}m {secs:.0f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours:.0f}h {minutes:.0f}m"


def estimate_processing_time(num_segments: int, avg_segment_time: float = 7.0) -> str:
    """
    Estimate total processing time for a given number of segments.

    Args:
        num_segments: Number of segments to process
        avg_segment_time: Average time per segment in seconds

    Returns:
        Formatted estimated time string
    """
    total_seconds = num_segments * avg_segment_time
    return format_duration(total_seconds)


def list_audio_files(directory: str, pattern: str = "*.wav") -> List[Path]:
    """
    List all audio files in a directory.

    Args:
        directory: Directory to search
        pattern: File pattern to match

    Returns:
        List of audio file paths
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    return sorted(list(dir_path.glob(pattern)))


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.

    Args:
        file_path: Path to the file

    Returns:
        File size in MB
    """
    path = Path(file_path)
    if not path.exists():
        return 0.0

    size_bytes = path.stat().st_size
    return size_bytes / (1024 * 1024)


def print_processing_summary(
    story_title: str,
    num_segments: int,
    generated_files: List[str],
    processing_time: Optional[float] = None,
):
    """
    Print a summary of processing results.

    Args:
        story_title: Title of the processed story
        num_segments: Number of segments processed
        generated_files: List of generated audio files
        processing_time: Total processing time in seconds (optional)
    """
    print(f"\n🎉 Processing Complete!")
    print(f"{'='*50}")
    print(f"📖 Story: {story_title}")
    print(f"📊 Segments: {num_segments}")
    print(f"🎵 Audio files: {len(generated_files)}")

    if generated_files:
        total_size = sum(get_file_size_mb(f) for f in generated_files)
        print(f"💾 Total size: {total_size:.1f} MB")

    if processing_time:
        print(f"⏱️  Processing time: {format_duration(processing_time)}")

    print(f"📁 Output directory: war_stories_output/")
    print(f"{'='*50}")
