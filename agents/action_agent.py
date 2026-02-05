from agents.base_agent import BaseAgent
from tools.knowledge_tool import KnowledgeTool
from tools.mock_crm_tool import MockCRMTool


class ActionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ActionAgent", role="Task Execution")
        self.knowledge_tool = KnowledgeTool()
        self.crm_tool = MockCRMTool()

    def _run(self, task, context=None, tools=None):
        intent = context["intent"]
        message = context["original_message"]

        if intent == "faq":
            answer = self.knowledge_tool.run(message)
        elif intent == "billing":
            crm_data = self.crm_tool.run(message)
            answer = f"Your last invoice of {crm_data['last_invoice_amount']} is marked as {crm_data['last_invoice_status']}."
        else:
            answer = "Thanks for reaching out! We’ll get back to you shortly."

        return {
            "draft_response": answer
        }
