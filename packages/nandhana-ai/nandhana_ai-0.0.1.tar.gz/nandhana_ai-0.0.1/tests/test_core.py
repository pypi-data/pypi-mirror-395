from nandhana_ai import get_response, summarize_text, format_response

def test_get_response():
    result = get_response("Hello")
    assert isinstance(result, str)

def test_summarize_text():
    result = summarize_text("This is a long text to summarize.")
    assert isinstance(result, str)

def test_format_response():
    result = format_response("Hello\nWorld")
    assert result == "Hello World"
