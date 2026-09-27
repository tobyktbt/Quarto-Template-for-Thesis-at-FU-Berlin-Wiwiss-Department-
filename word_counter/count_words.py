"""
Akademischer Wortzähler für Quarto / LaTeX Arbeiten.

Zählt pro Kapitel:
  - RAW      : Alle Tokens (wie wc -w)
  - PROSE    : Bereinigter Fließtext ohne Markup, Befehle und Display-Math

Verwendung:
    python word_counter/count_words.py [ziel_wortanzahl]
    z.B.:
    python word_counter/count_words.py 6000
"""

import re
import sys
from pathlib import Path

# Safe encoding for Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Optionales Ziel aus Argumenten (Standard: 5000)
TARGET = 5000
if len(sys.argv) > 1:
    try:
        TARGET = int(sys.argv[1])
    except ValueError:
        pass

chapter_dir = Path(__file__).resolve().parent.parent / "Chapters"
if not chapter_dir.is_dir():
    print(f"Fehler: Verzeichnis '{chapter_dir}' existiert nicht.")
    sys.exit(1)

ordered_names = [
    "1_introduction.qmd",
    "2_literature_review.qmd",
    "3_methodology.qmd",
    "4_results.qmd",
    "5_discussion.qmd",
    "6_conclusion.qmd",
]

files = [chapter_dir / name for name in ordered_names if (chapter_dir / name).exists()]
for p in sorted(chapter_dir.glob("*.qmd")):
    if p.name not in ordered_names and p.name != "appendix.qmd" and p.name != "abstract.qmd":
        files.append(p)

def strip_to_prose(text: str) -> str:
    s = text
    s = re.sub(r"<!--.*?-->", "", s, flags=re.DOTALL)
    s = re.sub(r"\$\$.*?\$\$", "", s, flags=re.DOTALL)
    s = re.sub(r"\\begin\{[^}]*\}.*?\\end\{[^}]*\}", "", s, flags=re.DOTALL)
    s = re.sub(r"!\[.*?\]\(.*?\)(\{.*?\})?", "", s)
    s = re.sub(r"\\(?:figurenote|tablenote)\{.*?\}", "", s)
    s = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = re.sub(r"\$[^$]+\$", " _NUM_ ", s)
    s = re.sub(r"\(@[a-z]+-[a-zA-Z0-9_-]+\)", "", s)
    s = re.sub(r"^#{1,6}\s+.*$", "", s, flags=re.MULTILINE)
    s = re.sub(r"\*{1,3}(.*?)\*{1,3}", r"\1", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\{\{<.*?>\}\}", "", s)
    s = re.sub(r"^\s*[-*]\s+", " ", s, flags=re.MULTILINE)
    s = re.sub(r"^\s*\d+\.\s+", " ", s, flags=re.MULTILINE)
    s = re.sub(r"[{}\\$]", " ", s)
    s = re.sub(r"§(\d+\.\d+)", r"section", s)
    return re.sub(r"\s+", " ", s).strip()

def count_words(text: str) -> int:
    return len(text.split()) if text.strip() else 0

print()
print("=" * 65)
print(f"  WORTZÄHLUNG — {chapter_dir.name}")
print("=" * 65)
print(f"  {'Kapitel':<30} {'Raw':>8}  {'Fließtext':>10}")
print(f"  {'-'*30} {'-'*8}  {'-'*10}")

total_raw, total_prose = 0, 0
for f in files:
    content = f.read_text(encoding="utf-8")
    raw = count_words(content)
    prose = count_words(strip_to_prose(content))
    total_raw += raw
    total_prose += prose
    label = f.stem.replace("_", " ").title()[:28]
    print(f"  {label:<30} {raw:>8,}  {prose:>10,}")

print(f"  {'-'*30} {'-'*8}  {'-'*10}")
print(f"  {'GESAMT':<30} {total_raw:>8,}  {total_prose:>10,}")
print()

diff = total_prose - TARGET
if diff >= 0:
    print(f"  [OK]   {total_prose:,} Wörter Fließtext (+{diff:,} über dem Ziel von {TARGET:,})")
else:
    print(f"  [!!]   {total_prose:,} Wörter Fließtext ({abs(diff):,} unter dem Ziel von {TARGET:,})")
print()
