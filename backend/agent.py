import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


# =========================
# LLM CALL
# =========================
def llm(prompt: str) -> str:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a strict JSON generator. Output ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2
            },
            timeout=60
        )

        data = response.json()
        print("\n=== RAW RESPONSE ===\n", data)

        return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    except Exception as e:
        print("ERROR:", str(e))
        return ""


# =========================
# JSON PARSER
# =========================
def extract_json(text):
    try:
        return json.loads(text)
    except:
        pass

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return None

import re

def clean_text(text: str) -> str:
    # remove weird unicode chars
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # fix broken words
    text = re.sub(r"\s+", " ", text)

    # remove weird patterns like (cid:xxx)
    text = re.sub(r"\(cid:\d+\)", "", text)

    return text.strip()
# =========================
# MAIN AGENT
# =========================
def run_agent(resume, jd):
    resume = resume[:2000]
    jd = jd[:2000]

    prompt = f"""
You are an AI hiring assistant.

Analyze the Resume and Job Description.

STRICT RULES:
- Return ONLY valid JSON
- No explanation text
- No markdown
- No extra words

Skill scoring rules:
- Strong project/internship → 7–9
- Moderate → 5–6
- Basic → 3–4
- Missing → 0–2

Resume:
{resume}

Job Description:
{jd}

Return JSON:

{{
  "match_score": "65%",
  "summary": "short summary",
  "decision": "short hiring decision",
  "resume_skills": ["Python"],
  "jd_skills": ["Agile"],
  "skill_scores": {{"Python": "8/10"}},
  "gaps": ["Agile"],
  "gap_priority": {{"Agile": "High"}},
  "questions": {{"Python": ["Question"]}},
  "learning_plan": [
    {{
      "skill": "Agile",
      "reason": "important",
      "time": "2 weeks",
      "resources": ["resource"]
    }}
  ]
}}
"""

    raw = llm(prompt)

    print("\n=== RAW AI OUTPUT ===\n", raw)

    parsed = extract_json(raw)

    if parsed:
        return parsed

    # fallback (rare now)
    return {
        "match_score": "60%",
        "summary": raw[:300] if raw else "AI response issue",
        "decision": "Fallback response",
        "resume_skills": [],
        "jd_skills": [],
        "skill_scores": {},
        "gaps": [],
        "gap_priority": {},
        "questions": {},
        "learning_plan": []
    }