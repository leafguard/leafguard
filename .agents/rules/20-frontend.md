---
activation: model_decision
description: Use when editing files under static/ (HTML, CSS, JS, manifest)
---
# Frontend rules

- Plain HTML, CSS and vanilla JS. No frameworks, bundlers or npm packages. One `app.js` unless it passes 300 lines.
- Phone first: tap targets of 44 px or more, high contrast, short text, icons beside labels, works at 360 px width.
- Camera: `<input type="file" accept="image/*" capture="environment">`. No getUserMedia (needs HTTPS).
- Before upload, shrink with canvas to a max side of 640 px, JPEG quality 0.85, using `createImageBitmap(file, {imageOrientation:"from-image"})`.
- All UI strings live in ONE object keyed by language (`en`, `hi`, `mr`). Never hard-code text inside handlers.
- Load Noto Sans Devanagari from Google Fonts with a fallback font stack.
- Voice: `speechSynthesis` with `lang` `en-IN|hi-IN|mr-IN`. Check `getVoices()`; hide the button or show a tip when no voice matches. Never assume a Marathi voice exists.
- Status UI has three states shown with TEXT as well as colour: confident, uncertain, unrecognised. Show top-3 with a confidence bar, the source link and the disclaimer on every result.
- History: last 10 scans in localStorage only, wrapped in try/catch.
- Errors in plain language ("Photo is too blurry. Try again in daylight."). Always show a spinner while waiting.
- Accessibility basics: labelled buttons, alt text, visible focus, usable with large fonts.
- No secrets, API keys or college branding in static files.
