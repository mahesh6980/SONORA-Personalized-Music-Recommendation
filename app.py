
import json
import html
import time
from pathlib import Path
import joblib
import pandas as pd
import requests
import streamlit as st

# ------------------------------------------------------------
# SONORA — V6
# ------------------------------------------------------------
st.set_page_config(
    page_title="SONORA — Music Intelligence",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
MODEL = joblib.load(ROOT / "sonora_recommendation_model.joblib")
DATA = pd.read_csv(ROOT / "sonora_research_data.csv")
METRICS = json.loads((ROOT / "model_metrics.json").read_text(encoding="utf-8"))

AGE = ["Under 18", "18–20", "21–23", "24+"]
YEAR = ["First Year", "Second Year", "Third Year", "Postgraduate"]
STRESS = ["1 - Very Low", "2 - Low", "3 - Moderate", "4 - High", "5 - Very High"]
MOOD = ["Calm", "Happy", "Neutral", "Tired", "Sad", "Anxious", "Irritated", "Energetic"]
ACTIVITY = ["Studying", "Working", "Travelling", "Relaxing", "Exercising", "Preparing for sleep", "Other"]
WORKLOAD = ["Very Low", "Low", "Moderate", "High", "Very High"]
DURATION = ["Less than 30 minutes", "30–60 minutes", "1–2 hours", "2–4 hours", "More than 4 hours"]
GENRES = [
    "Bollywood / Indian Film Music", "Pop", "Classical", "Lo-fi", "Instrumental",
    "Ambient", "Rock", "Electronic", "Hip-Hop / Rap", "Devotional / Spiritual", "Other"
]
GOALS = ["Relaxation", "Focus / Concentration", "Stress Relief", "Better Mood",
         "Energy / Motivation", "Sleep", "Emotional Comfort", "No Specific Goal"]

SHORT = {
    "Bollywood / Indian Film Music": "Bollywood",
    "Hip-Hop / Rap": "Hip-Hop",
    "Devotional / Spiritual": "Devotional",
}

INFO = {
    "Bollywood / Indian Film Music": ("Familiar • expressive • versatile", "Indian film and soundtrack music with a wide range of moods."),
    "Pop": ("Contemporary • melodic • accessible", "Modern popular music spanning a broad range of moods and energy."),
    "Classical": ("Structured • expressive • reflective", "Indian or Western classical compositions with a strong musical structure."),
    "Lo-fi": ("Soft • atmospheric • low-key", "Relaxed, repetitive and atmospheric listening."),
    "Instrumental": ("Vocal-free • focused • flexible", "Music without prominent vocals for listeners who prefer fewer lyrical distractions."),
    "Ambient": ("Atmospheric • spacious • immersive", "Texture-focused music built around a softer, immersive experience."),
    "Rock": ("Rhythmic • energetic • expressive", "Guitar- and rhythm-oriented music across different energy levels."),
    "Electronic": ("Digital • rhythmic • modern", "Electronically produced music from atmospheric to highly rhythmic."),
    "Hip-Hop / Rap": ("Beat-driven • expressive • energetic", "Rhythm-forward music with strong beats and lyrical expression."),
    "Devotional / Spiritual": ("Reflective • devotional • comforting", "Devotional or spiritually oriented listening."),
    "Other": ("Personal • varied • individual", "A category outside the listed genres."),
}

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root{
  --bg:#08070c; --panel:#111019; --panel2:#161421; --line:rgba(255,255,255,.085);
  --text:#f6f3fa; --muted:#9691a5; --violet:#9b7bff; --violet2:#c6b4ff;
}
.stApp{
  background:
    radial-gradient(850px 500px at 82% -10%,rgba(133,91,255,.16),transparent 60%),
    radial-gradient(600px 420px at 5% 28%,rgba(80,190,180,.045),transparent 62%),
    #08070c;
  color:var(--text);
  font-family:"DM Sans",sans-serif;
}
[data-testid="stHeader"]{background:transparent;}
[data-testid="stToolbar"]{visibility:hidden;}
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#11101a,#0c0b12);
  border-right:1px solid var(--line);
}
.block-container{max-width:1420px;padding:1.8rem 2.5rem 4rem;}
h1,h2,h3{font-family:"Manrope",sans-serif!important;letter-spacing:-.04em;}
h2{font-size:1.45rem!important;} h3{font-size:1.05rem!important;}

.sidebar-brand{padding:8px 4px 22px;}
.logo{
 width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;
 background:linear-gradient(135deg,#aa8aff,#6543dc);font-family:Manrope;font-weight:800;font-size:20px;
 box-shadow:0 12px 30px rgba(112,75,220,.22);
}
.brand{font-family:Manrope;font-size:1.25rem;font-weight:800;margin-top:10px;}
.sub{color:#898496;font-size:.72rem;line-height:1.45;margin-top:2px;}
.side-rule{height:1px;background:var(--line);margin:20px 0;}
.side-kicker{font-size:.65rem;letter-spacing:.16em;text-transform:uppercase;color:#a994ff;font-weight:800;}
.badges{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap;}
.badge{font-size:.65rem;padding:6px 8px;border-radius:999px;border:1px solid var(--line);color:#bdb8c8;background:rgba(255,255,255,.025);}

.hero{
 position:relative;overflow:hidden;border:1px solid var(--line);border-radius:27px;
 padding:36px 44px 34px;margin-bottom:25px;
 background:radial-gradient(circle at 88% 28%,rgba(151,113,255,.18),transparent 30%),
 linear-gradient(135deg,rgba(27,22,42,.96),rgba(13,12,20,.96));
 box-shadow:0 24px 80px rgba(0,0,0,.25);
}
.hero:after{
 content:"";position:absolute;width:350px;height:350px;right:-110px;top:-150px;border-radius:50%;
 border:1px solid rgba(200,180,255,.12);box-shadow:0 0 0 28px rgba(200,180,255,.025),0 0 0 62px rgba(200,180,255,.015);
}
.kicker{font-size:.66rem;letter-spacing:.2em;text-transform:uppercase;color:#b9a2ff;font-weight:800;}
.hero h1{
 font-size:clamp(3.2rem,6vw,5.5rem)!important;line-height:.9!important;margin:12px 0 15px!important;
 background:linear-gradient(100deg,#fff,#cbbcff,#9b83ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero-copy{max-width:780px;color:#bdb8c9;line-height:1.7;font-size:.93rem;}
.hero-tags{display:flex;gap:7px;flex-wrap:wrap;margin-top:20px;}
.tag{padding:6px 9px;border:1px solid var(--line);border-radius:999px;color:#c6c0d2;background:rgba(255,255,255,.03);font-size:.66rem;}

.section-kicker{font-size:.65rem;letter-spacing:.2em;text-transform:uppercase;color:#aa93ff;font-weight:800;}
.section-title{font-family:Manrope;font-size:1.4rem;font-weight:700;margin:5px 0 13px;letter-spacing:-.035em;}

.form-box{
 border:1px solid rgba(255,255,255,.10);border-radius:20px;padding:21px 20px 18px;
 background:linear-gradient(145deg,rgba(255,255,255,.035),rgba(255,255,255,.018));
}
.group-title{
 font-family:Manrope;font-size:.95rem;font-weight:700;margin:1px 0 13px;color:#f2eef8;
}
.group-title span{color:#8e7ad2;font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;margin-left:7px;}
.stButton>button{
 min-height:47px!important;border-radius:12px!important;border:1px solid rgba(194,169,255,.32)!important;
 background:linear-gradient(135deg,#9270f5,#6d4bdc)!important;color:#fff!important;font-weight:700!important;
 box-shadow:0 10px 28px rgba(104,69,214,.20)!important;
}
.stButton>button:hover{transform:translateY(-1px);box-shadow:0 14px 34px rgba(104,69,214,.30)!important;}
[data-baseweb="select"]>div{
 background:#292935!important;border:1px solid rgba(255,255,255,.06)!important;border-radius:10px!important;
}
[data-testid="stForm"]{border:0!important;padding:0!important;}

.engine{
 border:1px solid rgba(185,157,255,.23);border-radius:22px;padding:25px;
 background:radial-gradient(circle at 85% 5%,rgba(151,113,255,.25),transparent 35%),
 linear-gradient(145deg,#292040,#171321);
 min-height:230px;display:flex;flex-direction:column;justify-content:center;
 box-shadow:0 20px 65px rgba(54,31,106,.17);
}
.engine-label{font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:#b9a6d2;font-weight:800;}
.engine-title{font-family:Manrope;font-size:2rem;font-weight:800;letter-spacing:-.045em;margin:7px 0 10px;}
.engine-copy{color:#bdb7c8;line-height:1.65;font-size:.82rem;}
.engine-points{display:flex;gap:6px;flex-wrap:wrap;margin-top:16px;}
.engine-point{font-size:.63rem;color:#c9c1d7;border:1px solid rgba(255,255,255,.09);padding:6px 8px;border-radius:999px;}

.result{
 border:1px solid rgba(190,165,255,.26);border-radius:22px;padding:24px;
 background:radial-gradient(circle at 82% 12%,rgba(157,117,255,.30),transparent 40%),linear-gradient(145deg,#2a2042,#17131f);
 box-shadow:0 22px 65px rgba(58,35,110,.20);
}
.result-label{font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:#c0afd9;font-weight:800;}
.result-name{font-family:Manrope;font-size:2.15rem;font-weight:800;letter-spacing:-.045em;margin:6px 0;}
.result-desc{font-size:.82rem;color:#bdb6c8;line-height:1.6;}
.prob{margin-top:18px;padding:12px 14px;border-radius:13px;background:rgba(0,0,0,.17);border:1px solid rgba(255,255,255,.06);}
.prob-row{display:flex;justify-content:space-between;font-size:.68rem;color:#aaa4b4;margin-bottom:7px;}
.bar{height:6px;border-radius:999px;background:#2b2636;overflow:hidden;}
.fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#8664eb,#c1aaff);}
.alt-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px;}
.alt{border:1px solid var(--line);border-radius:14px;padding:12px;background:rgba(255,255,255,.025);}
.alt-name{font-size:.67rem;color:#9d97aa;}
.alt-value{font-family:Manrope;font-size:1.2rem;font-weight:800;margin-top:3px;}

.logic-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
.logic{
 border:1px solid var(--line);border-radius:18px;padding:18px;background:rgba(255,255,255,.025);
 min-height:135px;
}
.num{font-size:.62rem;letter-spacing:.15em;color:#a994ff;font-weight:800;}
.logic h3{margin:8px 0 7px!important;}
.logic p{font-size:.76rem;line-height:1.6;color:#8f899d;margin:0;}

.metric-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;}
.metric{border:1px solid var(--line);border-radius:18px;padding:17px 18px;background:rgba(255,255,255,.025);}
.metric-value{font-family:Manrope;font-size:1.5rem;font-weight:800;}
.metric-label{font-size:.62rem;letter-spacing:.13em;text-transform:uppercase;color:#8e899a;margin-top:4px;line-height:1.4;}

.data-section{border:1px solid var(--line);border-radius:20px;padding:20px;background:rgba(255,255,255,.018);}
.data-title{font-family:Manrope;font-size:1rem;font-weight:700;margin-bottom:16px;}
.data-row{margin:13px 0;}
.data-head{display:flex;justify-content:space-between;font-size:.68rem;color:#b4aebe;margin-bottom:6px;}
.data-track{height:7px;border-radius:99px;background:#26222e;overflow:hidden;}
.data-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#7654df,#a889ff);}

.research-note{
 margin-top:16px;padding:13px 15px;border-left:3px solid #9171ed;background:rgba(145,113,237,.055);
 color:#aaa4b4;border-radius:0 12px 12px 0;font-size:.73rem;line-height:1.6;
}
.footer{text-align:center;color:#5f5a69;font-size:.64rem;margin-top:28px;}


/* V5 — Discover page hierarchy + YouTube presentation */
.discovery-block{margin-top:4px;}
.discovery-divider{height:1px;background:linear-gradient(90deg,rgba(169,139,255,.25),rgba(255,255,255,.05),transparent);margin:30px 0 28px;}
.prediction-wide{
 border:1px solid rgba(190,165,255,.26);border-radius:24px;padding:28px 30px;
 background:radial-gradient(circle at 88% 8%,rgba(157,117,255,.28),transparent 34%),linear-gradient(145deg,#2a2042,#15111d);
 box-shadow:0 22px 65px rgba(58,35,110,.20);
}
.prediction-head{display:flex;justify-content:space-between;align-items:flex-start;gap:24px;}
.prediction-main{min-width:0;}
.prediction-side{min-width:260px;max-width:330px;width:30%;}
.prediction-kicker{font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;color:#c0afd9;font-weight:800;}
.prediction-name{font-family:Manrope;font-size:2.45rem;font-weight:800;letter-spacing:-.05em;margin:6px 0 7px;}
.prediction-desc{font-size:.82rem;color:#bdb6c8;line-height:1.65;max-width:720px;}
.prediction-tags{display:flex;gap:7px;flex-wrap:wrap;margin-top:14px;}
.prediction-tag{font-size:.64rem;color:#d1c8df;border:1px solid rgba(255,255,255,.09);padding:6px 9px;border-radius:999px;background:rgba(255,255,255,.025);}
.yt-shell{
 border:1px solid var(--line);border-radius:24px;padding:24px 24px 26px;
 background:linear-gradient(145deg,rgba(255,255,255,.028),rgba(255,255,255,.012));
}
.yt-intro{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:18px;}
.yt-heading{font-family:Manrope;font-size:1.28rem;font-weight:700;letter-spacing:-.035em;}
.yt-sub{color:#8f899d;font-size:.74rem;line-height:1.55;max-width:680px;margin-top:4px;}
.yt-live{font-size:.62rem;letter-spacing:.13em;text-transform:uppercase;color:#bfe7cf;border:1px solid rgba(120,220,160,.18);padding:6px 9px;border-radius:999px;white-space:nowrap;}
.yt-context{padding:11px 13px;border-left:3px solid #9171ed;background:rgba(145,113,237,.055);color:#aaa4b4;border-radius:0 11px 11px 0;font-size:.70rem;line-height:1.55;margin-bottom:18px;}
.yt-group-label{font-family:Manrope;font-size:.88rem;font-weight:700;margin:20px 0 11px;}
.yt-card{height:100%;border:1px solid rgba(255,255,255,.085);border-radius:16px;overflow:hidden;background:#0f0e15;display:flex;flex-direction:column;box-shadow:0 10px 30px rgba(0,0,0,.14);}
.yt-thumb{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#18151f;}
.yt-body{padding:12px 13px 13px;display:flex;flex-direction:column;flex:1;min-height:145px;}
.yt-title{font-family:Manrope;font-size:.78rem;font-weight:700;line-height:1.35;color:#f4f0f8;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
.yt-meta{color:#898394;font-size:.63rem;line-height:1.4;margin-top:6px;}
.yt-button{display:inline-block;margin-top:auto;padding-top:10px;}
.yt-button a{display:inline-block;padding:7px 10px;border:1px solid rgba(194,169,255,.28);border-radius:9px;color:#d7caff;text-decoration:none;font-size:.66rem;transition:.15s ease;}
.yt-button a:hover{background:rgba(151,113,255,.12);border-color:rgba(194,169,255,.5);}
.empty-engine{margin-top:4px;}
@media(max-width:900px){
 .prediction-head{flex-direction:column;}
 .prediction-side{width:100%;max-width:none;min-width:0;}
 .yt-intro{align-items:flex-start;flex-direction:column;}
 .yt-live{white-space:normal;}
}


/* V6 — final polish */
[data-testid="stForm"]{
  border:0!important;
  padding:0!important;
  background:transparent!important;
  box-shadow:none!important;
}
.profile-area{
  padding:0;
}
.yt-intro-card{
  border:1px solid var(--line);
  border-radius:18px;
  padding:18px 19px;
  background:linear-gradient(145deg,rgba(255,255,255,.028),rgba(255,255,255,.012));
  margin-bottom:18px;
}
.yt-context-v6{
  padding:11px 13px;
  border-left:3px solid #9171ed;
  background:rgba(145,113,237,.055);
  color:#aaa4b4;
  border-radius:0 11px 11px 0;
  font-size:.70rem;
  line-height:1.55;
  margin-bottom:18px;
}
.yt-group-label{
  margin-top:22px;
}
@media(max-width:900px){
  .prediction-name{font-size:2rem;}
}

@media(max-width:900px){
 .block-container{padding:1rem 1rem 3rem;}
 .hero{padding:28px 25px;}
 .metric-row{grid-template-columns:repeat(2,1fr);}
 .logic-grid{grid-template-columns:1fr;}
 .alt-grid{grid-template-columns:1fr;}
}
</style>
""", unsafe_allow_html=True)

def short(g): return SHORT.get(g, g)

def info(g): return INFO.get(g, ("Personalized match","A category selected from the learned research patterns."))

def make_input(vals):
    return pd.DataFrame([{
        "Age_Group": vals[0],
        "Study_Year": vals[1],
        "Stress_Level": vals[2],
        "Current_Mood": vals[3],
        "Current_Activity": vals[4],
        "Academic_Workload": vals[5],
        "Music_Duration": vals[6],
        "Preferred_Genre": vals[7],
        "Music_Goal": vals[8],
    }])

def predict(x):
    pred = MODEL.predict(x)[0]
    probs = MODEL.predict_proba(x)[0] if hasattr(MODEL, "predict_proba") else None
    return pred, probs

# ------------------------------------------------------------
# YouTube recommendation layer
# ------------------------------------------------------------
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

GOAL_QUERY = {
    "Relaxation": "relaxing",
    "Focus / Concentration": "focus study",
    "Stress Relief": "calm stress relief",
    "Better Mood": "feel good",
    "Energy / Motivation": "motivation energetic",
    "Sleep": "sleep",
    "Emotional Comfort": "comforting",
    "No Specific Goal": "music",
}

ACTIVITY_QUERY = {
    "Studying": "study", "Working": "work", "Travelling": "travel",
    "Relaxing": "relaxing", "Exercising": "workout",
    "Preparing for sleep": "sleep", "Other": "",
}

def get_youtube_key():
    # A session key intentionally takes precedence over Streamlit secrets so a
    # user can replace a bad deployment/local key without editing the app.
    session_key = st.session_state.get("youtube_api_key", "").strip()
    if session_key:
        return session_key
    try:
        secret_key = st.secrets.get("YOUTUBE_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key.strip() if secret_key else ""


def clear_youtube_cache():
    st.session_state.pop("youtube_result_cache", None)
    st.session_state.pop("youtube_last_query", None)


def validate_youtube_key(candidate):
    """Validate a key with one minimal public search request before saving it."""
    candidate = (candidate or "").strip()
    if not candidate:
        return False, "Enter a YouTube Data API key first."
    params = {
        "part": "snippet",
        "q": "SONORA music",
        "type": "video",
        "maxResults": 1,
        "key": candidate,
    }
    try:
        r = requests.get(YOUTUBE_API_URL, params=params, timeout=10)
        if r.status_code == 200:
            return True, "YouTube connection verified."
        try:
            err = r.json().get("error", {})
            errors = err.get("errors", []) or []
            reason = errors[0].get("reason", "") if errors else ""
            message = err.get("message", "YouTube API request failed")
        except Exception:
            reason, message = "", "YouTube API request failed"
        if reason == "quotaExceeded":
            return False, "The API key is valid, but the YouTube API quota has been exceeded."
        if reason in {"keyInvalid", "badRequest"} or r.status_code == 400:
            return False, "This API key was rejected by YouTube. Check the key and make sure YouTube Data API v3 is enabled."
        if r.status_code == 403:
            return False, "YouTube rejected this key. Check API restrictions, project settings, or quota."
        return False, message
    except requests.RequestException:
        return False, "Could not reach YouTube right now. Check your internet connection and try again."


def save_youtube_key(candidate):
    ok, message = validate_youtube_key(candidate)
    if ok:
        st.session_state["youtube_api_key"] = candidate.strip()
        st.session_state["youtube_key_status"] = (True, message)
        clear_youtube_cache()
    else:
        st.session_state["youtube_key_status"] = (False, message)


def youtube_search(query, resource_type, max_results=3):
    key = get_youtube_key()
    if not key:
        return {"error": "No YouTube API key is configured."}

    # Small in-session cache prevents repeated Generate clicks from burning
    # YouTube quota for the same query while keeping the API key out of cache data.
    cache = st.session_state.setdefault("youtube_result_cache", {})
    cache_key = (query, resource_type, max_results)
    cached = cache.get(cache_key)
    if cached and time.time() - cached["time"] < 600:
        return cached["value"]

    params = {
        "part": "snippet", "q": query, "type": resource_type,
        "maxResults": max_results, "order": "relevance", "regionCode": "IN",
        "relevanceLanguage": "en", "safeSearch": "moderate", "key": key,
    }
    try:
        r = requests.get(YOUTUBE_API_URL, params=params, timeout=12)
        if r.status_code != 200:
            try:
                err = r.json().get("error", {})
                errors = err.get("errors", []) or []
                reason = errors[0].get("reason", "") if errors else ""
                detail = err.get("message", "YouTube API request failed")
            except Exception:
                reason, detail = "", "YouTube API request failed"
            if reason == "quotaExceeded":
                detail = "YouTube API quota has been exceeded. Try again later or use a project with available quota."
            elif reason in {"keyInvalid", "badRequest"} or r.status_code == 400:
                detail = "The saved YouTube API key is invalid or rejected. Use 'Change YouTube API key' in the sidebar."
                st.session_state["youtube_key_status"] = (False, detail)
            elif r.status_code == 403:
                detail = "YouTube rejected the API request. Check API restrictions, project settings, or quota."
                st.session_state["youtube_key_status"] = (False, detail)
            return {"error": detail, "reason": reason, "status": r.status_code}
        results=[]
        for item in r.json().get("items", []):
            sid=item.get("id",{}); snippet=item.get("snippet",{})
            rid=sid.get("videoId") if resource_type=="video" else sid.get("playlistId")
            url=(f"https://www.youtube.com/watch?v={rid}" if resource_type=="video" else f"https://www.youtube.com/playlist?list={rid}") if rid else ""
            thumbs=snippet.get("thumbnails",{})
            thumb=(thumbs.get("high") or thumbs.get("medium") or thumbs.get("default") or {}).get("url","")
            if rid and url:
                results.append({"title":snippet.get("title","YouTube recommendation"),"channel":snippet.get("channelTitle","YouTube"),"thumbnail":thumb,"url":url})
        cache[cache_key] = {"time": time.time(), "value": results}
        return results
    except requests.RequestException:
        return {"error": "Could not reach YouTube right now. Check your internet connection and try again."}

def build_youtube_query(genre, goal, activity, resource_type="video"):
    genre_term={
        "Bollywood / Indian Film Music":"Bollywood Hindi songs",
        "Hip-Hop / Rap":"hip hop rap music",
        "Devotional / Spiritual":"devotional spiritual music",
        "Lo-fi":"lofi music",
        "Instrumental":"instrumental music",
        "Ambient":"ambient music",
        "Classical":"classical music",
        "Rock":"rock music",
        "Pop":"pop music",
        "Electronic":"electronic music",
    }.get(genre,genre)
    goal_term=GOAL_QUERY.get(goal,"music")
    activity_term=ACTIVITY_QUERY.get(activity,"")
    parts=[genre_term, goal_term]
    if activity_term:
        parts.append(activity_term)
    if resource_type == "video":
        parts.append("songs")
    else:
        parts.append("playlist")
    return " ".join(parts)

def youtube_recommendations(genre, goal, activity):
    video_query=build_youtube_query(genre,goal,activity,"video")
    playlist_query=build_youtube_query(genre,goal,activity,"playlist")
    return video_query, playlist_query, youtube_search(video_query,"video",3), youtube_search(playlist_query,"playlist",3)

def render_youtube_card(item,label):
    title=html.escape(item.get("title","YouTube recommendation"))
    channel=html.escape(item.get("channel","YouTube"))
    url=html.escape(item.get("url","#"), quote=True)
    thumb=html.escape(item.get("thumbnail",""), quote=True)
    image_html=f"<img class='yt-thumb' src='{thumb}' alt='' loading='lazy'>" if thumb else "<div class='yt-thumb'></div>"
    st.markdown(f"""
    <div class="yt-card">
      {image_html}
      <div class="yt-body">
        <div class="yt-title">{title}</div>
        <div class="yt-meta">{html.escape(label)} · {channel}</div>
        <div class="yt-button"><a href="{url}" target="_blank" rel="noopener noreferrer">Open on YouTube ↗</a></div>
      </div>
    </div>
    """,unsafe_allow_html=True)

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="logo">S</div>
      <div class="brand">SONORA</div>
      <div class="sub">Music intelligence for student wellbeing research.</div>
    </div>
    """, unsafe_allow_html=True)
    page = st.radio("Navigation", ["Discover","Research","Project"], label_visibility="collapsed")
    st.markdown('<div class="side-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-kicker">Research snapshot</div>', unsafe_allow_html=True)
    st.markdown('<div class="badges"><span class="badge">501 responses</span><span class="badge">ML prototype</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px"></div><div class="sub">Academic research prototype • SONORA</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-kicker">YouTube connection</div>', unsafe_allow_html=True)
    current_key = get_youtube_key()
    status = st.session_state.get("youtube_key_status")
    # If a key came from Streamlit secrets, treat it as configured but still
    # validate it lazily when the first live search is made.
    if current_key:
        if status and status[0] is False:
            st.markdown('<div class="badge" style="display:inline-block;margin-top:8px;color:#ffb4b4;border-color:rgba(255,110,110,.25)">API key needs attention</div>',unsafe_allow_html=True)
        elif status and status[0] is True:
            st.markdown('<div class="badge" style="display:inline-block;margin-top:8px;color:#bfe7cf;border-color:rgba(120,220,160,.20)">API verified</div>',unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge" style="display:inline-block;margin-top:8px;color:#d1c8df;border-color:rgba(255,255,255,.10)">API key configured</div>',unsafe_allow_html=True)
        expander_label = "Change YouTube API key"
    else:
        expander_label = "Add YouTube API key"

    with st.expander(expander_label, expanded=bool(status and status[0] is False)):
        st.caption("Enter a key and validate it before SONORA saves it. For deployment, store YOUTUBE_API_KEY in Streamlit secrets.")
        yt_key=st.text_input("YouTube Data API key",type="password",key="youtube_key_input",placeholder="AIza…")
        if st.button("Validate & connect", use_container_width=True, key="validate_youtube_key"):
            save_youtube_key(yt_key)
            st.rerun()
        if status:
            if status[0]:
                st.success(status[1])
            else:
                st.error(status[1])
        st.caption("A rejected key is not saved. Your previous valid key remains unchanged until a replacement is verified.")

# ============================================================
# DISCOVER
# ============================================================
if page == "Discover":
    st.markdown("""
    <div class="hero">
      <div class="kicker">Personalized music intelligence</div>
      <h1>SONORA</h1>
      <div class="hero-copy">
        A research-driven recommendation experience connecting your current state,
        academic context and listening habits with patterns learned from student responses.
      </div>
      <div class="hero-tags">
        <span class="tag">501 unique responses</span><span class="tag">Multiclass ML</span>
        <span class="tag">Student research</span><span class="tag">Music • Mood • Context</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">01 / Listening profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Build your current listening profile</div>', unsafe_allow_html=True)

    st.markdown('<div class="group-title">Your context <span>current state</span></div>', unsafe_allow_html=True)
    a,b=st.columns(2, gap="large")
    with a:
        age=st.selectbox("Age group", AGE)
        year=st.selectbox("Study year", YEAR)
        stress=st.selectbox("Current stress", STRESS, index=2)
        mood=st.selectbox("Current mood", MOOD, index=2)
    with b:
        activity=st.selectbox("Current activity", ACTIVITY)
        workload=st.selectbox("Academic workload", WORKLOAD, index=2)
        duration=st.selectbox("Daily music time", DURATION, index=1)
        genre=st.selectbox("Usual genre", GENRES)
    st.markdown('<div class="group-title" style="margin-top:12px">Listening intention <span>what you want</span></div>', unsafe_allow_html=True)
    goal=st.selectbox("Music goal", GOALS)
    submitted=st.button("Generate recommendation  →", use_container_width=True)

    if submitted:
        x=make_input([age,year,stress,mood,activity,workload,duration,genre,goal])
        pred,probs=predict(x)
        descriptor,description=info(pred)
        pairs=sorted(zip(MODEL.classes_,probs),key=lambda z:z[1],reverse=True)[:3]
        top_prob=float(pairs[0][1])

        st.markdown('<div class="discovery-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">02 / SONORA prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your SONORA recommendation</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="prediction-wide">
          <div class="prediction-head">
            <div class="prediction-main">
              <div class="prediction-kicker">SONORA recommendation</div>
              <div class="prediction-name">♬ {html.escape(short(pred))}</div>
              <div style="color:#c1afd8;font-size:.73rem;font-weight:700">{html.escape(descriptor)}</div>
              <div class="prediction-desc" style="margin-top:8px">{html.escape(description)}</div>
              <div class="prediction-tags">
                <span class="prediction-tag">{html.escape(short(pred))}</span>
                <span class="prediction-tag">{html.escape(goal)}</span>
                <span class="prediction-tag">{html.escape(activity)}</span>
              </div>
            </div>
            <div class="prediction-side">
              <div class="prob">
                <div class="prob-row"><span>Top predicted probability</span><strong>{top_prob*100:.1f}%</strong></div>
                <div class="bar"><div class="fill" style="width:{top_prob*100:.1f}%"></div></div>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">03 / Your listening picks</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Actual songs & playlists from YouTube</div>', unsafe_allow_html=True)
        yt_video_query,yt_playlist_query,yt_videos,yt_playlists=youtube_recommendations(pred,goal,activity)

        st.markdown(f"""
        <div class="yt-intro-card">
          <div class="yt-intro">
            <div>
              <div class="yt-heading">Live YouTube recommendations</div>
              <div class="yt-sub">SONORA searches YouTube using your predicted genre, music goal and current activity.</div>
            </div>
            <div class="yt-live">Live content retrieval</div>
          </div>
          <div class="yt-context-v6"><strong>Why these picks?</strong><br>{html.escape(short(pred))} · {html.escape(goal)} · {html.escape(activity)}</div>
        </div>
        """, unsafe_allow_html=True)
        if not get_youtube_key():
            st.markdown("<div class='research-note'>Add a YouTube Data API key in the sidebar to load live songs and playlists.</div>",unsafe_allow_html=True)
        else:
            video_error = yt_videos.get("error") if isinstance(yt_videos,dict) else None
            playlist_error = yt_playlists.get("error") if isinstance(yt_playlists,dict) else None

            # A bad key can be detected here even when it came from Streamlit secrets.
            if video_error and isinstance(yt_videos,dict) and yt_videos.get("reason") in {"keyInvalid","badRequest"}:
                st.error(video_error + " Open 'Change YouTube API key' in the sidebar to replace it.")
            if video_error and not (isinstance(yt_videos,dict) and yt_videos.get("reason") in {"keyInvalid","badRequest"}):
                st.error(f"Videos: {video_error}")
            if playlist_error and not (isinstance(yt_playlists,dict) and yt_playlists.get("reason") in {"keyInvalid","badRequest"}):
                st.error(f"Playlists: {playlist_error}")

            if isinstance(yt_videos,list) and yt_videos:
                st.markdown('<div class="yt-group-label">Videos & songs</div>',unsafe_allow_html=True)
                vcols=st.columns(3, gap="medium")
                for col,item in zip(vcols,yt_videos):
                    with col: render_youtube_card(item,"Song / video")
            if isinstance(yt_playlists,list) and yt_playlists:
                st.markdown('<div class="yt-group-label">Playlists</div>',unsafe_allow_html=True)
                pcols=st.columns(3, gap="medium")
                for col,item in zip(pcols,yt_playlists):
                    with col: render_youtube_card(item,"Playlist")
            if not (isinstance(yt_videos,list) and yt_videos) and not (isinstance(yt_playlists,list) and yt_playlists) and not video_error and not playlist_error:
                st.markdown("<div class='research-note'>No YouTube results were returned for this combination. Try another music goal or activity.</div>",unsafe_allow_html=True)

        st.markdown('<div style="height:22px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">04 / Other possible matches</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Other possible matches</div>', unsafe_allow_html=True)
        st.markdown('<div class="yt-sub" style="margin-bottom:12px">The next highest-probability genres from the model.</div>', unsafe_allow_html=True)
        cols=st.columns(3, gap="medium")
        for col,(g,p) in zip(cols,pairs):
            with col:
                st.markdown(f"""
                <div class="alt" style="min-height:92px">
                  <div class="alt-name">{html.escape(short(g))}</div>
                  <div class="alt-value">{p*100:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="discovery-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="empty-engine">', unsafe_allow_html=True)
        st.markdown('<div class="section-kicker">02 / SONORA prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your recommendation will appear here</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="engine">
          <div class="engine-label">SONORA engine</div>
          <div class="engine-title">Find your sound.</div>
          <div class="engine-copy">
            Complete the profile. The trained research model will translate your current context
            into a music-category recommendation, then connect that result to live YouTube listening options.
          </div>
          <div class="engine-points">
            <span class="engine-point">Stress</span><span class="engine-point">Mood</span>
            <span class="engine-point">Workload</span><span class="engine-point">Preferences</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="discovery-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">05 / Recommendation logic</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Three layers behind the recommendation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="logic-grid">
      <div class="logic"><div class="num">01</div><h3>Context</h3><p>Stress, mood, workload and activity describe the current situation.</p></div>
      <div class="logic"><div class="num">02</div><h3>Preference</h3><p>Usual genre, listening time and music goal add the personal layer.</p></div>
      <div class="logic"><div class="num">03</div><h3>Pattern</h3><p>A multiclass classifier learns genre-choice patterns from the survey data.</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="research-note">
    SONORA is a research recommendation prototype. It does not diagnose stress,
    provide medical advice, or claim that a music category will reduce stress for every listener.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RESEARCH
# ============================================================
elif page == "Research":
    st.markdown("""
    <div class="hero">
      <div class="kicker">Behind the recommendation</div>
      <h1>Research</h1>
      <div class="hero-copy">The evidence layer of SONORA — 501 unique student responses,
      exploratory analysis and multiclass model evaluation.</div>
    </div>
    """, unsafe_allow_html=True)

    high=((DATA["Stress_Level"].isin(["4 - High","5 - Very High"])).mean()*100)
    stress_genre=DATA["Stress_Genre"].value_counts()
    goal_counts=DATA["Music_Goal"].value_counts()
    most_genre=stress_genre.idxmax()
    most_goal=goal_counts.idxmax()

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric"><div class="metric-value">501</div><div class="metric-label">unique responses</div></div>
      <div class="metric"><div class="metric-value">{high:.1f}%</div><div class="metric-label">high / very high stress</div></div>
      <div class="metric"><div class="metric-value">{short(most_genre)}</div><div class="metric-label">most chosen under stress</div></div>
      <div class="metric"><div class="metric-value">{most_goal}</div><div class="metric-label">most common music goal</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:17px"></div>', unsafe_allow_html=True)
    left,right=st.columns(2,gap="large")

    with left:
        st.markdown('<div class="data-section"><div class="data-title">Stress distribution</div>', unsafe_allow_html=True)
        s_order=["1 - Very Low","2 - Low","3 - Moderate","4 - High","5 - Very High"]
        s_counts=DATA["Stress_Level"].value_counts().reindex(s_order).fillna(0)
        mx=max(s_counts)
        labels=["Very Low","Low","Moderate","High","Very High"]
        for lab,val in zip(labels,s_counts):
            pct=float(val/mx*100)
            st.markdown(f"""
            <div class="data-row"><div class="data-head"><span>{lab}</span><strong>{int(val)}</strong></div>
            <div class="data-track"><div class="data-fill" style="width:{pct:.1f}%"></div></div></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with right:
        st.markdown('<div class="data-section"><div class="data-title">Genres selected under stress</div>', unsafe_allow_html=True)
        g=stress_genre.sort_values(ascending=False).head(8)
        mx=max(g)
        for name,val in reversed(list(g.items())):
            pct=float(val/mx*100)
            st.markdown(f"""
            <div class="data-row"><div class="data-head"><span>{short(name)}</span><strong>{int(val)}</strong></div>
            <div class="data-track"><div class="data-fill" style="width:{pct:.1f}%"></div></div></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div style="height:22px"></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Model evaluation</div>',unsafe_allow_html=True)
    rows=[]
    for name,v in METRICS.items():
        rows.append([name,f"{v['accuracy']*100:.1f}%",f"{v['weighted_f1']:.3f}",f"{v['macro_f1']:.3f}"])
    table=pd.DataFrame(rows,columns=["Model","Accuracy","Weighted F1","Macro F1"])
    st.dataframe(table,use_container_width=True,hide_index=True)
    st.markdown("""
    <div class="research-note">
    Scores are specific to this research dataset and held-out test split. They do not establish
    that the prototype will generalize to every student population.
    </div>
    """,unsafe_allow_html=True)

# ============================================================
# PROJECT
# ============================================================
else:
    st.markdown("""
    <div class="hero">
      <div class="kicker">Project intelligence</div>
      <h1>SONORA /</h1>
      <div class="hero-copy">Personalized Music Recommendation for Student Stress & Well-being</div>
    </div>
    """,unsafe_allow_html=True)

    left,right=st.columns([1.12,.88],gap="large")
    with left:
        st.markdown('<div class="section-title">What the project does</div>',unsafe_allow_html=True)
        st.markdown("""
        <div class="data-section" style="min-height:170px">
        <p style="color:#c5bfce;line-height:1.75;font-size:.83rem;margin-top:0">
        SONORA is a B.Sc. Data Science research prototype studying how
        student-reported stress, mood, academic workload and music preferences
        can be used to recommend a music category.
        </p>
        <p style="color:#c5bfce;line-height:1.75;font-size:.83rem;margin-bottom:0">
        The prediction target is the <strong>genre usually chosen when stressed</strong>.
        Multiple classification algorithms are compared before integrating the selected model.
        </p>
        </div>
        """,unsafe_allow_html=True)

        st.markdown('<div style="height:18px"></div><div class="section-title">Research boundaries</div>',unsafe_allow_html=True)
        st.markdown("""
        <div class="data-section">
        <div style="color:#aaa4b3;font-size:.78rem;line-height:1.8">
        <div>• Self-reported stress is not a clinical diagnosis.</div>
        <div>• The project identifies patterns, not universal effects of music.</div>
        <div>• The survey sample may not represent all student populations.</div>
        <div>• Recommendations are suggestions rather than guarantees.</div>
        </div></div>
        """,unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">Current model</div>',unsafe_allow_html=True)
        best=METRICS["Random Forest"]
        st.markdown(f"""
        <div class="metric">
          <div class="side-kicker">Random Forest</div>
          <div class="metric-value" style="font-size:2rem;margin-top:5px">{best["accuracy"]*100:.1f}%</div>
          <div class="metric-label">test accuracy</div>
          <div style="height:13px"></div>
          <div style="color:#aaa4b4;font-size:.75rem;line-height:1.8">
          Weighted F1: <strong>{best["weighted_f1"]:.3f}</strong><br>
          Macro F1: <strong>{best["macro_f1"]:.3f}</strong>
          </div>
        </div>
        """,unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div><div class="section-title">YouTube recommendation layer</div>',unsafe_allow_html=True)
        st.markdown("<div class='metric'><div class='metric-value' style='font-size:1.15rem'>Genre → YouTube</div><div class='metric-label'>live content retrieval</div><div style='height:8px'></div><div style='color:#aaa4b4;font-size:.75rem;line-height:1.7'>The model predicts the music genre first. SONORA then builds a search from genre, music goal and activity to retrieve relevant public YouTube videos and playlists.</div></div>",unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div><div class="section-title">Research dataset</div>',unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric">
          <div class="metric-value" style="font-size:2rem">501</div>
          <div class="metric-label">unique responses</div>
          <div style="height:11px"></div>
          <div style="color:#aaa4b4;font-size:.75rem;line-height:1.7">
          10 questionnaire items · categorical survey data · multiclass target
          </div>
        </div>
        """,unsafe_allow_html=True)

st.markdown('<div class="footer">SONORA · B.Sc. Data Science Research Project · Academic Research Prototype</div>',unsafe_allow_html=True)
