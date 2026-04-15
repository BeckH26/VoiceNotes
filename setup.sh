#!/bin/bash
echo "========================================"
echo "   VOICENOTES SETUP"
echo "========================================"

# Get the directory where this script lives
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for Homebrew
if ! command -v brew &>/dev/null; then
    echo ">>> Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo ">>> Installing Python..."
    brew install python
fi

# Check for Ollama
if ! command -v ollama &>/dev/null; then
    echo ">>> Installing Ollama..."
    brew install ollama
fi

# Check for portaudio (required by sounddevice)
if ! brew list portaudio &>/dev/null; then
    echo ">>> Installing portaudio..."
    brew install portaudio
fi

# Install Python dependencies
echo ">>> Installing Python packages..."
pip install ollama openai-whisper sounddevice numpy scipy tqdm

# Pull Mistral model
echo ">>> Pulling Mistral 7B model (this may take a while ~4GB)..."
ollama pull mistral:7b

# Save the project folder path so the launcher app knows where to look
echo "$DIR" > ~/.voicenotes_path
echo ">>> Project path saved: $DIR"

echo ""
echo "========================================"
echo "   SETUP COMPLETE"
echo "   You can now double-click VoiceNotes.app to run."
echo "========================================"