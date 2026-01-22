"""
Repository for Document and DocumentChunk database operations.
"""
from transformers.models.esm.openfold_utils.chunk_utils import chunk_layer
from torch.fx.experimental.symbolic_shapes import Int
from typing import List
from uuid import UUID
from typing import TypedDict
import psycopg
import psycopg.rows
from dataclasses import dataclass

from infrastructure.connection import get_connection

@dataclass
class ChunkRow(TypedDict):
    id: UUID
    content: str

def persist_document(source: str, title: str | None = None, metadata: dict | None = None) -> UUID:
    """
    Persist a document and return its ID.
    """
    conn = get_connection()

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO documents (source, title, metadata)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    source,
                    title,
                    psycopg.types.json.Json(metadata) if metadata else None,
                ),
            )
            row = cursor.fetchone()
            conn.commit()
            return row["id"]
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def persist_chunks(document_id: UUID, chunks: List[str]) -> List[UUID]:
    """
    Persist multiple chunks for a document and return their IDs.
    
    Args:
        document_id: The parent document's ID
        chunks: List of text chunks to persist
    
    Returns:
        List of chunk IDs in order
    """
    conn = get_connection()
    chunk_ids: List[UUID] = []

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            for index, content in enumerate(chunks):
                cursor.execute(
                    """
                    INSERT INTO document_chunks (document_id, chunk_index, content)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (document_id, index, content),
                )
                row = cursor.fetchone()
                chunk_ids.append(row["id"])
            
            conn.commit()
            return chunk_ids
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def persist_document_with_chunks(
    source: str,
    chunks: List[str],
    title: str | None = None,
    metadata: dict | None = None
) -> tuple[UUID, List[UUID]]:
    """
    Persist a document and its chunks atomically.
    
    Args:
        source: Document source (e.g., filename)
        chunks: List of text chunks
        title: Optional document title
        metadata: Optional metadata dict
    
    Returns:
        Tuple of (document_id, list of chunk_ids)
    """
    conn = get_connection()
    chunk_ids: List[UUID] = []

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            # 1. Insert document
            cursor.execute(
                """
                INSERT INTO documents (source, title, metadata)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (
                    source,
                    title,
                    psycopg.types.json.Json(metadata) if metadata else None,
                ),
            )
            doc_row = cursor.fetchone()
            document_id = doc_row["id"]

            # 2. Insert all chunks
            for index, content in enumerate(chunks):
                cursor.execute(
                    """
                    INSERT INTO document_chunks (document_id, chunk_index, content)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (document_id, index, content),
                )
                chunk_row = cursor.fetchone()
                chunk_ids.append(chunk_row["id"])

            conn.commit()
            return document_id, chunk_ids
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_document_by_id(document_id: UUID) -> dict | None:
    """
    Get a document by its ID.
    """
    conn = get_connection()

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, source, title, metadata, created_at
                FROM documents
                WHERE id = %s
                """,
                (document_id,)
            )
            return cursor.fetchone()
    finally:
        conn.close()


def get_chunks_for_document(document_id: UUID) -> List[dict]:
    """
    Get all chunks for a document, ordered by chunk_index.
    """
    conn = get_connection()

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, document_id, chunk_index, content, created_at
                FROM document_chunks
                WHERE document_id = %s
                ORDER BY chunk_index ASC
                """,
                (document_id,)
            )
            return cursor.fetchall()
    finally:
        conn.close()

def get_chunks_without_embeddings(limit:int) ->List[ChunkRow]:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT id, content
                FROM document_chunks
                WHERE embedding is NULL
                ORDER BY created_at
                LIMIT %s
            ''',
            (limit,))
            return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def update_chunks_embeddings(chunk_id:UUID,embedding:list[float])->None:
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute('''
            UPDATE document_chunks
            SET embeddings = %s
            WHERE id = %s
            ''',
            (embedding,chunk_id))
            conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def list_documents(limit: int = 20, offset: int = 0) -> List[dict]:
    """
    List documents with pagination.
    """
    conn = get_connection()

    try:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, source, title, metadata, created_at
                FROM documents
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset)
            )
            return cursor.fetchall()
    finally:
        conn.close()
