from agents.base_agent import BaseAgent
from monitoring.quality_scorer import score_response
from monitoring.trace_logger import log_event


class ReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ReviewerAgent",
            role="Quality Assurance & Evaluation"
        )

    def _run(self, task, context=None, tools=None):
        response = task.get("draft_response", "")
        confidence = context.get("confidence", 0.0)
        intent = context.get("intent", "unknown")

        evaluation = score_response(response, confidence)

        log_event(
            agent=self.name,
            event_type="quality_evaluation",
            payload=evaluation
        )

        score = evaluation["quality_score"]

        # 🚨 HARD ESCALATION RULES (VERY IMPORTANT)
        if intent == "unknown" or confidence < 0.5:
            return {
                "status": "escalate",
                "quality_score": score,
                "reasons": ["Unknown intent or low confidence"],
                "final_response": None
            }

        # ⚠️ Soft warning
        if score < 0.85:
            return {
                "status": "warn",
                "quality_score": score,
                "reasons": evaluation["reasons"],
                "final_response": response
            }

        return {
            "status": "approved",
            "quality_score": score,
            "final_response": response
        }
