"""
Gemini client — handles:
  • Image → text description (Gemini Vision)
  • Text embedding generation
  • Final LLM answer generation
"""

import google.generativeai as genai
from PIL import Image
import io
import numpy as np
from typing import Optional


class GeminiClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.vision_model = genai.GenerativeModel("gemini-2.5-flash")
        self.text_model = genai.GenerativeModel("gemini-2.5-flash")
        self.embedding_model = "gemini-embedding-2"

    # ── 1. Image → Description ────────────────────────────────────────────────
    def describe_image(self, image_bytes: bytes) -> str:
        """Use Gemini Vision to extract a rich product description from image."""
        img = Image.open(io.BytesIO(image_bytes))

        prompt = """You are a product analysis AI for an e-commerce platform.
Analyze this product image and provide a detailed, structured description including:
1. Product type and category
2. Visual attributes (color, shape, material, style)
3. Brand if visible
4. Key features or specs visible
5. Estimated price range
6. Target audience

Be specific and descriptive. Output as a flowing paragraph, not bullet points.
Focus on attributes that would help match this to similar products in a database."""

        response = self.vision_model.generate_content([prompt, img])
        return response.text.strip()

    # ── 2. Text Embedding ─────────────────────────────────────────────────────
    def get_embedding(self, text: str) -> list[float]:
        """Generate embedding vector for a text string."""
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document",
        )
        return result["embedding"]

    def get_query_embedding(self, text: str) -> list[float]:
        """Generate query-optimized embedding."""
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_query",
        )
        print(len(result["embedding"]))  # what dimension is it actually?
        return result["embedding"]

    # ── 3. LLM Answer Generation ──────────────────────────────────────────────
    def generate_answer(
        self,
        query: str,
        context_products: list[dict],
        image_description: Optional[str] = None,
    ) -> str:
        """Generate a rich, grounded answer using retrieved product context."""

        context_str = ""
        for i, p in enumerate(context_products, 1):
            specs = ""
            if p.get("specs"):
                specs = ", ".join(f"{k}: {v}" for k, v in p["specs"].items())
            context_str += f"""
Product {i}: {p.get('name', 'Unknown')}
  Brand: {p.get('brand', '—')}
  Category: {p.get('category', '—')}
  Price: ${p.get('price', 'N/A')}
  Description: {p.get('description', '—')}
  Specs: {specs or '—'}
  URL: {p.get('url', '—')}
  Relevance Score: {p.get('score', 0):.3f}
"""

        image_ctx = f"\n\nImage Analysis:\n{image_description}" if image_description else ""

        system_prompt = f"""You are ShopMind, an expert AI shopping assistant for an e-commerce platform.
You help users find products, compare specs, and make informed purchase decisions.

Your knowledge comes from these retrieved products:
{context_str}{image_ctx}

Answer the user's question in a helpful, conversational tone. Structure your response as:
1. Direct answer to their question
2. Top product recommendation(s) with key specs
3. Price comparison if relevant
4. Any helpful buying tips

Always cite product names and prices. Use markdown for formatting.
If the query involves an uploaded image, reference what you observed in it."""

        response = self.text_model.generate_content(
            f"{system_prompt}\n\nUser question: {query}"
        )
        return response.text.strip()
