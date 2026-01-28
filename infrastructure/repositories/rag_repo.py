from infrastructure.connection import get_connection
from uuid import UUID
from typing import Iterable


def persist_rag_sources(
    *,
    execution_id: UUID,
    chunk_ids: Iterable[UUID],
) -> None:

    conn = get_connection()

    try:    
        with conn.cursor() as cursor:
            for rank,chunk_id in enumerate(chunk_ids,start=1):
                cursor.execute('''
                INSERT INTO rag_sources (execution_id,chunk_id,rank)
                VALUES (%s,%s,%s)
                ''',
                (execution_id,chunk_id,rank)
                )
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()