"""
Repository for vector similarity search operations.
"""
from uuid import UUID
from core.embeddings import embed_text
import psycopg
import psycopg.rows
from domain.models import DocumentChunk
from infrastructure.connection import get_connection


def search_similar_chunks(query_embedding: list[float], k: int) -> list[DocumentChunk]:
    """
    Search for the k most similar document chunks to the query embedding.
    """
    conn = get_connection()

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                '''
                SELECT
                    id,
                    document_id,
                    content,
                    embedding <=> %s::vector AS distance
                FROM document_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                ''',
                (query_embedding,query_embedding,k)
            )
            rows = cursor.fetchall()
            return [
                DocumentChunk(
                    id=row["id"],
                    document_id=row["document_id"],
                    content=row["content"],
                    embedding=None,  # we don’t need it again
                )
                for row in rows
            ]
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()