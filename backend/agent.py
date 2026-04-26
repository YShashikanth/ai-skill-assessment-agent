import requests
import json
import re

API_KEY = "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"

def llm(prompt: str) -> str:
    try:
        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        data = res.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        return f"ERROR: {str(e)}"


def extract_json(text):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return json.loads(match.group()) if match else None
    except:
        return None


def run_agent(resume, jd):
    prompt = f"""
You are an expert AI hiring assistant.

Resume:
{resume}

Job Description:
{jd}

STRICT RULES:
- Extract ONLY top 8 important skills
- Skill scores MUST be in format "7/10"
- Identify gaps and assign priority
- Generate interview questions (max 3 per skill)
- Create learning plan with reason + time + resources
- Calculate match score %
- Provide short summary
- Provide final hiring decision insight

Return ONLY JSON:

{{
  "match_score": "65%",
  "summary": "Short evaluation",
  "decision": "Hiring recommendation insight",
  "resume_skills": [],
  "jd_skills": [],
  "skill_scores": {{}},
  "gaps": [],
  "gap_priority": {{}},
  "questions": {{}},
  "learning_plan": [
    {{
      "skill": "",
      "reason": "",
      "time": "",
      "resources": []
    }}
  ]
}}
"""

    raw = llm(prompt)
    parsed = extract_json(raw)

    if parsed:
        return parsed

    return {
        "match_score": "0%",
        "summary": "No summary",
        "decision": "No decision",
        "resume_skills": [],
        "jd_skills": [],
        "skill_scores": {},
        "gaps": [],
        "gap_priority": {},
        "questions": {},
        "learning_plan": []
    }