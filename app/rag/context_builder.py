from typing import Dict
from core.embeddings import embed_text
from infrastructure.repositories.document_repo import search_similar_chunks


def build_rag_message(user_query:int,top_k:int = 3) -> Dict[str,str]:
    embedded_user_query = embed_text(user_query)
    rag_chunks = search_similar_chunks(
        embedded_user_query,limit=top_k)

    rag_context_text = "\n\n".join(
    f"[Context {i+1}]\n{chunk.content}"
    for i, chunk in enumerate(rag_chunks)
    )

    return {
    "role": "user",
    "content": f"""
                Use the following context to answer the question.

                Context:
                {rag_context_text}

                Question:
                {user_query}
                """
                }