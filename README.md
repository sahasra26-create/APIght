# 🔥 BizForge — GenAI-Powered Branding Suite

> **Team:** APIght | **Challenge:** BrandCraft · Generative AI Branding Automation

BizForge is a full-stack AI branding automation platform. Give it your business idea — it gives you a complete brand identity in under 3 minutes.

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
