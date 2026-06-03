import chromadb
from chromadb.utils import embedding_functions

COLLECTION_NAME = "drone_frames"

client = chromadb.PersistentClient(path="storage/chroma_db")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=ef
)

def add_frame(frame_id, description, metadata):
    collection.add(
        documents=[description],
        metadatas=[metadata],
        ids=[str(frame_id)]
    )
    print(f"[VECTOR] Frame {frame_id} added to vector store.")

def semantic_search(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results