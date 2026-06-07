📄 INSTRUCTIONS.md: Agentic Currency Converter Project GuideThis document outlines the architecture, setup, and steps required to build the Agentic Currency Converter application using FastAPI, Gemini LLM, and LangChain.1. 📂 Project StructureThis is the recommended file structure for your backend (FastAPI/Agent) to maintain professionalism and organization.currency-converter-agent/
├── backend/
│   ├── main.py             # FastAPI entry point, defines the /convert endpoint
│   ├── agent.py            # Contains the LangGraph/LangChain logic and agent definition
│   ├── tools.py            # Contains the Pydantic model and the currency conversion function (the Tool)
│   ├── Dockerfile          # Defines the container environment
│   ├── requirements.txt    # Lists all Python dependencies
│   └── .env                # Stores all API keys (must be kept secret!)
├── frontend/               # Your Vibe Code (e.g., React/Next.js) goes here
└── INSTRUCTIONS.md         # This file
2. 🔑 Prerequisites and KeysBefore starting, you must have the following keys set as environment variables (in your .env file):Key NamePurposeSourceGOOGLE_API_KEYAccess the Gemini LLM via LangChain.Google AI StudioCURRENCY_API_KEYFetch real-time exchange rates.ExchangeRate-API or similarLANGSMITH_API_KEYOptional: For debugging and tracing the agent's thought process (Highly Recommended).LangSmith3. ⚙️ Backend Core DependenciesYour requirements.txt should contain at least:fastapi
uvicorn[standard]
pydantic
langchain
langchain-google-genai
langgraph
requests # For calling the external currency API
python-dotenv # For loading the .env file
4. 🧠 Core Logic: Tool Definition (tools.py)The LLM must know exactly what to extract. Use Pydantic to define the tool's inputs and to ensure the final output is reliable JSON.A. Define the Pydantic Schema (Input & Output)Input Schema: Tells the LLM exactly what arguments to pass to the function.Python# tools.py
from pydantic import BaseModel, Field

class CurrencyConversionInput(BaseModel):
    """Input schema for the currency conversion tool."""
    amount: float = Field(description="The numeric amount of money to convert.")
    source_currency: str = Field(description="The three-letter ISO currency code (e.g., 'USD', 'EUR', 'JPY') to convert FROM.")
    target_currency: str = Field(description="The three-letter ISO currency code (e.g., 'CAD', 'GBP', 'AUD') to convert TO.")

class ConversionResult(BaseModel):
    """Output schema for the final response to the user."""
    initial_amount: float
    source_currency: str
    target_currency: str
    converted_amount: float
    explanation: str = Field(description="A natural language sentence explaining the result.")
B. Define the Tool FunctionUse the @tool decorator to expose your rate-fetching function to the agent.Python# tools.py (continued)
from langchain.tools import tool
import requests
import os

@tool(args_schema=CurrencyConversionInput)
def get_exchange_rate(amount: float, source_currency: str, target_currency: str) -> dict:
    """
    Fetches the current exchange rate and calculates the converted amount.
    This tool MUST be used when the user asks for a currency conversion.
    """
    # Call the external API (e.g., ExchangeRate-API)
    api_key = os.getenv("CURRENCY_API_KEY")
    # Example API call structure (adjust URL based on your chosen API)
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{source_currency}/{target_currency}/{amount}"
    response = requests.get(url)
    data = response.json()

    # Check for error and return a failure message if necessary
    if data.get("result") != "success":
        return {"error": "API failed to fetch rate.", "details": data.get("error-type")}

    # Return the raw result data for the agent to use
    return {
        "rate": data["conversion_rate"],
        "converted_amount": data["conversion_result"]
    }
