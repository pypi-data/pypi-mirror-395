"""
Vector store for semantic search in RAG system.

Provides a lightweight SQLite-based vector database for storing
and searching embeddings with cosine similarity.
"""

import logging
import sqlite3
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


class SQLiteVectorStore:
    """
    Lightweight vector store using SQLite.

    Stores embeddings as BLOBs and performs cosine similarity search
    in Python. For large-scale deployments, consider migrating to
    FAISS, Milvus, or pgvector.
    """

    def __init__(self, db_path: str, dimension: int):
        """
        Initialize vector store.

        Args:
            db_path: Path to SQLite database file (use ":memory:" for in-memory)
            dimension: Embedding dimension
        """
        self.db_path = db_path
        self.dimension = dimension

        # Ensure parent directory exists
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup_schema()

        logger.info(f"Initialized vector store at {db_path} (dim={dimension})")

    def _setup_schema(self):
        """Create database schema for embeddings."""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_id TEXT UNIQUE NOT NULL,
                entity_name TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                vector BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Index for entity lookups
        self.conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_entity
            ON embeddings(entity_name, entity_id)
        """
        )

        # Index for chunk lookups
        self.conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_chunk
            ON embeddings(chunk_id)
        """
        )

        self.conn.commit()

    def add(
        self,
        chunk_id: str,
        vector: np.ndarray,
        entity_name: str,
        entity_id: str,
        content: str,
        metadata: str | None = None,
    ):
        """
        Add a single embedding to the store.

        Args:
            chunk_id: Unique identifier for this chunk
            vector: Embedding vector (must match store dimension)
            entity_name: Entity type (e.g., "projects")
            entity_id: Entity ID
            content: Text content that was embedded
            metadata: Optional JSON metadata
        """
        if len(vector) != self.dimension:
            raise ValueError(
                f"Vector dimension {len(vector)} doesn't match store dimension {self.dimension}"
            )

        # Convert to float32 BLOB
        vector_blob = vector.astype(np.float32).tobytes()

        try:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO embeddings
                (chunk_id, vector, entity_name, entity_id, content, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (chunk_id, vector_blob, entity_name, entity_id, content, metadata),
            )
            self.conn.commit()
            logger.debug(f"Added embedding for chunk {chunk_id}")

        except sqlite3.Error as e:
            logger.error(f"Failed to add embedding for {chunk_id}: {e}")
            raise

    def add_batch(self, chunks: list[dict]):
        """
        Add multiple embeddings in a batch.

        Args:
            chunks: List of dicts with keys:
                - chunk_id: str
                - vector: np.ndarray
                - entity_name: str
                - entity_id: str
                - content: str
                - metadata: str (optional)
        """
        data = []
        for chunk in chunks:
            vector = chunk["vector"].astype(np.float32).tobytes()
            data.append(
                (
                    chunk["chunk_id"],
                    vector,
                    chunk["entity_name"],
                    chunk["entity_id"],
                    chunk["content"],
                    chunk.get("metadata"),
                )
            )

        try:
            self.conn.executemany(
                """
                INSERT OR REPLACE INTO embeddings
                (chunk_id, vector, entity_name, entity_id, content, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                data,
            )
            self.conn.commit()
            logger.info(f"Added {len(chunks)} embeddings in batch")

        except sqlite3.Error as e:
            logger.error(f"Failed to add batch: {e}")
            raise

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
        entity_filter: str | None = None,
        score_threshold: float = 0.0,
    ) -> list[tuple[str, float, str, dict]]:
        """
        Search for similar vectors using cosine similarity.

        Args:
            query_vector: Query embedding
            top_k: Number of results to return
            entity_filter: Optional entity name to filter by
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of tuples: (chunk_id, similarity_score, content, metadata_dict)
            Sorted by similarity (highest first)
        """
        if len(query_vector) != self.dimension:
            raise ValueError(
                f"Query vector dimension {len(query_vector)} doesn't match store dimension {self.dimension}"
            )

        # Build query
        query = "SELECT chunk_id, vector, content, entity_name, entity_id, metadata FROM embeddings"
        params = []

        if entity_filter:
            query += " WHERE entity_name = ?"
            params.append(entity_filter)

        cursor = self.conn.execute(query, params)

        # Compute similarities
        results = []
        for chunk_id, vec_blob, content, entity_name, entity_id, metadata in cursor:
            vec = np.frombuffer(vec_blob, dtype=np.float32)
            similarity = self._cosine_similarity(query_vector, vec)

            if similarity >= score_threshold:
                metadata_dict = {
                    "entity_name": entity_name,
                    "entity_id": entity_id,
                    "metadata": metadata,
                }
                results.append((chunk_id, float(similarity), content, metadata_dict))

        # Sort by similarity (descending) and limit
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def get_by_chunk_id(self, chunk_id: str) -> dict | None:
        """
        Retrieve a specific chunk by ID.

        Args:
            chunk_id: Chunk identifier

        Returns:
            Dict with chunk data or None if not found
        """
        cursor = self.conn.execute(
            """
            SELECT chunk_id, vector, content, entity_name, entity_id, metadata
            FROM embeddings
            WHERE chunk_id = ?
        """,
            (chunk_id,),
        )

        row = cursor.fetchone()
        if not row:
            return None

        chunk_id, vec_blob, content, entity_name, entity_id, metadata = row
        vector = np.frombuffer(vec_blob, dtype=np.float32)

        return {
            "chunk_id": chunk_id,
            "vector": vector,
            "content": content,
            "entity_name": entity_name,
            "entity_id": entity_id,
            "metadata": metadata,
        }

    def delete(self, chunk_id: str) -> bool:
        """
        Delete a chunk by ID.

        Args:
            chunk_id: Chunk identifier

        Returns:
            True if deleted, False if not found
        """
        cursor = self.conn.execute(
            "DELETE FROM embeddings WHERE chunk_id = ?", (chunk_id,)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_by_entity(self, entity_name: str, entity_id: str) -> int:
        """
        Delete all chunks for a specific entity.

        Args:
            entity_name: Entity type
            entity_id: Entity ID

        Returns:
            Number of chunks deleted
        """
        cursor = self.conn.execute(
            "DELETE FROM embeddings WHERE entity_name = ? AND entity_id = ?",
            (entity_name, entity_id),
        )
        self.conn.commit()
        return cursor.rowcount

    def count(self) -> int:
        """Return total number of embeddings in store."""
        cursor = self.conn.execute("SELECT COUNT(*) FROM embeddings")
        return cursor.fetchone()[0]

    def clear(self):
        """Delete all embeddings from the store."""
        self.conn.execute("DELETE FROM embeddings")
        self.conn.commit()
        logger.warning("Cleared all embeddings from vector store")

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.

        Args:
            a: First vector
            b: Second vector

        Returns:
            Similarity score (0-1, where 1 is identical)
        """
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def close(self):
        """Close the database connection."""
        self.conn.close()
        logger.info("Closed vector store connection")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


__all__ = ["SQLiteVectorStore"]
