from ai_helpers import get_response, summarize_text, format_response

def test_get_response():
    assert "valid" in get_response("   ")
    assert "Here is" in get_response("What is AI?")
    assert "You said:" in get_response("Hello world")

def test_summarize_text():
    long_text = "Python is a programming language. It is widely used in AI and data science."
    summary = summarize_text(long_text)
    assert summary.startswith("Summary:")

def test_format_response():
    assert format_response("   hello   ") == "hello"
