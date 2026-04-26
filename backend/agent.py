# backend/agent.py

import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


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


def clean_text(text: str) -> str:
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\(cid:\d+\)", "", text)
    return text.strip()


def run_agent(resume, jd):
    resume = clean_text(resume)[:2000]
    jd = clean_text(jd)[:2000]

    prompt = f"""
You are an AI hiring assistant.

STRICT RULES:
- Return ONLY valid JSON
- No explanation text

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
    parsed = extract_json(raw)

    if parsed:
        return parsed

    # fallback
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
