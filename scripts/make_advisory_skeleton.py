"""Generate or update app/data/advisory.json skeleton from labels.json.

Preserves any existing text and adds '<NEEDS ...>' placeholders for missing fields.
Usage: python scripts/make_advisory_skeleton.py
"""
import json
from pathlib import Path

LABELS_PATH = Path("app/data/labels.json")
ADVISORY_PATH = Path("app/data/advisory.json")

DEFAULT_DISCLAIMER = {
    "en": "Indicative result only. Confirm with your local KVK before spraying.",
    "hi": "<NEEDS TRANSLATION>",
    "mr": "<NEEDS TRANSLATION>",
}


def make_skeleton_entry(label: str) -> dict:
    """Create empty skeleton structure with '<NEEDS ...>' placeholders."""
    # Generate a sensible default title in English
    readable_name = label.replace("___", " - ").replace("_", " ")
    return {
        "name": {
            "en": readable_name,
            "hi": "<NEEDS TRANSLATION>",
            "mr": "<NEEDS TRANSLATION>",
        },
        "symptoms": {
            "en": ["<NEEDS SYMPTOMS>"],
            "hi": ["<NEEDS TRANSLATION>"],
            "mr": ["<NEEDS TRANSLATION>"],
        },
        "actions": {
            "en": ["<NEEDS ACTIONS>"],
            "hi": ["<NEEDS TRANSLATION>"],
            "mr": ["<NEEDS TRANSLATION>"],
        },
        "prevention": {
            "en": ["<NEEDS PREVENTION>"],
            "hi": ["<NEEDS TRANSLATION>"],
            "mr": ["<NEEDS TRANSLATION>"],
        },
        "source": {
            "name": "<NEEDS SOURCE NAME>",
            "url": "<NEEDS SOURCE URL>",
            "retrieved": "2026-11-13",
        },
        "reviewed": {
            "en": False,
            "hi": False,
            "mr": False,
        },
    }


def main():
    if not LABELS_PATH.exists():
        print(f"Error: {LABELS_PATH} not found.")
        return

    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        labels = json.load(f)

    if ADVISORY_PATH.exists():
        with open(ADVISORY_PATH, "r", encoding="utf-8") as f:
            advisory = json.load(f)
    else:
        advisory = {}

    # Initialize disclaimer if missing
    if "_disclaimer" not in advisory:
        advisory["_disclaimer"] = DEFAULT_DISCLAIMER

    added_count = 0
    for label in labels:
        if label not in advisory:
            advisory[label] = make_skeleton_entry(label)
            added_count += 1

    ADVISORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ADVISORY_PATH, "w", encoding="utf-8") as f:
        json.dump(advisory, f, indent=2, ensure_ascii=False)

    print(f"Advisory skeleton updated. Added {added_count} new class entries. Total entries: {len(labels)}")


if __name__ == "__main__":
    main()
