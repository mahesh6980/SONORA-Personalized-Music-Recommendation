# SONORA V6 — Personalized Music Recommendation for Student Stress & Well-being

SONORA is a Streamlit B.Sc. Data Science research prototype. It uses the trained Random Forest model to predict the genre usually chosen when stressed, then adds a live YouTube recommendation layer for actual videos and playlists.

## V6 UI update
- Discover page reorganized into a clear step-by-step flow.
- Full-width listening profile form.
- Dedicated ML prediction section.
- Dedicated YouTube listening section with consistent 16:9 cards.
- Separate videos/songs and playlists.
- Other possible model matches separated from YouTube content.
- Recommendation logic moved to a final section.
- Research and Project pages remain unchanged.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Add a YouTube Data API v3 key in the sidebar under **YouTube connection** for local/demo use, or store it as `YOUTUBE_API_KEY` in Streamlit secrets when deploying.


## V6 UI polish
- Removed empty visual containers from the profile and YouTube sections.
- Tightened the Discover-page hierarchy and spacing.
- Clarified the YouTube retrieval explanation.
- Separated video and playlist search queries for better relevance.
- Improved wording for model alternative matches.
