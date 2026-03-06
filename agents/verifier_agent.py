import json
import re
from utils.groq_client import chat

SYSTEM_PROMPT = """You are a Math Verifier and Critic Agent for a JEE tutoring system.
Your job is to critically check solutions for:
1. Mathematical correctness
2. Unit/domain validity
3. Edge case handling
4. Logical consistency
Be strict but fair. Respond with valid JSON only."""


def verify_solution(parsed_problem: dict, solution: dict) -> dict:
    """
    Verify the solution for correctness.
    Returns verification result with is_correct, issues, confidence, needs_hitl.
    """
    user_msg = f"""Verify this math solution:

PROBLEM: {parsed_problem.get('problem_text', '')}
TOPIC: {parsed_problem.get('topic', '')}
CONSTRAINTS: {parsed_problem.get('constraints', [])}

PROPOSED ANSWER: {solution.get('answer', '')}
SOLUTION STEPS:
{chr(10).join(solution.get('solution_steps', []))}

KEY FORMULA USED: {solution.get('key_formula_used', '')}
SOLVER CONFIDENCE: {solution.get('confidence', 0)}

Check for:
1. Is each step mathematically valid?
2. Is the final answer correct given the steps?
3. Are domain constraints respected (no division by zero, sqrt of negatives, etc.)?
4. Are there any logical errors or jumps?
5. Is the answer in correct form/units?

Respond with JSON:
{{
  "is_correct": true/false,
  "confidence": 0.0-1.0,
  "issues": ["list of issues found, empty if none"],
  "corrections": ["suggested corrections if any"],
  "domain_check": "passed | failed | warning",
  "edge_cases_handled": true/false,
  "needs_hitl": true/false,
  "hitl_reason": "reason for human review if needs_hitl is true",
  "verdict": "one-line summary of verification"
}}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    try:
        response = chat(messages, temperature=0.1)
        response = re.sub(r"```json|```", "", response).strip()
        verification = json.loads(response)
        verification.setdefault("is_correct", False)
        verification.setdefault("confidence", 0.5)
        verification.setdefault("issues", [])
        verification.setdefault("corrections", [])
        verification.setdefault("domain_check", "warning")
        verification.setdefault("edge_cases_handled", False)
        verification.setdefault("needs_hitl", True)
        verification.setdefault("hitl_reason", "Verification inconclusive")
        verification.setdefault("verdict", "Verification incomplete")
        return verification
    except Exception as e:
        return {
            "is_correct": False,
            "confidence": 0.0,
            "issues": [f"Verification error: {str(e)}"],
            "corrections": [],
            "domain_check": "failed",
            "edge_cases_handled": False,
            "needs_hitl": True,
            "hitl_reason": f"Verifier error: {str(e)}",
            "verdict": "Could not verify",
        }
