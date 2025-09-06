.PHONY: help auto manual clean install

# Default help target
help:
	@echo "War Story Narrator - AI Text-to-Speech"
	@echo "====================================="
	@echo ""
	@echo "Usage:"
	@echo "  make auto INPUT=<file>              Process large text file with automatic voice config"
	@echo "  make manual TEXT=\"<text>\"           Process small text with manual voice config"
	@echo ""
	@echo "Options:"
	@echo "  INPUT=<file>                        Input text file (for auto mode)"
	@echo "  TEXT=\"<text>\"                       Text to convert (for manual mode)"
	@echo "  VOICE_STYLE=<style>                 Voice style: neutral, calm (default: neutral)"
	@echo "  VOICE_PROMPT=<file>                 Reference audio file for voice cloning"
	@echo "  OUTPUT=<file>                       Output audio file (default: output.wav)"
	@echo "  DEVICE=<device>                     Processing device: cuda or cpu (default: cuda)"
	@echo ""
	@echo "Examples:"
	@echo "  make auto INPUT=chapter1.txt"
	@echo "  make auto INPUT=story.txt VOICE_PROMPT=voice.wav"
	@echo "  make manual TEXT=\"Hello world\" VOICE_STYLE=calm"
	@echo "  make manual TEXT=\"Calm scene\" VOICE_STYLE=calm OUTPUT=scene.wav"
	@echo ""
	@echo "Other targets:"
	@echo "  make install                        Install dependencies"
	@echo "  make clean                          Clean output directory"

# Auto mode for large texts
auto:
	@if [ -z "$(INPUT)" ]; then \
		echo "❌ Error: INPUT parameter required"; \
		echo "Usage: make auto INPUT=<file>"; \
		exit 1; \
	fi
	python3 main.py auto $(INPUT) $(if $(VOICE_PROMPT),--voice-prompt $(VOICE_PROMPT)) $(if $(DEVICE),--device $(DEVICE),--device cuda)

# Manual mode for small texts
manual:
	@if [ -z "$(TEXT)" ]; then \
		echo "❌ Error: TEXT parameter required"; \
		echo "Usage: make manual TEXT=\"<text>\""; \
		exit 1; \
	fi
	python3 main.py manual "$(TEXT)" \
		$(if $(VOICE_STYLE),--voice-style $(VOICE_STYLE),--voice-style neutral) \
		$(if $(VOICE_PROMPT),--voice-prompt $(VOICE_PROMPT)) \
		$(if $(OUTPUT),--output $(OUTPUT),--output output.wav) \
		$(if $(DEVICE),--device $(DEVICE),--device cuda)

# Install dependencies
install:
	pip install chatterbox-tts torch torchaudio

# Clean output directory
clean:
	rm -rf war_stories_output/*.wav
	@echo "✅ Cleaned output directory"
