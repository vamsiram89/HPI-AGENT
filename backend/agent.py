import os
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    name: str
    content: dict[str, Any]


class HPIAgent:
    """Small career-coach agent with deterministic tools and optional LLM wording."""

    def __init__(self, profile: dict[str, Any]):
        self.profile = profile

    def run(self, message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        tool_result = self._select_tool(message, context)
        response = self._llm_response(message, tool_result)
        if not response:
            response = self._fallback_response(message, tool_result)

        return {
            "response": response,
            "tool": tool_result.name,
            "tool_result": tool_result.content,
            "next_actions": self._next_actions(tool_result),
        }

    def _select_tool(self, message: str, context: dict[str, Any]) -> ToolResult:
        text = message.lower()
        role_text = " ".join(
            str(context.get(key, ""))
            for key in ["top_role", "goal", "interests"]
        ).lower()
        is_role_specific = bool(context.get("top_role")) or any(
            word in f"{text} {role_text}"
            for word in ["barber", "hair", "hairstyle", "stylist", "salon", "fade", "cut"]
        )
        if any(word in text for word in ["roadmap", "plan", "learn", "study", "month", "week", "day-wise"]):
            return ToolResult("generate_roadmap", self._roadmap(context))
        if is_role_specific and any(
            word in text
            for word in ["skill", "practice", "first", "photo", "image", "screenshot", "type", "style", "hairstyle", "haircut"]
        ):
            return ToolResult("recommend_career", self._career_recommendations(context))
        if any(word in text for word in ["career", "job", "role", "switch", "path"]):
            return ToolResult("recommend_career", self._career_recommendations(context))
        if any(word in text for word in ["reflect", "stuck", "challenge", "energy", "win"]):
            return ToolResult("reflect_growth", self._reflection(context))
        if is_role_specific:
            return ToolResult("recommend_career", self._career_recommendations(context))
        return ToolResult("analyze_profile", self._profile_analysis())

    def _profile_analysis(self) -> dict[str, Any]:
        skills = set(self.profile["profile"]["skills"])
        potential = self.profile["potential"]
        strengths = sorted(potential.items(), key=lambda item: item[1], reverse=True)[:3]
        gaps = ["RAG patterns", "LangGraph workflows", "model deployment", "LLM observability"]
        if "FastAPI" in skills:
            gaps.remove("model deployment")
        return {
            "summary": "Strong technical execution with a clear data-to-AI engineering direction.",
            "strengths": [{"name": name, "score": score} for name, score in strengths],
            "gaps": gaps,
            "confidence": "high",
        }

    def _career_recommendations(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        top_role = context.get("top_role")
        if top_role:
            is_hair = any(word in top_role.lower() for word in ["hair", "barber", "stylist"])
            default_skills = (
                ["sectioning", "clipper control", "scissor-over-comb", "face-shape consultation", "sanitation"]
                if is_hair
                else ["foundation skills", "practice", "portfolio proof"]
            )
            next_step = (
                "Practice sectioning, one-length cuts, fade blending, and client consultation with reference photos."
                if is_hair
                else f"Build one small {top_role} portfolio artifact and document the process."
            )
            return {
                "recommended_roles": [
                    {
                        "title": top_role,
                        "match": 90,
                        "why": f"Your latest scan points to {top_role}; focus on proof projects, guided practice, and feedback.",
                        "skills": context.get("skills") or default_skills,
                        "next": next_step,
                        "difficulty": "Medium",
                        "time": "4-12 months",
                        "confidence": "High",
                    }
                ],
                "best_first_move": next_step,
            }
        careers = sorted(self.profile["careers"], key=lambda career: career["match"], reverse=True)[:3]
        return {
            "recommended_roles": careers,
            "best_first_move": "Build a data science career predictor because it proves data preparation, modeling, and AI product thinking.",
        }

    def _roadmap(self, context: dict[str, Any]) -> dict[str, Any]:
        goal = context.get("top_role") or context.get("goal") or self.profile["profile"]["goal"]
        return {
            "goal": goal,
            "plan": [
                {
                    "week": 1,
                    "focus": f"Core foundations for {goal}",
                    "deliverable": "Reference notes, safety/quality checklist, and first practice artifact.",
                },
                {
                    "week": 2,
                    "focus": "Guided drills and feedback",
                    "deliverable": "Three practice attempts with improvement notes.",
                },
                {
                    "week": 3,
                    "focus": "Realistic project simulation",
                    "deliverable": "One complete portfolio-ready result.",
                },
                {
                    "week": 4,
                    "focus": "Portfolio polish",
                    "deliverable": "Photos/screenshots, process explanation, and next-step plan.",
                },
            ],
        }

    def _reflection(self, context: dict[str, Any]) -> dict[str, Any]:
        energy = int(context.get("energy", 7))
        challenge = context.get("challenges", "Balancing learning depth with shipping.")
        if energy <= 4:
            mode = "recovery sprint"
            action = "Pick one tiny deliverable and protect momentum."
        elif energy <= 7:
            mode = "steady builder sprint"
            action = "Ship one visible improvement and document the learning."
        else:
            mode = "deep work sprint"
            action = "Take on the hardest technical piece while energy is high."
        return {
            "mode": mode,
            "challenge": challenge,
            "action": action,
            "checkpoint": "End the week with one demo link and three bullet lessons.",
        }

    def _llm_response(self, message: str, tool_result: ToolResult) -> str | None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            result = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are HPI AI, a concise human-potential and career coach. "
                            "Use the supplied tool result as ground truth. Be specific, practical, and encouraging."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"User message: {message}\nTool result: {tool_result.content}",
                    },
                ],
            )
            return result.output_text
        except Exception:
            return None

    def _fallback_response(self, message: str, tool_result: ToolResult) -> str:
        content = tool_result.content
        if tool_result.name == "recommend_career":
            top = content["recommended_roles"][0]
            if any(word in top["title"].lower() for word in ["hair", "barber", "stylist"]):
                skills = ", ".join(top["skills"][:4])
                return (
                    f"For {top['title']}, practice these first: {skills}. "
                    "Start with clean sectioning, then one-length cutting, then fade blending, then consultation by face shape and hair type.\n\n"
                    "Relevant references:\n"
                    "![Sectioning and styling](https://images.unsplash.com/photo-1522336572468-97b06e8ef143?auto=format&fit=crop&w=900&q=80)\n"
                    "![Curly hair texture](https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?auto=format&fit=crop&w=900&q=80)\n"
                    "![Fade and clipper work](https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=900&q=80)"
                )
            return (
                f"Your strongest path is {top['title']} at {top['match']}% match. "
                f"The practical next move is: {content['best_first_move']}"
            )
        if tool_result.name == "generate_roadmap":
            first = content["plan"][0]
            return (
                f"For {content['goal']}, start with week {first['week']}: {first['focus']}. "
                f"Deliverable: {first['deliverable']}"
            )
        if tool_result.name == "reflect_growth":
            return (
                f"This looks like a {content['mode']}. {content['action']} "
                f"Checkpoint: {content['checkpoint']}"
            )
        strengths = ", ".join(item["name"] for item in content["strengths"])
        return f"Your strongest signals are {strengths}. Focus next on {', '.join(content['gaps'][:2])}."

    def _next_actions(self, tool_result: ToolResult) -> list[str]:
        actions = {
            "analyze_profile": [
                "Turn the top strength into one portfolio project.",
                "Close one skill gap with a 7-day build sprint.",
            ],
            "recommend_career": [
                "Pick one target role and collect five job descriptions.",
                "Build a project that proves two repeated skills from those roles.",
            ],
            "generate_roadmap": [
                "Create the week-one deliverable first.",
                "Review progress every Friday and adjust scope.",
            ],
            "reflect_growth": [
                "Choose one measurable checkpoint for the next seven days.",
                "Write a short public or private build note.",
            ],
        }
        return actions[tool_result.name]
