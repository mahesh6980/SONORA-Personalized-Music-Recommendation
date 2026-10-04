# SONORA V7 — YouTube setup

1. Create/choose a Google Cloud project.
2. Enable **YouTube Data API v3**.
3. Create an API key under APIs & Services → Credentials.
4. Restrict the key to **YouTube Data API v3** where practical.
5. Run SONORA with `streamlit run app.py`.
6. In the left sidebar, open **YouTube connection → Add YouTube API key**.
7. Paste the key and click **Validate & connect**.
8. SONORA only saves the key after YouTube accepts a test request. If validation fails, the rejected key is not saved and you can try another key.
9. If a key is already configured, use **Change YouTube API key** to replace it. A new key is not saved until it is verified.

For deployment, do not hard-code the key. Add:

```toml
YOUTUBE_API_KEY = "your-key-here"
```

to Streamlit secrets instead.

## V7 bug fixes / hardening

- API keys are no longer treated as valid merely because a non-empty string was entered.
- Invalid keys can be replaced without restarting the app.
- Previously valid keys are preserved if a replacement key fails validation.
- Live YouTube results are cached for 10 minutes per query during the current session to reduce repeated quota usage from accidental repeated clicks.
- Video and playlist errors are handled independently, so one failed request does not hide successful results from the other.
- YouTube API quota, invalid-key, restriction, and network errors receive clearer user-facing messages.
- The existing V6 visual hierarchy and styling are preserved.
