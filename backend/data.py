from copy import deepcopy


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
    ],
}


def get_demo_data() -> dict:
    return deepcopy(DEMO_DATA)
