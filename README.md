# 🎵 SONORA — Personalized Music Recommendation for Student Stress & Well-being

> A research-driven music recommendation system that uses student context,
> stress level, mood, academic workload, and listening preferences to
> recommend a music genre and relevant YouTube content.

[🚀 Live Demo](https://sonora-music.streamlit.app/) •
[📂 GitHub Repository](https://github.com/mahesh6980/SONORA-Personalized-Music-Recommendation)

---

## 📌 Project Overview

SONORA is a B.Sc. Data Science research project designed to explore
personalized music recommendation in the context of student stress and
well-being.

The system uses questionnaire responses from **501 unique student
responses** and applies machine learning to predict the music genre
associated with a student's current context.

The predicted genre is then combined with the user's music goal and
current activity to retrieve relevant YouTube videos and playlists.

> **Important:** SONORA is a research prototype. It is not a medical
> diagnostic system and does not claim that any particular genre reduces
> stress.

---

## 🎯 Problem Statement

Students experience different levels of academic stress and may use music
for purposes such as relaxation, stress relief, concentration, emotional
comfort, or motivation.

Traditional music recommendation systems generally focus on listening
history and preferences. SONORA explores whether additional contextual
information such as:

- Stress level
- Current mood
- Academic workload
- Current activity
- Study year
- Music duration
- Preferred genre
- Music goal

can be incorporated into a personalized recommendation workflow.

---

## 💡 Objectives

- Analyze music-listening patterns among students.
- Study associations between academic context, mood, stress and music choices.
- Develop a machine-learning-based genre recommendation model.
- Compare multiple classification algorithms.
- Integrate the recommendation system with YouTube.
- Provide an interactive Streamlit application.
- Present the research findings through an accessible dashboard.

---

## ⚙️ How SONORA Works

```text
Student Profile
      ↓
Data Preprocessing
      ↓
Random Forest Model
      ↓
Predicted Music Genre
      ↓
Music Goal + Current Activity
      ↓
YouTube Search
      ↓
Personalized Videos & Playlists
