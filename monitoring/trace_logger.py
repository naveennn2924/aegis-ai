import json
from monitoring.trace_context import get_trace_id
from storage.db import get_connection, init_db

# Ensure DB exists
init_db()


def log_event(agent, event_type, payload=None, latency=None):
    trace_id = get_trace_id()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO traces (trace_id, agent, event, latency, payload)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            trace_id,
            agent,
            event_type,
            latency,
            json.dumps(payload) if payload else None
        )
    )

    conn.commit()
    conn.close()
