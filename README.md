# ShopMind — Multimodal RAG for E-Commerce

> AI shopping assistant that understands both **images** and **text**.  
> Upload a product photo → ask natural language questions → get intelligent answers.

## Architecture (9-step pipeline)

```
User → [1] Streamlit UI
     → [2] Gemini Vision (image → text description)
     → [3] Feature Extraction & Embedding (Gemini text-embedding-004 + FAISS)
     → [4] Multimodal Retrieval System
              Retriever 1: Vector Search
              Retriever 2: Metadata Filter (price, category, brand)
              Retriever 3: Cross-modal Fusion (image + query embeddings blended)
     → [5] Re-Ranking (composite score: similarity + multi-retriever bonus + constraints)
     → [6] Context Construction (top-K products as context)
     → [7] Gemini Flash LLM → generates grounded answer
     → [8] Response Format (product name, specs, price, links)
     → [9] Final Response displayed to user
```

## Setup

### 1. Clone & install

```bash
git clone <your-repo>
cd multimodal-rag
pip install -r requirements.txt
```

### 2. Get a Gemini API key

1. Go to https://aistudio.google.com/
2. Click **Get API key** → Create API key
3. Copy the key

### 3. Configure

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 4. Run locally

```bash
streamlit run app.py
```

### 5. Deploy to Streamlit Cloud

1. Push this folder to a GitHub repo
2. Go to https://share.streamlit.io
3. Connect your repo → select `app.py`
4. Add `GEMINI_API_KEY` as a **Secret** in the app settings
5. Deploy!

## Using Your Own Product Catalog

Create a `products.json` file following this format:

```json
[
  {
    "name": "Product Name",
    "brand": "Brand",
    "category": "laptop",
    "price": 999,
    "description": "Product description...",
    "specs": {
      "processor": "Intel i7",
      "ram": "16GB"
    },
    "url": "https://example.com/product"
  }
]
```

Upload it via the sidebar when running the app.

## Example Queries

With or without an image:
- *"What are the specs of this laptop?"*
- *"Show me similar products under $500"*
- *"Compare this with other gaming laptops"*
- *"Is there a cheaper alternative with the same features?"*
- *"What brand is this and how does it rate?"*

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Vision Model | Gemini 1.5 Flash (Vision) |
| LLM | Gemini 1.5 Flash |
| Embeddings | Gemini text-embedding-004 (768-dim) |
| Vector Store | FAISS (IndexFlatIP) |
| Retrieval | Vector + Metadata + Cross-modal fusion |
