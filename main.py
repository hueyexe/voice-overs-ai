#!/usr/bin/env python3

import argparse
from pathlib import Path
from story_narrator import StoryNarrator


def auto_mode(input_file, voice_prompt=None, device="cuda"):
    """Process large text file with automatic voice configuration."""
    if not Path(input_file).exists():
        print(f"❌ File not found: {input_file}")
        return

    print(f"🎖️ Processing large text: {input_file}")
    narrator = StoryNarrator(device=device)

    kwargs = {}
    if voice_prompt and Path(voice_prompt).exists():
        kwargs["global_audio_prompt"] = voice_prompt

    audio_files = narrator.process_text_file_directly(input_file, **kwargs)
    print(f"✅ Generated {len(audio_files)} audio files")


def manual_mode(
    text, voice_style="neutral", voice_prompt=None, output="output.wav", device="cuda"
):
    """Process small text with manual voice configuration."""
    print(f"🎯 Generating audio with {voice_style} style")
    narrator = StoryNarrator(device=device)

    wav = narrator.generate_segment_audio(text, voice_style, voice_prompt)
    narrator.audio_generator.save_audio(wav, output)
    print(f"✅ Audio saved: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="AI Voice Narrator - AI Text-to-Speech"
    )
    subparsers = parser.add_subparsers(dest="mode", help="Processing mode")

    # Auto mode for large texts
    auto_parser = subparsers.add_parser(
        "auto", help="Automatic processing for large texts"
    )
    auto_parser.add_argument("input_file", help="Text file to process")
    auto_parser.add_argument(
        "--voice-prompt", help="Reference audio file for voice cloning"
    )
    auto_parser.add_argument(
        "--device", default="cuda", choices=["cuda", "cpu"], help="Processing device"
    )

    # Manual mode for small texts
    manual_parser = subparsers.add_parser(
        "manual", help="Manual processing for small texts"
    )
    manual_parser.add_argument("text", help="Text to convert to speech")
    manual_parser.add_argument(
        "--voice-style",
        default="neutral",
        choices=["neutral", "calm"],
        help="Voice style",
    )
    manual_parser.add_argument(
        "--voice-prompt", help="Reference audio file for voice cloning"
    )
    manual_parser.add_argument(
        "--output", default="output.wav", help="Output audio file"
    )
    manual_parser.add_argument(
        "--device", default="cuda", choices=["cuda", "cpu"], help="Processing device"
    )

    args = parser.parse_args()

    if not args.mode:
        parser.print_help()
        return

    if args.mode == "auto":
        auto_mode(args.input_file, args.voice_prompt, args.device)
    elif args.mode == "manual":
        manual_mode(
            args.text, args.voice_style, args.voice_prompt, args.output, args.device
        )


if __name__ == "__main__":
    main()
