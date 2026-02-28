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
SDXL_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

# ─────────────────── Language Mapping ────────────────────────────────────────
# Full names give the model a much clearer instruction than raw codes like "en"
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
}

def resolve_language(code: str) -> str:
    """Convert a language code to the full name the LLM understands best."""
    return LANGUAGE_NAMES.get(code.lower().strip(), code)


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
    lang = resolve_language(language)
    system = (
        "You are InKraft, a world-class brand strategist. "
        "Generate creative, memorable, and brand-ready business names. "
        "Each name must be unique, easy to spell, and suitable for trademark registration. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every single word — names, taglines, explanations — must be in {lang}."
    )
    prompt = (
        f"Generate 10 creative brand names for a {industry} business.\n"
        f"Keywords that must inspire the names: {keywords}\n"
        f"Tone/Style: {tone}\n\n"
        "For each name provide:\n"
        "1. The brand name\n"
        "2. A one-line tagline that reflects the tone\n"
        "3. Why it works for this specific industry and keyword set (one sentence)\n\n"
        "Format as a numbered list. Be specific — each name must feel tailored to "
        f"the '{industry}' industry with a '{tone}' personality."
    )
    result = await asyncio.to_thread(_groq, prompt, system, 700)
    return result.replace("*", "")


async def generate_marketing_content(description: str, tone: str, content_type: str, language: str) -> str:
    lang = resolve_language(language)
    type_map = {
        "product_description": "a compelling product description",
        "social_post":         "an engaging social media post (Instagram/LinkedIn)",
        "email":               "a professional marketing email with subject line",
        "ad_copy":             "punchy ad copy with a headline and body",
        "tagline":             "5 memorable taglines/slogans",
    }
    ctype = type_map.get(content_type, "marketing content")
    system = (
        "You are InKraft, an expert copywriter and brand voice specialist. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every single word must be in {lang}."
    )
    prompt = (
        f"Write {ctype} for the following brand:\n\n"
        f"Brand Description: {description}\n"
        f"Tone: {tone}\n\n"
        "Rules:\n"
        "- Speak directly to the target audience described above\n"
        "- Use the exact tone specified — do not default to generic corporate language\n"
        "- Reference specific details from the brand description, not generic filler\n"
        "- Make it professional, engaging, and on-brand."
    )
    return await asyncio.to_thread(_groq, prompt, system, 600)


async def analyze_sentiment(text: str, brand_tone: str, language: str = "en") -> str:
    lang = resolve_language(language)
    system = (
        "You are InKraft, a brand analytics and sentiment analysis expert. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every single word must be in {lang}."
    )
    prompt = (
        f"Analyze this customer review and provide:\n"
        f"1. Overall Sentiment: Positive / Neutral / Negative\n"
        f"2. Confidence Score: X/10\n"
        f"3. Key Emotional Signals (list the specific words/phrases that reveal emotion)\n"
        f"4. Brand Tone Alignment — does this review suggest the brand is achieving its "
        f"   target tone of '{brand_tone}'? Why or why not?\n"
        f"5. Suggested Improvements — what should the brand change based on this feedback?\n"
        f"6. Suggested Brand Reply — write a reply that addresses the review and improves "
        f"   brand image (match the reply warmth to the harshness of the review)\n\n"
        f"Review:\n{text}"
    )
    result = await asyncio.to_thread(_groq, prompt, system, 500)
    return result.replace("*", "")


async def get_color_palette(tone: str, industry: str, language: str = "en") -> str:
    lang = resolve_language(language)
    system = (
        "You are InKraft, a brand identity designer and color theory expert. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every word of description must be in {lang}. HEX codes are universal — keep them as-is."
    )
    prompt = (
        f"Suggest a professional brand color palette for:\n"
        f"Industry: {industry}\n"
        f"Tone/Vibe: {tone}\n\n"
        "Provide:\n"
        "1. Primary Color — HEX code + color name + psychological effect on this specific audience\n"
        "2. Secondary Color — HEX code + color name + psychological effect\n"
        "3. Accent Color — HEX code + color name + when to use it\n"
        "4. Background Color — HEX code + rationale\n"
        "5. Text Color — HEX code\n"
        "6. Recommended Font Pairing (Google Fonts) — explain why these fonts suit this industry\n"
        "7. Overall Brand Mood — 2-3 sentences describing the visual identity feeling\n\n"
        f"Make every choice specific to the '{industry}' industry with a '{tone}' tone. "
        "Do not give generic answers — justify each color choice."
    )
    result = await asyncio.to_thread(_groq, prompt, system, 500)
    return result.replace("*", "")


async def chat_with_ai(message: str, language: str = "en") -> str:
    lang = resolve_language(language)
    # Prefer Granite if loaded, else fall back to Groq
    if granite_pipeline:
        try:
            result = await asyncio.to_thread(
                granite_pipeline,
                f"You are InKraft, an expert branding assistant. Respond in {lang}. User: {message}\nAssistant:"
            )
            return result[0]["generated_text"].split("Assistant:")[-1].strip()
        except Exception:
            pass  # fall through to Groq
    system = (
        "You are InKraft, an expert AI branding consultant. "
        "Give concise, actionable, expert branding advice. "
        "Be warm, professional, and inspiring. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every single word must be in {lang}."
    )
    result = await asyncio.to_thread(_groq, message, system, 400)
    return result.replace("*", "")


async def generate_logo_prompt(brand_name: str, industry: str, keywords: str, language: str = "en") -> str:
    lang = resolve_language(language)
    system = (
        "You are InKraft, a professional logo designer and visual branding expert. "
        f"IMPORTANT: Write sections 1, 2, 3, and 5 entirely in {lang}. "
        "Section 4 (the SDXL generation prompt) MUST stay in English — image models require English."
    )
    prompt = (
        f"Create a detailed, professional logo design brief for:\n"
        f"Brand Name: {brand_name}\n"
        f"Industry: {industry}\n"
        f"Visual Keywords: {keywords}\n\n"
        "Provide:\n"
        f"1. Logo Concept Description — describe what the logo looks like visually, "
        f"   specifically designed for a {industry} brand called '{brand_name}'\n"
        "2. Style — choose and justify one of: minimalist / geometric / illustrative / wordmark / lettermark\n"
        "3. Color Palette — 2-3 colors with HEX codes, chosen specifically for this brand\n"
        "4. SDXL Image Generation Prompt (write this part in English only) — highly detailed, ready to paste\n"
        "5. Usage Tips — where and how to use this logo effectively\n\n"
        f"Every choice must be tailored specifically to '{brand_name}' in the '{industry}' space."
    )
    return await asyncio.to_thread(_groq, prompt, system, 500)


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


async def unique_selling_points(description: str, industry: str, language: str) -> str:
    lang = resolve_language(language)
    system = (
        "You are a branding expert and market strategist. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every single word must be in {lang}."
    )
    prompt = (
        f"Identify 3 powerful Unique Selling Propositions (USPs) for the following business:\n\n"
        f"Industry: {industry}\n"
        f"Business Description: {description}\n\n"
        "For each USP provide:\n"
        "1. The USP statement (one sharp, memorable sentence)\n"
        f"2. Why this is genuinely unique in the {industry} market\n"
        "3. How to communicate it in marketing materials (tagline angle, ad idea, or campaign concept)\n\n"
        "Base every USP on specific details from the business description above — "
        "do not give generic USPs that could apply to any business."
    )
    result = await asyncio.to_thread(_groq, prompt, system)
    return result.replace("*", "").replace("#", "")


async def analyze_competitors(brand_name: str, industry: str, competitors: str, language: str) -> str:
    lang = resolve_language(language)
    system = (
        "You are a Strategic Market Analyst with expertise in competitive positioning. "
        f"IMPORTANT: You MUST write your ENTIRE response in {lang}. "
        f"Every single word must be in {lang}."
    )
    prompt = (
        f"Perform a systematic competitive analysis for '{brand_name}' "
        f"in the {industry} sector against: {competitors}.\n\n"
        "Structure the analysis:\n\n"
        f"1. MARKET POSITIONING — Where does each player sit on price vs. quality? "
        f"Where should {brand_name} position itself and why?\n\n"
        "2. CORE STRENGTHS — What does each competitor do better than anyone else?\n\n"
        f"3. STRATEGIC GAPS — What are competitors missing that {brand_name} can own?\n\n"
        "4. FEATURE COMPARISON — Rate each on: Ease of Use / Innovation / Customer Trust\n\n"
        f"5. WINNING STRATEGY — The single most impactful move {brand_name} can make "
        "to out-position these competitors right now.\n\n"
        "Be specific. Every point must reference the actual competitors listed above."
    )
    result = await asyncio.to_thread(_groq, prompt, system)
    return result.replace("*", "").replace("#", "")