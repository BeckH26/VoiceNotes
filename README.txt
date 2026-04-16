========================================
  VOICENOTES AI WORKSTATION
========================================

WHAT IT DOES:
  Records audio from your microphone and transcribes it
  using OpenAI Whisper (runs locally), then uses Mistral 7B
  via Ollama to organize it into clean, structured
  bullet-point notes. A Save dialog lets you choose
  where to save your notes when done.

  Everything runs fully offline — no data is sent
  to any server.

  Great for lectures, meetings, voice memos, or any
  conversation you want to capture without typing.

  Note: Since Mistral 7B is a lightweight local model,
  it may occasionally make minor formatting mistakes.

----------------------------------------
FILES:
  main.py        — runs the app
  recorder.py    — handles recording and Whisper transcription
  organize.py    — formats notes with Mistral 7B via Ollama
  VoiceNotes     — standalone app (no Python required)
  README.txt     — this file

----------------------------------------
FIRST TIME SETUP — OLLAMA + MISTRAL 7B:
  The app uses Mistral 7B as its AI brain. You need to
  install Ollama and download the model once before
  running VoiceNotes for the first time.

  1. Install Ollama:
     Go to https://ollama.com and download the Mac app,
     or run this in Terminal:
       brew install ollama

  2. Start the Ollama server:
       ollama serve

     Leave this Terminal window open, or Ollama will stop.
     (After the first time, Ollama can be set to start
     automatically in its menu bar app.)

  3. Download Mistral 7B (~4GB, runs once):
     Open a new Terminal tab and run:
       ollama pull mistral:7b

     Wait for it to finish — this may take several minutes
     depending on your internet speed.

  4. Verify it worked:
       ollama list
     You should see mistral:7b in the list.

  Ollama must be running in the background any time
  you use VoiceNotes.

----------------------------------------
OPTION A — STANDALONE APP (easiest):
  Just double-click VoiceNotes.
  No Python or dependencies required.

  If macOS blocks it:
  System Settings → Privacy & Security → Open Anyway

----------------------------------------
OPTION B — RUN FROM SOURCE:
  Requires Python 3 and the following installed:
    pip install ollama openai-whisper sounddevice numpy scipy tqdm

  Then run:
    python3 main.py

----------------------------------------
USING THE APP:
  1. Press ENTER to start recording
  2. Speak — record as long as you need
  3. Press ENTER again to stop
  4. Whisper transcribes your audio automatically
  5. Mistral 7B organizes it into bullet-point notes
  6. A Save dialog appears — choose where to save

----------------------------------------
OUTPUT:
  Default filename format:
  notes_YYYY-MM-DD_HH-MM-SSam.txt

----------------------------------------
TROUBLESHOOTING:

  macOS blocked the app on launch:
    System Settings → Privacy & Security → Open Anyway

  Ollama not running / Mistral not responding:
    ollama serve
    (in a new tab) ollama pull mistral:7b

  Whisper model missing:
    python3 -c "import whisper; whisper.load_model('base')"

  No audio captured:
    Make sure your microphone is allowed in
    System Settings → Privacy & Security → Microphone

========================================