import recorder
import organize
import os

R   = "\033[91m"
G   = "\033[92m"
Y   = "\033[93m"
C   = "\033[96m"
P   = "\033[95m"
W   = "\033[97m"
DIM = "\033[2m"
RST = "\033[0m"
BOLD = "\033[1m"

def header():
    print(f"\n{C}╔══════════════════════════════════════════╗{RST}")
    print(f"{C}║{RST}    {BOLD}{W}VOICENOTES  AI  WORKSTATION{RST}           {C}║{RST}")
    print(f"{C}╚══════════════════════════════════════════╝{RST}")

def divider():
    print(f"{DIM}  ─────────────────────────────────────────{RST}")

def status(label, color, text):
    print(f"  {P}●{RST} {W}{label:<8}{RST}  {color}{text}{RST}")

def run_pipeline():
    header()
    divider()
    status("Status", G, "READY")
    print(f"\n  {Y}▶{RST}  You {C}ARE{RST} recording")
    print(f"  {Y}▶{RST}  Press {C}ENTER{RST} to stop\n")

    recorder.record_until_enter()

    if os.path.exists("notes.txt"):
        divider()
        status("Status", Y, "THINKING")
        print(f"  {DIM}Mistral 7B is organizing your notes...{RST}\n")

        success = organize.process_transcription()

        if success:
            divider()
            status("Status", G, "COMPLETE")
            print(f"\n  {DIM}Goodbye.{RST}\n")
    else:
        divider()
        status("Status", R, "ERROR")
        print(f"  {DIM}Transcription failed.{RST}\n")

if __name__ == "__main__":
    run_pipeline()