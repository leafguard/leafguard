"""Generate the official LeafGuard Srujan 2026 AI-05 PowerPoint Presentation (PPTX)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="docs/LeafGuard_Srujan2026_AI-05.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank layout

    # Palette
    c_bg = RGBColor(9, 26, 17)          # #091a11 deep forest
    c_card = RGBColor(17, 41, 29)       # #11291d dark emerald
    c_border = RGBColor(31, 69, 50)     # #1f4532
    c_primary = RGBColor(34, 197, 94)   # #22c55e emerald
    c_accent = RGBColor(74, 222, 128)   # #4ade80 light green
    c_white = RGBColor(240, 253, 244)   # #f0fdf4
    c_dim = RGBColor(148, 163, 184)     # #94a3b8 slate
    c_yellow = RGBColor(250, 204, 21)   # #facc15 amber
    c_quote_bg = RGBColor(28, 48, 32)   # dark quote background

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_bg
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text):
        # Badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8), Inches(0.4))
        tf = badge_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = badge_text.upper()
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_primary

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(9.5), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(10), Inches(0.4))
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = subtitle_text
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = c_dim

        # Logo on top right
        logo_path = "static/logo-cropped.png"
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(10.5), Inches(0.55), height=Inches(0.7))

    def add_card(slide, left, top, width, height, title=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = c_card
        card.line.color.rgb = c_border
        card.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = c_accent
        return card

    def add_footer(slide, left_text, right_text):
        fb = slide.shapes.add_textbox(Inches(0.8), Inches(6.85), Inches(6.0), Inches(0.35))
        p = fb.text_frame.paragraphs[0]
        p.text = left_text
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = c_dim

        fb_r = slide.shapes.add_textbox(Inches(7.2), Inches(6.85), Inches(5.3), Inches(0.35))
        p_r = fb_r.text_frame.paragraphs[0]
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.text = right_text
        p_r.font.name = "Arial"
        p_r.font.size = Pt(10)
        p_r.font.bold = True
        p_r.font.color.rgb = c_primary

    # =========================================================================
    # SLIDE 1: Problem Statement & Innovation
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    add_header(s1, "Srujan 2026 • Track T1 • Problem ID: AI-05",
               "LeafGuard: Edge AI Crop Health & ICAR Advisory",
               "Instant, CPU-first disease identification & verified cultural guidance for smallholder farmers")

    # Quote Box (Exact Problem Statement)
    q_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.05), Inches(5.7), Inches(2.0))
    q_box.fill.solid()
    q_box.fill.fore_color.rgb = c_quote_bg
    q_box.line.color.rgb = c_yellow
    q_box.line.width = Pt(2)
    q_tf = q_box.text_frame
    q_tf.word_wrap = True
    q_p1 = q_tf.paragraphs[0]
    q_p1.text = "\"Farmers often struggle to identify visible crop diseases at an early stage, which can lead to severe crop damage and financial losses.\n\nThe Task: Build an application that analyzes plant-leaf photographs, identifies likely diseases, and provides basic advisory guidelines sourced from an approved information source.\""
    q_p1.font.name = "Arial"
    q_p1.font.size = Pt(10.5)
    q_p1.font.italic = True
    q_p1.font.color.rgb = RGBColor(254, 240, 138)

    # Targeted Crops Card (Bottom Left)
    add_card(s1, Inches(0.8), Inches(4.2), Inches(5.7), Inches(2.45), "🎯 Targeted Regional Crops (27 Conditions)")
    tc_box = s1.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(5.3), Inches(1.85))
    tc_tf = tc_box.text_frame
    tc_tf.word_wrap = True
    crops = [
        "• Cotton (कापूस): Bacterial Blight, Leaf Curl Virus, Fusarium Wilt, Healthy",
        "• Turmeric (हळद): Leaf Blotch, Leaf Spot, Dry Leaf / Wilting, Healthy",
        "• Soybean (सोयाबीन): Septoria Brown Spot, Frogeye Leaf Spot, Mosaic Virus",
        "• Vegetables: Tomato (Early/Late Blight, Septoria, Curl Virus), Potato, Corn"
    ]
    for idx, c in enumerate(crops):
        p = tc_tf.paragraphs[0] if idx == 0 else tc_tf.add_paragraph()
        p.text = c
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = c_white

    # Right Card: Core Uniqueness
    add_card(s1, Inches(6.8), Inches(2.05), Inches(5.7), Inches(4.6), "💡 Our Core Uniqueness & Architecture")
    u_box = s1.shapes.add_textbox(Inches(7.05), Inches(2.65), Inches(5.2), Inches(3.8))
    u_tf = u_box.text_frame
    u_tf.word_wrap = True
    uniques = [
        ("Zero Chemical Hallucination: ", "Strictly uses official ICAR/KVK-verified cultural and bio-management protocols. Never generates or guesses synthetic chemical pesticides or doses with LLMs."),
        ("100% CPU Serving (~18 ms): ", "Quantized MobileNetV3-Large ONNX runtime executes in ~18ms on a single basic CPU core without expensive cloud GPU dependencies."),
        ("Zero-Friction Access & Privacy: ", "No login or password barrier. 100% stateless architecture; farmer photos are analyzed in-memory and NEVER stored on the server."),
        ("Trilingual Audio Player: ", "Integrated Web Speech audio player (Play / Pause / Stop) narrating verified guidance in English, Hindi, and Marathi for rural accessibility.")
    ]
    for idx, (title, desc) in enumerate(uniques):
        p = u_tf.paragraphs[0] if idx == 0 else u_tf.add_paragraph()
        p.space_after = Pt(10)
        run_b = p.add_run()
        run_b.text = title
        run_b.font.bold = True
        run_b.font.color.rgb = c_accent
        run_b.font.size = Pt(11)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = c_white
        run_d.font.size = Pt(10.5)

    add_footer(s1, "LeafGuard Technical Presentation • Srujan 2026", "Live App: https://leafguard-03zw.onrender.com")

    # =========================================================================
    # SLIDE 2: Technical Architecture & Pipeline
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "End-to-End System Pipeline",
               "Engineering Pipeline: From Field Photo to Action",
               "Designed specifically for rural connectivity constraints (2G/3G mobile networks)")

    # Left: 5 Pipeline Steps
    steps = [
        ("1. Client-Side Canvas Optimization (Browser)", "Resizes 48MP mobile photos down to 640px JPEG (~90 KB) in <50ms, saving rural 2G/3G data bandwidth."),
        ("2. Quality & Security Guardrails (FastAPI)", "EXIF orientation correction + Laplacian blur score (<40.0 -> Blurry Warning) + 50MP decompress cap."),
        ("3. Bayesian Crop Gating (Mismatch Filter)", "Prevents false confidence: rejects mismatched leaves (e.g. soybean under tomato) to 'unrecognised'."),
        ("4. Lightweight ONNX CPU Engine (16.4 MB)", "Operator-fused C++ runtime executes inference in ~18 ms with zero PyTorch serving bloat."),
        ("5. Verified ICAR Advisory & Audio Player", "Looks up exact cultural/biological practices in EN, HI, MR with interactive speech read-aloud.")
    ]
    for idx, (stitle, sdesc) in enumerate(steps):
        top_pos = Inches(2.05 + idx * 0.92)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_pos, Inches(5.7), Inches(0.82))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card
        box.line.color.rgb = c_border
        box.line.width = Pt(1)

        # Number circle
        num = s2.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.95), top_pos + Inches(0.18), Inches(0.45), Inches(0.45))
        num.fill.solid()
        num.fill.fore_color.rgb = c_primary
        num.line.fill.background()
        np = num.text_frame.paragraphs[0]
        np.text = str(idx + 1)
        np.font.bold = True
        np.font.size = Pt(13)
        np.font.color.rgb = RGBColor(0, 0, 0)
        np.alignment = PP_ALIGN.CENTER

        # Text
        tb = s2.shapes.add_textbox(Inches(1.5), top_pos + Inches(0.08), Inches(4.85), Inches(0.68))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = stitle
        p1.font.bold = True
        p1.font.size = Pt(11)
        p1.font.color.rgb = c_white
        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = c_dim

    # Right: Defensive UX & Safeguards
    add_card(s2, Inches(6.8), Inches(2.05), Inches(5.7), Inches(4.6), "🛡️ Critical UX & Algorithmic Defenses")
    rg_box = s2.shapes.add_textbox(Inches(7.05), Inches(2.65), Inches(5.2), Inches(3.8))
    rg_tf = rg_box.text_frame
    rg_tf.word_wrap = True
    defenses = [
        ("Three Actionable Status Bands:", "• Confident (>=40%): Clear symptoms; primary management displayed.\n• Uncertain (20–40%): Top-3 differential shown; caution to cross-check.\n• Unrecognised (<20%): Advice omitted; guided daylight retake."),
        ("Tactile Laser Scanning Animation:", "Pure CSS GPU-composited laser sweep with reticle brackets runs for a minimum of 1.2s to instill diagnostic confidence without battery drain."),
        ("Client-Side Offline History:", "Stores past 10 scans securely in browser localStorage. Farmers can review past advisories in zero-connectivity field zones.")
    ]
    for idx, (title, desc) in enumerate(defenses):
        p = rg_tf.paragraphs[0] if idx == 0 else rg_tf.add_paragraph()
        p.space_after = Pt(12)
        run_b = p.add_run()
        run_b.text = title + "\n"
        run_b.font.bold = True
        run_b.font.color.rgb = c_accent
        run_b.font.size = Pt(11)
        run_d = p.add_run()
        run_d.text = desc
        run_d.font.color.rgb = c_white
        run_d.font.size = Pt(10)

    add_footer(s2, "FastAPI (Python 3.11) • ONNX Runtime (CPU) • Vanilla Web Stack", "Slide 2 of 4")

    # =========================================================================
    # SLIDE 3: Empirical Validation & Confusion Matrix
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Empirical Results & Diagnostics",
               "Model Evaluation & Biological Failure Analysis",
               "Honest, measured metrics and deep domain insights from 6,842 test evaluations")

    # Left: Confusion Matrix Image
    cm_path = "docs/evidence/confusion_matrix.jpg"
    if os.path.exists(cm_path):
        # Frame
        cm_frame = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.05), Inches(5.7), Inches(4.6))
        cm_frame.fill.solid()
        cm_frame.fill.fore_color.rgb = RGBColor(255, 255, 255)
        cm_frame.line.color.rgb = c_border
        s3.shapes.add_picture(cm_path, Inches(0.9), Inches(2.15), width=Inches(5.5))

    # Right Top: Verified Metrics Table
    add_card(s3, Inches(6.8), Inches(2.05), Inches(5.7), Inches(2.7), "📊 Verified Performance (Zero Simulated Data)")
    m_box = s3.shapes.add_textbox(Inches(7.0), Inches(2.55), Inches(5.3), Inches(2.1))
    m_tf = m_box.text_frame
    metrics = [
        ("Laboratory Top-1 Accuracy: ", "98.85% (6,763 / 6,842 images)"),
        ("Top-3 Differential Accuracy: ", "100.00% (target in top-3)"),
        ("Macro F1 Score: ", "0.9669 (unweighted average)"),
        ("PyTorch vs ONNX Parity: ", "4.53e-06 (max absolute diff)"),
        ("Serving CPU Latency: ", "18.25 ms (Mean, single core)"),
        ("Model Size on Disk: ", "16.43 MB (Quantized ONNX)")
    ]
    for idx, (mname, mval) in enumerate(metrics):
        p = m_tf.paragraphs[0] if idx == 0 else m_tf.add_paragraph()
        run_n = p.add_run()
        run_n.text = mname
        run_n.font.size = Pt(10.5)
        run_n.font.color.rgb = c_white
        run_v = p.add_run()
        run_v.text = mval
        run_v.font.bold = True
        run_v.font.size = Pt(10.5)
        run_v.font.color.rgb = c_yellow

    # Right Bottom: Failure Analysis Insights
    add_card(s3, Inches(6.8), Inches(4.9), Inches(5.7), Inches(1.75), "🔬 Explainable Confusion Insights")
    fa_box = s3.shapes.add_textbox(Inches(7.0), Inches(5.35), Inches(5.3), Inches(1.2))
    fa_tf = fa_box.text_frame
    fa_tf.word_wrap = True
    fa_points = [
        "• Corn Blight Overlap: Northern Leaf Blight and Cercospora both form linear parallel lesions; captured in 100% of cases by our Top-3 display.",
        "• Soybean Complex: Early Septoria brown spots mimic early Frogeye lesions; solved by unified ICAR vector traps and rogueing advice."
    ]
    for idx, pt in enumerate(fa_points):
        p = fa_tf.paragraphs[0] if idx == 0 else fa_tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_white

    add_footer(s3, "Evaluated across 6,842 unseen test images • Full Confusion Matrix Proven", "Slide 3 of 4")

    # =========================================================================
    # SLIDE 4: Real-World Impact & Production Readiness
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Production Deployment & Impact",
               "Real-World Viability, Scalability & Roadmap",
               "Built for practical deployment by state agricultural cooperatives, KVKs, and farmers")

    # 3 Equal Cards Layout
    card_w = Inches(3.64)
    gap = Inches(0.4)
    c1_left = Inches(0.8)
    c2_left = c1_left + card_w + gap
    c3_left = c2_left + card_w + gap
    c_top = Inches(2.05)
    c_h = Inches(4.6)

    # Card 1: Scalability & Cost
    add_card(s4, c1_left, c_top, card_w, c_h, "🚀 Scalability & Cost")
    c1_box = s4.shapes.add_textbox(c1_left + Inches(0.2), c_top + Inches(0.6), card_w - Inches(0.4), Inches(3.8))
    c1_tf = c1_box.text_frame
    c1_tf.word_wrap = True
    c1_items = [
        ("100% Stateless: ", "Scales horizontally behind basic round-robin load balancers with linear cost efficiency."),
        ("Zero Cloud GPU Expenses: ", "Operates on standard $5/month CPU VPS instances handling ~180,000 requests/hour per core."),
        ("Zero SMS Transaction Fees: ", "Eliminating mandatory login OTPs saves ~₹0.20 per scan, eliminating operational burn.")
    ]
    for idx, (title, desc) in enumerate(c1_items):
        p = c1_tf.paragraphs[0] if idx == 0 else c1_tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.color.rgb = c_accent
        r1.font.size = Pt(10.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = c_white
        r2.font.size = Pt(9.5)

    # Card 2: Inclusive Farmer UX
    add_card(s4, c2_left, c_top, card_w, c_h, "🌱 Inclusive Farmer UX")
    c2_box = s4.shapes.add_textbox(c2_left + Inches(0.2), c_top + Inches(0.6), card_w - Inches(0.4), Inches(3.8))
    c2_tf = c2_box.text_frame
    c2_tf.word_wrap = True
    c2_items = [
        ("Trilingual Speech Narration: ", "Overcomes literacy barriers with native Marathi, Hindi, and English voice synthesis."),
        ("PWA Installability: ", "Add to Home Screen directly from Chrome without downloading heavy 50MB Play Store APKs."),
        ("Offline Safe History: ", "In-browser local history lets farmers review past advisories in areas with zero network connectivity.")
    ]
    for idx, (title, desc) in enumerate(c2_items):
        p = c2_tf.paragraphs[0] if idx == 0 else c2_tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.color.rgb = c_accent
        r1.font.size = Pt(10.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = c_white
        r2.font.size = Pt(9.5)

    # Card 3: Phase 2 Roadmap
    add_card(s4, c3_left, c_top, card_w, c_h, "🔮 Phase 2 Roadmap")
    c3_box = s4.shapes.add_textbox(c3_left + Inches(0.2), c_top + Inches(0.6), card_w - Inches(0.4), Inches(3.8))
    c3_tf = c3_box.text_frame
    c3_tf.word_wrap = True
    c3_items = [
        ("In-Browser ONNX Web: ", "Complete on-device inference via WebAssembly/WebGPU for zero-signal farm zones."),
        ("Progressive Authentication: ", "Optional phone login strictly for farmers requesting multi-year yield tracking or live KVK agronomist consultation."),
        ("Agromet Weather Feeds: ", "Integration of district-level IMD weather alerts for predictive disease risk forecasting.")
    ]
    for idx, (title, desc) in enumerate(c3_items):
        p = c3_tf.paragraphs[0] if idx == 0 else c3_tf.add_paragraph()
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = title
        r1.font.bold = True
        r1.font.color.rgb = c_accent
        r1.font.size = Pt(10.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = c_white
        r2.font.size = Pt(9.5)

    add_footer(s4, "Live Production URL: https://leafguard-03zw.onrender.com", "GitHub Repository Verified • MIT Licensed")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_presentation()
