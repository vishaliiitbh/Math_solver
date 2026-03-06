import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

MEMORY_INDEX = "math-mentor-memory"
MEMORY_FILE = Path(__file__).parent / "memory_log.json"
EMBED_MODEL = "all-MiniLM-L6-v2"

_embedder = None
_memory_index = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def get_memory_index():
    global _memory_index
    if _memory_index is None:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            return None
        pc = Pinecone(api_key=api_key)
        existing = [idx.name for idx in pc.list_indexes()]
        if MEMORY_INDEX not in existing:
            pc.create_index(
                name=MEMORY_INDEX,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        _memory_index = pc.Index(MEMORY_INDEX)
    return _memory_index


def load_memory_log() -> list:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_memory_log(log: list):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(log, f, indent=2)


def store_problem(
    raw_input: str,
    parsed_problem: dict,
    solution: dict,
    verification: dict,
    explanation: dict,
    user_feedback: str = "none",
) -> str:
    """Store a solved problem in memory. Returns memory ID."""
    memory_id = str(uuid.uuid4())[:8]
    timestamp = datetime.utcnow().isoformat()

    is_verified = verification.get("is_correct", False)
    is_positive_feedback = user_feedback in ("correct", "none")
    should_store = is_verified or is_positive_feedback

    record = {
        "id": memory_id,
        "timestamp": timestamp,
        "raw_input": raw_input,
        "problem_text": parsed_problem.get("problem_text", ""),
        "topic": parsed_problem.get("topic", ""),
        "answer": solution.get("answer", ""),
        "key_formula": solution.get("key_formula_used", ""),
        "is_correct": verification.get("is_correct", False),
        "user_feedback": user_feedback,
        "key_insight": explanation.get("key_insight", ""),
        "memory_tip": explanation.get("memory_tip", ""),
    }

    # Save to JSON log always
    log = load_memory_log()
    log.append(record)
    save_memory_log(log)

    # Embed and store in Pinecone only if solution is trusted
    if should_store:
        try:
            index = get_memory_index()
            if index:
                embedder = get_embedder()
                embedding = embedder.encode([record["problem_text"]])[0].tolist()
                index.upsert(vectors=[{
                    "id": memory_id,
                    "values": embedding,
                    "metadata": {
                        "problem_text": record["problem_text"][:500],
                        "topic": record["topic"],
                        "answer": record["answer"][:200],
                        "key_formula": record["key_formula"][:200],
                        "key_insight": record["key_insight"][:300],
                    }
                }])
        except Exception:
            pass

    return memory_id


def search_similar_problems(query: str, top_k: int = 3) -> list[dict]:
    """Search memory for similar past problems."""
    try:
        index = get_memory_index()
        if not index:
            return []
        embedder = get_embedder()
        embedding = embedder.encode([query])[0].tolist()
        results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
        similar = []
        for match in results.matches:
            if match.score > 0.7:
                similar.append({
                    "problem_text": match.metadata.get("problem_text", ""),
                    "answer": match.metadata.get("answer", ""),
                    "key_formula": match.metadata.get("key_formula", ""),
                    "key_insight": match.metadata.get("key_insight", ""),
                    "similarity": round(match.score, 3),
                })
        return similar
    except Exception:
        return []


def get_recent_problems(n: int = 10) -> list[dict]:
    """Return n most recent problems from the memory log."""
    log = load_memory_log()
    return log[-n:]
