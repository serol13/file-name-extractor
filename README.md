# 📂 File Name Extractor

A clean, minimal Streamlit app that lets you upload a folder of files and instantly export all their filenames to a CSV.

## Features

- Upload multiple files at once
- See file count, number of unique file types, and most common extension
- Preview the list of filenames in-app
- Download a clean CSV with one click

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/file-name-extractor.git
cd file-name-extractor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo, set `app.py` as the main file
5. Click **Deploy** — done!

## Tech Stack

- [Streamlit](https://streamlit.io)
- [Pandas](https://pandas.pydata.org)
