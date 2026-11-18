
import re

PATTERNS = {
    "Email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "Phone": re.compile(
        r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)"
    ),
    "URL": re.compile(
        r"\bhttps?://\S+", re.IGNORECASE
    ),
}


def profile_query(query: str) -> dict:
    """Detect common PII patterns and estimate the task type."""

    found = []

    # Step 1: Detect email, phone number and URL
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(query):
            value = match.group(0).strip()

            if label == "Phone":
                digits = re.sub(r"\D", "", value)

                if not 8 <= len(digits) <= 15:
                    continue

            found.append({
                "type": label,
                "value": value
            })

    # Step 2: Detect possible person names
    name_match = re.search(
        r"\b(?:my name is|i am|i'm)\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})"
        r"(?=\s*(?:[,.\n]|$|\band\b))",
        query,
        re.IGNORECASE
    )

    if name_match:
        candidate = name_match.group(1).strip()

        found.append({
            "type": "Possible person name",
            "value": candidate
        })

    # Step 3: Classify the task
    lower = query.lower()

    if any(word in lower for word in [
        "rewrite", "rephrase", "paraphrase", "correct this"
    ]):
        task = "Text transformation"

    elif any(word in lower for word in [
        "translate", "translation"
    ]):
        task = "Translation"

    elif any(word in lower for word in [
        "email", "application", "draft", "write"
    ]):
        task = "Drafting / writing"

    else:
        task = "Question answering / other"

    # Step 4: Remove duplicate detections
    unique = []
    seen = set()

    for item in found:
        key = (item["type"], item["value"])

        if key not in seen:
            unique.append(item)
            seen.add(key)

    # Step 5: Return profiling results
    return {
        "task_type": task,
        "pii": unique,
        "query_length": len(query)
    }
