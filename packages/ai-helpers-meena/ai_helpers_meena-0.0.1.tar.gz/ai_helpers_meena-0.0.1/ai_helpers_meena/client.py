"""Simple AI client wrapper.


This file shows example implementations that call an AI API. For your assignment,
replace the placeholder HTTP call with your chosen AI provider (OpenAI, Cohere, etc.).
"""
import os
from typing import Optional


API_KEY = os.environ.get("AI_API_KEY")


class AIClient:
"""A tiny wrapper around an AI text-generation / summarization service.


Example usage:
client = AIClient(api_key="...")
text = client.get_response("Explain binary search")
"""
def __init__(self, api_key: Optional[str] = None):
self.api_key = api_key or API_KEY
if not self.api_key:
# do not raise in constructor; allow graceful failure later
pass


def get_response(self, prompt: str) -> str:
"""Send `prompt` to an AI service and return the raw text response.


NOTE: Replace the body with actual API call code.
"""
if not prompt.strip():
return "Please provide a non-empty prompt."


# --- Placeholder: simulate an AI reply for local testing ---
return f"(Simulated AI reply) You asked: {prompt[:200]}"


def summarize_text(self, text: str, max_length: int = 150) -> str:
"""Return a short summary of `text`.


For production, call the AI summary endpoint or prompt-engineer to summarize.
"""
if not text.strip():
return ""
# naive local fallback (not a real summary):
return text.strip()[:max_length] + ("..." if len(text) > max_length else "")


def format_response(self, text: str) -> str:
"""Clean output before sending to the UI: strip excessive whitespace, limit length."""
out = " ".join(text.split())
if len(out) > 2000:
out = out[:2000] + "..."
return out