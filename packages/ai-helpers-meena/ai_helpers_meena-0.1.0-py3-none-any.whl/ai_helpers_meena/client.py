class AIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def format_response(self, text: str) -> str:
        return " ".join(text.split())

    def get_response(self, prompt: str) -> str:
        if not prompt.strip():
            return "Please provide a prompt."

        cleaned = self.format_response(prompt)
        return f"AI Response: {cleaned}"
