import os
import json
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


st.set_page_config(
    page_title="HPI AI | Human Potential Identifier",
    page_icon="HPI",
    layout="wide",
    initial_sidebar_state="expanded",
)


API_BASE_URL = os.getenv("HPI_API_BASE_URL", "http://localhost:8000")
API_URL = os.getenv("HPI_API_URL", f"{API_BASE_URL}/api/dashboard")
AGENT_URL = os.getenv("HPI_AGENT_URL", f"{API_BASE_URL}/api/agent/chat")
REFLECTION_URL = os.getenv("HPI_REFLECTION_URL", f"{API_BASE_URL}/api/reflection")
SCAN_URL = os.getenv("HPI_SCAN_URL", f"{API_BASE_URL}/api/potential-scan")

PAGES = [
    "Landing",
    "Potential Scan",
    "Executive Dashboard",
    "Potential Analysis",
    "Career Intelligence",
    "AI Agent",
    "Learning Style",
    "Roadmap",
    "Project Ideas",
    "Reflection & Growth",
    "Privacy & Ethics",
]


DEMO_DATA = {
    "profile": {
        "name": "Vamsi",
        "role": "Aspiring Data Science, Machine Learning, and AI Engineer",
        "goal": "Become an AI Engineer with strong ML and Data Science foundations",
        "skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "scikit-learn",
            "FastAPI",
            "Streamlit",
            "Machine Learning",
            "AI Agents",
        ],
        "interests": ["AI agents", "Machine Learning", "Data Science", "Career Growth"],
    },
    "kpis": {
        "Human Potential Score": {"value": 88, "delta": "+12%", "accent": "#7C3AED"},
        "Career Confidence": {"value": 91, "delta": "+9%", "accent": "#06B6D4"},
        "Learning Style Match": {"value": 84, "delta": "+7%", "accent": "#A855F7"},
        "Roadmap Completion": {"value": 62, "delta": "+18%", "accent": "#22C55E"},
        "Skill Growth": {"value": 76, "delta": "+14%", "accent": "#06B6D4"},
        "Reflection Consistency": {"value": 69, "delta": "+6%", "accent": "#F59E0B"},
    },
    "potential": {
        "Technical": 92,
        "Creative": 78,
        "Leadership": 74,
        "Business": 71,
        "Research": 82,
        "Communication": 80,
    },
    "growth": [
        {"week": "W1", "Python": 68, "AI Agents": 40, "Product": 42},
        {"week": "W2", "Python": 72, "AI Agents": 48, "Product": 46},
        {"week": "W3", "Python": 78, "AI Agents": 59, "Product": 54},
        {"week": "W4", "Python": 82, "AI Agents": 67, "Product": 61},
        {"week": "W5", "Python": 86, "AI Agents": 74, "Product": 68},
        {"week": "W6", "Python": 89, "AI Agents": 81, "Product": 72},
    ],
    "careers": [
        {
            "title": "AI Engineer",
            "match": 94,
            "why": "Strong Python, API, dashboard, and agent interests support applied AI product engineering.",
            "skills": ["LangGraph", "FastAPI", "RAG", "tool use", "LLM applications"],
            "next": "Build an AI assistant that answers questions from a curated knowledge base.",
            "difficulty": "Advanced",
            "time": "4-6 months",
            "confidence": "Very high",
        },
        {
            "title": "Machine Learning Engineer",
            "match": 90,
            "why": "Python, SQL, data handling, and backend skills map well to model training and deployment.",
            "skills": ["scikit-learn", "MLflow", "feature engineering", "Docker", "model serving"],
            "next": "Train, track, and deploy a career-fit prediction model as an API.",
            "difficulty": "Advanced",
            "time": "6-9 months",
            "confidence": "High",
        },
        {
            "title": "Data Scientist",
            "match": 87,
            "why": "SQL, Python, analytics thinking, and visualization skills support evidence-led problem solving.",
            "skills": ["statistics", "Pandas", "visualization", "feature analysis", "experimentation"],
            "next": "Create an end-to-end notebook that explores data, builds a baseline model, and explains insights.",
            "difficulty": "Medium",
            "time": "3-5 months",
            "confidence": "High",
        },
    ],
    "learning": {
        "style": "Project-first visual builder",
        "method": "Learn concepts through small builds, then document patterns in a reusable playbook.",
        "focus": "Deep work blocks of 75-90 minutes with a visible weekly shipping goal.",
        "format": "Interactive notebooks, architecture diagrams, short docs, and implementation videos.",
        "weekly": [
            "Mon: concept sprint and tiny prototype",
            "Tue: implementation block",
            "Wed: model experiments and error analysis",
            "Thu: polish, docs, and demo recording",
            "Fri: reflection and next-week planning",
        ],
    },
    "roadmaps": {
        "30-day": [
            ("Week 1", "Refresh Python, APIs, and Streamlit dashboard polish", 80),
            ("Week 2", "Build RAG basics with embeddings and retrieval quality checks", 58),
            ("Week 3", "Create a tool-using AI agent with FastAPI backend", 35),
            ("Week 4", "Package a demo with README, metrics, and portfolio story", 20),
        ],
        "90-day": [
            ("Month 1", "AI app fundamentals and one portfolio-grade agent", 55),
            ("Month 2", "ML metrics, experiment tracking, observability, and deployment", 30),
            ("Month 3", "Interview stories, system design, and product analytics", 15),
        ],
        "1-year": [
            ("Q1", "Foundation: agents, ML, backend APIs, and dashboards", 65),
            ("Q2", "Depth: MLOps, model monitoring, security, and production patterns", 30),
            ("Q3", "Signal: public projects, writing, and open-source contributions", 12),
            ("Q4", "Career launch: interviews, startup demos, and portfolio refinement", 5),
        ],
    },
    "projects": [
        {
            "title": "Data Science Career Predictor",
            "category": "Data science",
            "difficulty": "Advanced",
            "stack": "Python, Pandas, scikit-learn, FastAPI",
            "outcome": "Predicts career-fit scores from skills, interests, and learning behavior.",
            "resume": "Shows practical ML, feature engineering, and API deployment.",
            "interview": "Strong discussion of data preparation, model metrics, and explainability.",
        },
        {
            "title": "Career Intelligence Engine",
            "category": "AI portfolio",
            "difficulty": "Medium",
            "stack": "Streamlit, Plotly, Pandas, FastAPI",
            "outcome": "Maps strengths, skills, interests, and roadmaps into recommendations.",
            "resume": "Product thinking plus explainable AI.",
            "interview": "Clear demo with ethical framing.",
        },
        {
            "title": "Agentic Study Planner",
            "category": "Social impact",
            "difficulty": "Medium",
            "stack": "LangGraph, SQLite, Streamlit",
            "outcome": "Creates weekly plans and adapts based on reflections.",
            "resume": "Personalization and feedback loops.",
            "interview": "Good discussion of human-centered AI.",
        },
        {
            "title": "Startup Idea Validator",
            "category": "Startup idea",
            "difficulty": "Medium",
            "stack": "FastAPI, web research, embeddings, charts",
            "outcome": "Scores ideas by problem clarity, market pull, and build feasibility.",
            "resume": "Founder mindset and applied analytics.",
            "interview": "Strong product and data narrative.",
        },
    ],
}


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #050816;
    --panel: rgba(255, 255, 255, 0.06);
    --panel-strong: rgba(255, 255, 255, 0.09);
    --border: rgba(255, 255, 255, 0.12);
    --text: #F8FAFC;
    --muted: #94A3B8;
    --violet: #7C3AED;
    --cyan: #06B6D4;
    --pink: #A855F7;
    --green: #22C55E;
    --amber: #F59E0B;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    color: var(--text);
    background:
        radial-gradient(circle at 12% 8%, rgba(124, 58, 237, 0.35), transparent 32%),
        radial-gradient(circle at 88% 18%, rgba(6, 182, 212, 0.22), transparent 28%),
        radial-gradient(circle at 50% 110%, rgba(168, 85, 247, 0.18), transparent 40%),
        linear-gradient(135deg, #050816 0%, #080A1F 48%, #0B1026 100%);
}

#MainMenu, footer, header {visibility: hidden;}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1440px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(5, 8, 22, 0.96), rgba(11, 16, 38, 0.90));
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

.sidebar-logo {
    padding: 1rem 0.4rem 1.4rem;
}

.logo-mark {
    display: inline-flex;
    width: 42px;
    height: 42px;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    margin-right: 0.75rem;
    background: linear-gradient(135deg, var(--violet), var(--cyan));
    box-shadow: 0 0 36px rgba(6, 182, 212, 0.35);
    font-weight: 800;
}

.logo-title {
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: 0;
}

.logo-caption {
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 0.3rem;
}

.hero {
    min-height: 560px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: clamp(2rem, 5vw, 4.5rem);
    background:
        linear-gradient(120deg, rgba(124, 58, 237, 0.20), rgba(6, 182, 212, 0.06)),
        rgba(255, 255, 255, 0.045);
    box-shadow: 0 24px 90px rgba(0, 0, 0, 0.38), inset 0 0 0 1px rgba(255, 255, 255, 0.04);
    position: relative;
    overflow: hidden;
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
      linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size: 46px 46px;
    mask-image: linear-gradient(120deg, black, transparent 70%);
}

.hero > * {position: relative; z-index: 1;}

.eyebrow {
    color: #BAE6FD;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    margin-bottom: 0.8rem;
}

.hero h1 {
    font-size: clamp(3rem, 8vw, 6.8rem);
    line-height: 0.92;
    margin: 0;
    color: var(--text);
    letter-spacing: 0;
}

.hero h2 {
    font-size: clamp(1.25rem, 3vw, 2rem);
    color: #D8B4FE;
    margin: 0.8rem 0 0.5rem;
}

.hero p {
    max-width: 780px;
    color: #CBD5E1;
    font-size: 1.08rem;
    line-height: 1.75;
}

.hero-actions {
    display: flex;
    gap: 0.9rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.cta, .ghost-cta {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    min-height: 46px;
    padding: 0.78rem 1.1rem;
    border-radius: 8px;
    font-weight: 700;
    border: 1px solid var(--border);
}

.cta {
    background: linear-gradient(135deg, var(--violet), var(--cyan));
    color: white;
    box-shadow: 0 0 30px rgba(124, 58, 237, 0.35);
}

.ghost-cta {
    background: rgba(255, 255, 255, 0.06);
    color: var(--text);
}

.section-title {
    margin: 2rem 0 1rem;
    font-size: 1.5rem;
    font-weight: 800;
}

.glass-card {
    height: 100%;
    padding: 1.15rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--panel);
    backdrop-filter: blur(18px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.26);
    transition: transform .18s ease, border-color .18s ease, background .18s ease;
}

.glass-card:hover {
    transform: translateY(-3px);
    border-color: rgba(6, 182, 212, 0.38);
    background: var(--panel-strong);
}

.metric-card {
    min-height: 162px;
    position: relative;
    overflow: hidden;
}

.metric-card:after {
    content: "";
    position: absolute;
    width: 120px;
    height: 120px;
    right: -42px;
    top: -42px;
    background: var(--accent);
    filter: blur(40px);
    opacity: 0.32;
}

.metric-label {
    color: var(--muted);
    font-size: 0.86rem;
    font-weight: 650;
}

.metric-value {
    font-size: 2.35rem;
    font-weight: 850;
    margin-top: 0.35rem;
}

.metric-delta {
    color: #BBF7D0;
    font-weight: 700;
    font-size: 0.85rem;
}

.progress-track {
    height: 8px;
    background: rgba(255,255,255,0.10);
    border-radius: 999px;
    overflow: hidden;
    margin-top: 1rem;
}

.progress-fill {
    height: 100%;
    width: var(--value);
    background: linear-gradient(90deg, var(--accent), #06B6D4);
    border-radius: 999px;
    box-shadow: 0 0 24px var(--accent);
}

.card-title {
    font-weight: 800;
    font-size: 1.05rem;
    margin-bottom: 0.55rem;
}

.muted {
    color: var(--muted);
    line-height: 1.6;
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-top: 0.8rem;
}

.badge {
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.07);
    color: #DBEAFE;
    border-radius: 999px;
    padding: 0.28rem 0.62rem;
    font-size: 0.78rem;
    font-weight: 650;
}

.career-match {
    font-size: 2rem;
    font-weight: 850;
    background: linear-gradient(135deg, #F8FAFC, #67E8F9);
    -webkit-background-clip: text;
    color: transparent;
}

.timeline {
    border-left: 1px solid rgba(6, 182, 212, 0.4);
    padding-left: 1.2rem;
}

.timeline-item {
    position: relative;
    margin: 0 0 1rem;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.055);
}

.timeline-item:before {
    content: "";
    position: absolute;
    left: -1.55rem;
    top: 1.15rem;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #06B6D4;
    box-shadow: 0 0 18px rgba(6, 182, 212, 0.9);
}

.ethics-item {
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
    margin-bottom: 0.9rem;
    color: #CBD5E1;
}

.stTextArea textarea, .stTextInput input, .stSlider {
    color: var(--text);
}

div[data-testid="stForm"] {
    border: 1px solid var(--border);
    background: var(--panel);
    border-radius: 8px;
    padding: 1rem;
}

button[kind="primary"], .stButton > button {
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.15);
    background: linear-gradient(135deg, var(--violet), var(--cyan));
    color: white;
    font-weight: 750;
}

@media (max-width: 768px) {
    .hero {min-height: auto; padding: 2rem;}
    .hero-actions {display: block;}
    .cta, .ghost-cta {width: 100%; margin-bottom: 0.7rem;}
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def merge_demo_data(payload, fallback):
    merged = fallback.copy()
    for key, value in payload.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def fetch_data():
    try:
        with st.spinner("Syncing HPI AI intelligence layer..."):
            response = requests.get(API_URL, timeout=1.8)
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict) and payload:
                st.toast("Connected to backend intelligence API.")
                return merge_demo_data(payload, DEMO_DATA), True
    except requests.RequestException:
        return DEMO_DATA, False
    return DEMO_DATA, False


def call_agent(message, context=None):
    try:
        response = requests.post(
            AGENT_URL,
            json={"message": message, "context": context or {}},
            timeout=12,
        )
        response.raise_for_status()
        return response.json(), True
    except requests.RequestException:
        return {
            "response": "The backend agent is not reachable yet. Start FastAPI with uvicorn backend.main:app --reload --port 8000.",
            "tool": "offline",
            "tool_result": {},
            "next_actions": ["Start the backend server", "Refresh this Streamlit page"],
        }, False


def call_reflection(payload):
    try:
        response = requests.post(REFLECTION_URL, json=payload, timeout=12)
        response.raise_for_status()
        return response.json(), True
    except requests.RequestException:
        return None, False


def score_potential_scan(payload):
    skill_count = len(payload.get("skills", []))
    experience = int(payload.get("experience", 0))
    learning_hours = int(payload.get("learning_hours", 5))
    project_depth = int(payload.get("project_depth", 5))
    stats_level = int(payload.get("stats_level", 5))
    ml_level = int(payload.get("ml_level", 5))
    ai_level = int(payload.get("ai_level", 5))
    ds_score = min(98, 45 + skill_count * 3 + stats_level * 4 + project_depth * 2 + min(experience, 5) * 2)
    ml_score = min(98, 42 + skill_count * 2 + ml_level * 5 + stats_level * 2 + project_depth * 2)
    ai_score = min(98, 44 + skill_count * 2 + ai_level * 5 + learning_hours * 2 + project_depth)
    scores = {
        "Data Science": ds_score,
        "Machine Learning Engineering": ml_score,
        "AI Engineering": ai_score,
    }
    top_track = max(scores, key=scores.get)
    focus_map = {
        "Data Science": "statistics, exploratory analysis, visualization, and explainable insight stories",
        "Machine Learning Engineering": "feature engineering, experiment tracking, model serving, and monitoring",
        "AI Engineering": "RAG, tool-using agents, FastAPI backends, and product-ready AI workflows",
    }
    return {
        "scores": scores,
        "top_track": top_track,
        "summary": f"{payload.get('name', 'This profile')} is strongest for {top_track}.",
        "focus": focus_map[top_track],
        "next_actions": [
            f"Build one portfolio project focused on {focus_map[top_track]}.",
            "Create a weekly learning schedule with one measurable deliverable.",
            "Track skills, project proof, and confidence after each sprint.",
        ],
    }


def call_potential_scan(payload):
    try:
        response = requests.post(SCAN_URL, json=payload, timeout=12)
        response.raise_for_status()
        return response.json(), True
    except requests.RequestException:
        return score_potential_scan(payload), False


def card(html):
    st.markdown(html, unsafe_allow_html=True)


def go_to(page):
    st.session_state.current_page = page
    st.rerun()


def sidebar(data, connected):
    profile = data["profile"]
    st.sidebar.markdown(
        f"""
        <div class="sidebar-logo">
            <div style="display:flex; align-items:center;">
                <span class="logo-mark">H</span>
                <span class="logo-title">HPI AI</span>
            </div>
            <div class="logo-caption">Human Potential Identifier</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Landing"
    current_page = st.session_state.current_page
    page = st.sidebar.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(current_page) if current_page in PAGES else 0,
        label_visibility="collapsed",
    )
    st.session_state.current_page = page
    st.sidebar.markdown("---")
    status = "Backend API connected" if connected else "Demo profile mode"
    st.sidebar.markdown(
        f"""
        <div class="glass-card">
            <div class="card-title">{profile['name']}</div>
            <div class="muted">{profile['role']}</div>
            <div class="badge-row">
                <span class="badge">{status}</span>
                <span class="badge">Dark AI SaaS</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return page


def metric_card(label, meta):
    value = int(meta["value"])
    return f"""
    <div class="glass-card metric-card" style="--accent:{meta['accent']};">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}<span style="font-size:1rem;color:#94A3B8;">%</span></div>
        <div class="metric-delta">{meta['delta']} momentum</div>
        <div class="progress-track"><div class="progress-fill" style="--value:{value}%;"></div></div>
    </div>
    """


def potential_radar(potential):
    labels = list(potential.keys())
    values = list(potential.values())
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name="Potential",
            line=dict(color="#06B6D4", width=3),
            fillcolor="rgba(6, 182, 212, 0.22)",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC", family="Inter"),
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(visible=True, range=[0, 100], color="#94A3B8", gridcolor="rgba(255,255,255,0.12)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.10)"),
        ),
        margin=dict(l=30, r=30, t=40, b=30),
        height=430,
        showlegend=False,
    )
    return fig


def growth_chart(data):
    df = pd.DataFrame(data)
    fig = go.Figure()
    colors = {"Python": "#7C3AED", "AI Agents": "#06B6D4", "Product": "#22C55E"}
    for column in ["Python", "AI Agents", "Product"]:
        fig.add_trace(
            go.Scatter(
                x=df["week"],
                y=df[column],
                mode="lines+markers",
                name=column,
                line=dict(color=colors[column], width=3, shape="spline"),
                marker=dict(size=8),
            )
        )
    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.025)",
        font=dict(color="#F8FAFC", family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", range=[0, 100]),
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=20, r=20, t=45, b=20),
    )
    return fig


def bar_chart(potential):
    labels = list(potential.keys())
    values = list(potential.values())
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(
                color=values,
                colorscale=[[0, "#312E81"], [0.55, "#7C3AED"], [1, "#06B6D4"]],
                line=dict(color="rgba(255,255,255,0.18)", width=1),
            ),
        )
    )
    fig.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.025)",
        font=dict(color="#F8FAFC", family="Inter"),
        xaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.02)"),
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


def landing(data):
    profile = data["profile"]
    st.markdown(
        f"""
        <section class="hero">
            <div class="eyebrow">AI career intelligence platform</div>
            <h1>HPI AI</h1>
            <h2>Human Potential Identifier</h2>
            <p><strong>Identify strengths. Map careers. Build future potential.</strong></p>
            <p>HPI AI analyzes skills, learning behavior, interests, and reflection patterns to recommend ethical,
            explainable career paths and roadmaps. This demo profile follows {profile['name']}, an aspiring data science,
            machine learning, and AI engineering professional.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, _ = st.columns([0.22, 0.24, 0.54])
    with c1:
        if st.button("Start Potential Scan", type="primary", use_container_width=True):
            go_to("Potential Scan")
    with c2:
        if st.button("View Demo Dashboard", use_container_width=True):
            go_to("Executive Dashboard")

    st.markdown('<div class="section-title">Premium Intelligence Modules</div>', unsafe_allow_html=True)
    features = [
        ("Strength Intelligence", "Find high-signal strengths from skills, interests, and reflection patterns."),
        ("Career Fit Engine", "Rank career paths with transparent match logic and confidence indicators."),
        ("Learning Style Detection", "Translate behavior into study formats, focus rituals, and weekly plans."),
        ("Personalized Roadmaps", "Turn goals into 30-day, 90-day, and 1-year execution plans."),
        ("Project Idea Generator", "Recommend portfolio builds with resume and interview value."),
        ("Growth Analytics", "Track momentum, consistency, skill depth, and confidence over time."),
    ]
    cols = st.columns(3)
    for i, (title, text) in enumerate(features):
        with cols[i % 3]:
            card(f'<div class="glass-card"><div class="card-title">{title}</div><div class="muted">{text}</div></div>')


def potential_scan(data):
    st.title("Potential Scan")
    st.caption("Enter your current details to estimate fit across Data Science, ML Engineering, and AI Engineering.")
    profile = data["profile"]
    left, right = st.columns([0.56, 0.44])
    with left:
        with st.form("potential_scan_form"):
            name = st.text_input("Name", profile["name"])
            target_role = st.selectbox(
                "Target role",
                ["AI Engineer", "Machine Learning Engineer", "Data Scientist"],
            )
            skills = st.multiselect(
                "Current skills",
                [
                    "Python",
                    "SQL",
                    "Pandas",
                    "NumPy",
                    "statistics",
                    "scikit-learn",
                    "deep learning",
                    "FastAPI",
                    "Streamlit",
                    "RAG",
                    "LangGraph",
                    "MLOps",
                    "Docker",
                    "cloud deployment",
                ],
                default=[skill for skill in profile["skills"] if skill in ["Python", "SQL", "Pandas", "NumPy", "scikit-learn", "FastAPI", "Streamlit"]],
            )
            c1, c2 = st.columns(2)
            with c1:
                experience = st.number_input("Relevant experience in years", min_value=0, max_value=20, value=1)
                learning_hours = st.slider("Weekly learning hours", 1, 30, 10)
                stats_level = st.slider("Statistics and data analysis level", 1, 10, 6)
            with c2:
                ml_level = st.slider("Machine learning level", 1, 10, 6)
                ai_level = st.slider("AI agents and LLM app level", 1, 10, 7)
                project_depth = st.slider("Portfolio project depth", 1, 10, 6)
            interests = st.text_area("Interests", ", ".join(profile["interests"]))
            career_goal = st.text_area("Career goal", profile["goal"])
            constraints = st.text_area("Constraints or challenges", "Need a clear path and portfolio projects that prove job-ready skills.")
            submitted = st.form_submit_button("Analyze Potential", type="primary")
    if submitted:
        payload = {
            "name": name,
            "target_role": target_role,
            "skills": skills,
            "experience": experience,
            "learning_hours": learning_hours,
            "stats_level": stats_level,
            "ml_level": ml_level,
            "ai_level": ai_level,
            "project_depth": project_depth,
            "interests": interests,
            "career_goal": career_goal,
            "constraints": constraints,
        }
        result, live = call_potential_scan(payload)
        st.session_state.potential_scan_result = result
        st.session_state.potential_scan_live = live

    with right:
        result = st.session_state.get("potential_scan_result") or score_potential_scan(
            {
                "name": profile["name"],
                "skills": profile["skills"],
                "experience": 1,
                "learning_hours": 10,
                "stats_level": 6,
                "ml_level": 6,
                "ai_level": 7,
                "project_depth": 6,
            }
        )
        st.markdown('<div class="section-title">Scan Result</div>', unsafe_allow_html=True)
        card(
            f"""
            <div class="glass-card">
                <div class="metric-label">Best-fit track</div>
                <div class="metric-value" style="font-size:2rem;">{result['top_track']}</div>
                <div class="muted">{result['summary']} Focus next on {result['focus']}.</div>
                <div class="badge-row">
                    <span class="badge">{'Backend scan' if st.session_state.get('potential_scan_live') else 'Local scan'}</span>
                    <span class="badge">Guidance only</span>
                </div>
            </div>
            """
        )
        st.plotly_chart(bar_chart(result["scores"]), use_container_width=True)
        st.markdown('<div class="section-title">Next Actions</div>', unsafe_allow_html=True)
        for action in result["next_actions"]:
            card(f'<div class="glass-card"><div class="muted">{action}</div></div>')


def executive_dashboard(data):
    profile = data["profile"]
    st.title("Executive Dashboard")
    st.caption("A premium snapshot of potential, confidence, learning momentum, and career readiness.")
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-title">{profile['name']} - {profile['goal']}</div>
            <div class="muted">{profile['role']}</div>
            <div class="badge-row">{''.join(f'<span class="badge">{skill}</span>' for skill in profile['skills'])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-title">Performance Signals</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (label, meta) in enumerate(data["kpis"].items()):
        with cols[i % 3]:
            card(metric_card(label, meta))

    left, right = st.columns([1, 1])
    with left:
        st.markdown('<div class="section-title">Human Potential Radar</div>', unsafe_allow_html=True)
        st.plotly_chart(potential_radar(data["potential"]), use_container_width=True)
    with right:
        st.markdown('<div class="section-title">Skill Growth Trajectory</div>', unsafe_allow_html=True)
        st.plotly_chart(growth_chart(data["growth"]), use_container_width=True)


def potential_analysis(data):
    st.title("Potential Analysis")
    st.caption("Balanced view of technical, creative, leadership, business, research, and communication potential.")
    cols = st.columns(3)
    accent_cycle = ["#7C3AED", "#06B6D4", "#A855F7", "#22C55E", "#F59E0B", "#38BDF8"]
    for i, (label, value) in enumerate(data["potential"].items()):
        with cols[i % 3]:
            card(
                f"""
                <div class="glass-card metric-card" style="--accent:{accent_cycle[i]};">
                    <div class="metric-label">{label} Potential</div>
                    <div class="metric-value">{value}<span style="font-size:1rem;color:#94A3B8;">%</span></div>
                    <div class="progress-track"><div class="progress-fill" style="--value:{value}%;"></div></div>
                </div>
                """
            )
    left, right = st.columns([1.05, 0.95])
    with left:
        st.plotly_chart(bar_chart(data["potential"]), use_container_width=True)
    with right:
        st.plotly_chart(potential_radar(data["potential"]), use_container_width=True)
    card(
        """
        <div class="glass-card">
            <div class="card-title">AI Interpretation</div>
            <div class="muted">
            The strongest signal is technical execution, supported by research curiosity and communication clarity.
            The recommended growth strategy is to connect data science fundamentals with deployable ML and agentic
            AI workflows. This is guidance, not destiny prediction.
            </div>
        </div>
        """
    )


def career_card(career):
    return f"""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; gap:1rem; align-items:flex-start;">
            <div>
                <div class="card-title">{career['title']}</div>
                <div class="muted">{career['why']}</div>
            </div>
            <div class="career-match">{career['match']}%</div>
        </div>
        <div class="badge-row">
            <span class="badge">Difficulty: {career['difficulty']}</span>
            <span class="badge">{career['time']}</span>
            <span class="badge">Confidence: {career['confidence']}</span>
        </div>
        <div class="badge-row">{''.join(f'<span class="badge">{skill}</span>' for skill in career['skills'])}</div>
        <div style="margin-top:0.9rem;" class="muted"><strong style="color:#F8FAFC;">Next step:</strong> {career['next']}</div>
        <div class="progress-track"><div class="progress-fill" style="--value:{career['match']}%; --accent:#06B6D4;"></div></div>
    </div>
    """


def career_intelligence(data):
    st.title("Career Intelligence")
    st.caption("Top recommended career paths with explainable fit, effort, skills, and confidence.")
    for career in data["careers"]:
        card(career_card(career))


def ai_agent(data):
    st.title("AI Agent")
    st.caption("Ask the backend agent for career direction, roadmaps, learning plans, or reflection coaching.")

    if "agent_messages" not in st.session_state:
        st.session_state.agent_messages = [
            {
                "role": "assistant",
                "content": "I can analyze your profile, recommend careers, generate a roadmap, or coach a weekly reflection.",
            }
        ]

    left, right = st.columns([0.68, 0.32])
    with left:
        for message in st.session_state.agent_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        prompt = st.chat_input("Ask HPI AI what to do next...")
        if prompt:
            st.session_state.agent_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            context = {
                "goal": data["profile"]["goal"],
                "skills": data["profile"]["skills"],
                "interests": data["profile"]["interests"],
            }
            result, live = call_agent(prompt, context)
            answer = result["response"]
            st.session_state.agent_messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.write(answer)
                st.caption(f"Tool used: {result.get('tool', 'unknown')} | {'Backend live' if live else 'Offline fallback'}")

    with right:
        card(
            f"""
            <div class="glass-card">
                <div class="card-title">Agent Tooling</div>
                <div class="muted">The frontend calls FastAPI, and FastAPI routes each question to an agent tool.</div>
                <div class="badge-row">
                    <span class="badge">analyze_profile</span>
                    <span class="badge">recommend_career</span>
                    <span class="badge">generate_roadmap</span>
                    <span class="badge">reflect_growth</span>
                </div>
            </div>
            """
        )
        st.markdown('<div class="section-title">Try Prompts</div>', unsafe_allow_html=True)
        examples = [
            "What is my best AI career path?",
            "Create a 4-week roadmap for agentic AI.",
            "I feel stuck balancing ML and portfolio projects.",
            "Analyze my strongest profile signals.",
        ]
        for example in examples:
            if st.button(example, use_container_width=True):
                result, _ = call_agent(example, {"goal": data["profile"]["goal"]})
                st.session_state.agent_messages.append({"role": "user", "content": example})
                st.session_state.agent_messages.append({"role": "assistant", "content": result["response"]})
                st.rerun()


def learning_style(data):
    learning = data["learning"]
    st.title("Learning Style")
    st.caption("Detected learning preferences translated into a weekly execution system.")
    c1, c2 = st.columns([1, 1])
    with c1:
        card(
            f"""
            <div class="glass-card">
                <div class="metric-label">Detected Learning Style</div>
                <div class="metric-value" style="font-size:2rem;">{learning['style']}</div>
                <div class="muted">{learning['method']}</div>
                <div class="badge-row">
                    <span class="badge">Visual</span><span class="badge">Project-first</span>
                    <span class="badge">Build in public</span>
                </div>
            </div>
            """
        )
    with c2:
        card(
            f"""
            <div class="glass-card">
                <div class="card-title">Focus Pattern</div>
                <div class="muted">{learning['focus']}</div>
                <div class="card-title" style="margin-top:1rem;">Recommended Format</div>
                <div class="muted">{learning['format']}</div>
            </div>
            """
        )
    st.markdown('<div class="section-title">Weekly Learning Plan</div>', unsafe_allow_html=True)
    cols = st.columns(len(learning["weekly"]))
    for i, item in enumerate(learning["weekly"]):
        day, task = item.split(": ", 1)
        with cols[i]:
            card(f'<div class="glass-card"><div class="card-title">{day}</div><div class="muted">{task}</div></div>')


def roadmap(data):
    st.title("Roadmap")
    st.caption("Milestone-driven plans that connect near-term execution to long-term career movement.")
    tabs = st.tabs(["30-day", "90-day", "1-year"])
    for tab, key in zip(tabs, ["30-day", "90-day", "1-year"]):
        with tab:
            st.markdown('<div class="timeline">', unsafe_allow_html=True)
            for label, text, progress in data["roadmaps"][key]:
                card(
                    f"""
                    <div class="timeline-item">
                        <div class="card-title">{label}</div>
                        <div class="muted">{text}</div>
                        <div class="progress-track"><div class="progress-fill" style="--value:{progress}%; --accent:#7C3AED;"></div></div>
                        <div class="muted" style="margin-top:0.5rem;">{progress}% checkpoint readiness</div>
                    </div>
                    """
                )
            st.markdown("</div>", unsafe_allow_html=True)


def project_ideas(data):
    st.title("Project Ideas")
    st.caption("Portfolio projects chosen for skill proof, demo quality, resume value, and interview depth.")
    cols = st.columns(2)
    for i, project in enumerate(data["projects"]):
        with cols[i % 2]:
            card(
                f"""
                <div class="glass-card">
                    <div class="metric-label">{project['category']}</div>
                    <div class="card-title">{project['title']}</div>
                    <div class="badge-row">
                        <span class="badge">{project['difficulty']}</span>
                        <span class="badge">{project['stack']}</span>
                    </div>
                    <div class="muted" style="margin-top:0.9rem;"><strong style="color:#F8FAFC;">Outcome:</strong> {project['outcome']}</div>
                    <div class="muted"><strong style="color:#F8FAFC;">Resume value:</strong> {project['resume']}</div>
                    <div class="muted"><strong style="color:#F8FAFC;">Interview value:</strong> {project['interview']}</div>
                </div>
                """
            )


def reflection_growth(data):
    st.title("Reflection & Growth")
    st.caption("A personal AI coach surface for weekly reflection, momentum tracking, and growth insights.")
    left, right = st.columns([1, 1])
    with left:
        with st.form("reflection_form"):
            st.markdown("### Weekly Reflection")
            energy = st.slider("Energy level", 1, 10, 7)
            curiosity = st.text_input("Curiosity topics", "AI agents, ML deployment, data science projects")
            wins = st.text_area("Wins", "Shipped a cleaner Streamlit dashboard and clarified the AI engineer roadmap.")
            challenges = st.text_area("Challenges", "Balancing ML fundamentals with portfolio shipping.")
            submitted = st.form_submit_button("Generate Growth Insight")
    with right:
        insight = (
            "Your reflection pattern shows strong builder momentum. Keep one portfolio artifact as the weekly anchor, "
            "then use reflection to decide whether the next sprint needs depth, polish, or distribution."
        )
        if "submitted" in locals() and submitted:
            result, live = call_reflection(
                {
                    "energy": energy,
                    "curiosity": curiosity,
                    "wins": wins,
                    "challenges": challenges,
                }
            )
            if result:
                insight = result["response"]
                st.caption(f"Generated by backend reflection agent. Tool: {result.get('tool', 'unknown')}")
            else:
                insight = (
                    f"Energy is {energy}/10 with curiosity around {curiosity}. Convert wins into public proof, reduce friction "
                    "around the main challenge, and choose one measurable checkpoint for the next seven days."
                )
                st.caption("Backend unavailable, showing local fallback insight.")
        card(
            f"""
            <div class="glass-card">
                <div class="card-title">AI Growth Insight</div>
                <div class="muted">{insight}</div>
                <div class="badge-row">
                    <span class="badge">Reflection streak: 4 weeks</span>
                    <span class="badge">Momentum: rising</span>
                    <span class="badge">Coach mode</span>
                </div>
            </div>
            """
        )
        st.plotly_chart(growth_chart(data["growth"]), use_container_width=True)


def privacy_ethics(data):
    st.title("Privacy & Ethics")
    st.caption("Trustworthy AI guidance that respects consent, agency, transparency, and user control.")
    principles = [
        ("Privacy-first design", "User data should be minimized, encrypted in transit, and used only for visible product value."),
        ("User consent", "Profiles, reflections, and recommendations should be opt-in and clearly editable."),
        ("Delete data option", "Users should be able to remove their profile and reflection history at any time."),
        ("Explainable recommendations", "Every career suggestion should show the skills and signals behind it."),
        ("No destiny prediction", "HPI AI recommends paths; it never claims to determine a person's future."),
        ("No psychological diagnosis", "The platform is not a medical, psychological, or clinical assessment tool."),
        ("Guidance-only disclaimer", "Outputs are planning aids that should be combined with mentors, practice, and real evidence."),
    ]
    cols = st.columns(2)
    for i, (title, text) in enumerate(principles):
        with cols[i % 2]:
            card(
                f"""
                <div class="glass-card">
                    <div class="card-title">{title}</div>
                    <div class="muted">{text}</div>
                </div>
                """
            )
    st.markdown('<div class="section-title">Data Controls</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Export Profile",
            data=json.dumps(data["profile"], indent=2),
            file_name="hpi_ai_profile.json",
            mime="application/json",
            use_container_width=True,
        )
    with c2:
        if st.button("Review Consent", use_container_width=True):
            st.session_state.show_consent = True
    with c3:
        if st.button("Delete Demo Data", use_container_width=True):
            st.session_state.pop("agent_messages", None)
            st.session_state.pop("potential_scan_result", None)
            st.session_state.show_consent = False
            st.success("Demo session data cleared from this browser session.")
    if st.session_state.get("show_consent"):
        card(
            """
            <div class="glass-card">
                <div class="card-title">Consent Summary</div>
                <div class="muted">
                This demo uses profile, scan, and reflection inputs only to generate visible recommendations.
                You can export the profile or clear session-generated scan and chat data at any time.
                </div>
            </div>
            """
        )


def main():
    inject_css()
    data, connected = fetch_data()
    page = sidebar(data, connected)
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; gap:1rem;">
            <div class="muted">HPI AI - Human Potential Identifier</div>
            <div class="badge-row" style="margin-top:0;">
                <span class="badge">{'Live backend' if connected else 'Demo profile mode'}</span>
                <span class="badge">{datetime.now().strftime('%b %d, %Y')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = {
        "Landing": landing,
        "Potential Scan": potential_scan,
        "Executive Dashboard": executive_dashboard,
        "Potential Analysis": potential_analysis,
        "Career Intelligence": career_intelligence,
        "AI Agent": ai_agent,
        "Learning Style": learning_style,
        "Roadmap": roadmap,
        "Project Ideas": project_ideas,
        "Reflection & Growth": reflection_growth,
        "Privacy & Ethics": privacy_ethics,
    }
    pages[page](data)


if __name__ == "__main__":
    main()
