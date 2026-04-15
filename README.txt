========================================
  VOICENOTES AI WORKSTATION
========================================

WHAT IT DOES:
  Records audio from your microphone and transcribes it
  using OpenAI Whisper, then uses a local AI model (Mistral 7B)
  to clean it up into organized bullet-point notes.

  Great for lectures, meetings, or any conversation you
  want to capture without typing.

  Note: The AI runs fully offline after setup. Since it's
  a lightweight local model, it may occasionally make
  formatting mistakes.

----------------------------------------
FIRST TIME SETUP:
  1. Open Terminal
  2. Drag setup.sh into Terminal and press Enter
  3. Wait for everything to install (~4GB download)
  4. Drag create_app.sh into Terminal and press Enter
  5. A VoiceNotes.app will appear in the folder

----------------------------------------
TO RUN:
  Double-click VoiceNotes.app

  A Terminal window will open. Press ENTER
  to stop recording, and your notes will appear
  automatically.

----------------------------------------
REQUIREMENTS:
  - macOS
  - Python 3
  - ~5GB free disk space
  - Internet connection (first time setup only)

----------------------------------------
OUTPUT:
  Notes are saved to the summaries/ folder inside
  your VoiceNotes directory, named by date and time.

----------------------------------------
FILES:
  main.py        — runs the app
  recorder.py    — handles recording and transcription
  organize.py    — formats notes with AI
  setup.sh       — installs everything (run once)
  create_app.sh  — creates the launcher app (run once)
  README.txt     — this file

========================================