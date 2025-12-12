import unittest
from ai_helper_utils.core import get_response, summarize_text, format_response

class TestAIHelperUtils(unittest.TestCase):
    
    def test_get_response_empty(self):
        self.assertEqual(get_response(""), "Please provide a prompt.")

    def test_get_response_mock(self):
        prompt = "Hello"
        response = get_response(prompt)
        self.assertIn(prompt, response)

    def test_summarize_text_short(self):
        text = "Short text"
        self.assertEqual(summarize_text(text), text)

    def test_summarize_text_long(self):
        text = "One two three four five six seven eight nine ten eleven twelve"
        summary = summarize_text(text)
        self.assertTrue(summary.startswith("Summary:"))
        self.assertTrue(summary.endswith("..."))

    def test_format_response(self):
        text = "  hello world  "
        self.assertEqual(format_response(text), "Hello world")

if __name__ == '__main__':
    unittest.main()
