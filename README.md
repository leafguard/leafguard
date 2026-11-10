---
title: LeafGuard
emoji: 🌿
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# 🌿 LeafGuard

**LeafGuard** is a lightweight, mobile-first crop disease identification web application designed for smallholder farmers. A user captures or uploads a leaf photo; the application analyzes it and returns the top three predicted conditions, a confidence status, and concise, sourced advisory actions in English, Hindi, or Marathi.

## Privacy Statement
**Photos are not stored.** All image analysis occurs in memory during request execution. The service is strictly stateless; no uploaded photos or user data are saved to disk or any database.

## Status
*Status: work in progress (Milestone 0 - Walking Skeleton)*

## Running Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. **Run tests:**
   ```bash
   pytest tests/ -q
   ```
