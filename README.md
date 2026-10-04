# SONORA — Personalized Music Recommendation for Student Stress & Well-being

SONORA is a Streamlit B.Sc. Data Science research prototype. It uses the trained Random Forest model to predict the genre usually chosen when stressed, then adds a live YouTube recommendation layer for actual videos and playlists.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Add a YouTube Data API v3 key in the sidebar under **YouTube connection** for local/demo use, or store it as `YOUTUBE_API_KEY` in Streamlit secrets when deploying.

