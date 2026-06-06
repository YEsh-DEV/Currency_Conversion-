import os
import json
from typing import Dict

# Only use Gemini - no other frameworks
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
_GENAI = None

if GEMINI_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        _GENAI = genai
    except Exception:
        _GENAI = None


class LLMClient:
    """Simple LLM client that only uses Google Gemini for entity extraction."""
    
    def __init__(self):
        self.model_name = os.getenv("LLM_MODEL", "gemini-pro")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.0"))
    
    def generate(self, prompt: str) -> str:
        """
        Generate text from Gemini model.
        Returns raw text response or a JSON string with clarification request if LLM unavailable.
        """
        if not _GENAI:
            # No Gemini configured - return clarification
            from typing import Any, Dict, Optional
            import os

            try:
                # Prefer Google Gemini if available in environment
                import google.generativeai as genai
                GEMINI_AVAILABLE = True
            except Exception:
                GEMINI_AVAILABLE = False


            class LLMClient:
                """Simple wrapper around an LLM provider (Gemini preferred)."""
import os
import json
from typing import Any, Dict, Optional

try:
    import google.generativeai as genai
    GENAI = genai
except Exception:
    GENAI = None


class LLMClient:
    """Simple wrapper for an LLM provider. Prefers Google Gemini when configured.

    Methods:
    - generate(prompt): returns raw text from the model
    - extract_entities(text): attempts to extract amount/base/quote/date as a dict
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.0"))
        if self.api_key and GENAI:
            try:
                GENAI.configure(api_key=self.api_key)
            except Exception:
                pass

    def generate(self, prompt: str) -> str:
        """Generate text using the configured LLM provider. Returns raw text."""
        if self.api_key and GENAI:
            try:
                resp = GENAI.generate_text(model=self.model, prompt=prompt, temperature=self.temperature)
                return getattr(resp, "text", str(resp))
            except Exception:
                return ""

        # No LLM available
        return ""

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract amount, base, quote, and optional date from freeform text.

        Returns a dict with keys: amount (float|None), base (str|None), quote (str|None),
        date (str|None, YYYY-MM-DD), clarify (bool), question (str).
        """
        system_prompt = (
            "Extract the amount, base currency, quote currency, and optional date from the user text. "
            "Return a single JSON object containing the keys: amount, base, quote, date, clarify, question. "
            "If any information is missing, set clarify=true and include a question string asking for the missing info."
        )

        full_prompt = f"{system_prompt}\nUser: \"{text}\"\nJSON:" 
        raw = self.generate(full_prompt)

        # Try to parse JSON out of the response text
        try:
            cleaned = raw.strip()
            # Remove common markdown fences
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                json_text = cleaned[start:end+1]
                parsed = json.loads(json_text)
                return {
                    "amount": parsed.get("amount"),
                    "base": parsed.get("base"),
                    "quote": parsed.get("quote"),
                    "date": parsed.get("date"),
                    "clarify": parsed.get("clarify", False),
                    "question": parsed.get("question", ""),
                }
        except Exception:
            pass

        # Fallback: ask for clarification
        return {
            "amount": None,
            "base": None,
            "quote": None,
            "date": None,
            "clarify": True,
            "question": "Please specify amount, base currency and quote currency (e.g., 'Convert 100 USD to EUR').",
        }
