from agents.inbox_agent import InboxAgent
from agents.action_agent import ActionAgent
from agents.reviewer_agent import ReviewerAgent
from monitoring.trace_logger import log_event


class CoordinatorAgent:
    """
    CoordinatorAgent orchestrates the full multi-agent workflow.
    It does NOT generate content itself.
    It routes tasks, passes context, and aggregates results.
    """

    def __init__(self):
        self.inbox_agent = InboxAgent()
        self.action_agent = ActionAgent()
        self.reviewer_agent = ReviewerAgent()

    def run(self, task: dict) -> dict:
        """
        Orchestrates:
        1. InboxAgent -> intent + confidence
        2. ActionAgent -> draft response (tool usage)
        3. ReviewerAgent -> quality evaluation + decision
        """

        # --- Step 1: Understand the message ---
        inbox_result = self.inbox_agent.run(task)

        log_event(
            agent="CoordinatorAgent",
            event_type="intent_routed",
            payload={
                "intent": inbox_result.get("intent"),
                "confidence": inbox_result.get("confidence")
            }
        )

        # --- Step 2: Execute action based on intent ---
        action_result = self.action_agent.run(
            task,
            context=inbox_result
        )

        # --- Step 3: Review & evaluate quality ---
        review_result = self.reviewer_agent.run(
            action_result,
            context={
                "confidence": inbox_result.get("confidence", 0.0),
                "intent": inbox_result.get("intent")
            }
        )

        # --- Final aggregated response ---
        return {
            "intent": inbox_result.get("intent"),
            "confidence": inbox_result.get("confidence"),
            "review": review_result
        }
