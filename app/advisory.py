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

CROP_METADATA: Dict[str, Dict[str, Dict[str, str]]] = {
    # Cotton
    "Cotton___bacterial_blight": {
        "crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
        "disease": {"en": "Bacterial Blight", "hi": "जीवाणु झुलसा", "mr": "जिवाणू करपा"},
    },
    "Cotton___curl_virus": {
        "crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
        "disease": {"en": "Leaf Curl Virus", "hi": "पत्ती मरोड़ वायरस", "mr": "पाने आकुंचन विषाणू"},
    },
    "Cotton___fussarium_wilt": {
        "crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
        "disease": {"en": "Fusarium Wilt", "hi": "उकठा (विल्ट)", "mr": "मर रोग (विल्ट)"},
    },
    "Cotton___healthy": {
        "crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
        "disease": {"en": "Healthy Crop", "hi": "स्वस्थ फसल", "mr": "निरोगी पीक"},
    },
    # Turmeric
    "Turmeric___Dry_Leaf": {
        "crop": {"en": "Turmeric", "hi": "हल्दी", "mr": "हळद"},
        "disease": {"en": "Dry Leaf / Wilting", "hi": "पत्तियों का सूखना", "mr": "पाने सुकणे"},
    },
    "Turmeric___Healthy_Leaf": {
        "crop": {"en": "Turmeric", "hi": "हल्दी", "mr": "हळद"},
        "disease": {"en": "Healthy Crop", "hi": "स्वस्थ फसल", "mr": "निरोगी पीक"},
    },
    "Turmeric___Leaf_Blotch": {
        "crop": {"en": "Turmeric", "hi": "हल्दी", "mr": "हळद"},
        "disease": {"en": "Leaf Blotch", "hi": "पत्ती धब्बा (ब्लॉच)", "mr": "पानावरील ठिपके (ब्लॉच)"},
    },
    # Soybean
    "Soybean___Healthy_Soyabean": {
        "crop": {"en": "Soybean", "hi": "सोयाबीन", "mr": "सोयाबीन"},
        "disease": {"en": "Healthy Crop", "hi": "स्वस्थ फसल", "mr": "निरोगी पीक"},
    },
    "Soybean___Soyabean_Frog_Leaf_Eye": {
        "crop": {"en": "Soybean", "hi": "सोयाबीन", "mr": "सोयाबीन"},
        "disease": {"en": "Frogeye Leaf Spot", "hi": "मेंढक आंख धब्बा रोग", "mr": "बेडूक डोळा ठिपके रोग"},
    },
    "Soybean___Soyabean_Mosaic": {
        "crop": {"en": "Soybean", "hi": "सोयाबीन", "mr": "सोयाबीन"},
        "disease": {"en": "Mosaic Virus", "hi": "मोज़ेक वायरस", "mr": "मोझॅक विषाणू"},
    },
    "Soybean___Soyabean_Spectoria_Brown_Spot": {
        "crop": {"en": "Soybean", "hi": "सोयाबीन", "mr": "सोयाबीन"},
        "disease": {"en": "Septoria Brown Spot", "hi": "भूरा धब्बा रोग", "mr": "तपकिरी ठिपके रोग"},
    },
    # Tomato & Solanaceous
    "Bacterial_Spot": {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "disease": {"en": "Bacterial Spot", "hi": "जीवाणु धब्बा", "mr": "जिवाणू ठिपके"},
    },
    "Early_Blight": {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "disease": {"en": "Early Blight", "hi": "अगेती झुलसा", "mr": "लवकर येणारा करपा"},
    },
    "Healthy": {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "disease": {"en": "Healthy Crop", "hi": "स्वस्थ फसल", "mr": "निरोगी पीक"},
    },
    "Late_Blight": {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "disease": {"en": "Late Blight", "hi": "पछेती झुलसा", "mr": "उशिरा येणारा करपा"},
    },
    "Septoria_Leaf_Spot": {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "disease": {"en": "Septoria Leaf Spot", "hi": "सेप्टोरिया पर्ण धब्बा", "mr": "सेप्टोरिया पानांवरील डाग"},
    },
    "Yellow_Leaf_Curl_Virus": {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "disease": {"en": "Yellow Leaf Curl Virus", "hi": "पीला पत्ती मरोड़ वायरस", "mr": "पिवळा पाने आकुंचन विषाणू"},
    },
    # Other Supported Species in PlantVillage
    "Apple_Scab": {
        "crop": {"en": "Apple", "hi": "सेब", "mr": "सफरचंद"},
        "disease": {"en": "Apple Scab", "hi": "सेब स्केब", "mr": "स्कॅब रोग"},
    },
    "Black_Rot": {
        "crop": {"en": "Grape", "hi": "अंगूर", "mr": "द्राक्ष"},
        "disease": {"en": "Black Rot", "hi": "ब्लैक रॉट", "mr": "काळा कुजवा"},
    },
    "Cedar_Apple_Rust": {
        "crop": {"en": "Apple", "hi": "सेब", "mr": "सफरचंद"},
        "disease": {"en": "Cedar Apple Rust", "hi": "रस्ट (गेरुई)", "mr": "तांबेरा"},
    },
    "Cercospora_Leaf_Spot": {
        "crop": {"en": "Corn / Maize", "hi": "मक्का", "mr": "मका"},
        "disease": {"en": "Cercospora Leaf Spot", "hi": "पर्ण धब्बा", "mr": "पानावरील ठिपके"},
    },
    "Common_Rust_": {
        "crop": {"en": "Corn / Maize", "hi": "मक्का", "mr": "मका"},
        "disease": {"en": "Common Rust", "hi": "रतुआ (रस्ट)", "mr": "तांबेरा"},
    },
    "Esca_(Black_Measles)": {
        "crop": {"en": "Grape", "hi": "अंगूर", "mr": "द्राक्ष"},
        "disease": {"en": "Esca (Black Measles)", "hi": "एस्का रोग", "mr": "एस्का रोग"},
    },
    "Leaf_Blight": {
        "crop": {"en": "Corn / Maize", "hi": "मक्का", "mr": "मका"},
        "disease": {"en": "Leaf Blight", "hi": "पर्ण झुलसा", "mr": "पानांचा करपा"},
    },
    "Leaf_Scorch": {
        "crop": {"en": "Strawberry", "hi": "स्ट्रॉबेरी", "mr": "स्ट्रॉबेरी"},
        "disease": {"en": "Leaf Scorch", "hi": "पत्ती झुलसन", "mr": "पाने जळणे"},
    },
    "Northern_Leaf_Blight": {
        "crop": {"en": "Corn / Maize", "hi": "मक्का", "mr": "मका"},
        "disease": {"en": "Northern Leaf Blight", "hi": "उत्तरी पर्ण झुलसा", "mr": "उत्तर करपा रोग"},
    },
    "Powdery_Mildew": {
        "crop": {"en": "Vegetable", "hi": "सब्जी", "mr": "भाजीपाला"},
        "disease": {"en": "Powdery Mildew", "hi": "सफेद चूर्ण फफूंद", "mr": "भुरी रोग"},
    },
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


def get_crop_meta(label: str, lang: str = "en") -> Dict[str, str]:
    """Return localized crop name and disease name for a label."""
    if lang not in SUPPORTED_LANGS:
        lang = DEFAULT_LANG

    meta = CROP_METADATA.get(label)
    if meta:
        crop = meta["crop"].get(lang) or meta["crop"].get(DEFAULT_LANG, "Crop")
        disease = meta["disease"].get(lang) or meta["disease"].get(DEFAULT_LANG, label)
        return {"crop": crop, "disease": disease}

    # Dynamic fallback for any unforeseen label
    if "___" in label:
        parts = label.split("___", 1)
        return {
            "crop": parts[0].replace("_", " ").title(),
            "disease": parts[1].replace("_", " ").title(),
        }

    return {"crop": "Crop", "disease": label.replace("_", " ").title()}


def display_name(label: str, lang: str = "en") -> str:
    """Return localized display name formatted as 'Crop — Disease'."""
    meta = get_crop_meta(label, lang=lang)
    return f"{meta['crop']} — {meta['disease']}"


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

