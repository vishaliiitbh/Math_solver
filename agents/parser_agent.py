import json
import re
from utils.groq_client import chat

SYSTEM_PROMPT = """You are a Math Parser Agent for a JEE-style math tutoring system.
Your job is to:
1. Clean and normalize raw text extracted from OCR, audio transcription, or typed input
2. Identify the math topic and problem structure
3. Extract variables, constraints, and goal
4. Flag ambiguities that need human clarification

Always respond with valid JSON only. No markdown, no explanation outside JSON.
"""

def parse_problem(raw_text: str) -> dict:
    """
    Convert raw input text into a structured math problem.
    Returns a dict with problem_text, topic, variables, constraints, goal, needs_clarification, clarification_reason.
    """
    user_msg = f"""Parse the following math problem input:

INPUT: {raw_text}

Respond with JSON in exactly this format:
{{
  "problem_text": "cleaned and normalized version of the problem",
  "topic": "one of: algebra, probability, calculus_limits, calculus_derivatives, calculus_optimization, linear_algebra, other",
  "variables": ["list", "of", "variables"],
  "constraints": ["list of constraints like x > 0"],
  "goal": "what needs to be found or proven",
  "needs_clarification": false,
  "clarification_reason": "only if needs_clarification is true, otherwise empty string"
}}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    try:
        response = chat(messages, temperature=0.1)
        # Strip markdown code fences if present
        response = re.sub(r"```json|```", "", response).strip()
        parsed = json.loads(response)
        # Ensure required keys
        parsed.setdefault("problem_text", raw_text)
        parsed.setdefault("topic", "other")
        parsed.setdefault("variables", [])
        parsed.setdefault("constraints", [])
        parsed.setdefault("goal", "")
        parsed.setdefault("needs_clarification", False)
        parsed.setdefault("clarification_reason", "")
        return parsed
    except Exception as e:
        return {
            "problem_text": raw_text,
            "topic": "other",
            "variables": [],
            "constraints": [],
            "goal": "Unknown - parsing failed",
            "needs_clarification": True,
            "clarification_reason": f"Auto-parsing failed: {str(e)}",
        }
