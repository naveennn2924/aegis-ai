import json
from storage.db import get_connection


def get_items_for_review():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT trace_id, payload
    FROM traces
    WHERE agent = 'ReviewerAgent'
    AND event = 'end'
    """)

    rows = cursor.fetchall()
    conn.close()

    items = []

    for trace_id, payload in rows:
        if not payload:
            continue

        data = json.loads(payload)
        result = data.get("result", {})

        if result.get("status") in ["warn", "escalate"]:
            items.append({
                "trace_id": trace_id,
                "result": result
            })

    return items


def save_review(trace_id: str, decision: str, comment: str):
    """
    Save human review decision for a trace.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reviews (trace_id, decision, comment)
    VALUES (?, ?, ?)
    """, (trace_id, decision, comment))

    conn.commit()
    conn.close()
