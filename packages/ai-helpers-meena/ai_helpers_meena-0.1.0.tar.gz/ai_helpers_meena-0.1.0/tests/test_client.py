from ai_helpers_meena.client import AIClient

def test_format_response_trims_whitespace():
    c = AIClient(api_key="fake")
    assert c.format_response("  hello   world \n") == "hello world"

def test_get_response_empty_prompt_returns_message():
    c = AIClient(api_key=None)
    # if get_response returns a "Please provide" message on empty input
    assert "Please provide" in c.get_response("")
