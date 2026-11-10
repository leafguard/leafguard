"""Every label must have a complete EN/HI/MR advisory entry with a source. Run before each deploy."""
import json, sys
labels = json.load(open("app/data/labels.json", encoding="utf-8"))
kb = json.load(open("app/data/advisory.json", encoding="utf-8"))
problems = 0
for label in labels:
    e = kb.get(label)
    if not e:
        print("MISSING", label); problems += 1; continue
    for key in ("name", "symptoms", "actions", "prevention"):
        for lang in ("en", "hi", "mr"):
            if not e.get(key, {}).get(lang):
                print("EMPTY", label, key, lang); problems += 1
    src = e.get("source", {})
    if not (src.get("name") and src.get("url") and src.get("retrieved")):
        print("NO SOURCE", label); problems += 1
print(f"checked {len(labels)} labels, {problems} problem(s)")
sys.exit(1 if problems else 0)
