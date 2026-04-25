import streamlit as st
import os
import json
import time
from PIL import Image
import io
import base64
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopMind · Multimodal AI Assistant",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0b0c0f;
    --surface: #13151a;
    --surface2: #1c1f27;
    --accent: #f5a623;
    --accent2: #e05c5c;
    --text: #eaeaea;
    --muted: #6b7280;
    --border: #2a2d35;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif;
}

.main { background: var(--bg); }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.5rem !important;
    letter-spacing: 0.5px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #ffbc4d !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(245,166,35,0.3);
}

/* Text input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 10px !important;
}

/* Cards */
.product-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.product-card:hover { border-color: var(--accent); }

.score-badge {
    display: inline-block;
    background: rgba(245,166,35,0.15);
    color: var(--accent);
    border: 1px solid rgba(245,166,35,0.3);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
}

.tag {
    display: inline-block;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.72rem;
    color: var(--muted);
    margin: 2px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #f5a623 0%, #e05c5c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    margin-bottom: 2rem;
}

.pipeline-step {
    background: var(--surface);
    border-left: 3px solid var(--accent);
    padding: 0.5rem 1rem;
    border-radius: 0 6px 6px 0;
    margin: 0.4rem 0;
    font-size: 0.85rem;
    color: var(--muted);
}
.pipeline-step.active {
    border-left-color: #4ade80;
    color: #4ade80;
    background: rgba(74,222,128,0.05);
}
.pipeline-step.done {
    border-left-color: var(--accent);
    color: var(--text);
}

.answer-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    line-height: 1.7;
    font-size: 0.95rem;
}

.stExpander {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

div[data-testid="stChatMessage"] {
    background: var(--surface2);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# ── Imports (after CSS) ───────────────────────────────────────────────────────
from utils.vector_store import ProductVectorStore
from utils.gemini_client import GeminiClient
from utils.retriever import MultimodalRetriever
from utils.pipeline import RAGPipeline

# ── Session state ─────────────────────────────────────────────────────────────
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password",
                               value=os.getenv("GEMINI_API_KEY", ""),
                               help="Get yours at aistudio.google.com")

    st.markdown("---")
    st.markdown("### 📦 Product Catalog")
    
    uploaded_catalog = st.file_uploader("Upload products.json", type=["json"])

    with st.expander("📋 How to format products.json", expanded=False):
        st.markdown("Your JSON file must be a **list** of product objects. Each product supports these fields:")
        st.code('''[
  {
    "name": "Product Name",        ← required
    "brand": "Brand Name",         ← required
    "price": 999,                  ← number, not string
    "category": "laptop",          ← e.g. laptop, smartphone,
                                      headphones, smartwatch
    "description": "About the      ← 1-2 sentence summary
                    product...",
    "specs": {                     ← dict of key-value pairs
      "processor": "Intel i7",
      "ram": "16GB",
      "storage": "512GB SSD"
    },
    "url": "https://..."           ← product page link
  },
  {
    ... next product ...
  }
]''', language="json")
        st.markdown("**Important rules:**")
        st.markdown("- `price` must be a **number** (`999`), not a string (`\"999 Rs\"`)")
        st.markdown("- `specs` must be a **dictionary `{}`**, not a plain string")
        st.markdown("- The file must start with `[` and end with `]` (a JSON array)")
        st.markdown("- Minimum 1 product, no upper limit")

    if st.button("🚀 Build Index", use_container_width=True):
        if not gemini_key:
            st.error("Please enter your Gemini API key.")
        elif not uploaded_catalog:
            st.error("Please upload a products.json file.")
        else:
            with st.spinner("Building FAISS index..."):
                try:
                    gemini = GeminiClient(api_key=gemini_key)
                    vs = ProductVectorStore()
                    products = json.load(uploaded_catalog)
                    vs.build_index(products, gemini)
                    retriever = MultimodalRetriever(vs)
                    st.session_state.pipeline = RAGPipeline(gemini, retriever)
                    st.session_state.indexed = True
                    st.session_state.vector_store = vs
                    st.success(f"✅ Indexed {len(products)} products!")
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON file: {e}")
                except Exception as e:
                    import traceback
                    st.error(f"Error: {e}")
                    st.code(traceback.format_exc())
                    
    st.markdown("---")
    st.markdown("### 🔄 Pipeline Steps")
    steps = [
        ("1", "Upload Image + Query"),
        ("2", "Gemini Vision → Text"),
        ("3", "Feature Extraction & Embedding"),
        ("4", "Multimodal Retrieval"),
        ("5", "Re-Ranking"),
        ("6", "Context Construction"),
        ("7", "LLM Answer Generation"),
        ("8", "Format Response"),
    ]
    for num, label in steps:
        st.markdown(f'<div class="pipeline-step done">**{num}** {label}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Built with Gemini Vision · FAISS · Streamlit")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">ShopMind</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Multimodal RAG · E-Commerce Product Intelligence</div>', unsafe_allow_html=True)

if not st.session_state.indexed:
    st.info("👈 Enter your Gemini API key and click **Build Index** in the sidebar to get started.")
    st.markdown("#### How it works")
    cols = st.columns(4)
    steps_ui = [
        ("📸", "Upload", "Drop a product photo"),
        ("🔍", "Describe", "Gemini Vision extracts features"),
        ("🗄️", "Retrieve", "FAISS finds similar products"),
        ("💬", "Answer", "LLM synthesises a rich response"),
    ]
    for col, (icon, title, desc) in zip(cols, steps_ui):
        with col:
            st.markdown(f"### {icon} {title}")
            st.caption(desc)
    st.stop()

# ── Query interface ───────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("### 📸 Upload Product Image")
    uploaded_img = st.file_uploader("Drop an image here", type=["jpg", "jpeg", "png", "webp"],
                                    label_visibility="collapsed")
    if uploaded_img:
        img = Image.open(uploaded_img)
        st.image(img, use_container_width=True, caption="Uploaded product")

    st.markdown("### 💬 Your Question")
    user_query = st.text_input("Ask anything about this product...",
                               placeholder="What specs does this have? Show similar under $500.")

    search_clicked = st.button("🔎 Search", use_container_width=True)

with col_right:
    st.markdown("### 🤖 AI Response")

    if search_clicked:
        if not user_query:
            st.warning("Please type a question.")
        else:
            pipeline: RAGPipeline = st.session_state.pipeline

            # Status placeholders
            status = st.empty()
            result_area = st.empty()

            image_bytes = None
            if uploaded_img:
                uploaded_img.seek(0)
                image_bytes = uploaded_img.read()

            with st.spinner(""):
                status.markdown('<div class="pipeline-step active">⚡ Step 2: Generating image description via Gemini Vision...</div>', unsafe_allow_html=True)
                time.sleep(0.3)

                result = pipeline.run(
                    query=user_query,
                    image_bytes=image_bytes,
                    top_k=5,
                    status_callback=lambda msg: status.markdown(
                        f'<div class="pipeline-step active">⚡ {msg}</div>', unsafe_allow_html=True)
                )

            status.empty()

            # ── Answer
            st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)

            # ── Retrieved products
            st.markdown("---")
            st.markdown("#### 🗂️ Retrieved Products")
            for i, prod in enumerate(result["retrieved_products"]):
                with st.expander(f"#{i+1} · {prod['name']} — ${prod.get('price','N/A')}", expanded=i == 0):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.markdown(f"**Brand:** {prod.get('brand','—')}")
                        st.markdown(f"**Category:** {prod.get('category','—')}")
                        st.markdown(f"**Description:** {prod.get('description','—')}")
                        if prod.get("specs"):
                            st.markdown("**Specs:**")
                            for k, v in prod["specs"].items():
                                st.markdown(f"- {k}: `{v}`")
                    with c2:
                        score = prod.get("score", 0)
                        st.markdown(f'<span class="score-badge">Score: {score:.3f}</span>', unsafe_allow_html=True)
                        if prod.get("url"):
                            st.link_button("🔗 View Product", prod["url"])

            # Save to chat history
            st.session_state.chat_history.append({
                "query": user_query,
                "answer": result["answer"],
                "image_desc": result.get("image_description", ""),
            })

    elif st.session_state.chat_history:
        last = st.session_state.chat_history[-1]
        st.markdown(f'<div class="answer-box">{last["answer"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#6b7280;font-size:0.9rem;margin-top:2rem;">Upload an image and ask a question to get started.</div>', unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📜 Session History")
    for i, entry in enumerate(reversed(st.session_state.chat_history[-5:])):
        with st.expander(f"Q: {entry['query'][:80]}...", expanded=False):
            if entry.get("image_desc"):
                st.caption(f"🔍 Image described as: {entry['image_desc'][:200]}...")
            st.markdown(entry["answer"])
