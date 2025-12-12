def summarize_text(text: str) -> str:
    if len(text.split()) < 5:
        return "Text too short to summarize."
    return text[:80] + "..."
