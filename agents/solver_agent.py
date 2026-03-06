import json
import re
from utils.groq_client import chat
from rag.retriever import retrieve, format_context
from memory.memory_store import search_similar_problems

SYSTEM_PROMPT = """You are a Math Solver Agent for a JEE-style tutoring system.
You solve math problems step-by-step using provided context from the knowledge base.
Be precise, show all steps, and reference relevant formulas.
Respond with valid JSON only."""


def solve_problem(parsed_problem: dict, routing: dict, retrieved_context: list[dict] = None) -> dict:
    """
    Solve the math problem using RAG context.
    Returns solution dict with answer, steps, confidence, and used_context.
    """
    if retrieved_context is None:
        rag_query = routing.get("rag_query", parsed_problem.get("problem_text", ""))
        retrieved_context = retrieve(rag_query, top_k=5)

    context_str = format_context(retrieved_context)

    # Check memory for similar problems
    similar_problems = search_similar_problems(parsed_problem.get("problem_text", ""), top_k=2)
    memory_context = ""
    if similar_problems:
        mem_parts = []
        for mem in similar_problems:
            mem_parts.append(
                f"Similar past problem: {mem.get('problem_text', '')}\n"
                f"Answer was: {mem.get('answer', 'N/A')}"
            )
        memory_context = "\n\n".join(mem_parts)

    user_msg = f"""Solve this math problem:

PROBLEM: {parsed_problem.get('problem_text', '')}
TOPIC: {parsed_problem.get('topic', '')}
GOAL: {parsed_problem.get('goal', '')}
VARIABLES: {parsed_problem.get('variables', [])}
CONSTRAINTS: {parsed_problem.get('constraints', [])}
STRATEGY: {routing.get('solution_strategy', '')}

KNOWLEDGE BASE CONTEXT:
{context_str}

{"SIMILAR PAST PROBLEMS:" + memory_context if memory_context else ""}

Respond with JSON:
{{
  "answer": "final answer clearly stated",
  "solution_steps": [
    "Step 1: ...",
    "Step 2: ...",
    "..."
  ],
  "key_formula_used": "main formula or theorem used",
  "confidence": 0.0-1.0,
  "answer_type": "numerical | expression | proof | multiple_choice",
  "units": "if applicable, else empty string",
  "alternative_approaches": "brief mention of other methods if any"
}}
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    try:
        response = chat(messages, temperature=0.2, max_tokens=2048)
        response = re.sub(r"```json|```", "", response).strip()
        solution = json.loads(response)
        solution.setdefault("answer", "Could not determine answer")
        solution.setdefault("solution_steps", [])
        solution.setdefault("key_formula_used", "")
        solution.setdefault("confidence", 0.5)
        solution.setdefault("answer_type", "numerical")
        solution.setdefault("units", "")
        solution.setdefault("alternative_approaches", "")
        solution["retrieved_context"] = retrieved_context
        return solution
    except Exception as e:
        return {
            "answer": "Solving failed",
            "solution_steps": [f"Error: {str(e)}"],
            "key_formula_used": "",
            "confidence": 0.0,
            "answer_type": "error",
            "units": "",
            "alternative_approaches": "",
            "retrieved_context": retrieved_context,
            "error": str(e),
        }
