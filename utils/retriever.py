"""
Multimodal Retrieval System — Step 4 & 5 from the architecture diagram.

Three retrieval strategies:
  Retriever 1: Vector Search (semantic similarity)
  Retriever 2: Metadata Filter (structured constraints)
  Retriever 3: Cross-modal fusion (image desc + query combined)

Then: Re-ranking by composite score.
"""

import re
import numpy as np
from typing import Optional
from utils.vector_store import ProductVectorStore


class MultimodalRetriever:
    def __init__(self, vector_store: ProductVectorStore):
        self.vs = vector_store

    def retrieve(
        self,
        query: str,
        query_embedding: list[float],
        image_description: Optional[str] = None,
        image_embedding: Optional[list[float]] = None,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Full multimodal retrieval pipeline:
        1. Vector search on query
        2. Metadata-filter search
        3. Cross-modal fusion (image + query embedding blend)
        4. Merge, deduplicate, re-rank
        """
        all_results: dict[str, dict] = {}  # keyed by product name for dedup

        # ── Retriever 1: Vector Search on text query ──────────────────────────
        vector_results = self.vs.search_by_vector(query_embedding, top_k=top_k * 2)
        for r in vector_results:
            key = r.get("name", "")
            if key not in all_results:
                all_results[key] = r
            else:
                # Boost score if found by multiple retrievers
                all_results[key]["score"] = max(all_results[key]["score"], r["score"])
                all_results[key]["retrieval_types"] = (
                    all_results[key].get("retrieval_types", [r["retrieval_type"]]) + ["vector"]
                )

        # ── Retriever 2: Metadata Filter ──────────────────────────────────────
        filters = self._extract_filters(query)
        if filters:
            meta_results = self.vs.search_by_metadata(filters, top_k=top_k * 2)
            for r in meta_results:
                key = r.get("name", "")
                if key not in all_results:
                    all_results[key] = r
                    all_results[key]["retrieval_types"] = ["metadata"]
                else:
                    # Multi-retriever bonus
                    all_results[key]["score"] = all_results[key]["score"] * 0.7 + 0.3
                    types = all_results[key].get("retrieval_types", [])
                    if "metadata" not in types:
                        types.append("metadata")
                        all_results[key]["retrieval_types"] = types

        # ── Retriever 3: Cross-modal Fusion ───────────────────────────────────
        if image_embedding and image_description:
            # Blend query embedding with image embedding
            fused = self._fuse_embeddings(query_embedding, image_embedding, alpha=0.5)
            fusion_results = self.vs.search_by_vector(fused, top_k=top_k * 2)
            for r in fusion_results:
                key = r.get("name", "")
                if key not in all_results:
                    all_results[key] = r
                    all_results[key]["retrieval_types"] = ["cross-modal"]
                else:
                    all_results[key]["score"] = all_results[key]["score"] * 0.6 + r["score"] * 0.4
                    types = all_results[key].get("retrieval_types", [])
                    if "cross-modal" not in types:
                        types.append("cross-modal")
                        all_results[key]["retrieval_types"] = types

        # ── Re-Ranking (Step 5) ───────────────────────────────────────────────
        ranked = self._rerank(list(all_results.values()), query, image_description, filters)

        return ranked[:top_k]

    def _extract_filters(self, query: str) -> dict:
        """Parse price constraints and category hints from natural language."""
        filters = {}
        query_lower = query.lower()

        # Price extraction: "under $500", "below 200", "less than 300"
        price_patterns = [
            r"under \$?(\d+)",
            r"below \$?(\d+)",
            r"less than \$?(\d+)",
            r"cheaper than \$?(\d+)",
            r"max \$?(\d+)",
        ]
        for pat in price_patterns:
            m = re.search(pat, query_lower)
            if m:
                filters["max_price"] = float(m.group(1))
                break

        # Min price
        min_patterns = [r"over \$?(\d+)", r"above \$?(\d+)", r"more than \$?(\d+)"]
        for pat in min_patterns:
            m = re.search(pat, query_lower)
            if m:
                filters["min_price"] = float(m.group(1))
                break

        # Category hints
        category_hints = {
            "laptop": "laptop", "notebook": "laptop",
            "phone": "smartphone", "smartphone": "smartphone", "mobile": "smartphone",
            "headphone": "headphones", "earphone": "headphones", "earbuds": "earbuds",
            "watch": "smartwatch", "camera": "camera",
            "tablet": "tablet", "ipad": "tablet",
            "shoe": "shoes", "sneaker": "shoes",
            "tv": "television", "monitor": "monitor",
        }
        for hint, category in category_hints.items():
            if hint in query_lower:
                filters["category"] = category
                break

        return filters

    def _fuse_embeddings(
        self, vec1: list[float], vec2: list[float], alpha: float = 0.5
    ) -> list[float]:
        """Linearly interpolate two embeddings."""
        a = np.array(vec1, dtype=np.float32)
        b = np.array(vec2, dtype=np.float32)
        fused = alpha * a + (1 - alpha) * b
        norm = np.linalg.norm(fused)
        if norm > 0:
            fused = fused / norm
        return fused.tolist()

    def _rerank(
        self,
        results: list[dict],
        query: str,
        image_description: Optional[str],
        filters: dict,
    ) -> list[dict]:
        """
        Re-rank results by composite score:
          - Base vector similarity score
          - Multi-retriever bonus (found by 2+ retrievers)
          - Price constraint satisfaction
          - Query keyword overlap bonus
        """
        query_words = set(query.lower().split())

        for r in results:
            score = r.get("score", 0.0)

            # Multi-retriever bonus
            types = r.get("retrieval_types", [])
            if len(types) > 1:
                score *= (1 + 0.1 * (len(types) - 1))

            # Price filter satisfaction bonus
            if "max_price" in filters:
                try:
                    price = float(str(r.get("price", 9999)).replace("$", "").replace(",", ""))
                    if price <= filters["max_price"]:
                        score *= 1.1
                except (ValueError, TypeError):
                    pass

            # Keyword overlap with product name/description
            prod_text = (r.get("name", "") + " " + r.get("description", "")).lower()
            overlap = len(query_words & set(prod_text.split()))
            if overlap > 0:
                score *= (1 + 0.05 * overlap)

            r["final_score"] = score
            r["score"] = round(score, 4)

        results.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        return results
