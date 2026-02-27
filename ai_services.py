"""
InKraft AI Services
Integrates: Groq (LLaMA-3.3-70B) · IBM Granite (HuggingFace) · Stable Diffusion XL
"""

import os
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HF_API_KEY   = os.getenv("HF_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
IBM_MODEL    = os.getenv("IBM_MODEL", "ibm-granite/granite-4.0-h-350m")

# ── Groq client ──────────────────────────────────────────────────────────────
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅  Groq LLaMA client loaded!")
    except Exception as e:
        print(f"⚠️   Groq load failed: {e}")
else:
    print("⚠️   GROQ_API_KEY not set in .env — using mock responses")

# ── IBM Granite (HuggingFace pipeline) ───────────────────────────────────────
granite_pipeline = None
if HF_API_KEY:
    try:
        from transformers import pipeline as hf_pipeline
        granite_pipeline = hf_pipeline(
            "text-generation",
            model=IBM_MODEL,
            token=HF_API_KEY,
            max_new_tokens=256,
            device_map="auto",
        )
        print("✅  IBM Granite pipeline loaded!")
    except Exception as e:
        print(f"⚠️   Granite load failed: {e}")
else:
    print("⚠️   HF_API_KEY not set — chatbot will use Groq fallback")

# ── SDXL via HuggingFace Inference API ───────────────────────────────────────
SDXL_URL =  "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"


# ─────────────────── Helper ──────────────────────────────────────────────────

def _groq(prompt: str, system: str = "You are InKraft, an expert AI branding assistant.", max_tokens: int = 512) -> str:
    if not groq_client:
        return _mock_response(prompt)
    resp = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.8,
        top_p=0.95,
    )
    return resp.choices[0].message.content.strip()


def _mock_response(prompt: str) -> str:
    """Fallback when no API keys are set — useful for UI testing."""
    return (
        "⚠️  API key not configured. Add GROQ_API_KEY to your .env file.\n\n"
        "Example .env:\n"
        "  GROQ_API_KEY=gsk_...\n"
        "  HF_API_KEY=hf_...\n\n"
        f"Your prompt was: {prompt[:80]}..."
    )


# ─────────────────── Feature Functions ───────────────────────────────────────

async def generate_brand_names(keywords: str, industry: str, tone: str, language: str) -> str:
    system = (
        "You are InKraft, a world-class brand strategist. "
        "Generate creative, memorable, and brand-ready business names. "
        "Each name must be unique, easy to spell, and suitable for trademark registration."
    )
    prompt = (
        f"Generate 10 creative brand names for a {industry} business.\n"
        f"Keywords: {keywords}\n"
        f"Tone/Style: {tone}\n"
        f"Language: {language}\n\n"
        "For each name provide:\n"
        "1. The name (bold)\n"
        "2. A one-line tagline\n"
        "3. Why it works (one sentence)\n\n"
        "Format as a numbered list."
    )
    return await asyncio.to_thread(_groq, prompt, system, 600)


async def generate_marketing_content(description: str, tone: str, content_type: str, language: str) -> str:
    type_map = {
        "product_description": "a compelling product description",
        "social_post":         "an engaging social media post (Instagram/LinkedIn)",
        "email":               "a professional marketing email",
        "ad_copy":             "punchy ad copy (headline + body)",
        "tagline":             "5 memorable taglines/slogans",
    }
    ctype = type_map.get(content_type, "marketing content")
    system = "You are InKraft, an expert copywriter and brand voice specialist."
    prompt = (
        f"Write {ctype} for the following brand:\n\n"
        f"Brand Description: {description}\n"
        f"Tone: {tone}\n"
        f"Language: {language}\n\n"
        "Make it professional, engaging, and on-brand."
    )
    return await asyncio.to_thread(_groq, prompt, system, 500)


async def analyze_sentiment(text: str, brand_tone: str) -> str:
    system = "You are InKraft, a brand analytics and sentiment analysis expert."
    prompt = (
        f"Analyze this customer review and provide:\n"
        f"1. Overall Sentiment: Positive / Neutral / Negative\n"
        f"2. Confidence Score: X/10\n"
        f"3. Key Emotional Signals\n"
        f"4. Brand Tone Alignment (vs target tone: {brand_tone})\n"
        f"5. Suggest changes with respect to the review\n"
        f"6. Generate a reply to improve brand image based on the harshness of the review\n\n"
        f"Review:\n{text}"
    )
    return await asyncio.to_thread(_groq, prompt, system, 400)


async def get_color_palette(tone: str, industry: str) -> str:
    system = "You are InKraft, a brand identity designer and color theory expert."
    prompt = (
        f"Suggest a professional brand color palette for:\n"
        f"Industry: {industry}\n"
        f"Tone/Vibe: {tone}\n\n"
        "Provide:\n"
        "1. Primary Color — HEX code + name + psychology\n"
        "2. Secondary Color — HEX code + name + psychology\n"
        "3. Accent Color — HEX code + name + psychology\n"
        "4. Background Color — HEX code\n"
        "5. Text Color — HEX code\n"
        "6. Recommended Font Pairing (Google Fonts)\n"
        "7. Overall Brand Mood (2-3 sentences)\n\n"
        "Be specific with HEX codes."
    )
    return await asyncio.to_thread(_groq, prompt, system, 400)


async def chat_with_ai(message: str) -> str:
    # Prefer Granite if loaded, else fall back to Groq
    if granite_pipeline:
        try:
            result = await asyncio.to_thread(
                granite_pipeline,
                f"You are InKraft, an expert branding assistant. User: {message}\nAssistant:"
            )
            return result[0]["generated_text"].split("Assistant:")[-1].strip()
        except Exception:
            pass  # fall through to Groq
    system = (
        "You are InKraft, an expert AI branding consultant. "
        "Give concise, actionable, expert branding advice. "
        "Be warm, professional, and inspiring."
    )
    return await asyncio.to_thread(_groq, message, system, 350)


async def generate_logo_prompt(brand_name: str, industry: str, keywords: str) -> str:
    system = "You are InKraft, a professional logo designer and visual branding expert."
    prompt = (
        f"Create a detailed, professional logo prompt for:\n"
        f"Brand Name: {brand_name}\n"
        f"Industry: {industry}\n"
        f"Keywords: {keywords}\n\n"
        "Provide:\n"
        "1. Logo Concept Description (what it looks like)\n"
        "2. Style (minimalist/geometric/illustrative/etc.)\n"
        "3. Color Palette suggestion\n"
        "4. SDXL/DALL-E Generation Prompt (ready to use)\n"
        "5. Usage Tips\n\n"
        "Make the SDXL prompt highly detailed and professional."
    )
    return await asyncio.to_thread(_groq, prompt, system, 450)


async def generate_logo_image(logo_prompt: str) -> dict:
    """Call HuggingFace SDXL Inference API and save image."""
    if not HF_API_KEY:
        return {
            "image_url": None,
            "success": False,
            "error": "HF_API_KEY not set. Add it to .env to enable image generation.",
        }
    try:
        import requests as req
        enhanced = (
            f"Professional brand logo: {logo_prompt}. "
            "Modern minimalist vector design, clean lines, transparent background, "
            "high resolution, professional branding, 4K quality."
        )
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": enhanced}
        resp = req.post(SDXL_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            logos_dir = Path(__file__).parent.parent / "frontend/static/generated_logos"
            logos_dir.mkdir(parents=True, exist_ok=True)
            filename = f"logo_{int(time.time())}.png"
            filepath = logos_dir / filename
            with open(filepath, "wb") as f:
                f.write(resp.content)
            return {
                "image_url": f"/static/generated_logos/{filename}",
                "success": True,
                "error": None,
            }
        else:
            return {"image_url": None, "success": False, "error": f"SDXL API error: {resp.status_code}"}
    except Exception as e:
        return {"image_url": None, "success": False, "error": str(e)}
