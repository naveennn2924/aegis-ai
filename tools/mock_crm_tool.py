from tools.tool_interface import Tool


class MockCRMTool(Tool):
    def __init__(self):
        super().__init__(name="MockCRMTool")

    def run(self, input_data):
        return {
            "customer_id": "CUST-123",
            "last_invoice_status": "Paid",
            "last_invoice_amount": "€1000"
        }
