import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(
    page_title="File Name Extractor",
    page_icon="📂",
    layout="centered"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background-color: #0f0f0f;
            color: #f0f0f0;
        }

        .hero {
            text-align: center;
            padding: 3rem 0 2rem 0;
        }

        .hero h1 {
            font-family: 'Space Mono', monospace;
            font-size: 2.4rem;
            color: #f0f0f0;
            letter-spacing: -1px;
            margin-bottom: 0.5rem;
        }

        .hero h1 span {
            color: #00e5a0;
        }

        .hero p {
            color: #888;
            font-size: 1.05rem;
            font-weight: 300;
        }

        .stat-box {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .stat-box .number {
            font-family: 'Space Mono', monospace;
            font-size: 2.5rem;
            color: #00e5a0;
            line-height: 1;
        }

        .stat-box .label {
            color: #666;
            font-size: 0.85rem;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stDownloadButton button {
            background: #00e5a0 !important;
            color: #0f0f0f !important;
            font-family: 'Space Mono', monospace !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-size: 0.95rem !important;
            width: 100%;
            transition: opacity 0.2s;
        }

        .stDownloadButton button:hover {
            opacity: 0.85 !important;
        }

        .footer {
            text-align: center;
            color: #333;
            font-size: 0.8rem;
            margin-top: 3rem;
            font-family: 'Space Mono', monospace;
        }

        div[data-testid="stFileUploader"] {
            background: #1a1a1a;
            border: 2px dashed #2a2a2a;
            border-radius: 12px;
            padding: 1rem;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }
    </style>

    <div class="hero">
        <h1>📂 File <span>Name</span> Extractor</h1>
        <p>Upload your files — get a clean CSV of every filename instantly.</p>
    </div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drop your files here or click to browse",
    accept_multiple_files=True,
    label_visibility="visible"
)

if uploaded_files:
    file_names = [f.name for f in uploaded_files]
    df = pd.DataFrame({"File Name": file_names})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="stat-box">
                <div class="number">{len(file_names)}</div>
                <div class="label">Files Found</div>
            </div>
        """, unsafe_allow_html=True)

    extensions = pd.Series([n.rsplit(".", 1)[-1].lower() if "." in n else "none" for n in file_names])
    with col2:
        st.markdown(f"""
            <div class="stat-box">
                <div class="number">{extensions.nunique()}</div>
                <div class="label">File Types</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        most_common = extensions.value_counts().idxmax()
        st.markdown(f"""
            <div class="stat-box">
                <div class="number">.{most_common}</div>
                <div class="label">Most Common</div>
            </div>
        """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="file_names.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Upload files from your folder above to get started.")

st.markdown('<div class="footer">built with streamlit · deploy on streamlit cloud</div>', unsafe_allow_html=True)
