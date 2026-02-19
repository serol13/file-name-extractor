import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="File Name Extractor",
    page_icon=None,
    layout="centered"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background-color: #f5f7fa;
            color: #1a1a2e;
        }

        .hero {
            text-align: center;
            padding: 2.5rem 0 1.5rem 0;
        }

        .hero h1 {
            font-family: 'Space Mono', monospace;
            font-size: 2.2rem;
            color: #1a1a2e;
            letter-spacing: -1px;
            margin-bottom: 0.5rem;
        }

        .hero h1 span {
            color: #2563eb;
        }

        .hero p {
            color: #64748b;
            font-size: 1.05rem;
            font-weight: 300;
        }

        .stat-box {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }

        .stat-box .number {
            font-family: 'Space Mono', monospace;
            font-size: 2.2rem;
            color: #2563eb;
            line-height: 1;
        }

        .stat-box .label {
            color: #94a3b8;
            font-size: 0.8rem;
            margin-top: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .section-title {
            font-family: 'Space Mono', monospace;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #94a3b8;
            margin: 1.5rem 0 0.5rem 0;
        }

        .error-box {
            background: #fff5f5;
            border: 1px solid #fecaca;
            border-left: 4px solid #ef4444;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.5rem;
            color: #991b1b;
            font-size: 0.9rem;
        }

        .no-error-box {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-left: 4px solid #22c55e;
            border-radius: 8px;
            padding: 1rem 1.2rem;
            color: #166534;
            font-size: 0.9rem;
        }

        .stDownloadButton button {
            background: #2563eb !important;
            color: #ffffff !important;
            font-family: 'Space Mono', monospace !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-size: 0.9rem !important;
            width: 100%;
            transition: opacity 0.2s;
        }

        .stDownloadButton button:hover {
            opacity: 0.88 !important;
        }

        .footer {
            text-align: center;
            color: #cbd5e1;
            font-size: 0.78rem;
            margin-top: 3rem;
            font-family: 'Space Mono', monospace;
        }

        div[data-testid="stFileUploader"] {
            background: #ffffff;
            border: 2px dashed #cbd5e1;
            border-radius: 12px;
            padding: 1rem;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }
    </style>

    <div class="hero">
        <h1>File <span>Name</span> Extractor</h1>
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

    # Detect errors
    errors = []
    for name in file_names:
        if not name or name.strip() == "":
            errors.append("Empty or blank filename detected.")
        elif name.startswith("."):
            errors.append(f"Hidden file detected: {name}")
        elif "." not in name:
            errors.append(f"No file extension found: {name}")

    df = pd.DataFrame({"File Name": file_names})

    # Stats
    col1, col2, col3 = st.columns(3)
    extensions = pd.Series([n.rsplit(".", 1)[-1].lower() if "." in n else "none" for n in file_names])

    with col1:
        st.markdown(f'<div class="stat-box"><div class="number">{len(file_names)}</div><div class="label">Files Found</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="stat-box"><div class="number">{extensions.nunique()}</div><div class="label">File Types</div></div>', unsafe_allow_html=True)

    with col3:
        most_common = extensions.value_counts().idxmax()
        st.markdown(f'<div class="stat-box"><div class="number">.{most_common}</div><div class="label">Most Common</div></div>', unsafe_allow_html=True)

    # File list
    st.markdown('<div class="section-title">File List</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="file_names.csv",
        mime="text/csv"
    )

    # Errors section
    st.markdown('<div class="section-title">Errors & Warnings</div>', unsafe_allow_html=True)
    if errors:
        for err in errors:
            st.markdown(f'<div class="error-box">{err}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="no-error-box">No issues detected. All filenames look good.</div>', unsafe_allow_html=True)

else:
    st.info("Upload files from your folder above to get started.")

st.markdown('<div class="footer">built with streamlit · deployed on streamlit cloud</div>', unsafe_allow_html=True)
