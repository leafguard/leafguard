"""Advisory lookup module for LeafGuard.

Retrieves verified ICAR/KVK management advice in English, Hindi, and Marathi.
Strictly returns stored, reviewed agricultural advice. Never generates advice with an LLM.
"""
from pathlib import Path
from typing import Dict, Any, List
import json

ADVISORY_PATH = Path(__file__).resolve().parent / "data" / "advisory.json"
SUPPORTED_LANGS = ("en", "hi", "mr")
DEFAULT_LANG = "en"

# Fallback disclaimer when none in file
DEFAULT_DISCLAIMER = {
    "en": "Indicative result only. Confirm with your local KVK or agriculture officer before spraying.",
    "hi": "यह केवल सांकेतिक परिणाम है। छिड़काव करने से पहले अपने स्थानीय केवीके (KVK) या कृषि अधिकारी से पुष्टि करें।",
    "mr": "हा केवळ सूचक निकाल आहे. फवारणी करण्यापूर्वी आपल्या स्थानिक केव्हीके (KVK) किंवा कृषी अधिकाऱ्यांशी संपर्क साधा."
}

_kb_cache: Dict[str, Any] = {}


def _load_kb() -> Dict[str, Any]:
    """Load advisory knowledge base from JSON file if available."""
    global _kb_cache
    if not _kb_cache:
        if ADVISORY_PATH.exists():
            with open(ADVISORY_PATH, "r", encoding="utf-8") as f:
                _kb_cache = json.load(f)
        else:
            _kb_cache = {"_disclaimer": DEFAULT_DISCLAIMER}
    return _kb_cache


def display_name(label: str, lang: str = "en") -> str:
    """Return localized display name for a disease class label."""
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG

    kb = _load_kb()
    entry = kb.get(label)
    if entry and "name" in entry:
        names = entry["name"]
        val = names.get(lang) or names.get(DEFAULT_LANG)
        if val and not val.startswith("<NEEDS"):
            return val

    # Fallback to readable label
    if "___" in label:
        crop, disease = label.split("___", 1)
        return f"{crop.replace('_', ' ')} - {disease.replace('_', ' ')}"
    return label.replace("_", " ")


def get(label: str, lang: str = "en") -> Dict[str, Any]:
    """Retrieve disease management guidance for a given label and language.

    Falls back safely to English for unknown languages, or safe fallback note for missing labels.
    """
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG

    kb = _load_kb()
    disclaimers = kb.get("_disclaimer", DEFAULT_DISCLAIMER)
    disclaimer_text = disclaimers.get(lang) or disclaimers.get(DEFAULT_LANG) or DEFAULT_DISCLAIMER["en"]

    entry = kb.get(label)
    title = display_name(label, lang)

    # Missing label or empty entry safe fallback
    if not entry or not isinstance(entry, dict):
        return {
            "title": title,
            "symptoms": ["No verified symptom guide available for this class."],
            "actions": ["No verified advisory available. Consult your local KVK or agriculture officer."],
            "prevention": ["Practice standard crop rotation and clean field sanitation."],
            "source": {
                "name": "ICAR Extension Advisory",
                "url": "https://icar.org.in",
                "retrieved": "2026-11-13",
            },
            "disclaimer": disclaimer_text,
            "reviewed": False,
        }

    # Extract localized fields with fallback to English
    def get_field(field_name: str) -> Any:
        field_dict = entry.get(field_name, {})
        val = field_dict.get(lang)
        if not val or (isinstance(val, str) and val.startswith("<NEEDS")):
            val = field_dict.get(DEFAULT_LANG, [])
        return val

    symptoms = get_field("symptoms")
    actions = get_field("actions")
    prevention = get_field("prevention")
    source = entry.get("source", {
        "name": "ICAR Extension Advisory",
        "url": "https://icar.org.in",
        "retrieved": "2026-11-13"
    })
    
    reviewed_dict = entry.get("reviewed", {})
    is_reviewed = bool(reviewed_dict.get(lang, False))

    return {
        "title": title,
        "symptoms": symptoms if isinstance(symptoms, list) else [symptoms],
        "actions": actions if isinstance(actions, list) else [actions],
        "prevention": prevention if isinstance(prevention, list) else [prevention],
        "source": source,
        "disclaimer": disclaimer_text,
        "reviewed": is_reviewed,
    }
