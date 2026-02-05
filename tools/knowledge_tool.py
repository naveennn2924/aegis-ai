from tools.tool_interface import Tool


class KnowledgeTool(Tool):
    def __init__(self):
        super().__init__(name="KnowledgeTool")

    def run(self, input_data):
        faq = {
            "opening hours": "We are open Monday to Friday, 9am to 6pm.",
            "refund": "Refunds are processed within 5–7 business days."
        }

        for key, value in faq.items():
            if key in input_data.lower():
                return value

        return "No relevant knowledge found."
