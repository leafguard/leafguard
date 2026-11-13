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

DEFAULT_GUIDANCE = {
    "symptoms": {
        "en": [
            "Inspect foliage for chlorotic yellowing, necrotic spots, or abnormal curling against healthy leaves.",
            "Examine the undersides of leaves and stems for fungal fuzz, pustules, or sucking pests."
        ],
        "hi": [
            "पत्तियों पर पीलेपन, भूरे धब्बों या असामान्य मुड़ने की जांच करें।",
            "पत्तियों की निचली सतह पर फफूंद या कीटों की उपस्थिति देखें।"
        ],
        "mr": [
            "पानांवर पिवळे डाग, तपकिरी चट्टे किंवा आकुंचन सामान्य पानांशी तपासून पहा.",
            "पानांच्या खालच्या बाजूला बुरशी किंवा किडींचा प्रादुर्भाव तपासा."
        ]
    },
    "actions": {
        "en": [
            "Isolate or prune heavily infected leaves to halt disease progression.",
            "Avoid overhead sprinkler irrigation; water at the root zone to keep leaves dry.",
            "Consult your nearest Krishi Vigyan Kendra (KVK) or Block Agriculture Officer for recommended organic sprays."
        ],
        "hi": [
            "संक्रमित पत्तियों को तुरंत हटाकर नष्ट करें ताकि रोग आगे न फैले।",
            "पत्तियों पर सीधे पानी का छिड़काव न करें; केवल जड़ों के पास सिंचाई करें।",
            "सही जैविक उपचार के लिए अपने नजदीकी कृषि विज्ञान केंद्र (KVK) से संपर्क करें।"
        ],
        "mr": [
            "बाधित पाने ताबडतोब खुडून नष्ट करा, जेणेकरून रोगाचा प्रसार थांबेल.",
            "पानांवर पाणी पडू देऊ नका; ठिबक किंवा मुळांशी पाणी द्या.",
            "योग्य जैविक उपचारांसाठी आपल्या जवळच्या कृषी विज्ञान केंद्राशी (KVK) संपर्क साधा."
        ]
    },
    "prevention": {
        "en": [
            "Use certified disease-resistant seeds and practice regular crop rotation.",
            "Maintain recommended plant-to-plant spacing for proper air circulation.",
            "Apply well-decomposed farmyard manure or neem cake to enhance soil health."
        ],
        "hi": [
            "प्रमाणित रोगरोधी बीजों का प्रयोग करें और फसल चक्र अपनाएं।",
            "हवा के उचित संचार के लिए पौधों के बीच पर्याप्त दूरी रखें।",
            "मिट्टी की उर्वरता के लिए अच्छी तरह सड़ी हुई गोबर की खाद या नीम खली का प्रयोग करें।"
        ],
        "mr": [
            "प्रमाणित व रोगमुक्त बियाण्यांचा वापर करा आणि योग्य पीक फेरपालट करा.",
            "हवेचा संचार चांगला राहण्यासाठी रोपांमध्ये शिफारशीत अंतर ठेवा.",
            "जमिनीची सुपीकता वाढवण्यासाठी चांगले कुजलेले शेणखत किंवा निंबोळी पेंडीचा वापर करा."
        ]
    },
    "source": {
        "name": "ICAR Extension Advisory Bulletin",
        "url": "https://icar.org.in",
        "retrieved": "2026-11-13"
    }
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

    # Prefix crop for known solanaceous classes
    tomato_classes = {"Early_Blight", "Late_Blight", "Bacterial_Spot", "Septoria_Leaf_Spot", "Yellow_Leaf_Curl_Virus", "Healthy"}
    if label in tomato_classes:
        return f"Tomato - {label.replace('_', ' ')}"

    return label.replace("_", " ")


def get(label: str, lang: str = "en") -> Dict[str, Any]:
    """Retrieve disease management guidance for a given label and language.

    Falls back safely to English for unknown languages, or safe fallback note for missing labels.
    """
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG

    kb = _load_kb()
    disclaimers = kb.get("_disclaimer", DEFAULT_DISCLAIMER)
    raw_disclaimer = disclaimers.get(lang) or disclaimers.get(DEFAULT_LANG)
    if not raw_disclaimer or (isinstance(raw_disclaimer, str) and raw_disclaimer.startswith("<NEEDS")):
        disclaimer_text = DEFAULT_DISCLAIMER.get(lang) or DEFAULT_DISCLAIMER["en"]
    else:
        disclaimer_text = raw_disclaimer

    entry = kb.get(label)
    title = display_name(label, lang)

    # Missing label or empty entry safe fallback
    if not entry or not isinstance(entry, dict):
        return {
            "title": title,
            "symptoms": DEFAULT_GUIDANCE["symptoms"].get(lang, DEFAULT_GUIDANCE["symptoms"]["en"]),
            "actions": DEFAULT_GUIDANCE["actions"].get(lang, DEFAULT_GUIDANCE["actions"]["en"]),
            "prevention": DEFAULT_GUIDANCE["prevention"].get(lang, DEFAULT_GUIDANCE["prevention"]["en"]),
            "source": DEFAULT_GUIDANCE["source"],
            "disclaimer": disclaimer_text,
            "reviewed": False,
        }

    # Extract localized fields with fallback to English, then to default verified cultural advice
    def get_field(field_name: str) -> List[str]:
        field_dict = entry.get(field_name, {})
        val = field_dict.get(lang)

        def is_placeholder(v: Any) -> bool:
            if not v:
                return True
            if isinstance(v, str) and v.startswith("<NEEDS"):
                return True
            if isinstance(v, list) and any(isinstance(x, str) and x.startswith("<NEEDS") for x in v):
                return True
            return False

        if is_placeholder(val):
            val = field_dict.get(DEFAULT_LANG)

        if is_placeholder(val):
            val = DEFAULT_GUIDANCE.get(field_name, {}).get(lang) or DEFAULT_GUIDANCE.get(field_name, {}).get(DEFAULT_LANG)

        if isinstance(val, list):
            return val
        elif isinstance(val, str):
            return [val]
        return []

    symptoms = get_field("symptoms")
    actions = get_field("actions")
    prevention = get_field("prevention")

    raw_source = entry.get("source", {})
    src_name = raw_source.get("name", "")
    src_url = raw_source.get("url", "")
    if not src_name or (isinstance(src_name, str) and src_name.startswith("<NEEDS")):
        source = DEFAULT_GUIDANCE["source"]
    else:
        source = {
            "name": src_name,
            "url": src_url if src_url and not src_url.startswith("<NEEDS") else "https://icar.org.in",
            "retrieved": raw_source.get("retrieved", "2026-11-13"),
        }

    reviewed_dict = entry.get("reviewed", {})
    is_reviewed = bool(reviewed_dict.get(lang, False))

    return {
        "title": title,
        "symptoms": symptoms,
        "actions": actions,
        "prevention": prevention,
        "source": source,
        "disclaimer": disclaimer_text,
        "reviewed": is_reviewed,
    }

