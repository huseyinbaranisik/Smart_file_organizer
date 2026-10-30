"""Runs the real organizer on a sample Downloads folder and records the terminal as frames.

Builds <workdir>/Downloads with sample files (plus an existing Belgeler/rapor.pdf to show a name clash and a
subfolder to show that folders are skipped), runs Kaynak_Kodlar/main.py unchanged with typed answers
(path, "y", Enter), and saves pyte screen snapshots plus the folder tree before and after.

usage: python tools/record_terminal.py <workdir> <out.pkl>      (needs pyte)
"""
import builtins, os, pickle, runpy, shutil, sys

import pyte

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK, OUT = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
COLS, ROWS = 92, 34
SAMPLE = ["rapor.pdf", "fatura_mart.pdf", "tatil_01.jpg", "ekran_goruntusu.png", "sunum_final.pptx",
          "notlar.txt", "ders_kaydi.mp4", "sarki.mp3", "proje_yedek.zip", "vscode_setup.exe", "veri.json"]

def tree(path):
    out = []
    for p in sorted(os.listdir(path), key=lambda n: (not os.path.isdir(os.path.join(path, n)), n.lower())):
        full = os.path.join(path, p)
        out.append((p, os.path.isdir(full), sorted(os.listdir(full)) if os.path.isdir(full) else None))
    return out

downloads = os.path.join(WORK, "Downloads")
shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(os.path.join(downloads, "Belgeler"))
os.makedirs(os.path.join(downloads, "Eski Projeler"))
for name in SAMPLE + ["Belgeler/rapor.pdf"]:
    with open(os.path.join(downloads, name), "wb") as f:
        f.write(b"sample")
before = tree(downloads)

screen = pyte.Screen(COLS, ROWS)
stream = pyte.Stream(screen)
frames, clock = [], 0.0

def snap(hold=0.0):
    rows = [[(c.data, c.fg, c.bg, c.bold) for c in (screen.buffer[y][x] for x in range(COLS))] for y in range(ROWS)]
    frames.append({"t": clock, "hold": hold, "rows": rows})

class Term:
    encoding = "utf-8"
    def write(self, s):
        global clock
        for part in s.split("\n")[:-1]:  # one frame per printed line, so the list scrolls in
            stream.feed(part + "\r\n"); clock += 0.06; snap()
        stream.feed(s.split("\n")[-1])
        return len(s)
    def flush(self): pass

answers = [downloads, "y", ""]
def fake_input(prompt=""):
    global clock
    sys.stdout.write(prompt)
    if not answers:
        raise SystemExit
    snap(hold=0.8)
    answer = answers.pop(0)
    for ch in answer:
        sys.stdout.write(ch); clock += 0.03 if len(answer) > 20 else 0.12; snap()
    sys.stdout.write("\n")
    return answer

sys.stdout = Term()
builtins.input = fake_input
try:
    runpy.run_path(os.path.join(ROOT, "Kaynak_Kodlar", "main.py"), run_name="__main__")
except SystemExit:
    pass
snap(hold=2.0)
sys.stdout = sys.__stdout__
after = tree(downloads)
with open(OUT, "wb") as f:
    pickle.dump({"cols": COLS, "rows": ROWS, "frames": frames, "before": before, "after": after, "path": downloads}, f)
print(len(frames), "frames;", "after:", [(n, kids) for n, d, kids in after if d])
