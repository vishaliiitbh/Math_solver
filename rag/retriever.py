from rag.embedder import get_embedder, get_index


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Retrieve top_k relevant chunks from Pinecone for a given query.
    Returns list of dicts with 'text', 'source', 'score'.
    """
    embedder = get_embedder()
    index = get_index()

    query_embedding = embedder.encode([query])[0].tolist()

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )

    chunks = []
    for match in results.matches:
        chunks.append({
            "text": match.metadata.get("text", ""),
            "source": match.metadata.get("source", "unknown"),
            "score": round(match.score, 4),
        })

    return chunks


def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a context string for the LLM."""
    if not chunks:
        return "No relevant context found in knowledge base."
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Source {i}: {chunk['source']} | Relevance: {chunk['score']}]\n{chunk['text']}")
    return "\n\n".join(parts)
