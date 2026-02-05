import time
from monitoring.trace_logger import log_event


class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def run(self, task, context=None, tools=None):
        start = time.time()

        log_event(
            agent=self.name,
            event_type="start",
            payload={"task": task}
        )

        result = self._run(task, context, tools)

        latency = time.time() - start

        log_event(
            agent=self.name,
            event_type="end",
            payload={"result": result},
            latency=latency
        )

        return result

    def _run(self, task, context=None, tools=None):
        raise NotImplementedError
