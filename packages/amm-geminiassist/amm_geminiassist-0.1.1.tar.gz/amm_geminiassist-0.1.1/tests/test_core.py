from ai_queryhelper import format_response

def test_format_response():
    result = format_response("   Hello World    ", width=10)
    assert "Hello" in result
