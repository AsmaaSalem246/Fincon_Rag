
import streamlit as st
import sys
from pathlib import Path

# --------------------------------------------------
# Project Setup
# --------------------------------------------------

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.generation.chain import FinConRAGPipeline
from src.ingestion.run_ingestion import run_ingestion_pipeline


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="FinCon AI | Financial Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main application */
.stApp {
    background: linear-gradient(135deg, #071426 0%, #0B1D35 55%, #071426 100%);
    color: #F1F5F9;
}

/* Remove default top spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Main header */
.hero {
    background: linear-gradient(110deg, #102D55, #123D70, #0B2342);
    border: 1px solid rgba(59, 130, 246, 0.4);
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 28px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
}

.hero-title {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #B9D7F5;
    font-size: 14px;
    line-height: 1.8;
}

/* Section titles */
.section-title {
    color: #F8FAFC;
    font-size: 21px;
    font-weight: 750;
    margin: 22px 0 14px 0;
}

/* Answer card */
.answer-card {
    background: linear-gradient(135deg, #102B4C, #0D2039);
    border: 1px solid rgba(56, 189, 248, 0.45);
    border-left: 5px solid #38BDF8;
    border-radius: 14px;
    padding: 24px;
    margin-top: 10px;
    margin-bottom: 18px;
    color: #E2E8F0;
    line-height: 1.8;
}

/* Info cards */
.info-card {
    background: rgba(23, 48, 78, 0.85);
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    min-height: 75px;
}

.info-label {
    color: #93C5FD;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
}

.info-value {
    color: #F8FAFC;
    font-size: 14px;
}

/* Entity badges */
.entity-badge {
    display: inline-block;
    background: #173D68;
    color: #BAE6FD;
    border: 1px solid #2563A6;
    border-radius: 20px;
    padding: 7px 13px;
    margin: 4px 5px 4px 0;
    font-size: 13px;
}

/* Query expansion */
.query-card {
    background: rgba(15, 57, 91, 0.65);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 12px;
    padding: 16px;
    color: #BAE6FD;
    margin: 10px 0 20px 0;
}

/* Source cards */
.source-card {
    background: linear-gradient(135deg, #17365C, #112A49);
    border: 1px solid rgba(96, 165, 250, 0.3);
    border-radius: 12px;
    padding: 18px;
    min-height: 90px;
    color: #DBEAFE;
    overflow-wrap: anywhere;
}

/* Child chunk card */
.chunk-card {
    background: #10243D;
    border: 1px solid #294766;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
}

/* Metric values */
.metric-label {
    color: #94A3B8;
    font-size: 12px;
}

.metric-value {
    color: #38BDF8;
    font-size: 20px;
    font-weight: 800;
}

/* Streamlit buttons */
.stButton > button {
    background: linear-gradient(90deg, #087CF0, #0759D8);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1595FF, #087CF0);
    border: none;
    color: white;
    box-shadow: 0 4px 18px rgba(8, 124, 240, 0.3);
}

/* Inputs */
.stTextInput input {
    background-color: #10243D;
    color: white;
    border: 1px solid #315477;
    border-radius: 10px;
}

.stTextInput input:focus {
    border-color: #38BDF8;
    box-shadow: 0 0 0 1px #38BDF8;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #10243D;
    border-color: #315477;
    color: white;
    border-radius: 9px;
}

/* Slider */
.stSlider {
    padding-top: 8px;
}

/* Expanders */
.streamlit-expanderHeader {
    background: #132D4C;
    border: 1px solid #315477;
    border-radius: 10px;
    color: #E2E8F0;
    font-weight: 700;
}

.streamlit-expanderContent {
    background: rgba(12, 31, 53, 0.8);
    border: 1px solid #294766;
    border-radius: 0 0 10px 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C1D33, #102A49);
    border-right: 1px solid #23466B;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #E0F2FE;
}

/* Divider */
hr {
    border-color: #294766;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        💼 FinCon & Financial Regulatory Intelligence Assistant
    </div>
    <div class="hero-subtitle">
        Production Hybrid RAG &nbsp; • &nbsp;
        Hierarchical Parent-Child Indexing &nbsp; • &nbsp;
        Cross-Encoder Reranking &nbsp; • &nbsp;
        Citation Enforcement
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Sidebar: Configuration & Pipeline
# --------------------------------------------------

st.sidebar.markdown("## ⚙️ Configuration")
st.sidebar.caption("Manage your RAG pipeline settings")

st.sidebar.markdown("---")

top_k = st.sidebar.slider(
    "Top-K Rerank Results",
    min_value=1,
    max_value=8,
    value=3,
    help="Number of child chunks retained after reranking."
)

st.sidebar.markdown("### 🔄 Document Pipeline")

if st.sidebar.button("Run Document Ingestion", use_container_width=True):
    with st.spinner("Parsing documents and building hybrid indexes..."):
        try:
            run_ingestion_pipeline()
            st.sidebar.success("Ingestion and indexing completed successfully!")
            
            # Refresh cached pipeline after ingestion
            get_pipeline.clear()

        except Exception as e:
            st.sidebar.error(f"Ingestion failed: {e}")

st.sidebar.markdown("---")

# Sample Queries
st.sidebar.markdown("### 📊 2026 Financial Standards")

sample_queries = [
    "What is the mandatory timeline for Form 8-K disclosure under SEC Item 1.05 for material cybersecurity incidents?",
    "What are the differences between Scope 1, Scope 2, and Scope 3 emissions under IFRS S2 in 2026?",
    "What are the eligibility criteria and turnover thresholds for EU CSRD Wave 2 compliance in 2026?",
    "What is the Basel III Endgame capital output floor percentage for risk-weighted assets?",
    "What confidence level is required for Expected Shortfall under the FRTB market risk framework?"
]

selected_sample = st.sidebar.selectbox(
    "Choose a sample question",
    [""] + sample_queries,
    format_func=lambda x: "Select a query..." if x == "" else x
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align:center; color:#94A3B8; font-size:12px;">
        Powered by Hybrid RAG Architecture<br>
        Financial Intelligence System
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Initialize Pipeline
# --------------------------------------------------

@st.cache_resource
def get_pipeline():
    return FinConRAGPipeline()


pipeline = get_pipeline()


# --------------------------------------------------
# Main Search Section
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔎 Ask Your Financial Question</div>',
    unsafe_allow_html=True
)

user_query = st.text_input(
    "Financial Question",
    value=selected_sample,
    placeholder="Enter your Financial Controlling / Accounting Question...",
    label_visibility="collapsed"
)

search_col, info_col = st.columns([1, 5])

with search_col:
    search_clicked = st.button(
        "🔍 Search & Analyze",
        type="primary",
        use_container_width=True
    )

with info_col:
    st.caption(
        "Your question will pass through query expansion, hybrid retrieval, "
        "cross-encoder reranking, and grounded answer generation."
    )


# --------------------------------------------------
# Execute RAG Pipeline
# --------------------------------------------------

if search_clicked:

    if not user_query.strip():
        st.warning("Please enter a financial question first.")

    else:

        with st.spinner(
            "Analyzing your question through the Hybrid RAG pipeline..."
        ):

            try:
                result = pipeline.run(
                    query=user_query,
                    top_k_rerank=top_k
                )

                # ------------------------------------------
                # 1. Generated Answer
                # ------------------------------------------

                st.markdown("---")

                st.markdown(
                    '<div class="section-title">📝 Financial Controlling Synthesis</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="answer-card">
                        <div style="font-size:17px; font-weight:750;
                                    color:#7DD3FC; margin-bottom:14px;">
                            ✨ AI-Generated Financial Analysis
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(result.get("answer", "No answer generated."))

                # ------------------------------------------
                # 2. Recognized Financial Entities
                # ------------------------------------------

                entities = result.get("entities", [])

                if entities:

                    st.markdown(
                        '<div class="section-title">🏷️ Recognized Financial Entities</div>',
                        unsafe_allow_html=True
                    )

                    entity_html = ""

                    for entity in entities:
                        entity_html += (
                            f'<span class="entity-badge">'
                            f'{entity.get("text", "")} '
                            f'({entity.get("label", "")})'
                            f'</span>'
                        )

                    st.markdown(entity_html, unsafe_allow_html=True)

                # ------------------------------------------
                # 3. Query Expansion
                # ------------------------------------------

                expanded_query = result.get("expanded_query")

                if expanded_query and expanded_query != user_query:

                    st.markdown(
                        '<div class="section-title">🔄 Pre-Retrieval Query Expansion</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class="query-card">
                            <b>Expanded Query</b><br><br>
                            {expanded_query}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # ------------------------------------------
                # 4. Source Attributions
                # ------------------------------------------

                st.markdown("---")

                st.markdown(
                    '<div class="section-title">📚 Source Attributions</div>',
                    unsafe_allow_html=True
                )

                sources = result.get("sources", [])

                if sources:

                    source_cols = st.columns(min(len(sources), 3))

                    for i, source in enumerate(sources):

                        with source_cols[i % len(source_cols)]:
                            st.markdown(
                                f"""
                                <div class="source-card">
                                    <div style="font-size:22px;">📄</div>
                                    <div style="font-weight:700; margin-top:8px;">
                                        Source {i + 1}
                                    </div>
                                    <div style="font-size:13px; margin-top:5px;">
                                        {source}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:
                    st.info("No source attributions were returned.")

                # ------------------------------------------
                # 5. Retrieved Child Chunks
                # ------------------------------------------

                st.markdown("---")

                with st.expander(
                    "🔍 Inspect Retrieved Child Chunks & Reranker Scores",
                    expanded=False
                ):

                    child_chunks = result.get(
                        "retrieved_child_chunks", []
                    )

                    if child_chunks:

                        st.caption(
                            f"{len(child_chunks)} child chunks selected after reranking."
                        )

                        for idx, chunk in enumerate(child_chunks, start=1):

                            st.markdown(
                                f"""
                                <div class="chunk-card">
                                    <h4 style="color:#7DD3FC;">
                                        Rank {idx}
                                    </h4>
                                    <div style="color:#CBD5E1; font-size:13px;">
                                        Chunk ID: {chunk.get('id', 'N/A')}
                                    </div>
                                    <br>
                                    <b style="color:#38BDF8;">
                                        Cross-Encoder Rerank Score:
                                    </b>
                                    {chunk.get('rerank_score', 0.0):.4f}
                                    <br>
                                    <b style="color:#38BDF8;">
                                        RRF Score:
                                    </b>
                                    {chunk.get('rrf_score', 0.0):.4f}
                                    <br><br>
                                    <b>Parent ID:</b>
                                    {chunk.get('parent_id', 'N/A')}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            st.text_area(
                                f"Child Chunk #{idx} Content",
                                value=chunk.get("text", ""),
                                height=130,
                                key=f"child_{idx}"
                            )

                            st.json(chunk.get("metadata", {}))

                    else:
                        st.info("No child chunks were retrieved.")

                # ------------------------------------------
                # 6. Full Parent Context
                # ------------------------------------------

                with st.expander(
                    "📖 Inspect Full Parent Context Sent to LLM",
                    expanded=False
                ):

                    context_used = result.get("context_used", "")

                    if context_used:
                        st.code(
                            context_used,
                            language="markdown",
                            line_numbers=True
                        )
                    else:
                        st.info("No parent context was returned.")

            except Exception as e:
                st.error(f"An error occurred while processing your query: {e}")


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748B; font-size:12px;">
        FinCon & Financial Regulatory Intelligence Assistant
        <br>
        Hybrid Retrieval • Reranking • Grounded Generation
    </div>
    """,
    unsafe_allow_html=True
)
