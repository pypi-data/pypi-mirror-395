import uuid
import chromadb
from typing import List, Tuple, Optional, Dict, Any

from dragonglass.core.config import settings
from dragonglass.core.protocols import LLMProvider
from dragonglass.utils import console


class VectorSearch:
    """
    Manages vector storage and semantic search using ChromaDB.
    """

    def __init__(
        self, provider: LLMProvider, collection_name: str = "dragonglass_knowledge"
    ):
        self.provider = provider

        # Ensure data directory exists
        db_path = settings.data_dir / "chromadb"
        db_path.mkdir(parents=True, exist_ok=True)

        # Initialize persistent client
        self.client = chromadb.PersistentClient(path=str(db_path))

        # Get or create collection with Cosine similarity
        self.collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    async def ingest(
        self, text: str, metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Embeds text and saves it to the vector database."""
        if not text.strip():
            return False

        try:
            embedding = await self.provider.embed_text(text)

            self.collection.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[metadata or {}],
                ids=[str(uuid.uuid4())],
            )
            return True
        except Exception as e:
            console.print(f"Failed to ingest document: {e}")
            return False

    async def search(
        self, query: str, top_k: int = 5, threshold: float = 0.4
    ) -> List[Tuple[str, float]]:
        """
        Semantic search for relevant context.
        Returns: List of (text_content, similarity_score)
        """
        try:
            query_embedding = await self.provider.embed_text(query)

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "distances"],
            )

            if not results["documents"] or not results["documents"][0]:
                return []

            documents = results["documents"][0]
            # Chroma returns distance. Similarity = 1.0 - distance (for Cosine)
            distances = results["distances"][0]  # type: ignore

            matches: List[Tuple[str, float]] = []

            for doc, dist in zip(documents, distances):
                similarity = 1.0 - dist
                if similarity >= threshold:
                    matches.append((doc, similarity))

            return matches

        except Exception as e:
            console.print(f"Vector search failed: {e}")
            return []
