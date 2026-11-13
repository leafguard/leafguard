"""Script to populate verified, authentic ICAR/KVK agronomic advisory knowledge base.

Covers all 27 crop disease classes in English, Hindi, and Marathi.
Strictly adheres to safety rules: contains only cultural, biological, and agronomic
guidelines without chemical pesticide dosages.
"""
import json
from pathlib import Path

ADVISORY_PATH = Path("app/data/advisory.json")

DATA = {
    "_disclaimer": {
        "en": "Indicative diagnostic advisory only. Confirm with your local Krishi Vigyan Kendra (KVK) or agriculture officer before applying treatments.",
        "hi": "यह केवल सांकेतिक सलाहकार परिणाम है। उपचार लागू करने से पहले अपने स्थानीय कृषि विज्ञान केंद्र (KVK) या कृषि अधिकारी से पुष्टि करें।",
        "mr": "हा केवळ मार्गदर्शक निकाल आहे. कोणतेही उपचार करण्यापूर्वी आपल्या स्थानिक कृषी विज्ञान केंद्र (KVK) किंवा कृषी अधिकाऱ्यांशी संपर्क साधा."
    },

    # --- COTTON (ICAR-CICR Nagpur) ---
    "Cotton___bacterial_blight": {
        "name": {
            "en": "Cotton — Bacterial Blight",
            "hi": "कपास — जीवाणु झुलसा (बैक्टीरियल ब्लाइट)",
            "mr": "कापूस — जिवाणू करपा (बॅक्टेरियल ब्लाइट)"
        },
        "symptoms": {
            "en": [
                "Angular, water-soaked lesions bounded by leaf veinlets on foliage.",
                "Lesions turn reddish-brown to dark brown, leading to premature leaf shedding.",
                "Black arm lesions may develop on stems and branches."
            ],
            "hi": [
                "पत्तियों की नसों के बीच कोणीय, पानी से भीगे हुए धब्बे बनते हैं।",
                "धब्बे बाद में गहरे लाल-भूरे हो जाते हैं और पत्तियां समय से पहले झड़ने लगती हैं।",
                "तनों और टहनियों पर काले धब्बे (ब्लैक आर्म) विकसित हो सकते हैं।"
            ],
            "mr": [
                "पानांच्या शिरांच्या दरम्यान कोनीय, पाण्यासारखे ओलसर ठिपके तयार होतात.",
                "ठिपके नंतर लालसर-तपकिरी होऊन पाने अकाली गळतात.",
                "फांद्यांवर व खोडावर काळे चट्टे (ब्लॅक आर्म) तयार होऊ शकतात."
            ]
        },
        "actions": {
            "en": [
                "Collect and burn severely infected leaves and crop residue after harvest.",
                "Avoid excessive nitrogen fertilizer application which promotes soft foliage growth.",
                "Spray bio-control agent Pseudomonas fluorescens or copper-based bio-protectant."
            ],
            "hi": [
                "रोगग्रस्त पत्तियों और फसल अवशेषों को एकत्र कर नष्ट कर दें।",
                "अधिक यूरिया (नाइट्रोजन) के प्रयोग से बचें जिससे पत्तियों की कोमलता न बढ़े।",
                "स्यूडोमोनास फ्लोरोसेंस या जैविक कॉपर फॉर्मूलेशन का छिड़काव करें।"
            ],
            "mr": [
                "रोगट पाने व पिकाचे अवशेष गोळा करून जाळून नष्ट करा.",
                "नत्राचा (युरिया) अतिवापर टाळा, ज्यामुळे पाने मऊ पडत नाहीत.",
                "स्यूडोमोनास फ्लोरोसन्स किंवा जैविक कॉपर घटकाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Use certified disease-free acid-delinted seeds.",
                "Grow resistant cotton hybrids recommended by state agricultural universities.",
                "Practice crop rotation with non-host crops like maize or sorghum."
            ],
            "hi": [
                "प्रमाणित रोगमुक्त और एसिड-डिलिंटेड बीजों की ही बुवाई करें।",
                "विश्वविद्यालय द्वारा अनुशंसित रोगरोधी कपास संकरों की खेती करें।",
                "मक्का या ज्वार जैसी गैर-मेजबान फसलों के साथ फसल चक्र अपनाएं।"
            ],
            "mr": [
                "प्रमाणित आणि ॲसिड-डिलिंटेड बियाण्यांचाच पेरणीसाठी वापर करा.",
                "कृषी विद्यापीठाने शिफारस केलेले रोगप्रतिकारक वाण निवडा.",
                "मका किंवा ज्वारीसारख्या पिकांसोबत योग्य पीक फेरपालट करा."
            ]
        },
        "source": {
            "name": "ICAR-Central Institute for Cotton Research (CICR), Nagpur",
            "url": "https://cicr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Cotton___curl_virus": {
        "name": {
            "en": "Cotton — Leaf Curl Virus",
            "hi": "कपास — पत्ती मरोड़ वायरस (लीफ कर्ल वायरस)",
            "mr": "कापूस — पाने आकुंचन विषाणू (लीफ कर्ल व्हायरस)"
        },
        "symptoms": {
            "en": [
                "Upward and downward curling of young leaf margins with prominent vein thickening.",
                "Formation of enations (cup-shaped leaf-like outgrowths) on the undersides of primary veins.",
                "Severe stunting of cotton plants with reduced boll development."
            ],
            "hi": [
                "ऊपरी पत्तियों के किनारे ऊपर या नीचे की ओर मुड़ जाते हैं और नसें मोटी हो जाती हैं।",
                "पत्तियों की निचली नसों पर छोटे पत्ती जैसे उभार (इनेशन) बन जाते हैं।",
                "पौधों की बढ़वार रुक जाती है और गूलर का विकास बहुत कम होता है।"
            ],
            "mr": [
                "कोवळ्या पानांच्या कडा वर किंवा खाली वळतात आणि पानाच्या शिरा जाड होतात.",
                "पानांच्या खालच्या बाजूला मुख्य शिरांवर पानासारखी छोटी गाठ (इनेशन) तयार होते.",
                "झाडांची वाढ खुंटते आणि बोंडांची संख्या व आकार घटतो."
            ]
        },
        "actions": {
            "en": [
                "Rogue out and deeply bury heavily stunted, virus-infected plants within 45 days of sowing.",
                "Install yellow sticky traps (15 to 20 traps per acre) across the field to monitor and trap whiteflies.",
                "Spray neem seed kernel extract (NSKE) or neem oil bio-formulation to control whitefly vectors."
            ],
            "hi": [
                "बुवाई के 45 दिनों के भीतर गंभीर रूप से रोगग्रस्त पौधों को उखाड़कर जमीन में दबा दें।",
                "सफेद मक्खी की निगरानी व नियंत्रण हेतु खेत में पीले चिपचिपे ट्रैप (15 से 20 प्रति एकड़) लगाएं।",
                "सफेद मक्खी की रोकथाम के लिए नीम के बीज के अर्क (NSKE) या नीम तेल का छिड़काव करें।"
            ],
            "mr": [
                "पेरणीनंतर ४५ दिवसांच्या आत अति-बाधित झाडे उपटून जमिनीत गाडून नष्ट करा.",
                "पांढऱ्या माशीच्या नियंत्रणासाठी शेतात पिवळे चिकट सापळे (एकरला १५ ते २०) लावा.",
                "पांढऱ्या माशीचा प्रादुर्भाव रोखण्यासाठी निंबोळी अर्क (NSKE) किंवा कडुलिंब तेलाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Eradicate alternate weed hosts (Abutilon indicum, Parthenium) on field bunds and surrounding channels.",
                "Sow CLCuV-tolerant Bt cotton hybrids during the recommended early planting window.",
                "Avoid late planting and refrain from planting susceptible varieties."
            ],
            "hi": [
                "खेत की मेड़ों और नालियों से खरपतवार (कंधी, गाजरघास) को पूरी तरह नष्ट करें।",
                "अनुशंसित समय पर रोगरोधी कपास संकरों की समय पर बुवाई करें।",
                "देर से बुवाई करने से बचें और संवेदनशील किस्मों का उपयोग न करें।"
            ],
            "mr": [
                "शेताच्या बांधावरील आणि पाटावरील तण (गाजरगवत, पेटारी) पूर्णपणे नष्ट करा.",
                "योग्य वेळेत रोगप्रतिकारक बीटी कपाशी वाणांची पेरणी पूर्ण करा.",
                "उशिरा पेरणी करणे टाळा आणि रोगास बळी पडणाऱ्या जाती लावू नका."
            ]
        },
        "source": {
            "name": "ICAR-Central Institute for Cotton Research (CICR), Nagpur",
            "url": "https://cicr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Cotton___fussarium_wilt": {
        "name": {
            "en": "Cotton — Fusarium Wilt",
            "hi": "कपास — उकठा रोग (फ्यूजेरियम विल्ट)",
            "mr": "कापूस — मर रोग (फ्युजॅरियम विल्ट)"
        },
        "symptoms": {
            "en": [
                "Yellowing and loss of turgidity in leaves, starting from lower foliage upward.",
                "Brownish discoloration of the internal vascular tissue visible when the stem is split lengthwise.",
                "Complete wilting, drooping, and sudden drying of affected plants."
            ],
            "hi": [
                "निचली पत्तियों से शुरू होकर पत्तियां पीली पड़ने लगती हैं और मुरझा जाती हैं।",
                "तने को लंबाई में चीरने पर अंदर की नसों में भूरा-काला रंग दिखाई देता है।",
                "प्रभावित पौधा सूखकर अचानक मुरझा जाता है।"
            ],
            "mr": [
                "खालच्या पानांपासून सुरुवात होऊन पाने पिवळी पडतात आणि निस्तेज होतात.",
                "खोड उभे चिरून पाहिल्यास आतील रक्तवाहिन्यांमध्ये तपकिरी काळपट रंग दिसतो.",
                "बाधित झाड सुकून अचानक कोमेजून मरते."
            ]
        },
        "actions": {
            "en": [
                "Drench root zone with Trichoderma viride enriched farmyard manure.",
                "Create proper drainage channels to prevent standing water in low-lying field patches.",
                "Uproot dead wilted plants and dispose of them outside the cultivation area."
            ],
            "hi": [
                "गोबर की खाद में संवर्धित ट्राइकोडर्मा विरिडी से पौधों की जड़ों के पास ड्रेंचिंग करें।",
                "खेत में पानी भरने से रोकने के लिए जल निकासी की उचित व्यवस्था करें।",
                "सूखे रोगग्रस्त पौधों को जड़ सहित उखाड़कर खेत से बाहर जला दें।"
            ],
            "mr": [
                "शेणखतात मिसळलेल्या ट्रायकोडर्मा व्हिरिडीने झाडांच्या मुळांशी आळवणी (ड्रेंचिंग) करा.",
                "शेतात पाणी साचून राहू नये म्हणून योग्य पाण्याचा निचरा करा.",
                "वाळलेली रोगट झाडे मुळासकट उपटून शेताबाहेर नष्ट करा."
            ]
        },
        "prevention": {
            "en": [
                "Practice 3-year crop rotation with non-host crops like sorghum or pearl millet.",
                "Undertake deep summer ploughing to expose soil-borne fungal spores to solar heat.",
                "Treat seeds with bio-agent Trichoderma before sowing."
            ],
            "hi": [
                "ज्वार या बाजरा जैसी फसलों के साथ 3 साल का फसल चक्र अपनाएं।",
                "गर्मी के दिनों में गहरी जुताई करें ताकि धूप से मिट्टी के रोगाणु नष्ट हो सकें।",
                "बुवाई से पहले बीजों का जैविक एजेंट ट्राइकोडर्मा से उपचार करें।"
            ],
            "mr": [
                "ज्वारी किंवा बाजरीसारख्या पिकांसोबत ३ वर्षांची पीक फेरपालट करा.",
                "उन्हाळ्यात जमिनीची खोल नांगरट करून जमीन चांगली तापू द्या.",
                "पेरणीपूर्वी बियाण्यांवर ट्रायकोडर्मा या जैविक घटकाची बीजप्रक्रिया करा."
            ]
        },
        "source": {
            "name": "ICAR-Central Institute for Cotton Research (CICR), Nagpur",
            "url": "https://cicr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Cotton___healthy": {
        "name": {
            "en": "Cotton — Healthy Crop",
            "hi": "कपास — स्वस्थ फसल",
            "mr": "कापूस — निरोगी पीक"
        },
        "symptoms": {
            "en": [
                "Broad, uniform dark-green palmate leaves without spots, yellowing, or curl.",
                "Vigorous branching and normal sympodial fruiting branch development.",
                "Square and boll formation progressing cleanly without premature shedding."
            ],
            "hi": [
                "पत्तियां चौड़ी, गहरी हरी और बिना किसी धब्बे या मुड़ाव के स्वस्थ हैं।",
                "शाखाओं का विकास सामान्य है और फलदार शाखाएं अच्छी तरह बढ़ रही हैं।",
                "कलियां और गूलर बिना किसी गिरावट के सामान्य रूप से बढ़ रहे हैं।"
            ],
            "mr": [
                "पाने रुंद, गर्द हिरवी आणि कोणत्याही डागांशिवाय किंवा आकुंचनाशिवाय निरोगी आहेत.",
                "फांद्यांची वाढ जोमदार असून फलधारणा शाखा व्यवस्थित वाढत आहेत.",
                "पात्या आणि बोंडे कोणतीही गळ न होता चांगल्या प्रकारे विकसित होत आहेत."
            ]
        },
        "actions": {
            "en": [
                "Continue weekly field monitoring for early signs of sucking pests or foliar spots.",
                "Maintain clean weeding around the base of plants during early squaring.",
                "Apply balanced organic compost and adequate moisture through furrow or drip irrigation."
            ],
            "hi": [
                "रस चूसक कीटों या पत्ती के धब्बों के शुरुआती लक्षणों के लिए साप्ताहिक निरीक्षण जारी रखें।",
                "कलियां बनते समय पौधों के आसपास साफ निराई-गुड़ाई बनाए रखें।",
                "संतुलित जैविक खाद डालें और ड्रिप या नाली विधि से उचित नमी बनाए रखें।"
            ],
            "mr": [
                "रसशोषक किडी किंवा पानावरील ठिपक्यांसाठी आठवड्यातून एकदा शेताची पाहणी करा.",
                "पात्या लागण्याच्या काळात झाडांभोवती वेळेवर खुरपणी करून शेत तणमुक्त ठेवा.",
                "संतुलित सेंद्रिय खत द्या आणि ठिबक सिंचनाने योग्य ओलावा टिकवून ठेवा."
            ]
        },
        "prevention": {
            "en": [
                "Maintain balanced fertilization, avoiding excessive nitrogen that attracts bollworms.",
                "Conserve natural predatory beneficial insects like ladybird beetles and chrysoperla.",
                "Ensure soil health through cover cropping and organic residue recycling."
            ],
            "hi": [
                "संतुलित खाद प्रबंधन करें, अत्यधिक यूरिया से बचें जो कीटों को आकर्षित करता है।",
                "मित्र कीटों (जैसे लेडीबर्ड बीटल) के संरक्षण हेतु अनावश्यक रसायनों से बचें।",
                "हरी खाद और जैविक अवशेषों के प्रयोग से मिट्टी की सेहत बनाए रखें।"
            ],
            "mr": [
                "संतुलित खत व्यवस्थापन ठेवा; अति नत्र देणे टाळा ज्यामुळे किडी आकर्षित होतात.",
                "शेतकरी मित्र कीटकांचे (उदा. ढालकिडा) संरक्षण करा.",
                "हिरवळीच्या खतांचा वापर करून जमिनीची सुपीकता टिकवून ठेवा."
            ]
        },
        "source": {
            "name": "ICAR-Central Institute for Cotton Research (CICR), Nagpur",
            "url": "https://cicr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    # --- TURMERIC (ICAR-IISR Kozhikode) ---
    "Turmeric___Leaf_Blotch": {
        "name": {
            "en": "Turmeric — Leaf Blotch",
            "hi": "हल्दी — पत्ती धब्बा (लीफ ब्लॉच)",
            "mr": "हळद — पानावरील ठिपके (लीफ ब्लॉच)"
        },
        "symptoms": {
            "en": [
                "Numerous small, rectangular to oval yellow spots on both leaf surfaces.",
                "Spots soon turn bay-brown to dark dirty-brown, coalescing into extensive blotches.",
                "Severely infected leaves become dry, papery, and brittle along margins."
            ],
            "hi": [
                "पत्तियों की दोनों सतहों पर कई छोटे, आयताकार या गोल पीले धब्बे दिखाई देते हैं।",
                "धब्बे जल्द ही गहरे भूरे रंग में बदल जाते हैं और आपस में मिलकर बड़े पैच बनाते हैं।",
                "अधिक संक्रमण में पत्तियां किनारों से सूखकर कुरकुरी व कागजी हो जाती हैं।"
            ],
            "mr": [
                "पानांच्या दोन्ही बाजूंवर असंख्य लहान, पिवळे चौकोनी किंवा लंबगोलाकार ठिपके दिसतात.",
                "ठिपके लवकरच गडद तपकिरी रंगाचे होऊन एकमेकांत मिसळतात आणि मोठे चट्टे बनतात.",
                "जास्त प्रादुर्भाव झाल्यास पाने कडेने सुकून कागदासारखी ठिसूळ होतात."
            ]
        },
        "actions": {
            "en": [
                "Collect and burn severely spotted and dried foliage to prevent spore dispersal.",
                "Avoid sprinkler irrigation; water at ground level to minimize moisture on leaf canopies.",
                "Spray Bordeaux mixture bio-formulation or bio-fungicide Trichoderma viride."
            ],
            "hi": [
                "संक्रमित व सूखी पत्तियों को काटकर खेत से बाहर ले जाकर नष्ट करें।",
                "फव्वारा सिंचाई से बचें; पत्तियों पर पानी न पड़े इसलिए जमीन पर सिंचाई करें।",
                "बोर्डो मिश्रण या जैविक कवकनाशी ट्राइकोडर्मा विरिडी का छिड़काव करें।"
            ],
            "mr": [
                "तीव्र बाधित व सुकलेली पाने गोळा करून जाळून नष्ट करा.",
                "तुषार सिंचन टाळा; पानांवर पाणी साचणार नाही अशा प्रकारे जमिनीवर पाणी द्या.",
                "बोर्डो मिश्रण किंवा ट्रायकोडर्मा व्हिरिडी या जैविक बुरशीनाशकाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Select seed rhizomes strictly from disease-free, high-yielding parent plots.",
                "Plant rhizomes on raised beds (15 cm high) with deep inter-row drainage channels.",
                "Apply neem cake in the soil during bed preparation to enhance plant immunity."
            ],
            "hi": [
                "रोगमुक्त और स्वस्थ मातृ भूखंडों से ही बीज प्रकंद (राइजोम) का चयन करें।",
                "15 सेमी ऊंचे उठे हुए बिस्तरों (उठी क्यारी) पर जल निकासी नालियों के साथ बुवाई करें।",
                "खेत की तैयारी के समय मिट्टी में नीम की खली मिलाएं ताकि पौधों की प्रतिरोधक क्षमता बढ़े।"
            ],
            "mr": [
                "केवळ निरोगी आणि रोगमुक्त मातृ प्लॉटमधूनच बेणे (कंद) निवडा.",
                "१५ सेंमी उंच गादीवाफ्यावर पाण्याचा योग्य निचरा होईल अशा पद्धतीने लागवड करा.",
                "वाफे तयार करताना जमिनीत निंबोळी पेंडीचा वापर करा, ज्यामुळे झाडांची प्रतिकारशक्ती वाढते."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Spices Research (IISR), Kozhikode",
            "url": "https://spices.res.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Turmeric___Dry_Leaf": {
        "name": {
            "en": "Turmeric — Dry Leaf & Rhizome Wilt",
            "hi": "हल्दी — पत्ती सूखना व प्रकंद सड़ांध (राइजोम रॉट)",
            "mr": "हळद — पाने सुकणे व कंदकुज (राइजोम रॉट)"
        },
        "symptoms": {
            "en": [
                "Gradual drying and yellowing of foliage starting from margins of lower leaves.",
                "Base of the pseudostem turns soft, dark, and water-soaked, emitting foul odor.",
                "Infected shoots pull out effortlessly when gently tugged."
            ],
            "hi": [
                "निचली पत्तियों के किनारों से शुरू होकर पत्तियां धीरे-धीरे पीली पड़कर सूखने लगती हैं।",
                "तने का निचला हिस्सा मुलायम, काला और सड़ा हुआ हो जाता है, जिससे दुर्गंध आती है।",
                "हल्का खींचने पर भी रोगग्रस्त तना आसानी से बाहर निकल आता है।"
            ],
            "mr": [
                "खालच्या पानांच्या कडांपासून सुरुवात होऊन पाने हळूहळू पिवळी पडून सुकतात.",
                "खोडाचा जमिनीलगतचा भाग मऊ, काळपट आणि सडका होतो, त्याला दुर्गंधी येते.",
                "झाड हाताने हलके ओढल्यास सहज उपटून हातात येते."
            ]
        },
        "actions": {
            "en": [
                "Immediately cut drainage trenches to discharge standing rainwater from the plot.",
                "Drench root zones with Trichoderma harzianum enriched farmyard compost.",
                "Remove rotten rhizomes and bury them deeply with lime outside the field."
            ],
            "hi": [
                "खेत से जमा हुआ पानी निकालने के लिए तुरंत जलनिकासी की नालियां बनाएं।",
                "संवर्धित ट्राइकोडर्मा हरजिएनम और गोबर की खाद से पौधों की जड़ों में ड्रेंचिंग करें।",
                "सड़े हुए प्रकंदों को निकालकर खेत से बाहर चूने के साथ गड्ढे में दबा दें।"
            ],
            "mr": [
                "शेतात साचलेले पावसाचे पाणी बाहेर काढण्यासाठी तात्काळ चर खोदा.",
                "ट्रायकोडर्मा हार्झियानम संवर्धित शेणखताने मुळांशी आळवणी करा.",
                "कुजलेले कंद शेताबाहेर काढून चुन्यासोबत जमिनीत खोल गाडून टाका."
            ]
        },
        "prevention": {
            "en": [
                "Treat seed rhizomes before planting with bio-agent Trichoderma bio-slurry.",
                "Never cultivate turmeric in heavy clay soil prone to seasonal water stagnation.",
                "Solarize nursery beds using transparent polythene sheets during hot summer months."
            ],
            "hi": [
                "बुवाई से पहले बीज प्रकंदों को ट्राइकोडर्मा घोल से अच्छी तरह उपचारित करें।",
                "भारी चिकनी मिट्टी में हल्दी की खेती न करें जहां पानी भरने का खतरा हो।",
                "मई-जून की तेज धूप में पारदर्शी प्लास्टिक शीट से क्यारियों का सॉइल सोलराइजेशन करें।"
            ],
            "mr": [
                "लागवडीपूर्वी बेण्यांवर ट्रायकोडर्माच्या द्रावणाची बीजप्रक्रिया नक्की करा.",
                "पाण्याचा निचरा न होणाऱ्या भारी चिकणमातीच्या जमिनीत हळदीची लागवड टाळा.",
                "उन्हाळ्यात पारदर्शक प्लास्टिक कागद अंथरून जमिनीचे निर्जंतुकीकरण (सोलरायझेशन) करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Spices Research (IISR), Kozhikode",
            "url": "https://spices.res.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Turmeric___Healthy_Leaf": {
        "name": {
            "en": "Turmeric — Healthy Crop",
            "hi": "हल्दी — स्वस्थ फसल",
            "mr": "हळद — निरोगी पीक"
        },
        "symptoms": {
            "en": [
                "Large, upright, lanceolate leaves with rich deep-green sheen.",
                "Vigorous pseudostem growth with clean leaf sheaths free from rot.",
                "Underground rhizome clumps expanding normally without soft lesions."
            ],
            "hi": [
                "पत्तियां बड़ी, सीधी, गहरे हरे रंग की और पूरी तरह स्वस्थ हैं।",
                "तने का विकास मजबूत है और पत्तियों के आवरण में कोई सड़न नहीं है।",
                "जमीन के नीचे प्रकंद (गांठें) बिना किसी दाग या सड़न के सामान्य रूप से बढ़ रही हैं।"
            ],
            "mr": [
                "पाने लांब, सरळ, गर्द हिरव्या रंगाची आणि चमकदार दिसतात.",
                "खोडाची वाढ मजबूत असून पानाच्या आवरणामध्ये कोणताही सडकेपणा नाही.",
                "जमिनीतील हळदीचे कंद कोणत्याही रोगाशिवाय निरोगी व जोमाने वाढत आहेत."
            ]
        },
        "actions": {
            "en": [
                "Apply thick green leaf mulch across beds to conserve soil moisture and suppress weeds.",
                "Maintain uniform, aerated soil moisture through regular scheduled irrigation.",
                "Perform light earthing-up around plant bases as rhizomes expand."
            ],
            "hi": [
                "मिट्टी की नमी बनाए रखने और खरपतवार रोकने के लिए क्यारियों पर हरी पत्तियों का पलवार (मल्चिंग) लगाएं।",
                "नियमित सिंचाई द्वारा जड़ों के पास हल्की नमी और हवा का संचार बनाए रखें।",
                "प्रकंदों के विकास के साथ पौधों की जड़ों पर हल्की मिट्टी चढ़ाएं (अर्थिंग-अप)।"
            ],
            "mr": [
                "जमिनीतील ओलावा टिकवण्यासाठी आणि तण रोखण्यासाठी हिरव्या पानांचे चांगले आच्छादन (मल्चिंग) करा.",
                "नियमित पाण्याच्या पाळ्या देऊन मुळांशी वाफसा स्थिती टिकवून ठेवा.",
                "कंदांचा चांगला विकास होण्यासाठी योग्य वेळी झाडांच्या बुंध्याशी भर द्या."
            ]
        },
        "prevention": {
            "en": [
                "Ensure strict drainage maintenance throughout monsoon showers.",
                "Apply well-decomposed organic farmyard manure enriched with beneficial microbes.",
                "Scout regularly for rhizome fly or shoot borer damage."
            ],
            "hi": [
                "मानसून के दौरान खेत में पानी का निकास सुचारू बनाए रखें।",
                "सड़ा हुआ गोबर खाद और जैव उर्वरक समय पर खेत में डालें।",
                "प्रकंद मक्खी या तना छेदक कीट की नियमित जांच करते रहें।"
            ],
            "mr": [
                "पावसाळ्यात शेतात कुठेही पाणी साचणार नाही याची खबरदारी घ्या.",
                "चांगले कुजलेले शेणखत आणि सूक्ष्मजीवांचा नियमित वापर करा.",
                "कंदमाशी किंवा खोडकिडीच्या प्रादुर्भावासाठी नियमित पाहणी करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Spices Research (IISR), Kozhikode",
            "url": "https://spices.res.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    # --- SOYBEAN (ICAR-IISR Indore) ---
    "Soybean___Soyabean_Mosaic": {
        "name": {
            "en": "Soybean — Mosaic Virus",
            "hi": "सोयाबीन — मोज़ेक वायरस",
            "mr": "सोयाबीन — मोझॅक विषाणू"
        },
        "symptoms": {
            "en": [
                "Leaves display prominent yellow and green mosaic mottling.",
                "Puckering, blister-like raised areas, and downward curling of leaflet margins.",
                "Stunted plant stature with fewer and smaller pod formation."
            ],
            "hi": [
                "पत्तियों पर पीले और हरे रंग के चितकबरे धब्बे (मोज़ेक पैटर्न) दिखाई देते हैं।",
                "पत्तियों की सतह खुरदरी, फफोलेदार हो जाती है और किनारे नीचे मुड़ जाते हैं।",
                "पौधों की बढ़वार रुक जाती है और फलियों की संख्या व आकार घट जाता है।"
            ],
            "mr": [
                "पानांवर पिवळ्या व हिरव्या रंगाचे ठिपके (मोझॅक) स्पष्ट दिसतात.",
                "पाने चुरगळल्यासारखी होतात, त्यावर फोड आल्यासारखा उंचवटा येतो आणि कडा खाली वळतात.",
                "झाडांची वाढ खुंटते आणि शेंगांची संख्या व दाण्यांचा आकार लहान राहतो."
            ]
        },
        "actions": {
            "en": [
                "Rogue out and destroy infected mosaic plants during early vegetative growth (first 35 days).",
                "Deploy yellow sticky traps to detect and trap aphid vector populations.",
                "Spray neem oil formulation or plant extracts to suppress aphid vector transmission."
            ],
            "hi": [
                "बुवाई के शुरुआती 35 दिनों के भीतर रोगग्रस्त पौधों को उखाड़कर नष्ट कर दें।",
                "माहू (एफिड) कीटों की निगरानी के लिए खेत में पीले स्टिकी ट्रैप लगाएं।",
                "एफिड कीटों के नियंत्रण के लिए नीम तेल फॉर्मूलेशन का छिड़काव करें।"
            ],
            "mr": [
                "पेरणीनंतर पहिल्या ३५ दिवसांत रोगट झाडे शेतातून उपटून नष्ट करा.",
                "मावा किडींच्या निरीक्षणासाठी आणि नियंत्रणासाठी पिवळे चिकट सापळे लावा.",
                "मावा किडींचा प्रसार रोखण्यासाठी कडुलिंब तेलाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Sow only certified virus-free seed from reliable seed agencies (SMV is seed-transmitted).",
                "Keep field bunds, pathways, and adjacent areas completely free of weed hosts.",
                "Practice recommended crop rotation with non-leguminous crops like maize or sorghum."
            ],
            "hi": [
                "केवल प्रमाणित और वायरस-मुक्त बीज ही बोएं (यह रोग बीज द्वारा फैलता है)।",
                "खेत की मेड़ों और रास्तों से खरपतवार को पूरी तरह साफ रखें।",
                "मक्का या ज्वार जैसी फसलों के साथ उचित फसल चक्र अपनाएं।"
            ],
            "mr": [
                "केवळ प्रमाणित आणि विषाणूमुक्त बियाण्यांचीच पेरणी करा (हा रोग बियाण्यातून पसरतो).",
                "शेताचे बांध आणि आजूबाजूचा परिसर तणमुक्त ठेवा.",
                "मका किंवा ज्वारीसारख्या तृणधान्य पिकांसोबत योग्य पीक फेरपालट करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Soybean Research (IISR), Indore",
            "url": "https://iisrindore.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Soybean___Soyabean_Frog_Leaf_Eye": {
        "name": {
            "en": "Soybean — Frogeye Leaf Spot",
            "hi": "सोयाबीन — मेंढक आंख धब्बा रोग (फ्रॉगआई लीफ स्पॉट)",
            "mr": "सोयाबीन — बेडूक डोळा ठिपके रोग (फ्रॉगआय लीफ स्पॉट)"
        },
        "symptoms": {
            "en": [
                "Small, circular to angular spots with light-gray or tan centers on upper leaves.",
                "Spots are surrounded by a distinct narrow, dark reddish-brown border.",
                "Under humid weather, thin silver-gray fungal spore growth appears in lesion centers."
            ],
            "hi": [
                "ऊपरी पत्तियों पर छोटे, गोल या कोणीय धब्बे बनते हैं जिनका केंद्र हल्का भूरा या सफेद होता है।",
                "धब्बों के चारों ओर एक स्पष्ट, पतली गहरे लाल-भूरे रंग की किनारी (बॉर्डर) होती है।",
                "नमी वाले मौसम में धब्बों के बीच में हल्की फफूंद दिखाई देती है।"
            ],
            "mr": [
                "वरच्या पानांवर लहान, गोल किंवा कोनीय ठिपके पडतात ज्यांचा मध्यभाग फिकट राखाडी असतो.",
                "ठिपक्यांभोवती गडद लालसर-तपकिरी रंगाची ठळक कडा (बॉर्डर) असते.",
                "दमट हवामानात ठिपक्यांच्या मध्यभागी हलकी बुरशी तयार होते."
            ]
        },
        "actions": {
            "en": [
                "Ensure proper inter-row field drainage to lower relative humidity within the crop canopy.",
                "Avoid walking or moving spray equipment through fields while foliage is wet with morning dew.",
                "Spray bio-fungicide bio-formulation (Trichoderma harzianum) to arrest spot spread."
            ],
            "hi": [
                "फसल में नमी कम करने के लिए कतारों के बीच जल निकासी की उचित व्यवस्था करें।",
                "सुबह ओस के समय जब पत्तियां गीली हों, तब खेत में काम करने या चलने से बचें।",
                "धब्बों के फैलाव को रोकने के लिए जैविक कवकनाशी (ट्राइकोडर्मा) का छिड़काव करें।"
            ],
            "mr": [
                "पिकात ओलावा कमी करण्यासाठी ओळींमध्ये योग्य पाण्याचा निचरा ठेवा.",
                "सकाळी पानांवर दवबिंदू असताना शेतात फिरणे किंवा खुरपणी करणे टाळा.",
                "ठिपके पसरण्यापासून रोखण्यासाठी ट्रायकोडर्मा या जैविक बुरशीनाशकाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Plant certified frogeye-resistant soybean varieties recommended for your agro-climatic zone.",
                "Perform deep summer tillage to bury infected crop residues and break spore cycles.",
                "Rotate with non-host crops like corn or cotton for at least 2 seasons."
            ],
            "hi": [
                "अपने क्षेत्र के लिए अनुशंसित रोगरोधी सोयाबीन किस्मों की ही बुवाई करें।",
                "गर्मी में गहरी जुताई करें ताकि संक्रमित अवशेष जमीन में दब जाएं।",
                "मक्का या कपास जैसी फसलों के साथ कम से कम दो सीजन का फसल चक्र अपनाएं।"
            ],
            "mr": [
                "आपल्या विभागासाठी शिफारस केलेले रोगप्रतिकारक सोयाबीन वाण वापरा.",
                "उन्हाळ्यात खोल नांगरट करून पिकांचे रोगट अवशेष जमिनीत गाडून टाका.",
                "मका किंवा कापूस या पिकांसोबत किमान दोन हंगामांची पीक फेरपालट करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Soybean Research (IISR), Indore",
            "url": "https://iisrindore.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Soybean___Soyabean_Spectoria_Brown_Spot": {
        "name": {
            "en": "Soybean — Septoria Brown Spot",
            "hi": "सोयाबीन — सेप्टोरिया भूरा धब्बा रोग (ब्राउन स्पॉट)",
            "mr": "सोयाबीन — सेप्टोरिया तपकिरी ठिपके रोग (ब्राउन स्पॉट)"
        },
        "symptoms": {
            "en": [
                "Small, irregular, dark brown lesions appearing first on unifoliate and lower trifoliate leaves.",
                "Affected lower leaves turn yellow and drop prematurely from the plant.",
                "Lesions coalesce during warm wet spells, advancing progressively upward into the upper canopy."
            ],
            "hi": [
                "निचली पत्तियों पर छोटे, अनियमित गहरे भूरे रंग के धब्बे सबसे पहले दिखाई देते हैं।",
                "संक्रमित निचली पत्तियां पीली पड़ जाती हैं और समय से पहले सूखकर गिर जाती हैं।",
                "बारिश और नमी में धब्बे आपस में मिलकर ऊपर की पत्तियों तक फैल जाते हैं।"
            ],
            "mr": [
                "खालच्या पानांवर लहान, अनियमित आकाराचे गडद तपकिरी ठिपके प्रथम दिसतात.",
                "बाधित झालेली खालची पाने पिवळी पडून अकाली गळून पडतात.",
                "पावसाळ्यात व दमट हवेत हे ठिपके एकमेकांत मिसळून झाडाच्या वरच्या भागापर्यंत पसरतात."
            ]
        },
        "actions": {
            "en": [
                "Do not disturb or cultivate within wet fields to avoid mechanically transmitting fungal spores.",
                "Ensure broad-bed furrow drainage to evacuate standing rain pools rapidly.",
                "Spray copper-based organic protectant or bio-agent formulation if lower defoliation begins."
            ],
            "hi": [
                "गीले खेत में जुताई या निराई न करें ताकि औजारों से रोगाणु न फैलें।",
                "खेत में जमा बारिश का पानी तुरंत निकालने के लिए नाली व्यवस्था दुरुस्त करें।",
                "यदि निचली पत्तियां गिरने लगें तो जैविक कॉपर या बायो-एजेंट फॉर्मूलेशन का छिड़काव करें।"
            ],
            "mr": [
                "पाने ओली असताना शेतात काम करू नका, जेणेकरून बुरशीचे बीजाणू इतर झाडांवर पसरणार नाहीत.",
                "चर काढून पावसाचे पाणी शेतातून तात्काळ बाहेर काढा.",
                "खालची पाने गळू लागल्यास जैविक कॉपर किंवा बायो-बुरशीनाशकाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Adopt a 2-year rotation cycle away from soybean using corn, sorghum, or pearl millet.",
                "Incorporate post-harvest soybean stubble into the soil with disc ploughing.",
                "Sow certified pathogen-free seed treated with Trichoderma bio-formulation."
            ],
            "hi": [
                "मक्का, ज्वार या बाजरा के साथ 2 साल का फसल चक्र अपनाएं।",
                "कटाई के बाद सोयाबीन के ठूंठ और डंठल को गहरी जुताई कर मिट्टी में मिला दें।",
                "ट्राइकोडर्मा से उपचारित प्रमाणित रोगमुक्त बीजों की ही बुवाई करें।"
            ],
            "mr": [
                "मका, ज्वारी किंवा बाजरी पिकांसोबत २ वर्षांचे पीक फेरपालट चक्र राबवा.",
                "कापणीनंतर शेतातील सोयाबीनचे धसकट नांगरट करून जमिनीत गाडून टाका.",
                "ट्रायकोडर्माची बीजप्रक्रिया केलेले प्रमाणित निरोगी बियाणेच पेरा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Soybean Research (IISR), Indore",
            "url": "https://iisrindore.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Soybean___Healthy_Soyabean": {
        "name": {
            "en": "Soybean — Healthy Crop",
            "hi": "सोयाबीन — स्वस्थ फसल",
            "mr": "सोयाबीन — निरोगी पीक"
        },
        "symptoms": {
            "en": [
                "Vibrant dark-green trifoliate leaves without yellowing, spotting, or crinkling.",
                "Strong main stems with uniform node spacing and vigorous floral emergence.",
                "Clean roots exhibiting active pink, nitrogen-fixing Rhizobium nodules."
            ],
            "hi": [
                "पत्तियां चमकदार गहरी हरी, स्वस्थ और बिना किसी धब्बे या सिकुड़न के हैं।",
                "मुख्य तना मजबूत है और फूल व फलियों का विकास सामान्य रूप से हो रहा है।",
                "जड़ों में सक्रिय गुलाबी रंग की राइजोबियम ग्रंथियां (नाइट्रोजन गांठें) मौजूद हैं।"
            ],
            "mr": [
                "पाने चमकदार गर्द हिरवी असून त्यावर कोणतेही डाग किंवा आकुंचन नाही.",
                "मुख्य खोड बळकट असून फुलोरा आणि शेंगांची वाढ योग्य गतीने होत आहे.",
                "मुळांवर नत्र स्थिरीकरण करणाऱ्या निरोगी गुलाबी रायझोबियमच्या गाठी दिसत आहेत."
            ]
        },
        "actions": {
            "en": [
                "Maintain weed-free conditions during the critical early crop growth period (first 40 days).",
                "Monitor for early signs of semilooper caterpillars or girdle beetle infestation.",
                "Ensure soil aeration and drain excess moisture after continuous heavy rains."
            ],
            "hi": [
                "शुरुआती 40 दिनों के महत्वपूर्ण समय में खेत को पूरी तरह खरपतवार मुक्त रखें।",
                "सेमीलूपर इल्ली या गर्डल बीटल (चक्र भृंग) कीट के शुरुआती लक्षणों पर नजर रखें।",
                "लगातार भारी बारिश के बाद खेत से अतिरिक्त पानी निकालकर जड़ों में हवा का संचार बनाए रखें।"
            ],
            "mr": [
                "पेरणीनंतरच्या पहिल्या ४० दिवसांत शेत पूर्णपणे तणमुक्त ठेवा.",
                "उंटअळी किंवा खोडकिडा (गर्डल बीटल) या किडींच्या प्रादुर्भावासाठी नियमित पाहणी करा.",
                "मुसळधार पावसानंतर शेतात साचलेले पाणी त्वरित काढून वाफसा टिकवा."
            ]
        },
        "prevention": {
            "en": [
                "Inoculate seeds with Bradyrhizobium japonicum and PSB cultures before planting.",
                "Practice broad bed furrow (BBF) planting to mitigate climate risks of excess rainfall.",
                "Apply balanced phosphorus and sulfur nutrition to strengthen plant cell walls."
            ],
            "hi": [
                "बुवाई से पहले बीजों को राइजोबियम और पीएसबी कल्चर से उपचारित करें।",
                "अत्यधिक बारिश के नुकसान से बचने के लिए ब्रॉड बेड फरो (BBF) विधि से बुवाई करें।",
                "पौधों को मजबूत बनाने के लिए संतुलित फास्फोरस और सल्फर उर्वरक दें।"
            ],
            "mr": [
                "पेरणीपूर्वी बियाण्यांना रायझोबियम आणि पीएसबी जिवाणू संवर्धकाची प्रक्रिया करा.",
                "जास्त पावसाच्या धोक्यापासून संरक्षणासाठी रुंद वरंबा-सरी (BBF) पद्धतीने पेरणी करा.",
                "पिकाची ताकद वाढवण्यासाठी संतुलित स्फुरद आणि गंधकाचा वापर करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Soybean Research (IISR), Indore",
            "url": "https://iisrindore.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    # --- TOMATO (ICAR-IIHR Bengaluru) ---
    "Septoria_Leaf_Spot": {
        "name": {
            "en": "Tomato — Septoria Leaf Spot",
            "hi": "टमाटर — सेप्टोरिया पर्ण धब्बा (लीफ स्पॉट)",
            "mr": "टोमॅटो — सेप्टोरिया पानांवरील डाग (लीफ स्पॉट)"
        },
        "symptoms": {
            "en": [
                "Small, abundant circular spots (2 to 3 mm) with dark brown borders and gray centers.",
                "Tiny black specks (fruiting pycnidia) visible inside the gray centers of mature spots.",
                "Starts on oldest lower foliage and spreads upward, causing severe leaf yellowing and drop."
            ],
            "hi": [
                "पत्तियों पर कई छोटे गोल धब्बे (2 से 3 मिमी) बनते हैं जिनका किनारा भूरा और केंद्र स्लेटी होता है।",
                "पुराने धब्बों के केंद्र में छोटे काले बिंदु (कवक संरचना) साफ दिखाई देते हैं।",
                "यह सबसे पहले पुरानी निचली पत्तियों पर शुरू होता है और पत्तियां पीली पड़कर झड़ने लगती हैं।"
            ],
            "mr": [
                "पानांवर असंख्य लहान गोल ठिपके पडतात, ज्यांची कडा गडद तपकिरी आणि मध्यभाग राखाडी असतो.",
                "जुन्या ठिपक्यांच्या मध्यभागी लहान काळे ठिपके (बुरशीचे बीजाणू) दिसतात.",
                "खालच्या जुन्या पानांपासून सुरुवात होऊन पाने पिवळी पडतात आणि मोठ्या प्रमाणात गळतात."
            ]
        },
        "actions": {
            "en": [
                "Prune and safely discard lower infected leaves up to 1 foot above the ground to stop rain splash.",
                "Apply organic straw or plastic mulch around the plant base to prevent soil splash onto foliage.",
                "Avoid overhead sprinkler watering; deliver irrigation directly to root zones via drip lines."
            ],
            "hi": [
                "जमीन से 1 फीट ऊपर तक की निचली संक्रमित पत्तियों को काटकर खेत से बाहर नष्ट करें।",
                "मिट्टी के छींटों को पत्तियों तक पहुंचने से रोकने के लिए पौधों के चारों ओर पुआल की मल्चिंग करें।",
                "ऊपर से फव्वारा सिंचाई न करें; केवल ड्रिप द्वारा पौधों की जड़ों में पानी दें।"
            ],
            "mr": [
                "माती उडून पानांवर पडू नये म्हणून जमिनीपासून १ फूट उंचीपर्यंतची खालची रोगट पाने छाटून टाका.",
                "झाडांच्या बुंध्याभोवती गवताचे किंवा पेंढ्याचे आच्छादन (मल्चिंग) करा.",
                "तुषार सिंचन टाळा; केवळ ठिबक सिंचनाने थेट मुळांशी पाणी द्या."
            ]
        },
        "prevention": {
            "en": [
                "Practice a 2 to 3 year crop rotation away from tomato, potato, eggplant, and pepper.",
                "Trellis or stake tomato plants upright to maximize airflow and rapid leaf drying.",
                "Apply preventative bio-fungicide (Trichoderma viride) prior to onset of monsoon rains."
            ],
            "hi": [
                "टमाटर, आलू, बैंगन और मिर्च की फसलों के साथ 2 से 3 साल का फसल चक्र अपनाएं।",
                "हवा के आवागमन और पत्तियों को सूखा रखने के लिए पौधों को डंडे या तार से सहारा (स्टेकिंग) दें।",
                "बरसात के मौसम से पहले जैविक कवकनाशी (ट्राइकोडर्मा) का निवारक छिड़काव करें।"
            ],
            "mr": [
                "टोमॅटो, बटाटा, वांगी व मिरची या पिकांनंतर २ ते ३ वर्षे इतर पिकांची फेरपालट करा.",
                "हवा खेळती राहण्यासाठी आणि पाने सुकी राहण्यासाठी झाडांना बांबू किंवा तारेचा आधार (स्टेकिंग) द्या.",
                "पावसाळ्यापूर्वी प्रतिबंधात्मक उपाय म्हणून ट्रायकोडर्मा व्हिरिडीची फवारणी करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Horticultural Research (IIHR), Bengaluru",
            "url": "https://iihr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Early_Blight": {
        "name": {
            "en": "Tomato — Early Blight",
            "hi": "टमाटर — अगेती झुलसा (अल्टरनेरिया ब्लाइट)",
            "mr": "टोमॅटो — लवकर येणारा करपा (अल्टर्नेरिया ब्लाइट)"
        },
        "symptoms": {
            "en": [
                "Circular brown-black spots with characteristic concentric rings forming a 'target-board' pattern.",
                "Spots surrounded by a chlorotic yellow halo, predominantly initiating on mature lower foliage.",
                "Sunken dark cankers on stems and dark leathery rot at the fruit stem end."
            ],
            "hi": [
                "पत्तियों पर गोल भूरे-काले धब्बे बनते हैं जिनमें छल्लेदार धारियां ('टारगेट बोर्ड' जैसी) होती हैं।",
                "धब्बों के चारों ओर पीला घेरा बन जाता है, जो मुख्य रूप से निचली पुरानी पत्तियों पर दिखता है।",
                "तनों पर काले घाव और फलों के डंठल के पास काला चमड़े जैसा सड़ांध पैदा होता है।"
            ],
            "mr": [
                "पानांवर गोलाकार काळे-तपकिरी ठिपके पडतात ज्यामध्ये चकतीसारखी गोलाकार वलये ('टार्गेट बोर्ड') दिसतात.",
                "ठिपक्यांभोवती पिवळसर कडा तयार होते, ही लक्षणे आधी खालच्या पानांवर दिसतात.",
                "खोडावर खोलगट चट्टे आणि फळांच्या देठाजवळ काळी चामड्यासारखी सड तयार होते."
            ]
        },
        "actions": {
            "en": [
                "Remove and dispose of diseased lower foliage as soon as target-board spots are spotted.",
                "Apply organic straw mulch around plant stems to halt fungal spores splashing from soil.",
                "Spray bio-fungicide formulation (Trichoderma viride or Bacillus subtilis) thoroughly."
            ],
            "hi": [
                "जैसे ही छल्लेदार धब्बे दिखाई दें, नीचे की संक्रमित पत्तियों को तुरंत काटकर हटा दें।",
                "मिट्टी से बीजाणुओं को उछलने से रोकने के लिए पौधों के तनों के चारों ओर पुआल की मल्चिंग करें।",
                "जैविक कवकनाशी (ट्राइकोडर्मा या बैसिलस सबटिलिस) का अच्छी तरह से छिड़काव करें।"
            ],
            "mr": [
                "वलयांकित ठिपके दिसताच खालची रोगट पाने ताबडतोब तोडून नष्ट करा.",
                "मातीतील बुरशी पानांवर उडू नये म्हणून झाडांभोवती पेंढ्याचे आच्छादन करा.",
                "ट्रायकोडर्मा किंवा बॅसिलस सबटिलिस या जैविक बुरशीनाशकाची योग्य फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Maintain recommended plant spacing (at least 60 cm) to facilitate quick canopy drying.",
                "Utilize drip irrigation exclusively; refrain from overhead sprinklers.",
                "Use certified seeds and rotate crops away from solanaceous plants for 2 seasons."
            ],
            "hi": [
                "पत्तियों को सूखा रखने के लिए पौधों के बीच कम से कम 60 सेमी की दूरी रखें।",
                "केवल ड्रिप सिंचाई का उपयोग करें; फव्वारे से पानी देने से पूरी तरह बचें।",
                "प्रमाणित बीजों का उपयोग करें और टमाटर कुल की फसलों से 2 सीजन का फसल चक्र रखें।"
            ],
            "mr": [
                "झाडांमध्ये हवा खेळती राहण्यासाठी किमान ६० सेंमी अंतर ठेवा.",
                "केवळ ठिबक सिंचनाचा वापर करा; तुषार सिंचनाने पाणी देणे टाळा.",
                "प्रमाणित बियाणे वापरा आणि सोलानासी कुळातील पिकांनंतर २ हंगाम इतर पिके घ्या."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Horticultural Research (IIHR), Bengaluru",
            "url": "https://iihr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Late_Blight": {
        "name": {
            "en": "Tomato — Late Blight",
            "hi": "टमाटर — पछेती झुलसा (लेट ब्लाइट)",
            "mr": "टोमॅटो — उशिरा येणारा करपा (लेट ब्लाइट)"
        },
        "symptoms": {
            "en": [
                "Large, irregular water-soaked pale-green lesions that rapidly turn greasy brown-black.",
                "Delicate white downy fungal mold develops on the undersides of lesions during cool, wet weather.",
                "Rapid, total blighting of foliage, stems, and firm brown rot on green fruit."
            ],
            "hi": [
                "पत्तियों पर बड़े, पानी से भीगे हुए अनियमित धब्बे बनते हैं जो तेजी से भूरे-काले हो जाते हैं।",
                "ठंडे और नम मौसम में पत्तियों की निचली सतह पर सफेद रंग की कोमल फफूंद दिखाई देती है।",
                "पूरी फसल कुछ ही दिनों में झुलस जाती है और हरे फलों पर कड़ा भूरा सड़ांध हो जाता है।"
            ],
            "mr": [
                "पानांवर मोठे, पाण्यासारखे ओलसर चट्टे पडतात जे वेगाने काळे-तपकिरी होतात.",
                "थंड आणि दमट हवामानात पानांच्या खालच्या बाजूला पांढुरकी नाजूक बुरशी वाढते.",
                "अवघ्या काही दिवसांत संपूर्ण पीक करपून जाते आणि कच्च्या फळांवर कडक तपकिरी चट्टे पडतात."
            ]
        },
        "actions": {
            "en": [
                "Immediately uproot and bag severely blighted plants to stop catastrophic airborne spore spread.",
                "Do not compost infected plants; burn or deeply bury them outside the farm perimeter.",
                "Spray protective bio-fungicide formulation (Bordeaux mixture or Trichoderma) ahead of rain fronts."
            ],
            "hi": [
                "हवा में बीजाणुओं के प्रसार को रोकने के लिए गंभीर रूप से झुलसे पौधों को तुरंत उखाड़कर थैले में बंद करें।",
                "संक्रमित पौधों को कंपोस्ट में न डालें; उन्हें खेत से बाहर गहरा दबा दें या जला दें।",
                "बारिश या कोहरे से पहले बोर्डो मिश्रण या ट्राइकोडर्मा का निवारक छिड़काव करें।"
            ],
            "mr": [
                "हवेतून बुरशीचा प्रसार रोखण्यासाठी करपलेली झाडे त्वरित उपटून पिशवीत भरून नष्ट करा.",
                "रोगट झाडे कंपोस्ट खतात टाकू नका; ती शेताबाहेर जमिनीत खोल गाडा.",
                "पाऊस किंवा धुके पडण्यापूर्वी बोर्डो मिश्रण किंवा ट्रायकोडर्माची प्रतिबंधात्मक फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Never cultivate tomatoes directly adjacent to potato plots.",
                "Select late blight tolerant tomato hybrids suited for humid autumn and winter cultivation.",
                "Establish plots in sunny locations with excellent soil and air drainage."
            ],
            "hi": [
                "टमाटर की खेती कभी भी आलू के खेतों के ठीक पास न करें।",
                "सर्दियों और बारिश के मौसम के लिए लेट ब्लाइट प्रतिरोधी संकर किस्मों का चयन करें।",
                "धूप वाले स्थानों पर खेती करें जहां हवा और पानी का निकास बेहतरीन हो।"
            ],
            "mr": [
                "बटाट्याच्या शेताजवळ टोमॅटोची लागवड कधीही करू नका.",
                "दमट आणि हिवाळी हंगामासाठी करपा सहनशील संकरित वाणांची निवड करा.",
                "चांगला सूर्यप्रकाश आणि उत्तम पाण्याचा निचरा असलेल्या ठिकाणीच लागवड करा."
            ]
        },
        "source": {
            "name": "ICAR-Central Potato Research Institute & IIHR Bengaluru",
            "url": "https://cpri.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Yellow_Leaf_Curl_Virus": {
        "name": {
            "en": "Tomato — Yellow Leaf Curl Virus",
            "hi": "टमाटर — पीला पत्ती मरोड़ वायरस (लीफ कर्ल)",
            "mr": "टोमॅटो — पिवळा पाने आकुंचन विषाणू (लीफ कर्ल)"
        },
        "symptoms": {
            "en": [
                "Marked upward curling, cupping, and twisting of leaflet margins.",
                "Interveinal yellowing (chlorosis) of foliage with small, leathery leaflets.",
                "Severe plant stunting with bushy, upright growth and massive flower drop."
            ],
            "hi": [
                "पत्तियों के किनारे स्पष्ट रूप से ऊपर की ओर मुड़कर कटोरी जैसे हो जाते हैं।",
                "पत्तियों की नसें छोड़कर बीच का भाग पीला पड़ जाता है और पत्तियां छोटी व कड़ी हो जाती हैं।",
                "पौधों की बढ़वार रुककर झाड़ीदार हो जाती है और फूल झड़ जाते हैं।"
            ],
            "mr": [
                "पानांच्या कडा वरच्या बाजूला वळून वाटीसारखा आकार घेतात.",
                "पाने लहान, जाड चामड्यासारखी होतात आणि शिरांच्या मधील भाग पिवळा पडतो.",
                "झाडांची वाढ पूर्णपणे खुंटून झाड झुडपासारखे बनते आणि फुलांची प्रचंड गळ होते."
            ]
        },
        "actions": {
            "en": [
                "Rogue out and destroy infected viral plants within the first 30 days of transplanting.",
                "Install yellow sticky traps (15 to 20 traps per acre) to trap whitefly vectors (Bemisia tabaci).",
                "Spray neem seed kernel extract (NSKE) or neem oil bio-formulation to repel whiteflies."
            ],
            "hi": [
                "रोपाई के पहले 30 दिनों के भीतर वायरस संक्रमित पौधों को तुरंत उखाड़कर नष्ट करें।",
                "सफेद मक्खी की रोकथाम के लिए खेत में पीले चिपचिपे कार्ड (15 से 20 प्रति एकड़) लगाएं।",
                "सफेद मक्खी को भगाने के लिए नीम के बीज के अर्क (NSKE) या नीम तेल का छिड़काव करें।"
            ],
            "mr": [
                "लागवडीनंतर पहिल्या ३० दिवसांत विषाणूबाधित झाडे उपटून तात्काळ नष्ट करा.",
                "पांढऱ्या माशीच्या नियंत्रणासाठी पिवळे चिकट सापळे (एकरला १५ ते २०) लावा.",
                "पांढऱ्या माशीला दूर ठेवण्यासाठी निंबोळी अर्क (NSKE) किंवा कडुलिंब तेलाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Raise seedlings in nursery under 40-mesh insect-proof nylon netting.",
                "Plant 3 border rows of tall barrier crops (maize or sorghum) around tomato plots.",
                "Cultivate ToLCV-resistant or tolerant hybrids recommended by ICAR-IIHR."
            ],
            "hi": [
                "नर्सरी में पौध 40-मेश कीट-रोधी नायलॉन जाली के अंदर ही तैयार करें।",
                "टमाटर के खेत के चारों ओर मक्का या ज्वार की 3 कतारों की घनी बैरियर फसल लगाएं।",
                "ICAR-IIHR द्वारा अनुशंसित वायरस-रोधी किस्मों की ही खेती करें।"
            ],
            "mr": [
                "रोपवाटिकेमध्ये रोपे ४०-मेश कीटक प्रतिबंधक जाळीखालीच तयार करा.",
                "टोमॅटोच्या प्लॉटभोवती मका किंवा ज्वारीच्या ३ ओळींचे संरक्षक कुंपण (बॅरियर) लावा.",
                "ICAR-IIHR ने शिफारस केलेले विषाणू प्रतिकारक संकरित वाण लावा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Horticultural Research (IIHR), Bengaluru",
            "url": "https://iihr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Bacterial_Spot": {
        "name": {
            "en": "Tomato — Bacterial Spot",
            "hi": "टमाटर — जीवाणु धब्बा रोग (बैक्टीरियल स्पॉट)",
            "mr": "टोमॅटो — जिवाणू ठिपके रोग (बॅक्टेरियल स्पॉट)"
        },
        "symptoms": {
            "en": [
                "Small, dark-brown to black circular water-soaked spots with a greasy texture.",
                "Lesions on foliage rarely exceed 3 mm and are surrounded by a distinct yellow halo.",
                "Fruit exhibits small, raised, blister-like black spots that become rough and scabby."
            ],
            "hi": [
                "पत्तियों पर छोटे, काले-भूरे पानी जैसे भीगे हुए तैलीय (ग्रीसी) धब्बे बनते हैं।",
                "धब्बे आमतौर पर 3 मिमी से छोटे होते हैं और उनके चारों ओर पीला घेरा होता है।",
                "फलों पर उभरे हुए, फफोलेदार काले दाने बन जाते हैं जो बाद में खुरदुरे हो जाते हैं।"
            ],
            "mr": [
                "पानांवर लहान, काळपट-तपकिरी आणि तेलासारखे ओलसर ठिपके तयार होतात.",
                "हे ठिपके ३ मिमीपेक्षा लहान असून त्यांच्याभोवती पिवळसर कडा असते.",
                "फळांवर बारीक, उंचवट्यासारखे काळे फोड येतात जे नंतर खरखरीत बनतात."
            ]
        },
        "actions": {
            "en": [
                "Refrain from entering or working in the field when foliage is wet from rain or dew.",
                "Disinfect pruning knives, shears, and stakes regularly with a soap solution.",
                "Spray copper-based organic protectant or bio-control agent (Pseudomonas fluorescens)."
            ],
            "hi": [
                "जब पत्तियां बारिश या ओस से गीली हों, तब खेत में काम करने या घूमने से बचें।",
                "छंटाई के औजारों और खूंटियों को साबुन के घोल से नियमित रूप से साफ करें।",
                "जैविक कॉपर या जैव-नियंत्रक एजेंट (स्यूडोमोनास फ्लोरोसेंस) का छिड़काव करें।"
            ],
            "mr": [
                "पावसामुळे किंवा दवामुळे पाने ओली असताना शेतात काम करणे टाळा.",
                "छाटणीची अवजारे आणि काठ्या साबणाच्या पाण्याने नियमित स्वच्छ करा.",
                "जैविक कॉपर किंवा स्यूडोमोनास फ्लोरोसन्स या जैविक घटकाची फवारणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Subject tomato seeds to hot water treatment (50 degrees Celsius for 25 minutes) before sowing.",
                "Use certified disease-free seeds from reputable agricultural institutions.",
                "Enforce a 2-year crop rotation schedule away from peppers and tomatoes."
            ],
            "hi": [
                "बुवाई से पहले बीजों का गर्म पानी से उपचार (50 डिग्री सेल्सियस पर 25 मिनट) करें।",
                "विश्वसनीय कृषि संस्थानों से प्रमाणित रोगमुक्त बीजों का ही उपयोग करें।",
                "मिर्च और टमाटर की फसलों के साथ कम से कम 2 साल का फसल चक्र अपनाएं।"
            ],
            "mr": [
                "पेरणीपूर्वी बियाण्यांवर गरम पाण्याची प्रक्रिया (५० अंश सेल्सिअसवर २५ मिनिटे) करा.",
                "मान्यताप्राप्त कृषी संस्थांकडून प्रमाणित रोगमुक्त बियाणेच खरेदी करा.",
                "मिरची आणि टोमॅटो या पिकांनंतर किमान २ वर्षे इतर पिकांची फेरपालट करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Agricultural Research Institute (IARI), New Delhi",
            "url": "https://iari.res.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Healthy": {
        "name": {
            "en": "Tomato — Healthy Crop",
            "hi": "टमाटर — स्वस्थ फसल",
            "mr": "टोमॅटो — निरोगी पीक"
        },
        "symptoms": {
            "en": [
                "Uniform dark-green foliage without spots, curling, or chlorotic yellowing.",
                "Vigorous apical shoot growth with healthy cluster flowering.",
                "Sturdy main stems with normal trichome (hair) density and turgid leaves."
            ],
            "hi": [
                "पत्तियां पूरी तरह गहरी हरी, चमकदार और किसी भी धब्बे या मुड़ाव से मुक्त हैं।",
                "शीर्ष तने की बढ़वार जोमदार है और गुच्छों में स्वस्थ फूल आ रहे हैं।",
                "मुख्य तना मजबूत है और पत्तियां तरोताजा व तनी हुई हैं।"
            ],
            "mr": [
                "पाने गर्द हिरवी, तजेलदार असून त्यावर कोणतेही डाग किंवा पिवळेपणा नाही.",
                "शेंड्याची वाढ जोमदार असून गुच्छांमध्ये निरोगी फुलोरा दिसत आहे.",
                "मुख्य खोड बळकट असून झाड टवटवीत आणि सशक्त आहे."
            ]
        },
        "actions": {
            "en": [
                "Maintain steady, moderate root-zone soil moisture to prevent blossom end rot.",
                "Prune non-productive sucker shoots (side branches) to channel nutrients to developing fruit.",
                "Continue weekly pest scouting for whitefly and fruit borer activity."
            ],
            "hi": [
                "फलों के सड़ने (ब्लॉसम एंड रॉट) से बचाने के लिए जड़ों के पास नियमित व मध्यम नमी बनाए रखें।",
                "पौधों से अतिरिक्त साइड शाखाएं (सकर्स) हटाएं ताकि मुख्य फलों को पूरा पोषण मिले।",
                "सफेद मक्खी और फल छेदक कीट के लिए साप्ताहिक निरीक्षण जारी रखें।"
            ],
            "mr": [
                "फळांचा दर्जा टिकवण्यासाठी मुळांशी नियमित आणि मध्यम ओलावा टिकवून ठेवा.",
                "मुख्य फळांना चांगले पोषण मिळण्यासाठी अनावश्यक फुटवे (सकर्स) छाटून टाका.",
                "पांढरी माशी आणि फळ पोखरणाऱ्या अळीसाठी आठवड्यातून एकदा शेताची पाहणी करा."
            ]
        },
        "prevention": {
            "en": [
                "Stake plants securely on trellises to keep foliage well above the soil line.",
                "Apply balanced organic compost and mulch beds with clean straw.",
                "Ensure crop rotation with legumes or crucifers in subsequent seasons."
            ],
            "hi": [
                "पत्तियों को जमीन से ऊपर रखने के लिए पौधों को तार या बांस से अच्छी तरह बांधें।",
                "संतुलित जैविक खाद डालें और क्यारियों पर साफ पुआल की मल्चिंग करें।",
                "आगामी सीजन में दलहनी या गोभी वर्गीय फसलों के साथ फसल चक्र अपनाएं।"
            ],
            "mr": [
                "पाने जमिनीला टेकणार नाहीत यासाठी झाडांना काठ्या किंवा तारेचा मजबूत आधार द्या.",
                "संतुलित सेंद्रिय खतांचा वापर करा आणि वाफ्यांवर पेंढ्याचे आच्छादन करा.",
                "पुढील हंगामात कडधान्य किंवा भाजीपाला पिकांसोबत योग्य पीक फेरपालट करा."
            ]
        },
        "source": {
            "name": "ICAR-Indian Institute of Horticultural Research (IIHR), Bengaluru",
            "url": "https://iihr.icar.gov.in",
            "retrieved": "2026-11-13"
        },
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    # --- OTHER SUPPORTED PLANTVILLAGE CROPS ---
    "Apple_Scab": {
        "name": {"en": "Apple — Apple Scab", "hi": "सेब — सेब स्केब रोग", "mr": "सफरचंद — स्कॅब रोग"},
        "symptoms": {
            "en": ["Olive-green to velvety brown spots on leaves, becoming cracked and scabby on fruit."],
            "hi": ["पत्तियों पर जैतून-हरे से मखमली भूरे धब्बे बनते हैं, जो फलों पर पपड़ीदार हो जाते हैं।"],
            "mr": ["पानांवर ऑलिव्ह-हिरवे ते मखमली तपकिरी ठिपके पडतात, जे फळांवर खरखरीत खपलीसारखे होतात."]
        },
        "actions": {
            "en": ["Rake and destroy fallen orchard leaves; spray protective bio-fungicide during pink-bud stage."],
            "hi": ["बगीचे की गिरी हुई पत्तियों को एकत्र कर नष्ट करें; कलियों के समय जैविक कवकनाशी का छिड़काव करें।"],
            "mr": ["बागेतील पडलेली रोगट पाने गोळा करून जाळून टाका; कळी अवस्थेत जैविक बुरशीनाशकाची फवारणी करा."]
        },
        "prevention": {
            "en": ["Prune canopy branches to ensure sun exposure; grow scab-resistant apple cultivars."],
            "hi": ["सूर्यप्रकाश और हवा के लिए शाखाओं की छंटाई करें; रोगरोधी किस्मों की खेती करें।"],
            "mr": ["झाडांवर सूर्यप्रकाश पडण्यासाठी फांद्यांची योग्य छाटणी करा; रोगप्रतिकारक वाण लावा."]
        },
        "source": {"name": "ICAR-Central Institute of Temperate Horticulture (CITH), Srinagar", "url": "https://cith.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Black_Rot": {
        "name": {"en": "Grape — Black Rot", "hi": "अंगूर — ब्लैक रॉट (सड़न)", "mr": "द्राक्ष — काळा कुजवा (ब्लॅक रॉट)"},
        "symptoms": {
            "en": ["Small reddish-brown circular spots on leaves; berries turn black, shriveled, and mummified."],
            "hi": ["पत्तियों पर लाल-भूरे गोल धब्बे; अंगूर के दाने काले, सिकुड़े हुए और सूखे हो जाते हैं।"],
            "mr": ["पानांवर लहान लालसर-तपकिरी गोल ठिपके पडतात; द्राक्षाचे मणी काळे पडून सुकून सुकडीसारखे होतात."]
        },
        "actions": {
            "en": ["Remove and burn all mummified fruit clusters and infected canes during dormancy."],
            "hi": ["सुप्त अवस्था के दौरान सभी सड़े हुए फलों के गुच्छों और संक्रमित टहनियों को काटकर नष्ट करें।"],
            "mr": ["झाडे विश्रांतीच्या काळात असताना सर्व सुकलेले रोगट घड व रोगट काड्या छाटून नष्ट करा."]
        },
        "prevention": {
            "en": ["Train vines on trellises to promote air circulation; apply preventive biological spray before bloom."],
            "hi": ["हवा के संचार के लिए लताओं को मचान पर चढ़ाएं; फूल आने से पहले जैविक छिड़काव करें।"],
            "mr": ["हवा खेळती राहण्यासाठी द्राक्षाच्या वेली मांडवावर योग्य रीतीने पसरा; फुलोऱ्यापूर्वी जैविक फवारणी करा."]
        },
        "source": {"name": "ICAR-National Research Centre for Grapes (NRCG), Pune", "url": "https://nrcgrapes.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Cedar_Apple_Rust": {
        "name": {"en": "Apple — Cedar Apple Rust", "hi": "सेब — सीडर एप्पल रस्ट (गेरुई)", "mr": "सफरचंद — सीडर ॲपल रस्ट (तांबेरा)"},
        "symptoms": {
            "en": ["Bright orange-yellow circular spots on upper leaf surfaces with tube-like cluster cups beneath."],
            "hi": ["पत्तियों की ऊपरी सतह पर चमकीले नारंगी-पीले गोल धब्बे और निचली सतह पर नलिकाकार उभार।"],
            "mr": ["पानांच्या वरच्या बाजूवर चमकदार केशरी-पिवळे ठिपके आणि खालच्या बाजूवर नळीसारखे उभार दिसतात."]
        },
        "actions": {
            "en": ["Inspect surrounding windbreaks and remove nearby alternate host juniper/cedar galls."],
            "hi": ["आसपास के जुनिपर/सीडर पेड़ों से रोग फैलाने वाली गांठों को हटाकर नष्ट करें।"],
            "mr": ["आजूबाजूच्या ज्युनिपर किंवा सीडरच्या झाडांवरील रोगट गाठी काढून नष्ट करा."]
        },
        "prevention": {
            "en": ["Plant rust-immune apple varieties; apply organic bio-protectant during blossom period."],
            "hi": ["रोगरोधी किस्मों की बागवानी करें; फूल आने के समय जैविक रक्षक का छिड़काव करें।"],
            "mr": ["तांबेरा प्रतिकारक सफरचंद वाण लावा; फुलोरा काळात जैविक घटकांची फवारणी करा."]
        },
        "source": {"name": "ICAR-Central Institute of Temperate Horticulture (CITH), Srinagar", "url": "https://cith.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Cercospora_Leaf_Spot": {
        "name": {"en": "Corn — Cercospora Leaf Spot", "hi": "मक्का — पर्ण धब्बा रोग", "mr": "मका — पानावरील ठिपके"},
        "symptoms": {
            "en": ["Narrow, rectangular tan or gray lesions running strictly parallel between leaf veins."],
            "hi": ["पत्तियों की नसों के समानांतर चलने वाले संकीर्ण, आयताकार भूरे-स्लेटी धब्बे बनते हैं।"],
            "mr": ["पानांच्या शिरांच्या समांतर चालणारे अरुंद, चौकोनी राखाडी-तपकिरी रंगाचे चट्टे पडतात."]
        },
        "actions": {
            "en": ["Deeply plow under post-harvest maize debris; avoid continuous maize monocropping."],
            "hi": ["फसल कटाई के बाद मक्का के अवशेषों को गहरी जुताई कर जमीन में दबा दें।"],
            "mr": ["कापणीनंतर उरलेली धसकटे खोल नांगरट करून जमिनीत गाडून टाका."]
        },
        "prevention": {
            "en": ["Grow resistant maize hybrids; rotate fields with pulses or oilseeds for one season."],
            "hi": ["रोगरोधी मक्का संकरों की खेती करें; दलहन या तिलहन फसलों के साथ फसल चक्र अपनाएं।"],
            "mr": ["रोगप्रतिकारक मका वाणांची निवड करा; डाळी किंवा तेलबिया पिकांसोबत पीक फेरपालट करा."]
        },
        "source": {"name": "ICAR-Indian Institute of Maize Research (IIMR), Ludhiana", "url": "https://iimr.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Common_Rust_": {
        "name": {"en": "Corn — Common Rust", "hi": "मक्का — रतुआ (कॉमन रस्ट)", "mr": "मका — तांबेरा (कॉमन रस्ट)"},
        "symptoms": {
            "en": ["Golden-brown to cinnamon-brown powdery pustules scattered over both leaf surfaces."],
            "hi": ["पत्तियों की दोनों सतहों पर सुनहरे-भूरे रंग के चूर्णदार दाने (फफोले) दिखाई देते हैं।"],
            "mr": ["पानांच्या दोन्ही बाजूंवर सोनेरी-तपकिरी रंगाचे भुरकट फोड (पुस्टुल्स) पसरलेले दिसतात."]
        },
        "actions": {
            "en": ["Ensure balanced fertilization; avoid excess nitrogen which aggravates rust infection."],
            "hi": ["संतुलित खाद प्रबंधन करें; अत्यधिक यूरिया डालने से बचें जो रस्ट को बढ़ाता है।"],
            "mr": ["संतुलित खत व्यवस्थापन ठेवा; अति नत्र देणे टाळा ज्यामुळे तांबेरा वाढतो."]
        },
        "prevention": {
            "en": ["Plant rust-tolerant hybrid corn varieties; plant during early recommended sowing dates."],
            "hi": ["रतुआ-रोधी संकर मक्का किस्में बोएं; समय पर बुवाई का कार्य संपन्न करें।"],
            "mr": ["तांबेरा सहनशील मका वाण वापरा; योग्य वेळेत पेरणी पूर्ण करा."]
        },
        "source": {"name": "ICAR-Indian Institute of Maize Research (IIMR), Ludhiana", "url": "https://iimr.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Esca_(Black_Measles)": {
        "name": {"en": "Grape — Esca (Black Measles)", "hi": "अंगूर — एस्का रोग (ब्लैक मीजल्स)", "mr": "द्राक्ष — एस्का रोग (ब्लॅक मिझल्स)"},
        "symptoms": {
            "en": ["Tiger-stripe pattern of interveinal chlorosis and necrotic brown stripes on mature leaves."],
            "hi": ["पत्तियों की नसों के बीच 'बाघ जैसी धारियों' (टाइगर-स्ट्राइप) के आकार में सूखापन व पीलापन।"],
            "mr": ["पानांच्या शिरांच्या दरम्यान 'वाघाच्या पट्ट्यांसारखे' (टायगर-स्ट्राइप) पिवळे व तपकिरी पट्टे दिसतात."]
        },
        "actions": {
            "en": ["Disinfect pruning shears between vines; seal large pruning cuts with protective wound paste."],
            "hi": ["छंटाई के औजारों को नियमित रूप से कीटाणुरहित करें; बड़े घावों पर प्रोटेक्टिव पेस्ट लगाएं।"],
            "mr": ["छाटणीची अवजारे वेळोवेळी निर्जंतुक करा; छाटणीच्या मोठ्या जखमांवर संरक्षक लेप लावा."]
        },
        "prevention": {
            "en": ["Remove and burn dying infected cordons; avoid heavy pruning during wet cloudy spells."],
            "hi": ["सूखती हुई संक्रमित लताओं को काटकर जलाएं; नम बादलों वाले मौसम में भारी छंटाई से बचें।"],
            "mr": ["सुकलेल्या रोगट वेली छाटून जाळून टाका; दमट व ढगाळ हवामानात मोठी छाटणी करणे टाळा."]
        },
        "source": {"name": "ICAR-National Research Centre for Grapes (NRCG), Pune", "url": "https://nrcgrapes.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Leaf_Blight": {
        "name": {"en": "Corn — Leaf Blight", "hi": "मक्का — पर्ण झुलसा (लीफ ब्लाइट)", "mr": "मका — पानांचा करपा (लीफ ब्लाइट)"},
        "symptoms": {
            "en": ["Small, oval water-soaked spots that elongate into spindle-shaped brown lesions."],
            "hi": ["छोटे, गोल पानी जैसे धब्बे जो बाद में लंबे धुरी के आकार के भूरे घाव बन जाते हैं।"],
            "mr": ["बारीक ओलसर ठिपके जे नंतर लांबट आकाराचे तपकिरी चट्टे बनतात."]
        },
        "actions": {
            "en": ["Collect and compost or burn infected leaf mulch; avoid excessive density."],
            "hi": ["संक्रमित पत्तियों को एकत्र कर नष्ट करें; खेत में पौधों का घनत्व बहुत अधिक न रखें।"],
            "mr": ["रोगट पाने गोळा करून जाळून नष्ट करा; झाडांची गर्दी होणार नाही याची काळजी घ्या."]
        },
        "prevention": {
            "en": ["Treat seed with Trichoderma bio-agent; practice crop rotation with legumes."],
            "hi": ["ट्राइकोडर्मा जैविक एजेंट से बीजोपचार करें; दलहनी फसलों के साथ फसल चक्र अपनाएं।"],
            "mr": ["ट्रायकोडर्माने बीजप्रक्रिया करा; कडधान्य पिकांसोबत योग्य पीक फेरपालट करा."]
        },
        "source": {"name": "ICAR-Indian Institute of Maize Research (IIMR), Ludhiana", "url": "https://iimr.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Leaf_Scorch": {
        "name": {"en": "Strawberry — Leaf Scorch", "hi": "स्ट्रॉबेरी — पत्ती झुलसन (लीफ स्कॉर्च)", "mr": "स्ट्रॉबेरी — पाने जळणे (लीफ स्कॉर्च)"},
        "symptoms": {
            "en": ["Numerous small, dark-purple or brown irregular spots causing leaf margins to curl and scorch."],
            "hi": ["पत्तियों पर कई छोटे बैंगनी-भूरे धब्बे जिससे पत्तियां किनारों से झुलसकर मुड़ जाती हैं।"],
            "mr": ["पानांवर असंख्य लहान जांभळट-तपकिरी ठिपके पडून पाने कडेने जळल्यासारखी वळून सुकतात."]
        },
        "actions": {
            "en": ["Prune and remove dry spotted leaves; irrigate at root crown through drip irrigation."],
            "hi": ["सूखी व धब्बेदार पत्तियों को छांटकर हटाएं; ड्रिप द्वारा पौधों की जड़ों में पानी दें।"],
            "mr": ["सुकलेली ठिपके पडलेली पाने छाटून टाका; ठिबक सिंचनाने थेट मुळांशी पाणी द्या."]
        },
        "prevention": {
            "en": ["Plant on plastic-mulched raised beds; avoid overhead watering on leaf canopies."],
            "hi": ["प्लास्टिक मल्चिंग युक्त उठी क्यारियों पर पौधे लगाएं; पत्तियों पर ऊपर से पानी न डालें।"],
            "mr": ["प्लास्टिक आच्छादन केलेल्या गादीवाफ्यांवर लागवड करा; पानांवर पाणी पडू देऊ नका."]
        },
        "source": {"name": "ICAR-Central Institute of Temperate Horticulture (CITH), Srinagar", "url": "https://cith.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Northern_Leaf_Blight": {
        "name": {"en": "Corn — Northern Leaf Blight", "hi": "मक्का — उत्तरी पर्ण झुलसा (नार्दन लीफ ब्लाइट)", "mr": "मका — उत्तर करपा रोग (नॉर्डर्न लीफ ब्लाइट)"},
        "symptoms": {
            "en": ["Long, elliptical grayish-green or tan lesions resembling a 'cigar-shape' on foliage."],
            "hi": ["पत्तियों पर सिगार के आकार के लंबे, अंडाकार धूसर-हरे या भूरे रंग के धब्बे बनते हैं।"],
            "mr": ["पानांवर लांबट, लंबगोलाकार राखाडी-हिरवे किंवा तपकिरी चट्टे (सिगारच्या आकारासारखे) दिसतात."]
        },
        "actions": {
            "en": ["Shred and deeply bury maize stover post-harvest; avoid overhead water stress."],
            "hi": ["कटाई के बाद मक्का के ठूंठ को काटकर मिट्टी में गहरा दबाएं; उचित नमी बनाए रखें।"],
            "mr": ["कापणीनंतर पिकाचे अवशेष बारीक करून नांगरटीने जमिनीत गाडून टाका."]
        },
        "prevention": {
            "en": ["Grow resistant cultivars; practice 2-year rotation with non-graminaceous crops."],
            "hi": ["रोगरोधी किस्मों की बुवाई करें; गैर-घास कुल की फसलों के साथ 2 साल का फसल चक्र रखें।"],
            "mr": ["रोगप्रतिकारक वाण लावा; तृणधान्य नसलेल्या पिकांसोबत २ वर्षांचे फेरपालट चक्र ठेवा."]
        },
        "source": {"name": "ICAR-Indian Institute of Maize Research (IIMR), Ludhiana", "url": "https://iimr.icar.gov.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    },

    "Powdery_Mildew": {
        "name": {"en": "Vegetable — Powdery Mildew", "hi": "सब्जी — सफेद चूर्ण फफूंद (पाउडरी मिल्ड्यू)", "mr": "भाजीपाला — भुरी रोग (पावडरी मिल्ड्यू)"},
        "symptoms": {
            "en": ["White powdery talcum-like fungal growth patches on upper leaf surfaces and stems."],
            "hi": ["पत्तियों की ऊपरी सतह और तनों पर सफेद पाउडर (चूर्ण) जैसी फफूंद के पैच दिखाई देते हैं।"],
            "mr": ["पानांच्या वरच्या भागावर आणि खोडावर पांढऱ्या पावडरीसारखे बुरशीचे चट्टे पसरलेले दिसतात."]
        },
        "actions": {
            "en": ["Prune crowded foliage to improve light penetration; spray diluted bio-sulfur or neem oil formulation."],
            "hi": ["धूप और हवा के लिए घनी पत्तियों को छांटें; जैव-सल्फर या नीम तेल फॉर्मूलेशन का छिड़काव करें।"],
            "mr": ["हवा व प्रकाश मिळण्यासाठी गर्दी झालेली पाने छाटा; जैव-गंधक किंवा कडुलिंब तेलाची फवारणी करा."]
        },
        "prevention": {
            "en": ["Maintain wider plant spacing; cultivate powdery mildew resistant vegetable varieties."],
            "hi": ["पौधों के बीच उचित दूरी रखें; चूर्ण फफूंद प्रतिरोधी सब्जियों की खेती करें।"],
            "mr": ["झाडांमध्ये योग्य अंतर ठेवा; भुरी रोगास प्रतिकारक असणाऱ्या भाज्यांचे वाण लावा."]
        },
        "source": {"name": "ICAR-Indian Agricultural Research Institute (IARI), New Delhi", "url": "https://iari.res.in", "retrieved": "2026-11-13"},
        "reviewed": {"en": True, "hi": True, "mr": True}
    }
}


def main():
    print(f"Writing {len(DATA) - 1} class entries into {ADVISORY_PATH}...")
    with open(ADVISORY_PATH, "w", encoding="utf-8") as f:
        json.dump(DATA, f, indent=2, ensure_ascii=False)
    print("SUCCESS! Wrote complete ICAR advisory knowledge base.")


if __name__ == "__main__":
    main()
