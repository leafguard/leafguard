"""Search the working tree and git history for banned words. Banned words live in .banned_terms.txt
(one per line, git-ignored, NEVER committed). Usage: python scripts/anonymity_audit.py"""
import pathlib, subprocess, sys
terms_file = pathlib.Path(".banned_terms.txt")
if not terms_file.exists():
    sys.exit("Create .banned_terms.txt (one banned word per line: college name, short forms, city, staff names).")
terms = [t.strip().lower() for t in terms_file.read_text(encoding="utf-8").splitlines() if t.strip()]
skip_dirs = {".git", ".venv", "node_modules", "__pycache__"}
hits = 0
for p in pathlib.Path(".").rglob("*"):
    if not p.is_file() or skip_dirs & set(p.parts) or p.name == ".banned_terms.txt" or p.stat().st_size > 5_000_000:
        continue
    try:
        text = p.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        continue
    for t in terms:
        if t in text or t in str(p).lower():
            print(f"HIT in file {p}: '{t}'"); hits += 1
log = subprocess.run(["git", "log", "--all", "--format=%an|%ae|%cn|%ce|%s%n%b"], capture_output=True, text=True).stdout.lower()
for t in terms:
    if t in log:
        print(f"HIT in git history (author, email or message): '{t}'"); hits += 1
print("anonymity audit:", "FAIL, fix every hit above" if hits else "no hits (still check images and PDFs by eye)")
sys.exit(1 if hits else 0)
