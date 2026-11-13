// LeafGuard Client Application (Vanilla JS, Phone-First)
(() => {
  "use strict";

  // --- 1. Multilingual UI Strings Dictionary (EN, HI, MR) ---
  const STRINGS = {
    en: {
      tagline: "Scan a crop leaf to identify diseases with official ICAR advice.",
      cropLabel: "Filter by Crop (Optional):",
      cropAll: "🌱 Auto-Detect (All Crops)",
      cropCotton: "☁️ Cotton (कापूस / कपास)",
      cropTurmeric: "🟡 Turmeric (हळद / हल्दी)",
      cropSoybean: "🫘 Soybean (सोयाबीन)",
      cropTomato: "🍅 Tomato & Vegetables",
      takePhoto: "Take Photo",
      chooseGallery: "Choose from Gallery",
      scanNow: "Diagnose Leaf",
      processing: "Analyzing leaf patterns on CPU...",
      tipsTitle: "💡 Tips for Best Accuracy:",
      tip1: "Take photo in clear daylight (avoid flash glare).",
      tip2: "Hold phone steady and close to the infected leaf area.",
      tip3: "Avoid shadows, fingers, and background clutter.",
      blurNotice: "Photo appears blurry. If result seems incorrect, retake in better light.",
      confidence: "Confidence:",
      listenAdvice: "Listen Advisory",
      listening: "Playing Audio...",
      top3Title: "Top Differential Possibilities:",
      unrecognisedMsg: "We could not identify this disease with certainty. Please photograph a close-up of a supported crop leaf (Cotton, Soybean, Turmeric, Tomato) in clear daylight.",
      symptoms: "Symptoms to verify",
      actions: "What to do now (Immediate Action)",
      prevention: "Prevention for next season",
      sourceLabel: "Source:",
      scanAnother: "Scan Another Leaf",
      historyTitle: "Recent Scans",
      clearHistory: "Clear",
      historyNote: "Stored only on your phone's browser. Photos are not saved on the server.",
      emptyHistory: "No previous scans found.",
      aboutTitle: "About LeafGuard",
      aboutDesc: "LeafGuard is an edge-optimized agricultural diagnostic assistant built for smallholder farmers. It runs high-speed MobileNetV3 inference directly on low-cost CPU instances without cloud GPU dependencies.",
      supportedCrops: "Supported Crops (27 Diseases):",
      modelPerformance: "Empirical Model Performance:",
      safetyPolicy: "Safety & Advisory Policy:",
      safetyText: "LeafGuard never auto-generates or guesses chemical pesticide dosages. All management practices are compiled from Indian Council of Agricultural Research (ICAR) and Krishi Vigyan Kendra (KVK) bulletins. Always confirm with an agronomist before spraying.",
      navScan: "Scan",
      navHistory: "History",
      navAbout: "About",
      errOversize: "Image file is too large (must be under 8 MB).",
      errSmall: "Image is too small or blurry. Please take a clear close-up.",
      errInvalid: "Invalid image format. Please select a JPG or PNG photo.",
      errNetwork: "Network connection lost. Please check mobile data.",
      statusConfident: "Confident",
      statusUncertain: "Uncertain",
      statusUnrecognised: "Unrecognised",
    },
    hi: {
      tagline: "फसल की पत्ती को स्कैन करें और आधिकारिक ICAR सलाह प्राप्त करें।",
      cropLabel: "फसल चुनें (वैकल्पिक):",
      cropAll: "🌱 स्वतः पहचानें (सभी फसलें)",
      cropCotton: "☁️ कपास (Cotton)",
      cropTurmeric: "🟡 हल्दी (Turmeric)",
      cropSoybean: "🫘 सोयाबीन (Soybean)",
      cropTomato: "🍅 टमाटर व सब्जियां",
      takePhoto: "फोटो खींचें",
      chooseGallery: "गैलरी से चुनें",
      scanNow: "रोग की जांच करें",
      processing: "पत्ती के लक्षणों का विश्लेषण हो रहा है...",
      tipsTitle: "💡 सही पहचान के लिए सुझाव:",
      tip1: "दिन की प्राकृतिक धूप में साफ फोटो लें (फ्लैश से बचें)।",
      tip2: "मोबाइल को स्थिर रखें और रोगग्रस्त पत्ती के करीब ले जाएं।",
      tip3: "फोटो में छाया, अंगुलियां या अन्य कचरा न आने दें।",
      blurNotice: "फोटो धुंधली लग रही है। अच्छी रोशनी में दोबारा फोटो लें।",
      confidence: "विश्वसनीयता:",
      listenAdvice: "सलाह सुनें",
      listening: "सलाह पढ़ रहे हैं...",
      top3Title: "शीर्ष संभावित रोग:",
      unrecognisedMsg: "रोग की पुष्टि विश्वास के साथ नहीं हो सकी। कृपया कपास, सोयाबीन, हल्दी या टमाटर की पत्ती की साफ फोटो लें।",
      symptoms: "रोग के लक्षण",
      actions: "तुरंत क्या उपाय करें",
      prevention: "अगली फसल के लिए रोकथाम",
      sourceLabel: "स्रोत:",
      scanAnother: "अन्य पत्ती स्कैन करें",
      historyTitle: "हालिया स्कैन",
      clearHistory: "हटाएं",
      historyNote: "यह जानकारी केवल आपके फोन में सुरक्षित है। सर्वर पर फोटो सेव नहीं होती।",
      emptyHistory: "कोई पुराना स्कैन उपलब्ध नहीं है।",
      aboutTitle: "लीफगार्ड (LeafGuard) के बारे में",
      aboutDesc: "लीफगार्ड छोटे और सीमांत किसानों के लिए बनाया गया AI सलाहकार है। यह बिना महंगे इंटरनेट या GPU के तुरंत रोग पहचान करता है।",
      supportedCrops: "सपोर्टेड फसलें (27 रोग):",
      modelPerformance: "मॉडल की सटीकता:",
      safetyPolicy: "सुरक्षा एवं सलाह नीति:",
      safetyText: "लीफगार्ड कभी भी मनगढ़ंत रासायनिक दवाएं या खुराक नहीं बताता। सभी सलाह ICAR और कृषि विज्ञान केंद्र (KVK) से प्रमाणित हैं।",
      navScan: "स्कैन",
      navHistory: "इतिहास",
      navAbout: "जानकारी",
      errOversize: "फोटो 8 MB से बड़ी है।",
      errSmall: "फोटो बहुत छोटी या धुंधली है।",
      errInvalid: "अमान्य फोटो। कृपया JPG या PNG फोटो चुनें।",
      errNetwork: "इंटरनेट कनेक्शन नहीं मिल रहा है।",
      statusConfident: "सटीक परिणाम",
      statusUncertain: "अनिश्चित",
      statusUnrecognised: "पहचान नहीं हुई",
    },
    mr: {
      tagline: "पिकाच्या पानाचा फोटो काढून ICAR प्रमाणित मार्गदर्शन मिळवा.",
      cropLabel: "पीक निवडा (पर्यायी):",
      cropAll: "🌱 आपोआप ओळखा (सर्व पिके)",
      cropCotton: "☁️ कापूस (Cotton)",
      cropTurmeric: "🟡 हळद (Turmeric)",
      cropSoybean: "🫘 सोयाबीन (Soybean)",
      cropTomato: "🍅 टोमॅटो व भाज्या",
      takePhoto: "फोटो काढा",
      chooseGallery: "गॅलरीतून निवडा",
      scanNow: "रोग निदान करा",
      processing: "पानावरील रोगाचे विश्लेषण सुरू आहे...",
      tipsTitle: "💡 अचूक निदानासाठी टिप्स:",
      tip1: "दिवसाच्या उजेडात स्पष्ट फोटो काढा (फ्लॅश टाळा).",
      tip2: "फोन स्थिर धरून बाधित पानाजवळ नेऊन फोटो घ्या.",
      tip3: "फोटोत सावली, बोटे किंवा इतर कचरा येऊ देऊ नका.",
      blurNotice: "फोटो अस्पष्ट (धुसर) दिसत आहे. चांगल्या प्रकाशात पुन्हा फोटो घ्या.",
      confidence: "विश्वासार्हता:",
      listenAdvice: "सल्ला ऐका",
      listening: "सल्ला वाचत आहे...",
      top3Title: "संभाव्य रोग यादी:",
      unrecognisedMsg: "रोगाची खात्रीशीर ओळख पटू शकली नाही. कृपया कापूस, सोयाबीन, हळद किंवा टोमॅटोच्या पानाचा जवळून स्पष्ट फोटो काढा.",
      symptoms: "रोगाची लक्षणे",
      actions: "आत्ता काय उपाययोजना करावी",
      prevention: "पुढील हंगामासाठी प्रतिबंध",
      sourceLabel: "संदर्भ स्रोत:",
      scanAnother: "दुसरे पान तपासा",
      historyTitle: "मागील तपासण्या",
      clearHistory: "हटवा",
      historyNote: "ही माहिती फक्त तुमच्या मोबाईलमध्ये साठवली जाते. फोटो सेव्ह केले जात नाहीत.",
      emptyHistory: "मागील नोंदी आढळल्या नाहीत.",
      aboutTitle: "लीफगार्ड (LeafGuard) बद्दल",
      aboutDesc: "लीफगार्ड हे शेतकऱ्यांसाठी तयार केलेले AI साधन आहे. हे कमी वेळेत आणि कमी खर्चात अचूक रोग निदान करते.",
      supportedCrops: "समाविष्ट पिके (२७ रोग प्रकार):",
      modelPerformance: "मॉडेल अचूकता:",
      safetyPolicy: "सुरक्षितता व सल्ला नियम:",
      safetyText: "लीफगार्ड रासायनिक औषधांचे प्रमाण मनाने सुचवत नाही. सर्व उपाययोजना ICAR आणि KVK शास्त्रज्ञांच्या मार्गदर्शनावर आधारित आहेत.",
      navScan: "तपासा",
      navHistory: "नोंदी",
      navAbout: "माहिती",
      errOversize: "फोटो फाइल 8 MB पेक्षा मोठी आहे.",
      errSmall: "फोटो खूप लहान किंवा अस्पष्ट आहे.",
      errInvalid: "अवैध फोटो स्वरूप. कृपया योग्य फोटो निवडा.",
      errNetwork: "इंटरनेट संपर्कात अडचण येत आहे.",
      statusConfident: "निश्चित निदान",
      statusUncertain: "अनिश्चित",
      statusUnrecognised: "ओळख पटली नाही",
    }
  };

  // --- 2. State Management ---
  let currentLang = localStorage.getItem("leafguard_lang") || "en";
  let currentFileBlob = null;
  let lastPredictionData = null;

  // DOM Elements
  const cameraInput = document.getElementById("cameraInput");
  const galleryInput = document.getElementById("galleryInput");
  const cameraBtn = document.getElementById("cameraBtn");
  const galleryBtn = document.getElementById("galleryBtn");
  const scanBtn = document.getElementById("scanBtn");
  const scanAnotherBtn = document.getElementById("scanAnotherBtn");
  const cropSelect = document.getElementById("cropSelect");
  const imagePreviewContainer = document.getElementById("imagePreviewContainer");
  const imagePreview = document.getElementById("imagePreview");
  const loadingIndicator = document.getElementById("loadingIndicator");
  const errorBanner = document.getElementById("errorBanner");
  const voiceBtn = document.getElementById("voiceBtn");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");

  // --- 3. Language Switching & UI Translation ---
  function setLanguage(lang) {
    if (!STRINGS[lang]) lang = "en";
    currentLang = lang;
    localStorage.setItem("leafguard_lang", lang);

    document.querySelectorAll(".lang-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.lang === lang);
    });

    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.dataset.i18n;
      if (STRINGS[lang][key]) {
        el.textContent = STRINGS[lang][key];
      }
    });

    if (lastPredictionData) {
      renderResult(lastPredictionData);
    }
    renderHistory();
  }

  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.addEventListener("click", () => setLanguage(btn.dataset.lang));
  });

  // --- 4. Navigation (Screens: Home, Result, History, About) ---
  function showScreen(screenId) {
    document.querySelectorAll(".screen").forEach(s => s.classList.add("hidden"));
    const target = document.getElementById(screenId);
    if (target) target.classList.remove("hidden");

    document.querySelectorAll(".nav-item").forEach(item => {
      item.classList.toggle("active", item.dataset.target === screenId);
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      const target = item.dataset.target;
      if (target === "screen-history") renderHistory();
      showScreen(target);
    });
  });

  // --- 5. Image Compression & Canvas Resize (Max 640px, JPEG 0.85) ---
  async function processAndCompressImage(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          const maxDim = 640;
          let w = img.width;
          let h = img.height;

          if (w > maxDim || h > maxDim) {
            if (w > h) {
              h = Math.round((h * maxDim) / w);
              w = maxDim;
            } else {
              w = Math.round((w * maxDim) / h);
              h = maxDim;
            }
          }

          const canvas = document.createElement("canvas");
          canvas.width = w;
          canvas.height = h;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, w, h);

          canvas.toBlob((blob) => {
            resolve({ blob, dataUrl: canvas.toDataURL("image/jpeg", 0.85) });
          }, "image/jpeg", 0.85);
        };
        img.onerror = reject;
        img.src = e.target.result;
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  function handleFileSelected(file) {
    if (!file) return;
    errorBanner.classList.add("hidden");

    processAndCompressImage(file).then(({ blob, dataUrl }) => {
      currentFileBlob = blob;
      imagePreview.src = dataUrl;
      imagePreviewContainer.classList.remove("hidden");
      scanBtn.scrollIntoView({ behavior: "smooth" });
    }).catch(() => {
      showError(STRINGS[currentLang].errInvalid);
    });
  }

  cameraBtn.addEventListener("click", () => cameraInput.click());
  galleryBtn.addEventListener("click", () => galleryInput.click());
  cameraInput.addEventListener("change", (e) => handleFileSelected(e.target.files[0]));
  galleryInput.addEventListener("change", (e) => handleFileSelected(e.target.files[0]));

  function showError(msg) {
    errorBanner.textContent = msg;
    errorBanner.classList.remove("hidden");
  }

  // --- 6. Upload & Predict Flow ---
  scanBtn.addEventListener("click", async () => {
    if (!currentFileBlob) return;

    scanBtn.disabled = true;
    loadingIndicator.classList.remove("hidden");
    errorBanner.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", currentFileBlob, "leaf.jpg");
    formData.append("lang", currentLang);

    try {
      const res = await fetch("/predict", { method: "POST", body: formData });
      const data = await res.json();

      if (!res.ok) {
        if (res.status === 413) showError(STRINGS[currentLang].errOversize);
        else if (res.status === 400) showError(data.detail || STRINGS[currentLang].errSmall);
        else showError(data.detail || STRINGS[currentLang].errInvalid);
        return;
      }

      // Crop mapping for targeted filtering
      const CROP_CLASS_MAP = {
        cotton: ["cotton"],
        turmeric: ["turmeric"],
        soybean: ["soybean", "soyabean"],
        tomato: ["bacterial_spot", "early_blight", "late_blight", "septoria_leaf_spot", "yellow_leaf_curl_virus", "healthy", "leaf_mold"],
      };

      // Apply crop filter if selected
      const selectedCrop = cropSelect.value;
      if (selectedCrop !== "all" && data.top && data.top.length > 0 && CROP_CLASS_MAP[selectedCrop]) {
        const keywords = CROP_CLASS_MAP[selectedCrop];
        const isMatch = (item) => keywords.some(k => item.label.toLowerCase().includes(k));
        
        const matching = data.top.filter(isMatch);
        const nonMatching = data.top.filter(item => !isMatch(item));
        
        if (matching.length > 0) {
          data.top = matching.concat(nonMatching);
        }
      }

      lastPredictionData = data;
      renderResult(data);
      saveToHistory(data);
      showScreen("screen-result");

    } catch (err) {
      showError(STRINGS[currentLang].errNetwork);
    } finally {
      scanBtn.disabled = false;
      loadingIndicator.classList.add("hidden");
    }
  });

  scanAnotherBtn.addEventListener("click", () => {
    currentFileBlob = null;
    imagePreviewContainer.classList.add("hidden");
    cameraInput.value = "";
    galleryInput.value = "";
    showScreen("screen-home");
  });

  // --- 7. Result Rendering ---
  function renderResult(data) {
    const isUnrec = data.status === "unrecognised";
    const topItem = data.top && data.top[0] ? data.top[0] : null;

    // Photo preview
    document.getElementById("resultPhoto").src = imagePreview.src;

    // Status Badge
    const badge = document.getElementById("statusBadge");
    badge.className = `status-badge status-${data.status}`;
    const statusTextKey = data.status === "confident" ? "statusConfident" : (data.status === "uncertain" ? "statusUncertain" : "statusUnrecognised");
    badge.textContent = STRINGS[currentLang][statusTextKey];

    // Blur Warning
    document.getElementById("blurWarning").classList.toggle("hidden", !data.blurry);

    // Disease Title
    const titleEl = document.getElementById("diseaseTitle");
    titleEl.textContent = topItem ? topItem.name : "Leaf Scan";

    // Confidence Progress Bar
    const prob = topItem ? Math.round(topItem.prob * 100) : 0;
    document.getElementById("confidenceValue").textContent = `${prob}%`;
    const bar = document.getElementById("confidenceBar");
    bar.style.width = `${prob}%`;
    bar.style.backgroundColor = data.status === "confident" ? "var(--primary)" : (data.status === "uncertain" ? "var(--badge-uncertain)" : "var(--badge-unrecognised)");

    // Top 3 List
    const top3List = document.getElementById("top3List");
    top3List.innerHTML = "";
    if (data.top) {
      data.top.slice(0, 3).forEach((item) => {
        const li = document.createElement("li");
        li.className = "top3-item";
        li.innerHTML = `<span>${item.name}</span><strong>${Math.round(item.prob * 100)}%</strong>`;
        top3List.appendChild(li);
      });
    }

    // Toggle Advisory vs Unrecognised Notice
    const advSection = document.getElementById("advisorySection");
    const unrecCard = document.getElementById("unrecognisedCard");
    const voiceActionWrap = document.querySelector(".voice-action-wrap");

    if (isUnrec) {
      advSection.classList.add("hidden");
      unrecCard.classList.remove("hidden");
      voiceActionWrap.classList.add("hidden");
    } else {
      advSection.classList.remove("hidden");
      unrecCard.classList.add("hidden");
      voiceActionWrap.classList.remove("hidden");

      const adv = data.advice || {};
      const formatList = (arr) => (Array.isArray(arr) ? `<ul>${arr.map(i => `<li>${i}</li>`).join("")}</ul>` : `<p>${arr || ""}</p>`);

      document.getElementById("symptomsContent").innerHTML = formatList(adv.symptoms);
      document.getElementById("actionsContent").innerHTML = formatList(adv.actions);
      document.getElementById("preventionContent").innerHTML = formatList(adv.prevention);

      const src = adv.source || {};
      const srcLink = document.getElementById("sourceLink");
      srcLink.textContent = src.name || "ICAR Extension Advisory";
      srcLink.href = src.url || "https://icar.org.in";

      document.getElementById("disclaimerText").textContent = adv.disclaimer || "";
    }
  }

  // --- 8. Voice Read-Aloud (speechSynthesis) ---
  voiceBtn.addEventListener("click", () => {
    if (!("speechSynthesis" in window)) {
      alert("Text-to-speech is not supported on this browser.");
      return;
    }

    window.speechSynthesis.cancel();
    if (!lastPredictionData || !lastPredictionData.advice) return;

    const adv = lastPredictionData.advice;
    const actionsText = Array.isArray(adv.actions) ? adv.actions.join(". ") : adv.actions;
    const spokenText = `${adv.title}. ${actionsText}`;

    const utter = new SpeechSynthesisUtterance(spokenText);
    utter.rate = 0.95;

    // Map language to speech locale
    const voiceLangMap = { en: "en-IN", hi: "hi-IN", mr: "mr-IN" };
    utter.lang = voiceLangMap[currentLang] || "en-IN";

    const voices = window.speechSynthesis.getVoices();
    const match = voices.find(v => v.lang.startsWith(utter.lang) || v.lang.startsWith(currentLang));
    if (match) utter.voice = match;

    voiceBtn.textContent = STRINGS[currentLang].listening;
    utter.onend = () => {
      voiceBtn.innerHTML = `<span class="btn-icon" aria-hidden="true">🔊</span> <span>${STRINGS[currentLang].listenAdvice}</span>`;
    };
    utter.onerror = () => {
      voiceBtn.innerHTML = `<span class="btn-icon" aria-hidden="true">🔊</span> <span>${STRINGS[currentLang].listenAdvice}</span>`;
    };

    window.speechSynthesis.speak(utter);
  });

  // --- 9. Local Scan History (localStorage) ---
  function saveToHistory(data) {
    try {
      const history = JSON.parse(localStorage.getItem("leafguard_history") || "[]");
      const topItem = data.top && data.top[0] ? data.top[0] : { name: "Unknown" };
      const entry = {
        name: topItem.name,
        status: data.status,
        prob: Math.round((topItem.prob || 0) * 100),
        date: new Date().toLocaleDateString(),
      };
      history.unshift(entry);
      if (history.length > 10) history.pop();
      localStorage.setItem("leafguard_history", JSON.stringify(history));
    } catch (_) {}
  }

  function renderHistory() {
    const list = document.getElementById("historyList");
    const emptyMsg = document.getElementById("emptyHistoryMsg");
    list.innerHTML = "";

    try {
      const history = JSON.parse(localStorage.getItem("leafguard_history") || "[]");
      if (history.length === 0) {
        emptyMsg.classList.remove("hidden");
        return;
      }
      emptyMsg.classList.add("hidden");

      history.forEach(item => {
        const li = document.createElement("li");
        li.className = "history-item";
        li.innerHTML = `
          <div>
            <strong>${item.name}</strong>
            <div style="font-size:0.75rem; color:var(--text-muted);">${item.date}</div>
          </div>
          <div>
            <span class="status-badge status-${item.status}">${item.prob}%</span>
          </div>
        `;
        list.appendChild(li);
      });
    } catch (_) {
      emptyMsg.classList.remove("hidden");
    }
  }

  clearHistoryBtn.addEventListener("click", () => {
    localStorage.removeItem("leafguard_history");
    renderHistory();
  });

  // --- 10. Initialization ---
  setLanguage(currentLang);
})();
