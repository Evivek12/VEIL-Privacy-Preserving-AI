def create_safe_prompt(query: str, profile: dict) -> str:
    """Replace detected private spans with typed placeholders."""
    safe = query
    # Replace longer values first to avoid partial overlapping replacements.
    for item in sorted(profile.get("pii", []), key=lambda x: len(x["value"]), reverse=True):
        value = item["value"]
        placeholder = f"[{item['type'].upper().replace(' ', '_')}]"
        safe = safe.replace(value, placeholder)
    return safe
