# 🎖️ AI Voice Narrator

AI-powered text-to-speech system for voice generation with automatic and manual voice configuration.

## 🚀 Quick Start

```bash
# Install dependencies
make install

# Process large text file (automatic voice variation)
make auto INPUT=chapter1.txt

# Process small text with manual voice control
make manual TEXT="Your text here" VOICE_STYLE=calm
```

## 📋 Usage

### Auto Mode (Large Texts)
For chapters, articles, or long content with automatic voice variation:

```bash
# Basic usage
make auto INPUT=story.txt

# With voice cloning
make auto INPUT=chapter.txt VOICE_PROMPT=reference_voice.wav

# Use CPU instead of GPU
make auto INPUT=text.txt DEVICE=cpu
```

### Manual Mode (Small Texts)  
For quotes, sentences, or specific voice control:

```bash
# Basic usage
make manual TEXT="Hello world"

# With voice style
make manual TEXT="Calm narration" VOICE_STYLE=calm

# Custom output file
make manual TEXT="Calm narration" VOICE_STYLE=calm OUTPUT=narration.wav

# With voice cloning
make manual TEXT="Custom voice" VOICE_PROMPT=voice.wav OUTPUT=result.wav
```

## 📊 Voice Styles

| Style | Use Case |
|-------|----------|
| **neutral** | General narration |
| **calm** | Reflective moments |

## 🛠️ Commands

```bash
make help        # Show all available commands
make install     # Install dependencies  
make clean       # Clean output directory
```

## 🎖️ Credits

Built with [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) by Resemble AI.
