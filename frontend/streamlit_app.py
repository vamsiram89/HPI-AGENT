import os
import json
import html
import re
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
    "Learning Plan Detail",
    "Roadmap",
    "Project Ideas",
    "Reflection & Growth",
    "Exercises",
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


ROLE_CATALOG = [
    {
        "title": "Barber / Hair Stylist",
        "keywords": ["hair", "haircut", "haircutting", "barber", "salon", "hairstyle", "styling", "grooming", "beard", "fade"],
        "skills": ["sectioning", "clipper control", "scissor-over-comb", "face-shape consultation", "sanitation", "client communication"],
        "why": "Your interest in haircutting maps to a practical, visual, client-facing profession where technique improves through repeated hands-on practice.",
        "focus": "hair types, head shapes, cutting angles, tool safety, consultation, and portfolio photos",
        "next": "Practice sectioning, one-length cuts, fades, and consultation scripts on mannequin heads before moving to supervised real clients.",
        "difficulty": "Medium",
        "time": "6-12 months",
        "image": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Chef / Culinary Professional",
        "keywords": ["cook", "cooking", "recipe", "recipes", "chef", "food", "kitchen", "baking", "culinary", "flavor"],
        "skills": ["knife skills", "mise en place", "food safety", "sauce foundations", "menu planning", "plating"],
        "why": "Knowing recipes is a strong signal for culinary work, especially when paired with disciplined technique, timing, taste testing, and service practice.",
        "focus": "knife skills, heat control, mother sauces, food safety, menu costing, and service timing",
        "next": "Build a 12-dish portfolio across breakfast, mains, desserts, and plated specials with photos and tasting notes.",
        "difficulty": "Medium",
        "time": "4-9 months",
        "image": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Pastry Chef / Baker",
        "keywords": ["bake", "baking", "pastry", "cake", "dessert", "bread", "cookies", "chocolate"],
        "skills": ["weighing", "dough handling", "lamination", "temperature control", "decoration", "recipe testing"],
        "why": "Baking rewards precision, patience, and visual presentation, making it a strong path for someone who enjoys recipe mastery.",
        "focus": "ingredient ratios, fermentation, pastry cream, decoration, costing, and batch consistency",
        "next": "Create a pastry sampler: bread, cake, tart, cookies, and one decorated celebration item.",
        "difficulty": "Medium",
        "time": "4-8 months",
        "image": "https://images.unsplash.com/photo-1517433367423-c7e5b0f35086?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Photographer",
        "keywords": ["photo", "photography", "camera", "portrait", "lighting", "editing", "visual"],
        "skills": ["composition", "lighting", "manual exposure", "photo editing", "posing", "client briefs"],
        "why": "A visual interest profile can translate into photography when you enjoy framing, detail, people, places, or product storytelling.",
        "focus": "composition, light direction, editing workflow, client shot lists, and portfolio curation",
        "next": "Shoot five small collections: portrait, product, food, event, and street/documentary.",
        "difficulty": "Medium",
        "time": "3-6 months",
        "image": "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Graphic Designer",
        "keywords": ["design", "drawing", "logo", "poster", "brand", "graphics", "canva", "figma", "photoshop"],
        "skills": ["typography", "layout", "color systems", "brand identity", "Figma", "asset export"],
        "why": "Design interests point toward visual problem solving, brand communication, and polished digital deliverables.",
        "focus": "layout, typography, visual hierarchy, brand systems, critique, and client presentation",
        "next": "Design a mini brand kit with logo, colors, social posts, poster, and landing section.",
        "difficulty": "Medium",
        "time": "3-6 months",
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "UI/UX Designer",
        "keywords": ["ui", "ux", "app design", "wireframe", "prototype", "figma", "user experience"],
        "skills": ["user research", "wireframing", "prototyping", "usability testing", "design systems", "accessibility"],
        "why": "UX is a fit when you enjoy improving how people use apps, services, and workflows.",
        "focus": "research, user flows, wireframes, components, usability tests, and case studies",
        "next": "Redesign one everyday app flow and document the problem, users, screens, tests, and final prototype.",
        "difficulty": "Medium",
        "time": "4-8 months",
        "image": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Digital Marketer",
        "keywords": ["marketing", "social media", "seo", "ads", "content", "instagram", "youtube", "campaign"],
        "skills": ["SEO", "copywriting", "campaign analytics", "content calendar", "paid ads", "landing pages"],
        "why": "Marketing fits people who like audience behavior, creative messaging, experiments, and measurable growth.",
        "focus": "SEO, short-form content, analytics, funnels, ad tests, and campaign reporting",
        "next": "Run a 14-day content campaign for a real or mock brand and report reach, clicks, and lessons.",
        "difficulty": "Medium",
        "time": "3-5 months",
        "image": "https://images.unsplash.com/photo-1557838923-2985c318be48?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Teacher / Tutor",
        "keywords": ["teach", "teacher", "tutor", "explain", "students", "education", "training"],
        "skills": ["lesson planning", "concept explanation", "assessment", "classroom management", "feedback", "empathy"],
        "why": "Teaching fits when you enjoy explaining ideas, helping others improve, and building structured learning experiences.",
        "focus": "lesson design, diagnostics, examples, practice sets, feedback loops, and learner motivation",
        "next": "Create and deliver a 5-lesson mini-course with worksheets, quizzes, and learner feedback.",
        "difficulty": "Medium",
        "time": "3-6 months",
        "image": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Fitness Trainer",
        "keywords": ["fitness", "gym", "workout", "training", "exercise", "nutrition", "sports"],
        "skills": ["movement screening", "program design", "coaching cues", "nutrition basics", "progress tracking", "safety"],
        "why": "Fitness training fits a profile that enjoys health, movement, motivation, and measurable client progress.",
        "focus": "anatomy basics, exercise technique, program design, safety, habit coaching, and assessments",
        "next": "Build beginner, fat-loss, strength, and mobility plans with demo videos and progress metrics.",
        "difficulty": "Medium",
        "time": "3-8 months",
        "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Electrician",
        "keywords": ["electric", "electrician", "wiring", "repair", "circuits", "tools", "hardware"],
        "skills": ["safety codes", "circuit basics", "wiring diagrams", "multimeter use", "installation", "troubleshooting"],
        "why": "Hands-on technical interests can fit electrical work when you enjoy tools, systems, safety, and precise troubleshooting.",
        "focus": "electrical safety, circuit theory, wiring standards, tools, diagnostics, and supervised practice",
        "next": "Study local code basics and practice safe low-voltage circuits before pursuing supervised apprenticeship work.",
        "difficulty": "Advanced",
        "time": "1-3 years",
        "image": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Software Developer",
        "keywords": ["code", "coding", "software", "app", "web", "javascript", "python", "programming"],
        "skills": ["programming", "debugging", "Git", "APIs", "databases", "testing"],
        "why": "Coding and app-building interests point toward software development, where proof comes from working products.",
        "focus": "programming fundamentals, web apps, APIs, databases, testing, and deployment",
        "next": "Build a CRUD app with login, database, API, tests, and a deployed demo.",
        "difficulty": "Advanced",
        "time": "6-12 months",
        "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Data Scientist",
        "keywords": ["data", "statistics", "analytics", "sql", "python", "pandas", "dashboard", "visualization"],
        "skills": ["statistics", "SQL", "Pandas", "visualization", "experimentation", "storytelling"],
        "why": "Data science fits when you like finding patterns, explaining evidence, and turning messy data into decisions.",
        "focus": "statistics, SQL, exploratory analysis, visualization, experiments, and explainable insights",
        "next": "Create an end-to-end analysis notebook with clear questions, charts, findings, and business recommendations.",
        "difficulty": "Advanced",
        "time": "5-9 months",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "Machine Learning Engineer",
        "keywords": ["machine learning", "ml", "model", "scikit", "tensorflow", "pytorch", "prediction"],
        "skills": ["feature engineering", "model training", "evaluation", "MLflow", "Docker", "model serving"],
        "why": "Machine learning engineering fits when you enjoy building models and making them reliable in real applications.",
        "focus": "features, metrics, experiment tracking, model serving, monitoring, and reproducibility",
        "next": "Train, evaluate, and deploy a prediction model behind an API with monitoring notes.",
        "difficulty": "Advanced",
        "time": "6-12 months",
        "image": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
    },
    {
        "title": "AI Engineer",
        "keywords": ["ai", "llm", "agent", "rag", "chatbot", "openai", "langchain", "langgraph"],
        "skills": ["LLM apps", "RAG", "tool use", "FastAPI", "evaluation", "prompt design"],
        "why": "AI engineering fits when you enjoy turning models into useful assistants, workflows, and product features.",
        "focus": "RAG, tool-using agents, evaluation, backend APIs, safety, and product UX",
        "next": "Build an assistant that answers from documents, calls tools, and shows evaluation examples.",
        "difficulty": "Advanced",
        "time": "4-9 months",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
    },
]


ROLE_BY_TITLE = {role["title"]: role for role in ROLE_CATALOG}
SKILL_OPTIONS = sorted({skill for role in ROLE_CATALOG for skill in role["skills"]} | {keyword.title() for role in ROLE_CATALOG for keyword in role["keywords"]})


def esc(value):
    return html.escape(str(value or ""))


def split_terms(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value or "").replace("\n", ",").split(",") if item.strip()]


def term_in_text(term, text):
    term = str(term or "").strip().lower()
    if not term:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def count_term_hits(terms, text):
    return sum(1 for term in terms if term_in_text(term, text))


def active_scan_result(data):
    return st.session_state.get("potential_scan_result") or score_potential_scan(
        {
            "name": data["profile"]["name"],
            "target_role": "AI Engineer",
            "skills": data["profile"]["skills"],
            "experience": 1,
            "learning_hours": 10,
            "general_level": 6,
            "project_depth": 6,
            "interests": ", ".join(data["profile"]["interests"]),
            "career_goal": data["profile"]["goal"],
            "profile_details": "I like AI agents, machine learning, data science, and building useful software.",
        }
    )


def top_role(result):
    roles = result.get("recommended_roles") or []
    if roles:
        return roles[0]
    return ROLE_BY_TITLE.get(result.get("top_track"), ROLE_CATALOG[-1])


def role_learning_plan(role, hours=10):
    title = role["title"]
    if "Hair" in title or "Barber" in title:
        return {
            "style": "Hands-on barber and hair stylist builder",
            "method": "Learn hair styling through visual references, mannequin practice, guided cutting drills, feedback, and before-after photo proof.",
            "focus": f"Use {max(45, min(90, int(hours) * 6))}-minute salon practice blocks: consult, section, cut or style, check symmetry, photograph, and correct.",
            "format": "Haircut reference photos, short technique videos, mannequin-head drills, sanitation checklists, client consultation scripts, and mentor feedback.",
            "weekly": [
                "Mon: identify hair types, face shapes, sectioning lines, and haircut reference photos",
                "Tue: practice clean sectioning, comb control, and one-length cutting on a mannequin head",
                "Wed: practice clipper guards, taper lines, and low-to-mid fade blending",
                "Thu: style straight, wavy, and curly finishes, then photograph before-after results",
                "Fri: run a client consultation roleplay and choose suitable haircut types from photos",
            ],
        }
    return {
        "style": f"Hands-on {title} builder",
        "method": f"Learn {title} skills through demonstrations, guided drills, small projects, feedback, and a weekly proof artifact.",
        "focus": f"Use {max(45, min(90, int(hours) * 6))}-minute practice blocks: observe, copy, practice, review, and improve one visible result.",
        "format": f"Visual references, expert tutorials, checklists, practice logs, mentor/client feedback, and before-after evidence for {title}.",
        "weekly": [
            f"Mon: study core concepts for {role['focus']}",
            f"Tue: practice two foundation drills for {role['skills'][0]} and {role['skills'][1]}",
            f"Wed: complete a supervised mini task and capture mistakes",
            f"Thu: polish one portfolio sample with photos, notes, or a short demo",
            "Fri: reflect, compare against references, and plan next week",
        ],
    }


def role_learning_images(role):
    title = role["title"]
    if "Hair" in title or "Barber" in title:
        return [
            {
                "title": "Straight Hair Reference",
                "caption": "Use this for clean sectioning, even tension, and blunt-line practice.",
                "url": "https://images.unsplash.com/photo-1522336572468-97b06e8ef143?auto=format&fit=crop&w=900&q=80",
            },
            {
                "title": "Curly Hair Texture",
                "caption": "Study curl pattern, volume control, and shape before choosing a cutting angle.",
                "url": "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=900&q=80",
            },
            {
                "title": "Fade And Clipper Work",
                "caption": "Compare low, mid, and high fade transitions while logging guard choices.",
                "url": "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80",
            },
            {
                "title": "Consultation And Styling",
                "caption": "Connect face shape, lifestyle, finish, and maintenance to the final style.",
                "url": role["image"],
            },
        ]
    if "Chef" in title or "Pastry" in title or "Baker" in title:
        return [
            {"title": "Knife Skills", "caption": "Check cut size, safety grip, and board setup.", "url": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=900&q=80"},
            {"title": "Heat Control", "caption": "Compare color, texture, and doneness across heat levels.", "url": "https://images.unsplash.com/photo-1551218808-94e220e084d2?auto=format&fit=crop&w=900&q=80"},
            {"title": "Plating", "caption": "Use overhead and 45-degree photos to improve presentation.", "url": "https://images.unsplash.com/photo-1543353071-10c8ba85a904?auto=format&fit=crop&w=900&q=80"},
        ]
    images = role_exercises(role)[0].get("images") or [role["image"]]
    return [
        {"title": f"{title} Reference {i + 1}", "caption": "Use this as a visual benchmark for your practice output.", "url": image}
        for i, image in enumerate(images[:4])
    ]


def hair_day_images(day):
    day = day.lower()
    image_sets = {
        "mon": [
            ("Hair Type Chart Practice", "Compare straight, wavy, curly, and coily textures before choosing a cut.", "https://images.unsplash.com/photo-1522336572468-97b06e8ef143?auto=format&fit=crop&w=900&q=80"),
            ("Face Shape Consultation", "Match face shape and maintenance level to a suitable haircut reference.", "https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=900&q=80"),
            ("Clean Section Lines", "Look for controlled partings before any cutting starts.", "https://images.unsplash.com/photo-1562004760-aceed7bb0fe3?auto=format&fit=crop&w=900&q=80"),
        ],
        "tue": [
            ("Sectioning Drill", "Create front, side, crown, and nape sections with clean clips.", "https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&w=900&q=80"),
            ("One-Length Cut", "Practice even tension and a clean guide line on a mannequin head.", "https://images.unsplash.com/photo-1560869713-da86a9ecbfa3?auto=format&fit=crop&w=900&q=80"),
            ("Scissor Control", "Keep hand position stable and check balance after each pass.", "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=900&q=80"),
        ],
        "wed": [
            ("Clipper Guard Setup", "Compare guard lengths before blending.", "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80"),
            ("Low Fade Reference", "Study the fade transition below the temple.", "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=900&q=80"),
            ("Blend Check", "Photograph side and back angles to find harsh lines.", "https://images.unsplash.com/photo-1622288432450-277d0fef5ed6?auto=format&fit=crop&w=900&q=80"),
        ],
        "thu": [
            ("Curly Finish", "Preserve curl pattern and shape without flattening volume.", "https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=900&q=80"),
            ("Blow-Dry Styling", "Practice direction, lift, and polished finish.", "https://images.unsplash.com/photo-1521590832167-7bcbfaa6381f?auto=format&fit=crop&w=900&q=80"),
            ("Before-After Photo", "Capture consistent angles and lighting for portfolio proof.", "https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=900&q=80"),
        ],
        "fri": [
            ("Consultation Reference", "Ask about lifestyle, maintenance, and preferred shape before recommending.", "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?auto=format&fit=crop&w=900&q=80"),
            ("Haircut Type Choice", "Compare bob, layers, crop, taper, fade, and textured cut options.", "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=900&q=80"),
            ("Portfolio Review", "Choose the strongest result and write what improved.", "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=900&q=80"),
        ],
    }
    key = next((name for name in image_sets if day.startswith(name)), "mon")
    return [{"title": title, "caption": caption, "url": url} for title, caption, url in image_sets[key]]


def day_detail_steps(role, day, task):
    if "Hair" not in role["title"] and "Barber" not in role["title"]:
        return [
            ("Observe", f"Review 2-3 trusted examples for {role['focus']} and note what good work looks like."),
            ("Practice", f"Complete the task: {task}. Keep the scope small enough to finish today."),
            ("Capture", "Take photos, screenshots, notes, or a short demo as proof of the session."),
            ("Improve", "Compare your result against the reference and write one correction for tomorrow."),
        ]
    day_key = day.lower()[:3]
    plans = {
        "mon": [
            ("Identify", "Pick 3 haircut photos and label hair texture, density, face shape, neckline, and maintenance level."),
            ("Map", "Draw sectioning lines for front, sides, crown, and nape before touching tools."),
            ("Choose", "Select the best haircut type for each reference: blunt cut, layers, bob, taper, fade, or textured crop."),
            ("Log", "Write why the chosen style fits the person and what tool sequence you would use."),
        ],
        "tue": [
            ("Prepare", "Sanitize tools, set combs/clips, dampen mannequin hair, and create four clean sections."),
            ("Cut", "Use a stable guide line for one-length cutting, keeping even tension and body position."),
            ("Check", "Cross-check left/right balance from front, side, and back views."),
            ("Correct", "Photograph the result and mark one uneven area to fix in the next pass."),
        ],
        "wed": [
            ("Set Guards", "Choose guard sequence for low or mid fade practice and mark the first guideline."),
            ("Blend", "Use controlled lever movement and remove one harsh line at a time."),
            ("Inspect", "Photograph side and back angles under bright light to find dark bands."),
            ("Adjust", "Repeat only the weak transition zone and write the guard/lever correction."),
        ],
        "thu": [
            ("Select Finish", "Choose straight, wavy, or curly styling based on the reference photo."),
            ("Style", "Use product, brush direction, heat control, or curl definition without changing the cut shape."),
            ("Shoot", "Take before-after photos from consistent front, side, and back angles."),
            ("Review", "Compare volume, shine, symmetry, and client-ready polish against the reference."),
        ],
        "fri": [
            ("Consult", "Ask face shape, lifestyle, hair type, styling time, and maintenance questions."),
            ("Recommend", "Pick 2 suitable haircut types and explain the reason for each."),
            ("Roleplay", "Practice a client conversation including expectations, constraints, and aftercare."),
            ("Portfolio", "Choose the best weekly photo and write a short improvement note."),
        ],
    }
    return plans.get(day_key, plans["mon"])


def role_roadmaps(role):
    title = role["title"]
    skills = role["skills"]
    return {
        "30-day": [
            ("Week 1", f"Foundations: {skills[0]}, {skills[1]}, safety, tools, and quality standards.", 25, skills[:3], "Create a beginner reference sheet and one clean practice sample."),
            ("Week 2", f"Technique: repeat core drills for {skills[2]} and {skills[3]} with feedback.", 45, skills[2:5], "Finish three practice attempts and note visible improvement."),
            ("Week 3", f"Real workflow: combine skills into one small {title} project.", 65, skills[1:5], "Produce one portfolio-ready result with process photos or screenshots."),
            ("Week 4", "Professional proof: polish portfolio, pricing/resume story, and interview/client explanation.", 85, skills[3:], "Publish a mini case study with what you did, why, and what improved."),
        ],
        "90-day": [
            ("Month 1", f"Build dependable fundamentals for {title} with repeated guided practice.", 35, skills[:4], "Complete 8-10 small practice outputs."),
            ("Month 2", "Work on realistic scenarios, client/user needs, and quality review.", 60, skills[2:], "Complete 3 portfolio projects with feedback."),
            ("Month 3", "Prepare for opportunities: portfolio, resume, outreach, interviews, and trial work.", 82, skills, "Apply to internships, apprenticeships, freelance gigs, or entry roles."),
        ],
        "1-year": [
            ("Q1", f"Foundation: learn tools, safety, vocabulary, and basic execution for {title}.", 30, skills[:3], "Document 20 practice sessions."),
            ("Q2", "Depth: handle varied real-world examples and build a stronger portfolio.", 55, skills[2:5], "Complete 6 polished projects."),
            ("Q3", "Professional signal: client work, competitions, certifications, or public case studies.", 75, skills[3:], "Earn testimonials or mentor reviews."),
            ("Q4", "Career launch: job applications, freelance packages, advanced specialization, and growth plan.", 92, skills, "Secure a role, apprenticeship, clients, or advanced training path."),
        ],
    }


def role_projects(role):
    title = role["title"]
    return [
        {
            "title": f"{title} Starter Portfolio",
            "category": "Portfolio proof",
            "difficulty": role["difficulty"],
            "stack": ", ".join(role["skills"][:4]),
            "outcome": f"Shows your ability to perform core {title} work with clear before-after or process evidence.",
            "resume": f"Demonstrates practical {title} skill, consistency, and attention to quality.",
            "interview": "Gives you a concrete story about process, mistakes, feedback, and improvement.",
            "image": role["image"],
        },
        {
            "title": f"Real Client Simulation for {title}",
            "category": "Real-world practice",
            "difficulty": "Medium",
            "stack": ", ".join(role["skills"][2:]),
            "outcome": "Solves a realistic brief with requirements, constraints, result, and reflection.",
            "resume": "Shows professional judgment and not only isolated practice.",
            "interview": "Helps explain how you understand clients, users, safety, quality, and tradeoffs.",
            "image": role["image"],
        },
    ]


def role_exercises(role):
    title = role["title"]
    if "AI Engineer" in title:
        drills = [
            {
                "title": "MIT-style RAG evaluation lab",
                "text": "Build a small retrieval assistant, create 20 test questions, measure answer faithfulness, and write an error analysis.",
                "source": "Inspired by MIT OpenCourseWare AI and software engineering practice",
                "images": [
                    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Stanford-style prompt and agent experiment",
                "text": "Design one tool-using agent, run five controlled prompt variants, compare failure modes, and keep the best prompt with evidence.",
                "source": "Inspired by Stanford AI coursework and agent evaluation habits",
                "images": [
                    "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Harvard CS50-style product build",
                "text": "Ship a working AI web app with a clear problem, backend API, user flow, demo data, README, and a short demo script.",
                "source": "Inspired by Harvard CS50 final-project practice",
                "images": [
                    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1484417894907-623942c8ee29?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Berkeley-style model behavior report",
                "text": "Create a benchmark table for latency, cost, accuracy, safety issues, and user experience tradeoffs across three model settings.",
                "source": "Inspired by UC Berkeley data and AI systems coursework",
                "images": [
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    elif "Machine Learning" in title:
        drills = [
            {
                "title": "Stanford CS229-style baseline challenge",
                "text": "Train a baseline model, tune one stronger model, compare metrics, and explain exactly why the winner improved.",
                "source": "Inspired by Stanford machine learning coursework",
                "images": [
                    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "MIT-style reproducibility notebook",
                "text": "Rebuild one experiment from a paper or tutorial with clean data splits, fixed seeds, metrics, and a reproducible notebook.",
                "source": "Inspired by MIT OpenCourseWare engineering rigor",
                "images": [
                    "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Berkeley-style error analysis",
                "text": "Collect 50 wrong predictions, group errors by cause, and propose data, feature, or modeling fixes for each group.",
                "source": "Inspired by UC Berkeley data science practice",
                "images": [
                    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    elif "Data Scientist" in title:
        drills = [
            {
                "title": "Berkeley DS100-style EDA memo",
                "text": "Clean a messy dataset, make five charts, state three findings, and write one decision recommendation.",
                "source": "Inspired by UC Berkeley data science coursework",
                "images": [
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Harvard statistics-style experiment brief",
                "text": "Define a hypothesis, choose a metric, compare two groups, report uncertainty, and explain what you would test next.",
                "source": "Inspired by Harvard statistics and CS data practice",
                "images": [
                    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "MIT-style decision dashboard",
                "text": "Build a dashboard that answers one business question with filters, a KPI, a trend chart, and a written recommendation.",
                "source": "Inspired by MIT analytics and systems thinking",
                "images": [
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    elif "Software Developer" in title:
        drills = [
            {
                "title": "Harvard CS50-style CRUD app",
                "text": "Build a small app with create, read, update, delete, validation, a database, and a README that explains the design.",
                "source": "Inspired by Harvard CS50 project practice",
                "images": [
                    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "MIT-style debugging journal",
                "text": "Fix three bugs, write the root cause for each, add one regression test, and document the lesson learned.",
                "source": "Inspired by MIT software construction practice",
                "images": [
                    "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1484417894907-623942c8ee29?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Stanford-style design review",
                "text": "Sketch an architecture, list tradeoffs, identify failure cases, and refactor one part for simpler maintenance.",
                "source": "Inspired by Stanford engineering design habits",
                "images": [
                    "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    elif "Hair" in title or "Barber" in title:
        drills = [
            {
                "title": "Front guide and sectioning",
                "text": "Use front, side, crown, and back reference images. Mark clean sections and practice even tension before cutting.",
                "source": "Professional cosmetology practice drill",
                "images": [
                    "https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1562004760-aceed7bb0fe3?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "45-degree layered cut drill",
                "text": "Compare side-angle references, lift sections consistently, and photograph each angle after the pass.",
                "source": "Professional cosmetology practice drill",
                "images": [
                    "https://images.unsplash.com/photo-1522336572468-97b06e8ef143?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1519699047748-de8e457a634e?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1560869713-da86a9ecbfa3?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Fade blending practice",
                "text": "Use low, mid, and high fade reference photos. Practice guard transitions on a mannequin head and log harsh-line fixes.",
                "source": "Professional barbering practice drill",
                "images": [
                    "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1622288432450-277d0fef5ed6?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Client consultation roleplay",
                "text": "Match face shape, hair type, lifestyle, and maintenance level to a suitable haircut recommendation.",
                "source": "Professional consultation practice drill",
                "images": [
                    "https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1562322140-8baeececf3df?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    elif "Chef" in title or "Pastry" in title or "Baker" in title:
        drills = [
            {"title": "Knife cuts board", "text": "Practice dice, julienne, chiffonade, and batonnet; photograph the board from above to check size consistency.", "source": "Culinary school fundamentals drill", "images": [role["image"]]},
            {"title": "Heat-control comparison", "text": "Cook the same ingredient three ways and document texture, color, time, and taste differences.", "source": "Culinary school fundamentals drill", "images": [role["image"]]},
            {"title": "Plating angles", "text": "Photograph one dish from overhead, 45 degrees, and table level to improve presentation.", "source": "Culinary school presentation drill", "images": [role["image"]]},
            {"title": "Recipe scaling", "text": "Convert one recipe for 2, 4, and 10 servings and verify ingredient ratios.", "source": "Culinary production practice drill", "images": [role["image"]]},
        ]
    else:
        drills = [
            {"title": f"{role['skills'][0]} drill", "text": f"Study 3 reference examples, copy the structure, then create your own version for {title}.", "source": "University-style deliberate practice", "images": [role["image"]]},
            {"title": f"{role['skills'][1]} practice", "text": "Do three timed repetitions, compare against a trusted reference, and write one improvement note per attempt.", "source": "University-style deliberate practice", "images": [role["image"]]},
            {"title": "Real-world scenario", "text": f"Solve a small realistic {title} task with constraints, quality checks, and final evidence.", "source": "University-style project practice", "images": [role["image"]]},
            {"title": "Portfolio reflection", "text": "Capture screenshots/photos, explain your process, and list what you will improve next.", "source": "University-style critique practice", "images": [role["image"]]},
        ]
    return [
        {
            **drill,
            "image": drill.get("images", [role["image"]])[0],
            "images": drill.get("images", [role["image"]]),
        }
        for drill in drills
    ]


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

.learning-image-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 0.85rem;
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


def local_agent_response(message, context=None):
    context = context or {}
    role_title = context.get("top_role") or context.get("goal") or "your selected role"
    text = str(message or "").lower()
    is_hair = any(word in f"{role_title} {text}".lower() for word in ["hair", "barber", "stylist", "hairstyle", "haircut", "fade"])
    if is_hair and not any(word in str(role_title).lower() for word in ["hair", "barber", "stylist"]):
        role_title = "Barber / Hair Stylist"
    if is_hair and any(word in text for word in ["skill", "practice", "first", "photo", "image", "screenshot", "type", "style", "hairstyle", "haircut"]):
        return {
            "response": (
                f"For {role_title}, practice these first: sectioning, clipper control, scissor-over-comb, and face-shape consultation. "
                "Start with clean sectioning, then one-length cutting, then fade blending, then consultation by face shape and hair type.\n\n"
                "Relevant references:\n"
                "![Sectioning and styling](https://images.unsplash.com/photo-1522336572468-97b06e8ef143?auto=format&fit=crop&w=900&q=80)\n"
                "![Curly hair texture](https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=900&q=80)\n"
                "![Fade and clipper work](https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80)"
            ),
            "tool": "recommend_career",
            "tool_result": {},
            "next_actions": [
                "Practice sectioning on a mannequin head.",
                "Photograph each attempt from front, side, and back.",
            ],
        }
    return {
        "response": f"For {role_title}, start with one visible practice deliverable, compare it against a trusted reference, and write one improvement note.",
        "tool": "local_fallback",
        "tool_result": {},
        "next_actions": ["Create one small proof artifact", "Review it with a mentor or reference"],
    }


def call_agent(message, context=None):
    context = context or {}
    try:
        response = requests.post(
            AGENT_URL,
            json={"message": message, "context": context},
            timeout=12,
        )
        response.raise_for_status()
        result = response.json()
        role_title = str(context.get("top_role") or context.get("goal") or "")
        message_text = str(message or "").lower()
        stale_hair_response = (
            any(word in f"{role_title} {message_text}".lower() for word in ["hair", "barber", "stylist", "hairstyle", "haircut", "fade"])
            and any(term in str(result.get("response", "")).lower() for term in ["rag", "langgraph", "technical, research", "ai engineer"])
        )
        if stale_hair_response:
            return local_agent_response(message, context), False
        return result, True
    except requests.RequestException:
        return local_agent_response(message, context), False


def call_reflection(payload):
    try:
        response = requests.post(REFLECTION_URL, json=payload, timeout=12)
        response.raise_for_status()
        return response.json(), True
    except requests.RequestException:
        return None, False


def score_potential_scan(payload):
    skills = split_terms(payload.get("skills", []))
    narrative_text = " ".join(
        [
            payload.get("target_role", ""),
            payload.get("interests", ""),
            payload.get("career_goal", ""),
            payload.get("constraints", ""),
            payload.get("profile_details", ""),
        ]
    ).lower()
    text = f"{narrative_text} {' '.join(skills).lower()}"
    experience = int(payload.get("experience", 0))
    learning_hours = int(payload.get("learning_hours", 5))
    project_depth = int(payload.get("project_depth", 5))
    general_level = int(payload.get("general_level", payload.get("ai_level", 5)))
    skill_text = " ".join(skill.lower() for skill in skills)
    scored_roles = []
    for role in ROLE_CATALOG:
        keyword_hits = count_term_hits(role["keywords"], narrative_text)
        skill_hits = sum(1 for skill in role["skills"] if term_in_text(skill, skill_text) or term_in_text(skill, text))
        target_role = payload.get("target_role", "")
        exact_role_bonus = 24 if term_in_text(role["title"], text) or term_in_text(target_role, role["title"].lower()) else 0
        signal_count = keyword_hits + skill_hits + (1 if exact_role_bonus else 0)
        readiness = min(experience, 6) * 1.5 + min(learning_hours, 18) * 0.7 + project_depth * 1.4 + general_level * 1.4
        if signal_count:
            score = 30 + keyword_hits * 13 + skill_hits * 9 + exact_role_bonus + readiness
        else:
            score = 18 + readiness * 0.45
        scored = {**role, "match": int(max(12, min(98, round(score))))}
        scored_roles.append(scored)
    scored_roles = sorted(scored_roles, key=lambda role: role["match"], reverse=True)
    top = scored_roles[0]
    high_signal_roles = [role for role in scored_roles if role["match"] >= 70 or role["title"] == top["title"]]
    scores = {role["title"]: role["match"] for role in high_signal_roles[:8]}
    learning = role_learning_plan(top, learning_hours)
    roadmaps = role_roadmaps(top)
    projects = role_projects(top)
    exercises = role_exercises(top)
    prompts = [
        f"Create a 30-day beginner-to-pro plan for {top['title']}.",
        f"What skills should I practice first for {top['title']}?",
        f"Give me project ideas and portfolio proof for {top['title']}.",
        f"Analyze my strengths and gaps for becoming a {top['title']}.",
        f"Make day-wise exercises with reference-image guidance for {top['title']}.",
    ]
    return {
        "scores": scores,
        "top_track": top["title"],
        "summary": f"{payload.get('name', 'This profile')} is strongest for {top['title']} based on interests, skills, goals, and practice readiness.",
        "focus": top["focus"],
        "recommended_roles": high_signal_roles[:5],
        "learning": learning,
        "roadmaps": roadmaps,
        "projects": projects,
        "exercises": exercises,
        "prompts": prompts,
        "growth": [
            {"week": "W1", "Core Skill": min(100, top["match"] - 18), "Practice": min(100, project_depth * 8), "Confidence": min(100, general_level * 8)},
            {"week": "W2", "Core Skill": min(100, top["match"] - 12), "Practice": min(100, project_depth * 9), "Confidence": min(100, general_level * 8 + 6)},
            {"week": "W3", "Core Skill": min(100, top["match"] - 6), "Practice": min(100, project_depth * 10), "Confidence": min(100, general_level * 8 + 12)},
            {"week": "W4", "Core Skill": top["match"], "Practice": min(100, project_depth * 10 + 8), "Confidence": min(100, general_level * 8 + 18)},
        ],
        "next_actions": [
            f"Start with {top['skills'][0]} and {top['skills'][1]} because they unlock visible beginner progress.",
            f"Build one proof project focused on {top['focus']}.",
            "Capture photos, screenshots, notes, or demos after every practice session.",
        ],
    }


def call_potential_scan(payload):
    local_result = score_potential_scan(payload)
    try:
        response = requests.post(SCAN_URL, json=payload, timeout=12)
        response.raise_for_status()
        return local_result, True
    except requests.RequestException:
        return local_result, False


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
    palette = ["#7C3AED", "#06B6D4", "#22C55E", "#F59E0B", "#A855F7"]
    columns = [column for column in df.columns if column != "week"]
    for i, column in enumerate(columns):
        fig.add_trace(
            go.Scatter(
                x=df["week"],
                y=df[column],
                mode="lines+markers",
                name=column,
                line=dict(color=palette[i % len(palette)], width=3, shape="spline"),
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


def bar_chart(potential, orientation="h"):
    labels = list(potential.keys())
    values = list(potential.values())
    is_vertical = orientation == "v"
    fig = go.Figure(
        go.Bar(
            x=labels if is_vertical else values,
            y=values if is_vertical else labels,
            orientation="v" if is_vertical else "h",
            marker=dict(
                color=values,
                colorscale=[[0, "#312E81"], [0.55, "#7C3AED"], [1, "#06B6D4"]],
                line=dict(color="rgba(255,255,255,0.18)", width=1),
            ),
            text=[f"{value}%" for value in values],
            textposition="outside" if is_vertical else "auto",
        )
    )
    fig.update_layout(
        height=390,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.025)",
        font=dict(color="#F8FAFC", family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickangle=-20 if is_vertical else 0),
        yaxis=dict(range=[0, 105], gridcolor="rgba(255,255,255,0.08)") if is_vertical else dict(gridcolor="rgba(255,255,255,0.02)"),
        margin=dict(l=20, r=20, t=30, b=80 if is_vertical else 20),
    )
    if not is_vertical:
        fig.update_xaxes(range=[0, 100])
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
    st.caption("Enter interests, skills, and goals to estimate fit across many professional roles.")
    profile = data["profile"]
    left, right = st.columns([0.56, 0.44])
    with left:
        with st.form("potential_scan_form"):
            name = st.text_input("Name", profile["name"])
            target_role = st.text_input("Target role or area", "Open to best match")
            profile_details = st.text_area(
                "Tell HPI AI what you like or know",
                "Example: I like haircutting, styling hair, and helping people look confident.",
            )
            skills = st.multiselect(
                "Current skills",
                SKILL_OPTIONS,
                default=[skill for skill in profile["skills"] if skill in SKILL_OPTIONS],
            )
            custom_skills = st.text_input("Other skills or knowledge", "consultation, practice, visual learning")
            c1, c2 = st.columns(2)
            with c1:
                experience = st.number_input("Relevant experience in years", min_value=0, max_value=20, value=1)
                learning_hours = st.slider("Weekly learning hours", 1, 30, 10)
                general_level = st.slider("Current confidence level", 1, 10, 6)
            with c2:
                visual_level = st.slider("Visual or practical learning level", 1, 10, 7)
                project_depth = st.slider("Portfolio project depth", 1, 10, 6)
            interests = st.text_area("Interests", ", ".join(profile["interests"]))
            career_goal = st.text_area("Career goal", profile["goal"])
            constraints = st.text_area("Constraints or challenges", "Need a clear path and portfolio projects that prove job-ready skills.")
            submitted = st.form_submit_button("Analyze Potential", type="primary")
    if submitted:
        payload = {
            "name": name,
            "target_role": target_role,
            "skills": skills + split_terms(custom_skills),
            "experience": experience,
            "learning_hours": learning_hours,
            "general_level": max(general_level, visual_level),
            "project_depth": project_depth,
            "interests": interests,
            "career_goal": career_goal,
            "constraints": constraints,
            "profile_details": profile_details,
        }
        result, live = call_potential_scan(payload)
        st.session_state.potential_scan_result = result
        st.session_state.potential_scan_live = live
        st.session_state.scan_payload = payload
        st.session_state.agent_messages = [
            {
                "role": "assistant",
                "content": f"Your strongest match is {result['top_track']}. Ask me for prompts, roadmaps, exercises, or project ideas for this role.",
            }
        ]
        st.session_state.current_page = "Career Intelligence"
        st.rerun()

    with right:
        result = st.session_state.get("potential_scan_result") or score_potential_scan(
            {
                "name": profile["name"],
                "skills": profile["skills"],
                "experience": 1,
                "learning_hours": 10,
                "general_level": 7,
                "project_depth": 6,
                "interests": ", ".join(profile["interests"]),
                "career_goal": profile["goal"],
                "profile_details": "I enjoy AI agents, machine learning, and building useful products.",
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
    result = active_scan_result(data)
    st.title("Potential Analysis")
    st.caption("Balanced view of the strongest career signals from the latest scan.")
    cols = st.columns(3)
    accent_cycle = ["#7C3AED", "#06B6D4", "#A855F7", "#22C55E", "#F59E0B", "#38BDF8"]
    for i, (label, value) in enumerate(result["scores"].items()):
        with cols[i % 3]:
            accent = accent_cycle[i % len(accent_cycle)]
            card(
                f"""
                <div class="glass-card metric-card" style="--accent:{accent};">
                    <div class="metric-label">{esc(label)} Match</div>
                    <div class="metric-value">{value}<span style="font-size:1rem;color:#94A3B8;">%</span></div>
                    <div class="progress-track"><div class="progress-fill" style="--value:{value}%;"></div></div>
                </div>
                """
            )
    left, right = st.columns([1.05, 0.95])
    with left:
        st.plotly_chart(bar_chart(result["scores"]), use_container_width=True)
    with right:
        st.plotly_chart(potential_radar(dict(list(result["scores"].items())[:6])), use_container_width=True)
    card(
        f"""
        <div class="glass-card">
            <div class="card-title">AI Interpretation</div>
            <div class="muted">
            {esc(result['summary'])} The recommended growth strategy is to focus on {esc(result['focus'])}.
            This is guidance, not destiny prediction.
            </div>
        </div>
        """
    )


def career_card(career):
    confidence = career.get("confidence", "High" if career.get("match", 0) >= 75 else "Medium")
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
            <span class="badge">Confidence: {confidence}</span>
        </div>
        <div class="badge-row">{''.join(f'<span class="badge">{skill}</span>' for skill in career['skills'])}</div>
        <div style="margin-top:0.9rem;" class="muted"><strong style="color:#F8FAFC;">Next step:</strong> {career['next']}</div>
        <div class="progress-track"><div class="progress-fill" style="--value:{career['match']}%; --accent:#06B6D4;"></div></div>
    </div>
    """


def career_intelligence(data):
    result = active_scan_result(data)
    roles = result.get("recommended_roles") or []
    top = roles[0] if roles else top_role(result)
    top_score = int(top.get("match", result.get("scores", {}).get(result["top_track"], 0)))
    highlighted_scores = {top["title"]: top_score} if top_score >= 90 else {top["title"]: top_score}
    st.title("Career Intelligence")
    st.caption("Highlighted best-fit career path from the latest scan.")
    card(
        f"""
        <div class="glass-card">
            <div class="metric-label">Best-fit role</div>
            <div class="metric-value" style="font-size:2rem;">{esc(top['title'])}</div>
            <div class="career-match">{top_score}%</div>
            <div class="muted">{esc(result['summary'])} Focus next on {esc(result['focus'])}.</div>
            <div class="badge-row">
                <span class="badge">{'Backend scan' if st.session_state.get('potential_scan_live') else 'Local scan'}</span>
                <span class="badge">Explainable recommendation</span>
                <span class="badge">{'90%+ match' if top_score >= 90 else 'Highest available match'}</span>
            </div>
        </div>
        """
    )
    st.plotly_chart(bar_chart(highlighted_scores, orientation="v"), use_container_width=True)
    card(career_card(top))


def ai_agent(data):
    result = active_scan_result(data)
    role = top_role(result)
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
                "goal": st.session_state.get("scan_payload", {}).get("career_goal", data["profile"]["goal"]),
                "skills": st.session_state.get("scan_payload", {}).get("skills", data["profile"]["skills"]),
                "interests": st.session_state.get("scan_payload", {}).get("interests", data["profile"]["interests"]),
                "top_role": role["title"],
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
            *result.get("prompts", [])[:5],
        ]
        for example in examples:
            if st.button(example, use_container_width=True):
                result, _ = call_agent(example, {"goal": role["title"], "top_role": role["title"]})
                st.session_state.agent_messages.append({"role": "user", "content": example})
                st.session_state.agent_messages.append({"role": "assistant", "content": result["response"]})
                st.rerun()


def learning_style(data):
    result = active_scan_result(data)
    learning = result.get("learning", data["learning"])
    role = top_role(result)
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
                    <span class="badge">Visual</span><span class="badge">Practice-first</span>
                    <span class="badge">{esc(role['title'])}</span>
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
            if st.button(day, key=f"learning_{day}", use_container_width=True):
                st.session_state.learning_detail = item
                st.session_state.current_page = "Learning Plan Detail"
                st.rerun()
            card(f'<div class="glass-card"><div class="card-title">{esc(day)}</div><div class="muted">{esc(task)}</div></div>')
    selected = st.session_state.get("learning_detail", learning["weekly"][0])
    if selected not in learning["weekly"]:
        selected = learning["weekly"][0]
        st.session_state.learning_detail = selected
    day, task = selected.split(": ", 1)
    card(
        f"""
        <div class="glass-card">
            <div class="card-title">{esc(day)} Detailed Plan</div>
            <div class="muted">{esc(task)}. Use trusted tutorials, mentor feedback, reference images, and a written practice log. End the session with one visible proof item and one improvement note.</div>
        </div>
        """
    )


def learning_plan_detail(data):
    result = active_scan_result(data)
    learning = result.get("learning", data["learning"])
    role = top_role(result)
    selected = st.session_state.get("learning_detail", learning["weekly"][0])
    if selected not in learning["weekly"]:
        selected = learning["weekly"][0]
        st.session_state.learning_detail = selected
    day, task = selected.split(": ", 1)
    st.title(f"{day} Learning Plan")
    st.caption(f"Focused practice plan for {role['title']}.")
    c1, c2 = st.columns([0.58, 0.42])
    with c1:
        card(
            f"""
            <div class="glass-card">
                <div class="metric-label">Selected Day</div>
                <div class="metric-value" style="font-size:2rem;">{esc(day)}</div>
                <div class="muted">{esc(task)}.</div>
                <div class="badge-row">
                    <span class="badge">{esc(role['title'])}</span>
                    <span class="badge">Practice log</span>
                    <span class="badge">Visual reference</span>
                </div>
            </div>
            """
        )
        st.markdown('<div class="section-title">Step-by-Step Plan</div>', unsafe_allow_html=True)
        steps = day_detail_steps(role, day, task)
        for title, text in steps:
            card(f'<div class="glass-card"><div class="card-title">{esc(title)}</div><div class="muted">{esc(text)}</div></div>')
    with c2:
        st.markdown('<div class="section-title">Skill References</div>', unsafe_allow_html=True)
        images = hair_day_images(day) if "Hair" in role["title"] or "Barber" in role["title"] else role_learning_images(role)
        for image in images:
            card(
                f"""
                <div class="glass-card learning-image-card">
                    <img src="{esc(image['url'])}" alt="{esc(image['title'])}" />
                    <div class="card-title">{esc(image['title'])}</div>
                    <div class="muted">{esc(image['caption'])}</div>
                </div>
                """
            )
    if st.button("Back to Weekly Plan", use_container_width=True):
        go_to("Learning Style")


def roadmap(data):
    result = active_scan_result(data)
    roadmaps = result.get("roadmaps", data["roadmaps"])
    st.title("Roadmap")
    st.caption("Milestone-driven plans that connect near-term execution to long-term career movement.")
    tabs = st.tabs(["30-day", "90-day", "1-year"])
    for tab, key in zip(tabs, ["30-day", "90-day", "1-year"]):
        with tab:
            st.markdown('<div class="timeline">', unsafe_allow_html=True)
            for item in roadmaps[key]:
                label, text, progress = item[:3]
                skills = item[3] if len(item) > 3 else []
                deliverable = item[4] if len(item) > 4 else "Complete the checkpoint and document what improved."
                card(
                    f"""
                    <div class="timeline-item">
                        <div class="card-title">{esc(label)}</div>
                        <div class="muted">{esc(text)}</div>
                        <div class="badge-row">{''.join(f'<span class="badge">{esc(skill)}</span>' for skill in skills)}</div>
                        <div class="muted" style="margin-top:0.65rem;"><strong style="color:#F8FAFC;">Deliverable:</strong> {esc(deliverable)}</div>
                        <div class="progress-track"><div class="progress-fill" style="--value:{progress}%; --accent:#7C3AED;"></div></div>
                        <div class="muted" style="margin-top:0.5rem;">{progress}% checkpoint readiness</div>
                    </div>
                    """
                )
            st.markdown("</div>", unsafe_allow_html=True)


def project_ideas(data):
    result = active_scan_result(data)
    projects = result.get("projects", data["projects"])
    st.title("Project Ideas")
    st.caption("Portfolio projects chosen for skill proof, demo quality, resume value, and interview depth.")
    cols = st.columns(2)
    for i, project in enumerate(projects):
        with cols[i % 2]:
            card(
                f"""
                <div class="glass-card">
                    <img src="{esc(project.get('image', 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80'))}" style="width:100%;height:190px;object-fit:cover;border-radius:8px;margin-bottom:0.9rem;border:1px solid rgba(255,255,255,0.12);" />
                    <div class="metric-label">{esc(project['category'])}</div>
                    <div class="card-title">{esc(project['title'])}</div>
                    <div class="badge-row">
                        <span class="badge">{esc(project['difficulty'])}</span>
                        <span class="badge">{esc(project['stack'])}</span>
                    </div>
                    <div class="muted" style="margin-top:0.9rem;"><strong style="color:#F8FAFC;">Outcome:</strong> {esc(project['outcome'])}</div>
                    <div class="muted"><strong style="color:#F8FAFC;">Resume value:</strong> {esc(project['resume'])}</div>
                    <div class="muted"><strong style="color:#F8FAFC;">Interview value:</strong> {esc(project['interview'])}</div>
                </div>
                """
            )


def reflection_growth(data):
    result = active_scan_result(data)
    role = top_role(result)
    st.title("Reflection & Growth")
    st.caption("A personal AI coach surface for weekly reflection, momentum tracking, and growth insights.")
    left, right = st.columns([1, 1])
    with left:
        with st.form("reflection_form"):
            st.markdown("### Weekly Reflection")
            energy = st.slider("Energy level", 1, 10, 7)
            curiosity = st.text_input("Curiosity topics", role["focus"])
            wins = st.text_area("Wins", f"Practiced {role['skills'][0]} and collected evidence for {role['title']}.")
            challenges = st.text_area("Challenges", f"Need a clearer practice routine and feedback loop for {role['title']}.")
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
                    f"Energy is {energy}/10 with curiosity around {curiosity}. For {role['title']}, convert wins into visible proof, reduce friction "
                    f"around {role['skills'][0]}, and choose one measurable checkpoint for the next seven days."
                )
                st.caption("Backend unavailable, showing local fallback insight.")
        card(
            f"""
            <div class="glass-card">
                <div class="card-title">AI Growth Insight</div>
                <div class="muted">{insight}</div>
                <div class="badge-row">
                    <span class="badge">{esc(role['title'])}</span>
                    <span class="badge">Momentum: {esc('rising' if energy >= 6 else 'needs recovery')}</span>
                    <span class="badge">Practice coach mode</span>
                </div>
            </div>
            """
        )
        st.plotly_chart(growth_chart(result.get("growth", data["growth"])), use_container_width=True)


def exercises(data):
    result = active_scan_result(data)
    role = top_role(result)
    items = result.get("exercises", role_exercises(role))
    st.title("Exercises")
    st.caption("Best practice exercises inspired by top university learning patterns, with reference images available on demand.")
    card(
        f"""
        <div class="glass-card">
            <div class="metric-label">Practice role</div>
            <div class="metric-value" style="font-size:2rem;">{esc(role['title'])}</div>
            <div class="muted">These exercises are matched to the scan result and focus on becoming job-ready through repeated, visible practice, evidence, and review.</div>
        </div>
        """
    )
    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i % 2]:
            card(
                f"""
                <div class="glass-card">
                    <div class="metric-label">{esc(item.get('source', 'University-style practice'))}</div>
                    <div class="card-title">{esc(item['title'])}</div>
                    <div class="muted">{esc(item['text'])}</div>
                    <div class="badge-row">
                        <span class="badge">Top university inspired</span>
                        <span class="badge">Practice log</span>
                        <span class="badge">Feedback cycle</span>
                    </div>
                </div>
                """
            )
            refs_key = f"exercise_refs_{role['title']}_{i}"
            if st.button("Reference images", key=f"reference_images_{i}", use_container_width=True):
                st.session_state[refs_key] = not st.session_state.get(refs_key, False)
            if st.session_state.get(refs_key):
                ref_images = item.get("images") or [item.get("image", role["image"])]
                image_cols = st.columns(min(3, len(ref_images)))
                for img_i, image in enumerate(ref_images):
                    with image_cols[img_i % len(image_cols)]:
                        st.image(image, use_container_width=True)


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
        "Learning Plan Detail": learning_plan_detail,
        "Roadmap": roadmap,
        "Project Ideas": project_ideas,
        "Reflection & Growth": reflection_growth,
        "Exercises": exercises,
        "Privacy & Ethics": privacy_ethics,
    }
    pages[page](data)


if __name__ == "__main__":
    main()
