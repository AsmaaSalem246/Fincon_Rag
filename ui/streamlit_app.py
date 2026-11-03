import streamlit as st
import sys
import html
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT SETUP
# --------------------------------------------------

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.generation.chain import FinConRAGPipeline
from src.ingestion.run_ingestion import run_ingestion_pipeline


# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FinCon AI | Financial Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 3. CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* ===== GLOBAL ===== */

.stApp {
    background-color: #F4F7FB;
    color: #24364B;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main text */
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #334155;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background-color: #172F4D;
    border-right: 1px solid #D8E2ED;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #F1F5F9;
}

section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #C5D2E0;
}

/* Sidebar selectbox */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFFFFF;
    border-color: #CBD5E1;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #24364B !important;
}

/* ===== HEADER ===== */

.hero {
    background: linear-gradient(115deg, #173B60, #245B83);
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0 5px 18px rgba(23, 59, 96, 0.10);
}

.hero-title {
    color: #FFFFFF !important;
    font-size: 29px;
    font-weight: 800;
    line-height: 1.5;
}

.hero-subtitle {
    color: #DCEAF5 !important;
    font-size: 14px;
    line-height: 1.8;
}

/* ===== SECTION HEADINGS ===== */

.section-title {
    color: #173B60 !important;
    font-size: 21px;
    font-weight: 750;
    margin-top: 22px;
    margin-bottom: 14px;
}

/* ===== ANSWER CARD ===== */

.answer-heading {
    color: #245B83 !important;
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 14px;
}

/* ===== ENTITY BADGES ===== */

.entity-badge {
    display: inline-block;
    background-color: #E8F1F8;
    color: #245B83 !important;
    border: 1px solid #C9DCEB;
    border-radius: 20px;
    padding: 7px 13px;
    margin: 4px 5px 4px 0;
    font-size: 13px;
    font-weight: 600;
}

/* ===== QUERY EXPANSION ===== */

.query-card {
    background-color: #EDF4FA;
    border: 1px solid #D4E4F1;
    border-left: 4px solid #4386B5;
    border-radius: 11px;
    padding: 17px;
    margin: 10px 0 20px 0;
    color: #294D6A !important;
    line-height: 1.8;
}

/* ===== SOURCE CARDS ===== */

.source-card {
    background-color: #FFFFFF;
    border: 1px solid #DFE7F0;
    border-radius: 12px;
    padding: 18px;
    min-height: 110px;
    box-shadow: 0 3px 10px rgba(23, 59, 96, 0.04);
    overflow-wrap: anywhere;
}

.source-number {
    color: #4386B5 !important;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 8px;
}

.source-name {
    color: #334155 !important;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.6;
}

/* ===== CHUNK CARDS ===== */

.chunk-card {
    background-color: #F8FAFC;
    border: 1px solid #DFE7F0;
    border-radius: 11px;
    padding: 17px;
    margin: 10px 0;
}

.chunk-title {
    color: #245B83 !important;
    font-size: 15px;
    font-weight: 750;
}

.chunk-meta {
    color: #64748B !important;
    font-size: 13px;
    line-height: 1.8;
}

/* ===== INPUTS ===== */

.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #24364B !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder {
    color: #94A3B8 !important;
    opacity: 1;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #4386B5 !important;
    box-shadow: 0 0 0 1px #4386B5 !important;
}

/* ===== SELECTBOX ===== */

.stSelectbox [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #CBD5E1 !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #24364B !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
}

[data-baseweb="menu"] * {
    color: #24364B !important;
}

/* ===== BUTTONS ===== */

.stButton > button {
    background-color: #326F9D;
    color: #FFFFFF !important;
    border: 1px solid #326F9D;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button p,
.stButton > button span {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: #245B83;
    border-color: #245B83;
    color: #FFFFFF !important;
}

/* ===== EXPANDERS ===== */

[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #DFE7F0;
    border-radius: 12px;
    margin: 12px 0;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #245B83 !important;
    font-weight: 700;
}

/* ===== CODE & JSON ===== */

[data-testid="stCode"],
[data-testid="stJson"] {
    background-color: #F1F5F9 !important;
    border: 1px solid #DFE7F0;
    border-radius: 10px;
}

/* ===== CAPTIONS ===== */

[data-testid="stCaptionContainer"] {
    color: #64748B !important;
}

/* ===== DIVIDERS & FOOTER ===== */

hr {
    border-color: #DFE7F0;
}

.footer {
    text-align: center;
    color: #8291A5 !important;
    font-size: 12px;
    line-height: 1.8;
    padding: 15px;
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
# 4. INITIALIZE PIPELINE
# --------------------------------------------------

@st.cache_resource
def get_pipeline():
    return FinConRAGPipeline()


pipeline = get_pipeline()


# --------------------------------------------------
# 5. HEADER - USING NATIVE STREAMLIT COMPONENTS
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-title">
        💼 FinCon & Financial Regulatory Intelligence Assistant
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        color: #52677D;
        font-size: 14px;
        margin-top: -15px;
        margin-bottom: 25px;
        line-height: 1.8;
    ">
        Hybrid RAG Architecture &nbsp; • &nbsp;
        Hierarchical Parent-Child Indexing &nbsp; • &nbsp;
        Cross-Encoder Reranking &nbsp; • &nbsp;
        Citation Enforcement
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 6. SIDEBAR
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

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Document Pipeline")

if st.sidebar.button(
    "Run Document Ingestion",
    use_container_width=True
):

    with st.spinner("Parsing documents and building hybrid indexes..."):

        try:
            run_ingestion_pipeline()

            get_pipeline.clear()
            pipeline = get_pipeline()

            st.sidebar.success(
                "Ingestion and indexing completed successfully!"
            )

        except Exception as e:
            st.sidebar.error(f"Ingestion failed: {e}")


st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 2026 Financial Standards")

sample_queries = [
    "What is the mandatory timeline for Form 8-K disclosure under SEC Item 1.05 for material cybersecurity incidents?",
    "What are the differences between Scope 1, Scope 2, and Scope 3 emissions under IFRS S2 in 2026?",
    "What are the eligibility criteria and turnover thresholds for EU CSRD Wave 2 compliance in 2026?",
    "What is the Basel III Endgame capital output floor percentage for risk-weighted assets?",
    "What confidence level is required for Expected Shortfall under the FRTB market risk framework?"
]

selected_sample = st.sidebar.selectbox(
    "Choose a sample question:",
    [""] + sample_queries,
    format_func=lambda x: "Select a query..." if x == "" else x
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
    text-align:center;
    color:#DCEAF5;
    font-size:12px;
    line-height:1.8;
">
    Financial Intelligence System<br>
    Powered by Hybrid RAG Architecture
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 7. MAIN SEARCH SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔎 Ask Your Financial Question</div>',
    unsafe_allow_html=True
)

st.caption(
    "Ask a question about financial controlling, accounting, "
    "or regulatory standards."
)

user_query = st.text_input(
    "Financial Question",
    value=selected_sample,
    placeholder="Enter your financial question here...",
    label_visibility="collapsed"
)

search_col, description_col = st.columns([1, 4])

with search_col:
    search_clicked = st.button(
        "🔍 Search & Analyze",
        type="primary",
        use_container_width=True
    )

with description_col:
    st.caption(
        "Query Expansion → Hybrid Retrieval → Cross-Encoder Reranking "
        "→ Grounded Answer Generation"
    )


# --------------------------------------------------
# 8. EXECUTE RAG PIPELINE
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

                # ======================================
                # A. GENERATED ANSWER
                # ======================================

                st.markdown("---")

                st.markdown(
                    '<div class="section-title">'
                    '📝 Financial Controlling Synthesis'
                    '</div>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):

                    st.markdown(
                        '<div class="answer-heading">'
                        '✨ AI-Generated Financial Analysis'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        result.get("answer", "No answer generated.")
                    )

                # ======================================
                # B. RECOGNIZED ENTITIES
                # ======================================

                entities = result.get("entities", [])

                if entities:

                    st.markdown(
                        '<div class="section-title">'
                        '🏷️ Recognized Financial Entities'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    entity_html = ""

                    for entity in entities:

                        entity_text = html.escape(
                            str(entity.get("text", ""))
                        )

                        entity_label = html.escape(
                            str(entity.get("label", ""))
                        )

                        entity_html += (
                            f'<span class="entity-badge">'
                            f'{entity_text} ({entity_label})'
                            f'</span>'
                        )

                    st.markdown(
                        entity_html,
                        unsafe_allow_html=True
                    )

                # ======================================
                # C. QUERY EXPANSION
                # ======================================

                expanded_query = result.get("expanded_query")

                if expanded_query and expanded_query != user_query:

                    st.markdown(
                        '<div class="section-title">'
                        '🔄 Pre-Retrieval Query Expansion'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    safe_expanded_query = html.escape(
                        str(expanded_query)
                    )

                    st.markdown(
                        f"""
                        <div class="query-card">
                            <b>Expanded Query</b>
                            <br><br>
                            {safe_expanded_query}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # ======================================
                # D. SOURCE ATTRIBUTIONS
                # ======================================

                st.markdown("---")

                st.markdown(
                    '<div class="section-title">'
                    '📚 Source Attributions'
                    '</div>',
                    unsafe_allow_html=True
                )

                sources = result.get("sources", [])

                if sources:

                    source_cols = st.columns(min(len(sources), 3))

                    for i, source in enumerate(sources):

                        safe_source = html.escape(str(source))

                        with source_cols[i % len(source_cols)]:

                            st.markdown(
                                f"""
                                <div class="source-card">
                                    <div class="source-number">
                                        SOURCE {i + 1}
                                    </div>
                                    <div class="source-name">
                                        📄 {safe_source}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                else:
                    st.info("No source attributions were returned.")

                # ======================================
                # E. CHILD CHUNKS & RERANKER SCORES
                # ======================================

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
                            f"{len(child_chunks)} child chunks "
                            "selected after reranking."
                        )

                        for idx, chunk in enumerate(
                            child_chunks,
                            start=1
                        ):

                            chunk_id = html.escape(
                                str(chunk.get("id", "N/A"))
                            )

                            parent_id = html.escape(
                                str(chunk.get("parent_id", "N/A"))
                            )

                            rerank_score = chunk.get(
                                "rerank_score", 0.0
                            )

                            rrf_score = chunk.get(
                                "rrf_score", 0.0
                            )

                            st.markdown(
                                f"""
                                <div class="chunk-card">

                                    <div class="chunk-title">
                                        Rank {idx}
                                    </div>

                                    <div class="chunk-meta">
                                        <b>Chunk ID:</b> {chunk_id}
                                        <br>
                                        <b>Parent ID:</b> {parent_id}
                                    </div>

                                    <br>

                                    <div>
                                        <b style="color:#326F9D;">
                                            Cross-Encoder Rerank Score:
                                        </b>
                                        {rerank_score:.4f}
                                    </div>

                                    <div>
                                        <b style="color:#326F9D;">
                                            RRF Score:
                                        </b>
                                        {rrf_score:.4f}
                                    </div>

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

                            with st.expander(
                                f"Metadata - Chunk #{idx}"
                            ):

                                st.json(
                                    chunk.get("metadata", {})
                                )

                    else:
                        st.info("No child chunks were retrieved.")

                # ======================================
                # F. FULL PARENT CONTEXT
                # ======================================

                with st.expander(
                    "📖 Inspect Full Parent Context Sent to LLM",
                    expanded=False
                ):

                    context_used = result.get(
                        "context_used", ""
                    )

                    if context_used:

                        st.code(
                            context_used,
                            language="markdown",
                            line_numbers=True
                        )

                    else:
                        st.info("No parent context was returned.")

            except Exception as e:

                st.error(
                    f"An error occurred while processing your query: {e}"
                )


# --------------------------------------------------
# 9. FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown("""
<div class="footer">
    FinCon & Financial Regulatory Intelligence Assistant
    <br>
    Hybrid Retrieval • Reranking • Grounded Generation
</div>
""", unsafe_allow_html=True)
