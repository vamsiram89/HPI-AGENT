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
    project_depth: int = Field(default=6, ge=1, le=10)
    interests: str = ""
    career_goal: str = ""
    constraints: str = ""


def analyze_potential_scan(payload: PotentialScanRequest) -> dict:
    skill_count = len(payload.skills)
    experience_weight = min(payload.experience, 5) * 2
    scores = {
        "Data Science": min(
            98,
            45 + skill_count * 3 + payload.stats_level * 4 + payload.project_depth * 2 + experience_weight,
        ),
        "Machine Learning Engineering": min(
            98,
            42 + skill_count * 2 + payload.ml_level * 5 + payload.stats_level * 2 + payload.project_depth * 2,
        ),
        "AI Engineering": min(
            98,
            44 + skill_count * 2 + payload.ai_level * 5 + payload.learning_hours * 2 + payload.project_depth,
        ),
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
        "summary": f"{payload.name} is strongest for {top_track}.",
        "focus": focus_map[top_track],
        "next_actions": [
            f"Build one portfolio project focused on {focus_map[top_track]}.",
            "Create a weekly learning schedule with one measurable deliverable.",
            "Track skills, project proof, and confidence after each sprint.",
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
