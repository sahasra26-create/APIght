# 🔥 BizForge — GenAI-Powered Branding Suite

> **Team:** APIght | **Challenge:** BrandCraft · Generative AI Branding Automation

BizForge is a full-stack AI branding automation platform. Give it your business idea — it gives you a complete brand identity in under 3 minutes.

---

## 🚀 Quick Start (5 Steps)

### Step 1 — Get API Keys (FREE)

| Key | Where to Get |
|-----|-------------|
| `GROQ_API_KEY` | https://console.groq.com/keys |
| `HF_API_KEY` | https://huggingface.co/settings/tokens |

### Step 2 — Clone & Navigate
```bash
cd bizforge
```

### Step 3 — Set Up Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 5 — Configure & Run
```bash
# 1. Copy the env template
cp .env.example .env

# 2. Edit .env with your keys:
#    GROQ_API_KEY=gsk_...
#    HF_API_KEY=hf_...

# 3. Start the server
python main.py
```

### ✅ Open http://localhost:8000

---

## 🌟 Features

| Feature | Model Used | Endpoint |
|---------|-----------|---------|
| Brand Name Generator | Groq LLaMA-3.3-70B | `POST /api/generate-brand` |
| Logo Concept Generator | Groq LLaMA-3.3-70B | `POST /api/generate-logo` |
| Logo Image (SDXL) | Stable Diffusion XL | `POST /api/generate-logo-image` |
| Marketing Content | Groq LLaMA-3.3-70B | `POST /api/generate-content` |
| Design System / Colors | Groq LLaMA-3.3-70B | `POST /api/get-colors` |
| Sentiment Analyzer | Groq LLaMA-3.3-70B | `POST /api/analyze-sentiment` |
| Branding Chatbot | IBM Granite (HF) | `POST /api/chat` |

---

## 📁 Project Structure

```
bizforge/
├── backend/
│   ├── main.py           ← FastAPI app + all routes
│   ├── ai_services.py    ← All AI integrations (Groq, IBM, SDXL)
│   ├── requirements.txt  ← Python dependencies
│   └── .env.example      ← API key template
├── frontend/
│   ├── index.html        ← Landing page
│   ├── branding.html     ← Main app (all 6 tools)
│   └── static/
│       └── generated_logos/  ← SDXL-generated images saved here
├── setup.sh              ← One-command setup (Mac/Linux)
└── README.md
```

---

## 🏗️ Architecture

```
User Browser
     │
     ▼
HTML/CSS/JS Frontend (index.html + branding.html)
     │
     ▼
FastAPI Backend (main.py) — localhost:8000
     │
     ├── /api/generate-brand  ──► Groq Cloud (LLaMA-3.3-70B-Versatile)
     ├── /api/generate-logo   ──► Groq Cloud (LLaMA-3.3-70B-Versatile)
     ├── /api/generate-logo-image ► HuggingFace (SDXL)
     ├── /api/generate-content ──► Groq Cloud (LLaMA-3.3-70B-Versatile)
     ├── /api/get-colors      ──► Groq Cloud (LLaMA-3.3-70B-Versatile)
     ├── /api/analyze-sentiment ► Groq Cloud (LLaMA-3.3-70B-Versatile)
     └── /api/chat            ──► IBM Granite 4.0 (HuggingFace)
                                   (falls back to Groq if Granite unavailable)
```

---

## 🧪 API Test with curl

```bash
# Test Brand Name Generator
curl -X POST http://localhost:8000/api/generate-brand \
  -H "Content-Type: application/json" \
  -d '{"keywords":"smart AI startup","industry":"Technology","tone":"Professional","language":"en"}'

# Test Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What makes a strong brand name?"}'
```

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `GROQ_API_KEY not set` | Edit `backend/.env` and add your key |
| IBM Granite slow to load | It downloads on first run (~700MB). Be patient! |
| SDXL returns error | Model may be loading (cold start). Try again in 30s. |
| Port 8000 in use | Change port in `main.py`: `uvicorn.run(app, port=8001)` |
| Frontend not loading | Make sure you're at `http://localhost:8000` not opening the HTML file directly |

---

## 📖 API Reference

All endpoints accept/return JSON.

### `POST /api/generate-brand`
```json
{ "keywords": "str", "industry": "str", "tone": "str", "language": "en" }
```

### `POST /api/generate-content`
```json
{ "brand_description": "str", "tone": "str", "content_type": "product_description|social_post|email|ad_copy|tagline", "language": "en" }
```

### `POST /api/analyze-sentiment`
```json
{ "text": "str", "brand_tone": "str" }
```

### `POST /api/get-colors`
```json
{ "tone": "str", "industry": "str" }
```

### `POST /api/generate-logo`
```json
{ "brand_name": "str", "industry": "str", "keywords": "str" }
```

### `POST /api/generate-logo-image`
```json
{ "prompt": "str" }
```

### `POST /api/chat`
```json
{ "message": "str" }
```

---

## 🛠️ Tech Stack

- **FastAPI** — Python web framework
- **Uvicorn** — ASGI server
- **Groq SDK** — LLaMA-3.3-70B API client
- **HuggingFace Transformers** — IBM Granite model
- **Requests** — SDXL Inference API calls
- **Pillow** — Image processing
- **python-dotenv** — Environment variable management

---

*Built for SmartBridge × SkillWallet Hackathon 2025*
