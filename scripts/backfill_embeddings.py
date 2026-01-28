from core.embeddings import embed_text
from infrastructure.repositories.document_repo import (
    get_chunks_without_embeddings, update_chunks_embeddings
)

Batch_size = 50

while True:
    chunks = get_chunks_without_embeddings(Batch_size)
    
    if not chunks:
        print("No chunks to fetch!")
        break
    
    for row in chunks:
        embeddings = embed_text(row['content'])
        update_chunks_embeddings(row['id'],embeddings)

    print(f"Embedded {len(chunks)} chunks...")