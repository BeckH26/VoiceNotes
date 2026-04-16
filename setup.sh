#!/bin/bash
echo "========================================"
echo "   VOICENOTES SETUP"
echo "========================================"

# Get the directory where this script lives
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ─── Homebrew ────────────────────────────────────────────────────────────────
if ! command -v brew &>/dev/null; then
    echo ">>> Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    fi
fi

# ─── Python 3 ────────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo ">>> Installing Python..."
    brew install python
fi

# ─── Ollama ──────────────────────────────────────────────────────────────────
if ! command -v ollama &>/dev/null; then
    echo ">>> Installing Ollama..."
    brew install ollama
fi

# ─── PortAudio (required by sounddevice) ─────────────────────────────────────
if ! brew list portaudio &>/dev/null; then
    echo ">>> Installing portaudio..."
    brew install portaudio
fi

# ─── Fix macOS Python SSL certificates ───────────────────────────────────────
echo ">>> Fixing Python SSL certificates..."

# Method 1: Run Apple's own certificate installer if available
CERT_CMD=$(find /Applications -name "Install Certificates.command" 2>/dev/null | head -1)
if [[ -n "$CERT_CMD" ]]; then
    echo "    Found certificate installer, running it..."
    bash "$CERT_CMD" > /dev/null 2>&1
fi

# Method 2: Install/upgrade certifi
pip install --upgrade certifi > /dev/null 2>&1

# ─── Persist SSL env vars dynamically (survives Python version changes) ───────
SHELL_RC="$HOME/.zshrc"
if [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bash_profile"
fi

# Remove any old hardcoded SSL_CERT_FILE or REQUESTS_CA_BUNDLE lines
sed -i '' '/SSL_CERT_FILE/d' "$SHELL_RC" 2>/dev/null
sed -i '' '/REQUESTS_CA_BUNDLE/d' "$SHELL_RC" 2>/dev/null
sed -i '' '/VoiceNotes SSL fix/d' "$SHELL_RC" 2>/dev/null

# Add dynamic versions that resolve at shell startup, not install time
echo "" >> "$SHELL_RC"
echo "# VoiceNotes SSL fix" >> "$SHELL_RC"
echo 'export SSL_CERT_FILE="$(python3 -c \"import certifi; print(certifi.where())\" 2>/dev/null)"' >> "$SHELL_RC"
echo 'export REQUESTS_CA_BUNDLE="$(python3 -c \"import certifi; print(certifi.where())\" 2>/dev/null)"' >> "$SHELL_RC"
echo "    SSL vars added dynamically to $SHELL_RC"

# Apply to current session too
export SSL_CERT_FILE="$(python3 -c "import certifi; print(certifi.where())" 2>/dev/null)"
export REQUESTS_CA_BUNDLE="$SSL_CERT_FILE"

# ─── Python packages ─────────────────────────────────────────────────────────
echo ">>> Installing Python packages..."
pip install ollama openai-whisper sounddevice numpy scipy tqdm certifi

# ─── Pre-download Whisper model (avoids SSL error on first run) ───────────────
echo ">>> Pre-downloading Whisper base model (this runs once, ~150MB)..."
python3 -c "
import ssl, certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
import whisper
print('    Downloading...')
whisper.load_model('base')
print('    Whisper base model ready.')
"

if [[ $? -ne 0 ]]; then
    echo ""
    echo "!!! WARNING: Whisper model download failed."
    echo "    The app will try again on first run."
    echo "    If it fails again, run: python3 -c \"import whisper; whisper.load_model('base')\""
    echo ""
fi

# ─── Start Ollama server in background ───────────────────────────────────────
echo ">>> Starting Ollama server in background..."
if ! pgrep -x "ollama" > /dev/null; then
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    echo "    Ollama started (PID $OLLAMA_PID)"
    sleep 3
else
    echo "    Ollama already running."
fi

# ─── Pull Mistral 7B model ────────────────────────────────────────────────────
echo ">>> Pulling Mistral 7B model (~4GB, this will take a while)..."
ollama pull mistral:7b

# ─── Save project path for launcher ──────────────────────────────────────────
echo "$DIR" > ~/.voicenotes_path
echo ">>> Project path saved: $DIR"

echo ""
echo "========================================"
echo "   SETUP COMPLETE"
echo "   Run create_app.sh once, then"
echo "   double-click VoiceNotes.app to launch."
echo "========================================"
