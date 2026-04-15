#!/bin/bash

# Get the directory where this script lives (your project folder)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APP_NAME="VoiceNotes.app"
APP_PATH="$DIR/$APP_NAME"

echo "Creating $APP_NAME in your project folder..."

# Create the .app bundle folder structure
mkdir -p "$APP_PATH/Contents/MacOS"

# Write the Info.plist
cat > "$APP_PATH/Contents/Info.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launch</string>
    <key>CFBundleName</key>
    <string>VoiceNotes</string>
    <key>CFBundleIdentifier</key>
    <string>com.voicenotes.app</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
</dict>
</plist>
PLIST

# Write the launcher script inside the .app
cat > "$APP_PATH/Contents/MacOS/launch" << 'LAUNCH'
#!/bin/bash
FOLDER=$(cat ~/.voicenotes_path)

# Add Homebrew to PATH for Apple Silicon Macs (M1/M2/M3)
if [[ -f "/opt/homebrew/bin/brew" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Pick the right python3: prefer Homebrew's, fall back to whatever is available
if [[ -f "/opt/homebrew/bin/python3" ]]; then
    PY="/opt/homebrew/bin/python3"
else
    PY="python3"
fi

osascript -e "tell application \"Terminal\" to do script \"cd '$FOLDER' && $PY main.py\""
LAUNCH

# Make the launcher executable
chmod +x "$APP_PATH/Contents/MacOS/launch"

echo ""
echo "========================================"
echo "  Done! VoiceNotes.app created."
echo "  You can now double-click it to run."
echo "========================================"
