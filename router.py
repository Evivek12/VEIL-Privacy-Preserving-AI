def choose_route(profile: dict) -> dict:
    """Transparent starter rule: transformation tasks stay local."""
    task = profile.get("task_type", "")
    if task in {"Text transformation", "Translation"}:
        return {
            "route": "LOCAL_ONLY",
            "reason": "The starter routing rule keeps text transformation and translation local."
        }
    if profile.get("pii"):
        return {
            "route": "VERIFY_BEFORE_DELEGATION",
            "reason": "Private information was detected. A sanitized prompt must pass verification first."
        }
    return {
        "route": "VERIFY_BEFORE_DELEGATION",
        "reason": "The query may benefit from delegation, subject to verification."
    }
