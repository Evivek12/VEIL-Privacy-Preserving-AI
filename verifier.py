def verify_prompt(original_query: str, safe_prompt: str, profile: dict) -> dict:
    """Basic deterministic checks; this is not a semantic or formal privacy verifier."""
    leakage_items = [
        item["value"] for item in profile.get("pii", [])
        if item["value"] and item["value"].lower() in safe_prompt.lower()
    ]
    leakage_ok = len(leakage_items) == 0
    well_formed = bool(safe_prompt.strip()) and len(safe_prompt) <= max(2000, len(original_query) * 3)

    # Heuristic intent check: sanitization should not make the prompt empty.
    # A real VEIL study should use a local language-model judge and human validation.
    intent_ok = bool(safe_prompt.strip()) and len(safe_prompt.split()) >= min(2, len(original_query.split()))

    passed = leakage_ok and well_formed and intent_ok
    return {
        "passed": passed,
        "intent": "PASS (basic heuristic)" if intent_ok else "FAIL",
        "leakage": "PASS (detected spans absent)" if leakage_ok else f"FAIL ({len(leakage_items)} detected span(s) remain)",
        "well_formed": "PASS" if well_formed else "FAIL",
        "leaked_items": leakage_items
    }
