"""
RAGPipeline — orchestrates the full 9-step pipeline from the architecture diagram.

Step 1: User uploads image + query (handled in app.py)
Step 2: Image Processing Pipeline — Gemini Vision → text
Step 3: Feature Extraction & Embedding
Step 4: Multimodal Retrieval System
Step 5: Re-Ranking
Step 6: Context Construction
Step 7: Query + Context → LLM
Step 8: Response Format
Step 9: Final Response (returned to app.py)
"""

from typing import Optional, Callable
from utils.gemini_client import GeminiClient
from utils.retriever import MultimodalRetriever


class RAGPipeline:
    def __init__(self, gemini: GeminiClient, retriever: MultimodalRetriever):
        self.gemini = gemini
        self.retriever = retriever

    def run(
        self,
        query: str,
        image_bytes: Optional[bytes] = None,
        top_k: int = 5,
        status_callback: Optional[Callable[[str], None]] = None,
    ) -> dict:
        """
        Run the full multimodal RAG pipeline.

        Returns:
            {
                "answer": str,
                "retrieved_products": list[dict],
                "image_description": str,
                "query": str,
            }
        """
        def update(msg: str):
            if status_callback:
                status_callback(msg)

        # ── Step 2: Image → Text ──────────────────────────────────────────────
        image_description = None
        image_embedding = None

        if image_bytes:
            update("Step 2: Gemini Vision analyzing image...")
            image_description = self.gemini.describe_image(image_bytes)

            # ── Step 3a: Embed image description ─────────────────────────────
            update("Step 3: Creating image embedding...")
            image_embedding = self.gemini.get_embedding(image_description)

        # ── Step 3b: Embed query ──────────────────────────────────────────────
        update("Step 3: Creating query embedding...")

        # Combine query with image description for richer embedding
        combined_query = query
        if image_description:
            combined_query = f"{query}\n\nProduct image shows: {image_description}"

        query_embedding = self.gemini.get_query_embedding(combined_query)

        # ── Steps 4 & 5: Retrieve + Re-rank ──────────────────────────────────
        update("Step 4: Running multimodal retrieval (vector + metadata + cross-modal)...")
        retrieved = self.retriever.retrieve(
            query=query,
            query_embedding=query_embedding,
            image_description=image_description,
            image_embedding=image_embedding,
            top_k=top_k,
        )

        update("Step 5: Re-ranking results by relevance, visual similarity, and user constraints...")

        # ── Step 6: Context Construction ──────────────────────────────────────
        update("Step 6: Building context from top results...")
        context_products = retrieved[:top_k]

        # ── Step 7: LLM Answer Generation ─────────────────────────────────────
        update("Step 7: Generating answer with Gemini Flash LLM...")
        answer = self.gemini.generate_answer(
            query=query,
            context_products=context_products,
            image_description=image_description,
        )

        # ── Steps 8 & 9: Format + Return ──────────────────────────────────────
        update("Step 8: Formatting final response...")

        return {
            "answer": answer,
            "retrieved_products": context_products,
            "image_description": image_description or "",
            "query": query,
        }
