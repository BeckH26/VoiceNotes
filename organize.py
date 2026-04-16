import ollama
import re
import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# ANSI Color Codes
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
P = "\033[95m"
W = "\033[97m"
DIM = "\033[2m"
RST = "\033[0m"
BOLD = "\033[1m"

def clean_output(text):
    lines = text.splitlines()
    bullets = []
    for line in lines:
        line = line.strip()
        # Convert numbered lists to bullets
        line = re.sub(r'^\d+[\.\)]\s*', '- ', line)
        # Remove stray bold markers
        line = re.sub(r'\*+', '', line)
        # Keep headers, main bullets, and sub-bullets
        if line.startswith('# ') or line.startswith('## '):
            bullets.append(line)
        elif line.startswith('- '):
            bullets.append(line)
        elif line.startswith('  - '):
            bullets.append(line)
    return '\n'.join(bullets)

def process_transcription():
    try:
        with open("notes.txt", "r") as f:
            transcript = f.read().strip()
    except FileNotFoundError:
        print(f"  {R}No transcription found.{RST}")
        return False

    if not transcript:
        print(f"  {R}Empty transcription.{RST}")
        return False

    print(f"  {Y}► Summarizing transcript...{RST}")

    response = ollama.chat(
        model='mistral:7b',
        options={
            "temperature": 0.1,
            "num_ctx": 8192 
        },
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a note-taking assistant. Summarize transcripts into structured bullet points.\n"
                    "Rules:\n"
                    "- Identify the main topic and create a header with '# Topic'\n"
                    "- Create logical sections based on context shifts using '## Section'\n"
                    "- Use '- ' for main points\n"
                    "- Use '  - ' (2 spaces) for sub-points and supporting details\n"
                    "- Ignore filler words, false starts, repetition, and transcription noise\n"
                    "- Group related ideas together under the same section\n"
                    "- Be concise but preserve all important details\n"
                )
            },
            {
                "role": "user",
                "content": f"Summarize this transcript into structured bullet points:\n\n{transcript}"
            }
        ]
    )

    raw = response['message']['content'].strip()
    summary = clean_output(raw)

    if not summary:
        print(f"  {Y}► First pass failed, retrying...{RST}")
        response2 = ollama.chat(
            model='mistral:7b',
            options={"temperature": 0.1, "num_ctx": 8192},
            messages=[{"role": "user", "content": f"Convert to bullet points:\n\n{raw}"}]
        )
        summary = clean_output(response2['message']['content'].strip())

    # --- SAVE FILE VIA POPUP ---
    print(f"  {Y}▶ Select save location...{RST}")
    
    # Setup hidden root for file dialog
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True) 

    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S%p")
    default_filename = f"notes_{timestamp}.txt"

    # Open the native Save As dialog
    save_path = filedialog.asksaveasfilename(
        initialfile=default_filename,
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save Organized Notes"
    )
    
    root.destroy()

    if not save_path:
        print(f"  {R}Save cancelled.{RST}")
        return False

    with open(save_path, "w") as f:
        f.write(summary)

    # Print formatted output to console
    print(f"\n  {C}┌─ {BOLD}SUMMARY{RST}{C} ──────────────────────────────┐{RST}")
    print(f"  {C}│{RST}")
    for line in summary.splitlines():
        if line.startswith('# '):
            print(f"  {C}│{RST}  {BOLD}{P}{line[2:]}{RST}")
            print(f"  {C}│{RST}")
        elif line.startswith('## '):
            print(f"  {C}│{RST}  {Y}{line[3:]}{RST}")
        elif line.startswith('  - '):
            print(f"  {C}│{RST}      {DIM}-{RST} {W}{line[4:]}{RST}")
        elif line.startswith('- '):
            print(f"  {C}│{RST}    {G}-{RST} {W}{line[2:]}{RST}")
    print(f"  {C}│{RST}")
    print(f"  {C}└──────────────────────────────────────────┘{RST}")
    print(f"\n  {DIM}Saved → {RST}{P}{save_path}{RST}")

    return True