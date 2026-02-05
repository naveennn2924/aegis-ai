from agents.base_agent import BaseAgent
from llm.llm_client import call_llm


class InboxAgent(BaseAgent):
    """
    InboxAgent is responsible ONLY for understanding incoming messages.
    It classifies intent and extracts structured information.
    It does NOT generate final user-facing responses.
    """

    def __init__(self):
        super().__init__(
            name="InboxAgent",
            role="Message Understanding & Intent Classification"
        )

    def _run(self, task, context=None, tools=None):
        message = task.get("message", "").strip()

        if not message:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "original_message": message,
                "extracted_entities": {}
            }

        system_prompt = """
        You are an AI system that classifies customer messages for a business.
        Your job is to understand intent and extract key information.

        Valid intents:
        - billing
        - refund
        - faq
        - general_query

        Return the result STRICTLY as JSON with the following fields:
        {
          "intent": "<one of the valid intents>",
          "confidence": <number between 0 and 1>,
          "entities": {
            "invoice_id": null or string,
            "order_id": null or string
          }
        }

        Do not include explanations.
        """

        try:
            llm_response = call_llm(
                system_prompt=system_prompt,
                user_prompt=message
            )

            parsed = self._safe_parse(llm_response)

            return {
                "intent": parsed.get("intent", "unknown"),
                "confidence": parsed.get("confidence", 0.0),
                "extracted_entities": parsed.get("entities", {}),
                "original_message": message
            }

        except Exception as e:
            # Fail-safe behavior (very important in production)
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "extracted_entities": {},
                "original_message": message,
                "error": str(e)
            }

    def _safe_parse(self, raw_response: str) -> dict:
        """
        Safely parse LLM JSON output.
        Prevents crashes due to malformed responses.
        """
        import json

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": {}
            }
