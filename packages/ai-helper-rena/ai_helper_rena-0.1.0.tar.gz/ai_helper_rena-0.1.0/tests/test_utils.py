from GPT_Helper.utils import format_response

def test_format_response_cleanup():
    s = "  Hello\n\n\nWorld  "
    assert format_response(s) == "Hello\n\nWorld"

def test_format_response_truncate():
    s = "a" * 50
    result = format_response(s, max_length=10)
    assert result.endswith("...")
