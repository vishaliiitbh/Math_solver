import json
import re
from utils.groq_client import chat

SYSTEM_PROMPT = """You are a Math Explainer and Tutor Agent. 
You take a solved math problem and create a clear, student-friendly, step-by-step explanation.
Your tone should be encouraging, educational, and easy to follow for a JEE student.
Respond with valid JSON only."""


def explain_solution(parsed_problem: dict, solution: dict, verification: dict) -> dict:
    """
    Generate a student-friendly explanation of the solution.
    Returns explanation dict with formatted steps, key insights, and tips.
    """
    is_correct = verification.get("is_correct", False)
    issues = verification.get("issues", [])

    corrections_note = ""
    if not is_correct and issues:
        corrections_note = f"""
NOTE: The solution had these issues that need addressing:
{chr(10).join(issues)}
Please incorporate corrections: {verification.get('corrections', [])}
"""

    user_msg = f"""Create a student-friendly explanation for this math problem and solution:

PROBLEM: {parsed_problem.get('problem_text', '')}
TOPIC: {parsed_problem.get('topic', '')}
ANSWER: {solution.get('answer', '')}
SOLUTION STEPS: {solution.get('solution_steps', [])}
KEY FORMULA: {solution.get('key_formula_used', '')}
{corrections_note}

Create an explanation that:
1. Starts with what type of problem this is
2. Explains the strategy chosen and why
3. Walks through each step clearly with reasoning
4. Highlights the key formula/theorem used
5. Points out common pitfalls to avoid
6. Ends with a memory tip

Respond with JSON:
{{
  "explanation": "full multi-paragraph student-friendly explanation",
  "step_by_step": [
    {{"step": 1, "action": "what we do", "why": "why we do it", "math": "the math expression"}},
    ...
  ],
  "key_insight": "the most important concept to understand",
  "common_pitfalls": ["pitfall 1", "pitfall 2"],
  "memory_tip": "a short tip to remember this type of problem",
  "related_topics": ["related topic 1", "related topic 2"],
  "difficulty_rating": "easy | medium | hard"
}}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    try:
        response = chat(messages, temperature=0.4, max_tokens=2048)
        response = re.sub(r"```json|```", "", response).strip()
        explanation = json.loads(response)
        explanation.setdefault("explanation", "No explanation generated.")
        explanation.setdefault("step_by_step", [])
        explanation.setdefault("key_insight", "")
        explanation.setdefault("common_pitfalls", [])
        explanation.setdefault("memory_tip", "")
        explanation.setdefault("related_topics", [])
        explanation.setdefault("difficulty_rating", "medium")
        return explanation
    except Exception as e:
        return {
            "explanation": f"Explanation generation failed: {str(e)}",
            "step_by_step": [],
            "key_insight": "",
            "common_pitfalls": [],
            "memory_tip": "",
            "related_topics": [],
            "difficulty_rating": "unknown",
        }
