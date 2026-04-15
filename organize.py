import ollama
import re
import os
from datetime import datetime

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
            "num_ctx": 8192  # Increased from default 2048 to handle long transcripts
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
                    "- If the transcript shifts topic, start a new section"
                )
            },
            {
                "role": "user",
                "content": f"Summarize this transcript into structured bullet points with sub-bullets where appropriate:\n\n{transcript}"
            }
        ]
    )

    raw = response['message']['content'].strip()
    summary = clean_output(raw)

    if not summary:
        print(f"  {Y}► First pass failed, retrying...{RST}")
        response2 = ollama.chat(
            model='mistral:7b',
            options={
                "temperature": 0.1,
                "num_ctx": 8192
            },
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Convert this into structured bullet points.\n"
                        "Use '# ' for main topics, '- ' for points, '  - ' for sub-points.\n"
                        "One idea per line:\n\n" + raw
                    )
                }
            ]
        )
        summary = clean_output(response2['message']['content'].strip())

    # Save to file
    summaries_dir = "summaries"
    os.makedirs(summaries_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S%p")
    filename = os.path.join(summaries_dir, f"notes_{timestamp}.txt")

    with open(filename, "w") as f:
        f.write(summary)

    # Print formatted output
    print(f"\n  {C}┌─ {BOLD}SUMMARY{RST}{C} ──────────────────────────────┐{RST}")
    print(f"  {C}│{RST}")
    for line in summary.splitlines():
        if line.startswith('# '):
            # Main topic header
            print(f"  {C}│{RST}  {BOLD}{P}{line[2:]}{RST}")
            print(f"  {C}│{RST}")
        elif line.startswith('## '):
            # Section header
            print(f"  {C}│{RST}  {Y}{line[3:]}{RST}")
        elif line.startswith('  - '):
            # Sub-bullet
            content = line[4:]
            print(f"  {C}│{RST}      {DIM}-{RST} {W}{content}{RST}")
        elif line.startswith('- '):
            # Main bullet
            content = line[2:]
            print(f"  {C}│{RST}    {G}-{RST} {W}{content}{RST}")
    print(f"  {C}│{RST}")
    print(f"  {C}└──────────────────────────────────────────┘{RST}")
    print(f"\n  {DIM}Saved → {RST}{P}{filename}{RST}")

    return True
