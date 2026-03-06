import os
import glob
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

EMBED_MODEL = "all-MiniLM-L6-v2"
INDEX_NAME = "math-mentor"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
KB_DIR = Path(__file__).parent / "knowledge_base"

_embedder = None
_index = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def get_index():
    global _index
    if _index is None:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY not set in environment")
        pc = Pinecone(api_key=api_key)
        existing = [idx.name for idx in pc.list_indexes()]
        if INDEX_NAME not in existing:
            pc.create_index(
                name=INDEX_NAME,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        _index = pc.Index(INDEX_NAME)
    return _index


def chunk_text(text: str, source: str) -> list[dict]:
    words = text.split()
    chunks = []
    i = 0
    chunk_id = 0
    while i < len(words):
        chunk_words = words[i : i + CHUNK_SIZE]
        chunk_text = " ".join(chunk_words)
        chunks.append({
            "id": f"{source}_{chunk_id}",
            "text": chunk_text,
            "source": source,
        })
        i += CHUNK_SIZE - CHUNK_OVERLAP
        chunk_id += 1
    return chunks


def ingest_knowledge_base(force: bool = False) -> dict:
    """Embed and upsert all knowledge base documents into Pinecone."""
    index = get_index()
    embedder = get_embedder()

    stats = index.describe_index_stats()
    if stats.total_vector_count > 0 and not force:
        return {"status": "already_ingested", "vector_count": stats.total_vector_count}

    txt_files = glob.glob(str(KB_DIR / "*.txt"))
    all_chunks = []
    for filepath in txt_files:
        source = Path(filepath).stem
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text, source)
        all_chunks.extend(chunks)

    vectors = []
    texts = [c["text"] for c in all_chunks]
    embeddings = embedder.encode(texts, batch_size=32, show_progress_bar=False)

    for chunk, embedding in zip(all_chunks, embeddings):
        vectors.append({
            "id": chunk["id"],
            "values": embedding.tolist(),
            "metadata": {
                "text": chunk["text"],
                "source": chunk["source"],
            },
        })

    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i : i + batch_size])

    return {"status": "ingested", "chunks": len(vectors), "files": len(txt_files)}
