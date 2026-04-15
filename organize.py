import ollama
import re
import os
from datetime import datetime

R   = "\033[91m"
G   = "\033[92m"
Y   = "\033[93m"
C   = "\033[96m"
P   = "\033[95m"
W   = "\033[97m"
DIM = "\033[2m"
RST = "\033[0m"
BOLD = "\033[1m"

def clean_output(text):
    lines = text.splitlines()
    bullets = []
    for line in lines:
        line = line.strip()
        line = re.sub(r'^\d+[\.\)]\s*', '- ', line)
        line = re.sub(r'\*+', '', line)
        if line.startswith('- '):
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

    response = ollama.chat(
        model='mistral:7b',
        options={"temperature": 0.1},
        messages=[
            {
                "role": "system",
                "content": (
                    "OUTPUT ONLY DASH BULLETS. NOTHING ELSE.\n"
                    "Format: - idea here\n"
                    "FORBIDDEN: paragraphs, numbering, bold, headers, intro sentences, nested bullets.\n"
                    "If you add anything other than dash bullets, you have failed.\n"
                    "Start your response with '- ' immediately."
                )
            },
            {
                "role": "user",
                "content": f"Convert this transcription into simple dash-bullet notes with one idea per bullet:\n\n{transcript}"
            }
        ]
    )

    raw = response['message']['content'].strip()
    summary = clean_output(raw)

    if not summary:
        print(f"  {Y}► First pass failed, retrying...{RST}")
        response2 = ollama.chat(
            model='mistral:7b',
            options={"temperature": 0.1},
            messages=[
                {"role": "user", "content": f"Convert this into dash bullet points only, one per line, starting each with '- ':\n\n{raw}"}
            ]
        )
        summary = clean_output(response2['message']['content'].strip())

    summaries_dir = "summaries"
    os.makedirs(summaries_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S%p")
    filename = os.path.join(summaries_dir, f"notes_{timestamp}.txt")

    with open(filename, "w") as f:
        f.write(summary)

    print(f"\n  {C}┌─ {BOLD}SUMMARY{RST}{C} ──────────────────────────────┐{RST}")
    print(f"  {C}│{RST}")
    for line in summary.splitlines():
        content = line[2:] if line.startswith('- ') else line
        print(f"  {C}│{RST}  {G}-{RST} {W}{content}{RST}")
    print(f"  {C}│{RST}")
    print(f"  {C}└──────────────────────────────────────────┘{RST}")
    print(f"\n  {DIM}Saved → {RST}{P}{filename}{RST}")

    return True