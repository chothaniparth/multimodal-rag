"""
FAISS-based vector store for product embeddings.
Stores:
  - Dense vectors (Gemini text embeddings)
  - Structured metadata (brand, category, price, specs)
"""

import numpy as np
import faiss
import json
import os
import pickle
from typing import Optional


class ProductVectorStore:
    def __init__(self):
        self.index: Optional[faiss.Index] = None
        self.products: list[dict] = []
        self.dimension = 768  # Gemini text-embedding-004 dimension

    # ── Build index from product catalog ─────────────────────────────────────
    def build_index(self, products: list[dict], gemini_client) -> None:
        """Embed all products and build FAISS index."""
        self.products = products
        vectors = []

        for i, product in enumerate(products):
            # Build rich text representation for embedding
            text = self._product_to_text(product)
            embedding = gemini_client.get_embedding(text)
            vectors.append(embedding)
            print(f"  Embedded {i+1}/{len(products)}: {product.get('name','?')}")

            matrix = np.array(vectors, dtype=np.float32)

            # Auto-detect dimension from actual embeddings
            self.dimension = matrix.shape[1]
            print(f"  Embedding dimension detected: {self.dimension}")

            # Normalize for cosine similarity
            faiss.normalize_L2(matrix)

            # Use IVF index for larger catalogs, flat for small ones
            if len(products) > 100:
                quantizer = faiss.IndexFlatIP(self.dimension)
                self.index = faiss.IndexIVFFlat(quantizer, self.dimension, min(len(products)//10, 10))
                self.index.train(matrix)
            else:
                self.index = faiss.IndexFlatIP(self.dimension)

        self.index.add(matrix)

    def _product_to_text(self, product: dict) -> str:
        """Convert product dict to searchable text for embedding."""
        parts = [
            product.get("name", ""),
            product.get("brand", ""),
            product.get("category", ""),
            product.get("description", ""),
        ]
        if product.get("specs"):
            spec_text = " ".join(f"{k} {v}" for k, v in product["specs"].items())
            parts.append(spec_text)
        return " | ".join(filter(None, parts))

    # ── Vector search ─────────────────────────────────────────────────────────
    def search_by_vector(self, query_vector: list[float], top_k: int = 10) -> list[dict]:
        """Pure vector similarity search."""
        if self.index is None:
            return []

        vec = np.array([query_vector], dtype=np.float32)
        faiss.normalize_L2(vec)

        scores, indices = self.index.search(vec, min(top_k, len(self.products)))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            product = dict(self.products[idx])
            product["score"] = float(score)
            product["retrieval_type"] = "vector"
            results.append(product)

        return results

    # ── Metadata filter search ────────────────────────────────────────────────
    def search_by_metadata(self, filters: dict, top_k: int = 10) -> list[dict]:
        """Filter products by structured metadata (category, brand, price range)."""
        results = []
        for product in self.products:
            match = True

            if "category" in filters:
                if filters["category"].lower() not in product.get("category", "").lower():
                    match = False

            if "brand" in filters:
                if filters["brand"].lower() not in product.get("brand", "").lower():
                    match = False

            if "max_price" in filters:
                try:
                    price = float(str(product.get("price", 9999)).replace("$", "").replace(",", ""))
                    if price > filters["max_price"]:
                        match = False
                except (ValueError, TypeError):
                    pass

            if "min_price" in filters:
                try:
                    price = float(str(product.get("price", 0)).replace("$", "").replace(",", ""))
                    if price < filters["min_price"]:
                        match = False
                except (ValueError, TypeError):
                    pass

            if match:
                product_copy = dict(product)
                product_copy["score"] = 0.5  # neutral score for metadata matches
                product_copy["retrieval_type"] = "metadata"
                results.append(product_copy)

        return results[:top_k]

    # ── Save / Load ───────────────────────────────────────────────────────────
    def save(self, path: str = "vector_store"):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/products.json", "w") as f:
            json.dump(self.products, f)

    def load(self, path: str = "vector_store"):
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/products.json") as f:
            self.products = json.load(f)
