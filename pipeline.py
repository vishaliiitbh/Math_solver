"""
Main pipeline orchestrator — coordinates all agents end-to-end.
"""
from agents.parser_agent import parse_problem
from agents.router_agent import route_problem
from agents.solver_agent import solve_problem
from agents.verifier_agent import verify_solution
from agents.explainer_agent import explain_solution
from rag.retriever import retrieve
from memory.memory_store import store_problem


def run_pipeline(
    raw_text: str,
    input_source: str = "text",
    ocr_confidence: float = 1.0,
    asr_confidence: float = 1.0,
    on_step=None,
) -> dict:
    """
    Full pipeline: parse → route → retrieve → solve → verify → explain.

    Args:
        raw_text: cleaned text of the math problem
        input_source: 'text', 'image', or 'audio'
        ocr_confidence: OCR confidence if source is image
        asr_confidence: ASR confidence if source is audio
        on_step: optional callback(step_name, result) for streaming progress

    Returns:
        Full result dict with all agent outputs.
    """
    trace = []

    def step(name, fn, *args, **kwargs):
        result = fn(*args, **kwargs)
        trace.append({"step": name, "result": result})
        if on_step:
            on_step(name, result)
        return result

    # Step 1: Parse
    parsed = step("parser", parse_problem, raw_text)

    # Determine if HITL needed before solving
    needs_hitl = parsed.get("needs_clarification", False)
    hitl_reason = parsed.get("clarification_reason", "")

    # Low confidence from OCR/ASR
    if input_source == "image" and ocr_confidence < 0.75:
        needs_hitl = True
        hitl_reason = f"OCR confidence is low ({ocr_confidence:.0%}). Please review extracted text."
    elif input_source == "audio" and asr_confidence < 0.75:
        needs_hitl = True
        hitl_reason = f"Audio transcription may be inaccurate. Please review transcript."

    # Step 2: Route
    routing = step("router", route_problem, parsed)

    # Step 3: RAG Retrieve
    rag_query = routing.get("rag_query", raw_text)
    retrieved_context = step("retriever", retrieve, rag_query, 5)

    # Step 4: Solve
    solution = step("solver", solve_problem, parsed, routing, retrieved_context)

    # Step 5: Verify
    verification = step("verifier", verify_solution, parsed, solution)

    # Update needs_hitl based on verifier
    if verification.get("needs_hitl", False):
        needs_hitl = True
        hitl_reason = verification.get("hitl_reason", "Verifier flagged this for review")

    # Step 6: Explain
    explanation = step("explainer", explain_solution, parsed, solution, verification)

    return {
        "raw_input": raw_text,
        "input_source": input_source,
        "parsed_problem": parsed,
        "routing": routing,
        "retrieved_context": retrieved_context,
        "solution": solution,
        "verification": verification,
        "explanation": explanation,
        "needs_hitl": needs_hitl,
        "hitl_reason": hitl_reason,
        "agent_trace": trace,
    }


def save_result_to_memory(result: dict, user_feedback: str = "none") -> str:
    """Save pipeline result to memory store."""
    return store_problem(
        raw_input=result["raw_input"],
        parsed_problem=result["parsed_problem"],
        solution=result["solution"],
        verification=result["verification"],
        explanation=result["explanation"],
        user_feedback=user_feedback,
    )
