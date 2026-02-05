def score_response(response: str, confidence: float) -> dict:
    """
    Scores AI output quality.
    Returns numeric score + human-readable reasons.
    """

    score = 1.0
    reasons = []

    # 1️⃣ Length check
    if not response or len(response.strip()) < 30:
        score -= 0.4
        reasons.append("Response too short")

    # 2️⃣ Confidence check (from InboxAgent)
    if confidence < 0.6:
        score -= 0.3
        reasons.append("Low intent confidence")

    # 3️⃣ Placeholder for grounding / safety checks
    if "not sure" in response.lower():
        score -= 0.2
        reasons.append("Low certainty language detected")

    score = max(score, 0.0)

    return {
        "quality_score": round(score, 2),
        "reasons": reasons
    }
