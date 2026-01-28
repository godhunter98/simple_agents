from typing import Dict
from core.embeddings import embed_text
from infrastructure.repositories.vector_search import search_similar_chunks


def build_rag_context(user_query:int,top_k:int = 3) -> Dict[str,str]:

    embedded_user_query = embed_text(user_query)

    chunks = search_similar_chunks(
        embedded_user_query,limit=top_k)

    context = "\n\n".join(
    f"[Context {i+1}]\n{chunk.content}"
    for i, chunk in enumerate(chunks)
    )

    chunk_ids = [chunk.id for chunk in chunks]

    prompt = (
        "Use the following context to answer the question.\n\n"
        f"{context}\n\n"
        f"Question: {user_query}"
    )

    return chunk_ids, prompt