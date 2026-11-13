"""Strict advisory checker for LeafGuard knowledge base.

Checks that every class label in labels.json has a valid, non-placeholder entry,
verifies sources, and flags any potential chemical pesticide dosage patterns.
Usage: python scripts/check_advisory.py
"""
import json
import re
import sys
from pathlib import Path

LABELS_PATH = Path("app/data/labels.json")
ADVISORY_PATH = Path("app/data/advisory.json")

# Regex pattern to catch pesticide / chemical dosages (e.g., '2 ml', '5g/l', '10%', '500ppm')
DOSE_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\s*(?:ml|g/|kg/|l/|%|ppm|gm)\b", re.IGNORECASE)


def check_text(text: str, label: str, field: str, lang: str) -> int:
    """Inspect text value for placeholder marks and chemical dosage patterns."""
    problems = 0
    if not isinstance(text, str):
        return 0

    stripped = text.strip()
    if stripped.startswith("<NEEDS"):
        print(f"PLACEHOLDER in {label} -> {field} [{lang}]: {stripped}")
        problems += 1

    # Check for chemical doses
    doses = DOSE_PATTERN.findall(stripped)
    if doses:
        print(f"POSSIBLE DOSE in {label} -> {field} [{lang}]: found {doses} in '{stripped}'")
        problems += 1

    return problems


def main():
    if not LABELS_PATH.exists() or not ADVISORY_PATH.exists():
        sys.exit("Error: labels.json or advisory.json missing.")

    labels = json.load(open(LABELS_PATH, encoding="utf-8"))
    kb = json.load(open(ADVISORY_PATH, encoding="utf-8"))
    problems = 0

    # Check disclaimer
    disclaimer = kb.get("_disclaimer", {})
    for lang in ("en", "hi", "mr"):
        disc_text = disclaimer.get(lang, "")
        if not disc_text or disc_text.startswith("<NEEDS"):
            print(f"DISCLAIMER INCOMPLETE [{lang}]: {disc_text}")
            problems += 1

    # Check each class entry
    for label in labels:
        entry = kb.get(label)
        if not entry:
            print(f"MISSING ENTRY: {label}")
            problems += 1
            continue

        for field in ("name", "symptoms", "actions", "prevention"):
            field_data = entry.get(field, {})
            for lang in ("en", "hi", "mr"):
                val = field_data.get(lang)
                if not val:
                    print(f"EMPTY FIELD in {label} -> {field} [{lang}]")
                    problems += 1
                elif isinstance(val, list):
                    for item in val:
                        problems += check_text(item, label, field, lang)
                elif isinstance(val, str):
                    problems += check_text(val, label, field, lang)

        # Source verification
        src = entry.get("source", {})
        for src_key in ("name", "url", "retrieved"):
            src_val = src.get(src_key, "")
            if not src_val or str(src_val).startswith("<NEEDS"):
                print(f"NO SOURCE in {label} -> {src_key}: {src_val}")
                problems += 1

    print(f"\nChecked {len(labels)} labels. Total problems found: {problems}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
