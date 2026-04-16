import ollama
import re
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

R = "\033[91m"; G = "\033[92m"; Y = "\033[93m"; C = "\033[96m"
P = "\033[95m"; W = "\033[97m"; DIM = "\033[2m"; RST = "\033[0m"; BOLD = "\033[1m"

def clean_output(text):
    lines = text.splitlines()
    bullets = []
    for line in lines:
        line = line.strip()
        line = re.sub(r'^\d+[\.\)]\s*', '- ', line)
        line = re.sub(r'\*+', '', line)
        if any(line.startswith(s) for s in ['# ', '## ', '- ', '  - ']):
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

    # FIX 1: RUN AI FIRST (Before Popup)
    print(f"  {Y}▶ Summarizing transcript...{RST}")

    response = ollama.chat(
        model='mistral:7b',
        options={
            "temperature": 0.0,  # FIX 2: NO HALLUCINATIONS
            "num_ctx": 8192
        },
        messages=[
            {
                "role": "system", 
                "content": "You are a strict assistant. ONLY use facts from the transcript. DO NOT invent details. Use # for headers and - for bullets."
            },
            {"role": "user", "content": f"Summarize this exactly:\n\n{transcript}"}
        ]
    )

    summary = clean_output(response['message']['content'].strip())

    # FIX 3: POPUP AT THE END
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S%p")
    default_name = f"notes_{timestamp}.txt"

    print(f"  {Y}▶ Select save location...{RST}")
    target_path = filedialog.asksaveasfilename(
        title="Save Your AI Notes",
        initialfile=default_name,
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    root.destroy()

    if not target_path:
        print(f"  {R}Save cancelled.{RST}")
        return False

    # FIX 4: WRITE TO SELECTED PATH
    with open(target_path, "w") as f:
        f.write(summary)

    # UI Preview
    print(f"\n  {C}┌─ {BOLD}SUMMARY{RST}{C} ──────────────────────────────┐{RST}")
    for line in summary.splitlines():
        if line.startswith('# '): print(f"  {C}│{RST}  {BOLD}{P}{line[2:]}{RST}")
        elif line.startswith('## '): print(f"  {C}│{RST}  {Y}{line[3:]}{RST}")
        elif line.startswith('  - '): print(f"  {C}│{RST}      {DIM}-{RST} {W}{line[4:]}{RST}")
        elif line.startswith('- '): print(f"  {C}│{RST}    {G}-{RST} {W}{line[2:]}{RST}")
    print(f"  {C}└──────────────────────────────────────────┘{RST}")
    
    print(f"\n  {G}SUCCESS:{RST} Saved to {target_path}")
    return True
