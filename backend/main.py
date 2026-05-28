import re
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.agent import HPIAgent
from backend.data import get_demo_data


app = FastAPI(title="HPI AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=3000)
    context: dict[str, Any] = Field(default_factory=dict)


class ReflectionRequest(BaseModel):
    energy: int = Field(default=7, ge=1, le=10)
    curiosity: str = ""
    wins: str = ""
    challenges: str = ""


class PotentialScanRequest(BaseModel):
    name: str = Field(default="Vamsi", max_length=120)
    target_role: str = Field(default="AI Engineer", max_length=120)
    skills: list[str] = Field(default_factory=list)
    experience: int = Field(default=1, ge=0, le=20)
    learning_hours: int = Field(default=10, ge=1, le=30)
    stats_level: int = Field(default=6, ge=1, le=10)
    ml_level: int = Field(default=6, ge=1, le=10)
    ai_level: int = Field(default=7, ge=1, le=10)
    general_level: int = Field(default=6, ge=1, le=10)
    project_depth: int = Field(default=6, ge=1, le=10)
    interests: str = ""
    career_goal: str = ""
    constraints: str = ""
    profile_details: str = ""


ROLE_CATALOG = [
    ("Barber / Hair Stylist", ["hair", "haircut", "haircutting", "barber", "salon", "hairstyle", "styling", "grooming", "beard", "fade"], ["sectioning", "clipper control", "scissor-over-comb", "consultation", "sanitation"], "hair types, cutting angles, face shapes, tool safety, and portfolio photos", "Practice sectioning, one-length cuts, fades, and consultation scripts on mannequin heads."),
    ("Chef / Culinary Professional", ["cook", "cooking", "recipe", "recipes", "chef", "food", "kitchen", "culinary"], ["knife skills", "mise en place", "food safety", "sauce foundations", "plating"], "knife skills, heat control, mother sauces, food safety, menu costing, and service timing", "Build a 12-dish portfolio with photos, tasting notes, and improvements."),
    ("Pastry Chef / Baker", ["bake", "baking", "pastry", "cake", "dessert", "bread"], ["weighing", "dough handling", "temperature control", "decoration", "recipe testing"], "ingredient ratios, fermentation, pastry technique, decoration, and batch consistency", "Create a pastry sampler with bread, cake, tart, cookies, and one decorated item."),
    ("Photographer", ["photo", "photography", "camera", "portrait", "lighting", "editing"], ["composition", "lighting", "manual exposure", "photo editing", "posing"], "composition, light direction, editing workflow, client shot lists, and portfolio curation", "Shoot five collections: portrait, product, food, event, and documentary."),
    ("Graphic Designer", ["design", "drawing", "logo", "poster", "brand", "graphics", "figma"], ["typography", "layout", "color systems", "brand identity", "Figma"], "layout, typography, visual hierarchy, brand systems, critique, and client presentation", "Design a mini brand kit with logo, colors, social posts, and a poster."),
    ("UI/UX Designer", ["ui", "ux", "wireframe", "prototype", "figma", "user experience"], ["user research", "wireframing", "prototyping", "usability testing", "accessibility"], "research, user flows, wireframes, components, usability tests, and case studies", "Redesign one everyday app flow and document the case study."),
    ("Digital Marketer", ["marketing", "social media", "seo", "ads", "content", "campaign"], ["SEO", "copywriting", "campaign analytics", "content calendar", "paid ads"], "SEO, short-form content, analytics, funnels, ad tests, and campaign reporting", "Run a 14-day content campaign and report reach, clicks, and lessons."),
    ("Teacher / Tutor", ["teach", "teacher", "tutor", "explain", "students", "education"], ["lesson planning", "concept explanation", "assessment", "feedback", "empathy"], "lesson design, diagnostics, examples, practice sets, feedback loops, and learner motivation", "Create and deliver a 5-lesson mini-course with worksheets and quizzes."),
    ("Fitness Trainer", ["fitness", "gym", "workout", "training", "exercise", "nutrition"], ["movement screening", "program design", "coaching cues", "nutrition basics", "progress tracking"], "anatomy basics, exercise technique, program design, safety, and assessments", "Build beginner, fat-loss, strength, and mobility plans with demo videos."),
    ("Electrician", ["electric", "electrician", "wiring", "repair", "circuits", "tools"], ["safety codes", "circuit basics", "wiring diagrams", "multimeter use", "troubleshooting"], "electrical safety, circuit theory, wiring standards, tools, diagnostics, and supervised practice", "Study local code basics and practice safe low-voltage circuits."),
    ("Software Developer", ["code", "coding", "software", "app", "web", "javascript", "python", "programming"], ["programming", "debugging", "Git", "APIs", "databases", "testing"], "programming fundamentals, web apps, APIs, databases, testing, and deployment", "Build a CRUD app with login, database, API, tests, and a deployed demo."),
    ("Data Scientist", ["data", "statistics", "analytics", "sql", "python", "pandas", "dashboard"], ["statistics", "SQL", "Pandas", "visualization", "experimentation"], "statistics, SQL, exploratory analysis, visualization, experiments, and explainable insights", "Create an end-to-end analysis notebook with findings and recommendations."),
    ("Machine Learning Engineer", ["machine learning", "ml", "model", "scikit", "tensorflow", "pytorch"], ["feature engineering", "model training", "evaluation", "MLflow", "model serving"], "features, metrics, experiment tracking, model serving, monitoring, and reproducibility", "Train, evaluate, and deploy a prediction model behind an API."),
    ("AI Engineer", ["ai", "llm", "agent", "rag", "chatbot", "openai", "langchain"], ["LLM apps", "RAG", "tool use", "FastAPI", "evaluation"], "RAG, tool-using agents, evaluation, backend APIs, safety, and product UX", "Build an assistant that answers from documents and calls tools."),
]

ROLE_IMAGES = {
    "Barber / Hair Stylist": "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=900&q=80",
    "Chef / Culinary Professional": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=900&q=80",
    "Pastry Chef / Baker": "https://images.unsplash.com/photo-1517433367423-c7e5b0f35086?auto=format&fit=crop&w=900&q=80",
    "Photographer": "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?auto=format&fit=crop&w=900&q=80",
    "Graphic Designer": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
    "UI/UX Designer": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=900&q=80",
    "Digital Marketer": "https://images.unsplash.com/photo-1557838923-2985c318be48?auto=format&fit=crop&w=900&q=80",
    "Teacher / Tutor": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=900&q=80",
    "Software Developer": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
    "Data Scientist": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
    "Machine Learning Engineer": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
    "AI Engineer": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
}


def term_in_text(term: str, text: str) -> bool:
    term = str(term or "").strip().lower()
    if not term:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None


def count_term_hits(terms: list[str], text: str) -> int:
    return sum(1 for term in terms if term_in_text(term, text))


def university_exercises_for_role(top: dict) -> list[dict]:
    title = top["title"]
    fallback_image = top.get("image", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80")
    if title == "AI Engineer":
        return [
            {
                "title": "MIT-style RAG evaluation lab",
                "text": "Build a small retrieval assistant, create 20 test questions, measure answer faithfulness, and write an error analysis.",
                "source": "Inspired by MIT OpenCourseWare AI and software engineering practice",
                "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=900&q=80",
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
                "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=900&q=80",
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
                "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
                "images": [
                    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1484417894907-623942c8ee29?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    if title == "Machine Learning Engineer":
        return [
            {
                "title": "Stanford CS229-style baseline challenge",
                "text": "Train a baseline model, tune one stronger model, compare metrics, and explain exactly why the winner improved.",
                "source": "Inspired by Stanford machine learning coursework",
                "image": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
                "images": [
                    "https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?auto=format&fit=crop&w=900&q=80",
                ],
            },
            {
                "title": "Berkeley-style error analysis",
                "text": "Collect 50 wrong predictions, group errors by cause, and propose data, feature, or modeling fixes for each group.",
                "source": "Inspired by UC Berkeley data science practice",
                "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80",
                "images": [
                    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    if title == "Data Scientist":
        return [
            {
                "title": "Berkeley DS100-style EDA memo",
                "text": "Clean a messy dataset, make five charts, state three findings, and write one decision recommendation.",
                "source": "Inspired by UC Berkeley data science coursework",
                "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=80",
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
                "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=80",
                "images": [
                    "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1542744095-fcf48d80b0fd?auto=format&fit=crop&w=900&q=80",
                ],
            },
        ]
    return [
        {
            "title": f"{top['skills'][0]} drill",
            "text": f"Study 3 reference examples, copy the structure, then create your own version for {title}.",
            "source": "University-style deliberate practice",
            "image": fallback_image,
            "images": [fallback_image],
        },
        {
            "title": "Real-world scenario",
            "text": f"Solve a small realistic {title} task with constraints, quality checks, and final evidence.",
            "source": "University-style project practice",
            "image": fallback_image,
            "images": [fallback_image],
        },
    ]


def analyze_potential_scan(payload: PotentialScanRequest) -> dict:
    narrative_text = " ".join(
        [
            payload.target_role,
            payload.interests,
            payload.career_goal,
            payload.constraints,
            payload.profile_details,
        ]
    ).lower()
    text = f"{narrative_text} {' '.join(payload.skills).lower()}"
    skill_text = " ".join(payload.skills).lower()
    scored_roles = []
    for title, keywords, skills, focus, next_step in ROLE_CATALOG:
        keyword_hits = count_term_hits(keywords, narrative_text)
        skill_hits = sum(1 for skill in skills if term_in_text(skill, skill_text) or term_in_text(skill, text))
        exact_role_bonus = 24 if term_in_text(title, text) or term_in_text(payload.target_role, title.lower()) else 0
        signal_count = keyword_hits + skill_hits + (1 if exact_role_bonus else 0)
        readiness = min(payload.experience, 6) * 1.5 + min(payload.learning_hours, 18) * 0.7 + payload.project_depth * 1.4 + payload.general_level * 1.4
        if signal_count:
            score = 30 + keyword_hits * 13 + skill_hits * 9 + exact_role_bonus + readiness
        else:
            score = 18 + readiness * 0.45
        scored_roles.append(
            {
                "title": title,
                "match": int(max(12, min(98, round(score)))),
                "why": f"Your profile signals connect to {title} through interests, current skills, and practice readiness.",
                "skills": skills,
                "next": next_step,
                "difficulty": "Advanced" if score >= 86 else "Medium",
                "time": "4-12 months",
                "confidence": "High" if score >= 75 else "Medium",
                "focus": focus,
                "image": ROLE_IMAGES.get(title, "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80"),
            }
        )
    scored_roles = sorted(scored_roles, key=lambda role: role["match"], reverse=True)
    top = scored_roles[0]
    high_signal_roles = [role for role in scored_roles if role["match"] >= 70 or role["title"] == top["title"]]
    scores = {role["title"]: role["match"] for role in high_signal_roles[:8]}
    learning = {
        "style": f"Hands-on {top['title']} builder",
        "method": f"Learn {top['title']} through demonstrations, guided drills, small projects, feedback, and weekly proof.",
        "focus": f"Use focused practice blocks for {top['focus']}.",
        "format": "Visual references, expert tutorials, checklists, practice logs, and mentor/client feedback.",
        "weekly": [
            f"Mon: study core concepts for {top['focus']}",
            f"Tue: practice {top['skills'][0]} and {top['skills'][1]}",
            "Wed: complete a supervised mini task and capture mistakes",
            "Thu: polish one portfolio sample with photos, notes, or a demo",
            "Fri: reflect, compare against references, and plan next week",
        ],
    }
    roadmaps = {
        "30-day": [
            ("Week 1", f"Foundations: {top['skills'][0]}, {top['skills'][1]}, safety, tools, and quality standards.", 25, top["skills"][:3], "Create a beginner reference sheet and one clean practice sample."),
            ("Week 2", f"Technique: repeat core drills for {top['skills'][2]} and feedback.", 45, top["skills"][2:], "Finish three practice attempts and note visible improvement."),
            ("Week 3", f"Real workflow: combine skills into one small {top['title']} project.", 65, top["skills"], "Produce one portfolio-ready result."),
            ("Week 4", "Professional proof: polish portfolio, resume story, and interview/client explanation.", 85, top["skills"], "Publish a mini case study."),
        ],
        "90-day": [
            ("Month 1", f"Build dependable fundamentals for {top['title']}.", 35, top["skills"][:4], "Complete 8-10 practice outputs."),
            ("Month 2", "Work on realistic scenarios, client/user needs, and quality review.", 60, top["skills"], "Complete 3 portfolio projects."),
            ("Month 3", "Prepare for opportunities: portfolio, resume, outreach, interviews, and trial work.", 82, top["skills"], "Apply to internships, apprenticeships, freelance gigs, or entry roles."),
        ],
        "1-year": [
            ("Q1", f"Foundation: learn tools, safety, vocabulary, and basic execution for {top['title']}.", 30, top["skills"][:3], "Document 20 practice sessions."),
            ("Q2", "Depth: handle varied real-world examples and build a stronger portfolio.", 55, top["skills"], "Complete 6 polished projects."),
            ("Q3", "Professional signal: client work, certifications, or public case studies.", 75, top["skills"], "Earn testimonials or mentor reviews."),
            ("Q4", "Career launch: applications, freelance packages, specialization, and growth plan.", 92, top["skills"], "Secure a role, apprenticeship, clients, or advanced training path."),
        ],
    }
    return {
        "scores": scores,
        "top_track": top["title"],
        "summary": f"{payload.name} is strongest for {top['title']} based on interests, skills, goals, and practice readiness.",
        "focus": top["focus"],
        "recommended_roles": high_signal_roles[:5],
        "learning": learning,
        "roadmaps": roadmaps,
        "projects": [
            {
                "title": f"{top['title']} Starter Portfolio",
                "category": "Portfolio proof",
                "difficulty": top["difficulty"],
                "stack": ", ".join(top["skills"][:4]),
                "outcome": f"Shows core {top['title']} ability with clear process evidence.",
                "resume": f"Demonstrates practical {top['title']} skill and consistency.",
                "interview": "Gives a concrete process, feedback, and improvement story.",
                "image": top["image"],
            }
        ],
        "exercises": university_exercises_for_role(top),
        "prompts": [
            f"Create a 30-day beginner-to-pro plan for {top['title']}.",
            f"What skills should I practice first for {top['title']}?",
            f"Give me project ideas and portfolio proof for {top['title']}.",
            f"Analyze my strengths and gaps for becoming a {top['title']}.",
            f"Make day-wise exercises with reference-image guidance for {top['title']}.",
        ],
        "growth": [
            {"week": "W1", "Core Skill": min(100, top["match"] - 18), "Practice": min(100, payload.project_depth * 8), "Confidence": min(100, payload.general_level * 8)},
            {"week": "W2", "Core Skill": min(100, top["match"] - 12), "Practice": min(100, payload.project_depth * 9), "Confidence": min(100, payload.general_level * 8 + 6)},
            {"week": "W3", "Core Skill": min(100, top["match"] - 6), "Practice": min(100, payload.project_depth * 10), "Confidence": min(100, payload.general_level * 8 + 12)},
            {"week": "W4", "Core Skill": top["match"], "Practice": min(100, payload.project_depth * 10 + 8), "Confidence": min(100, payload.general_level * 8 + 18)},
        ],
        "next_actions": [
            f"Start with {top['skills'][0]} and {top['skills'][1]}.",
            f"Build one proof project focused on {top['focus']}.",
            "Capture photos, screenshots, notes, or demos after every practice session.",
        ],
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "hpi-ai-backend"}


@app.get("/api/dashboard")
def dashboard() -> dict:
    return get_demo_data()


@app.post("/api/agent/chat")
def chat(payload: AgentRequest) -> dict:
    agent = HPIAgent(get_demo_data())
    return agent.run(payload.message, payload.context)


@app.post("/api/reflection")
def reflection(payload: ReflectionRequest) -> dict:
    agent = HPIAgent(get_demo_data())
    message = (
        "Reflect on this weekly update and generate a growth insight. "
        f"Curiosity: {payload.curiosity}. Wins: {payload.wins}. Challenges: {payload.challenges}."
    )
    return agent.run(message, payload.dict())


@app.post("/api/potential-scan")
def potential_scan(payload: PotentialScanRequest) -> dict:
    return analyze_potential_scan(payload)
