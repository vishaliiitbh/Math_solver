import json
import re
from utils.groq_client import chat

SYSTEM_PROMPT = """You are a Math Intent Router Agent. Given a structured math problem, 
you classify the problem type and determine the best solution strategy and which tools/approaches to use.
Respond with valid JSON only."""


def route_problem(parsed_problem: dict) -> dict:
    """
    Classify problem type and route to appropriate solution strategy.
    Returns routing info including strategy, difficulty, and suggested tools.
    """
    user_msg = f"""Given this parsed math problem:
{json.dumps(parsed_problem, indent=2)}

Determine the routing strategy. Respond with JSON:
{{
  "problem_type": "equation_solving | optimization | limit_evaluation | derivative | probability_calculation | matrix_operation | proof | other",
  "topic": "{parsed_problem.get('topic', 'other')}",
  "difficulty": "easy | medium | hard",
  "solution_strategy": "brief description of approach to take",
  "needs_calculator": true/false,
  "key_concepts": ["list", "of", "relevant", "concepts"],
  "rag_query": "optimized query to retrieve relevant formulas from knowledge base"
}}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    try:
        response = chat(messages, temperature=0.1)
        response = re.sub(r"```json|```", "", response).strip()
        routing = json.loads(response)
        routing.setdefault("problem_type", "other")
        routing.setdefault("difficulty", "medium")
        routing.setdefault("solution_strategy", "General problem solving")
        routing.setdefault("needs_calculator", False)
        routing.setdefault("key_concepts", [])
        routing.setdefault("rag_query", parsed_problem.get("problem_text", ""))
        return routing
    except Exception as e:
        return {
            "problem_type": "other",
            "topic": parsed_problem.get("topic", "other"),
            "difficulty": "medium",
            "solution_strategy": "Standard approach",
            "needs_calculator": False,
            "key_concepts": [],
            "rag_query": parsed_problem.get("problem_text", ""),
            "error": str(e),
        }
