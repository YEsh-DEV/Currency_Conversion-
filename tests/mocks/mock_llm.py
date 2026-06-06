# Simple mock LLM client for tests. Replace with more realistic fixtures as needed.

class MockLLM:
    def __init__(self, responses=None):
        self.responses = responses or []

    def call(self, prompt, **kwargs):
        if self.responses:
            return self.responses.pop(0)
        return {"tool": "none"}


mock_llm = MockLLM()
