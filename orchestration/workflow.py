from agents.coordinator_agent import CoordinatorAgent
from monitoring.trace_context import new_trace_id


def run_workflow(task):
    trace_id = new_trace_id()
    coordinator = CoordinatorAgent()
    result = coordinator.run(task)

    return {
        "trace_id": trace_id,
        "result": result
    }

