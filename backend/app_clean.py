from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import ConvertRequest, ConvertResponse, ErrorResponse
from backend.agent import Agent

app = FastAPI(
    title="Currency Conversion API",
    description="AI-powered currency converter with natural language support",
    version="1.0.0"
)

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent with LLM client
agent = Agent()


@app.get("/health")
async def health():
    """
    Health check endpoint.
    Returns server status.
    """
    return {"status": "ok", "service": "currency-converter"}


@app.post("/convert", response_model=ConvertResponse, responses={
    400: {"model": ErrorResponse, "description": "Validation error or clarification needed"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def convert(req: ConvertRequest):
    """
    Convert currency with optional natural language input.
    
    **Explicit Mode Example:**
    ```json
    {
        "amount": 100,
        "base": "USD",
        "quote": "EUR",
        "date": null
    }
    ```
    
    **Natural Language Mode Example:**
    ```json
    {
        "amount": 0,
        "text": "Convert 100 USD to EUR"
    }
    ```
    
    **Historical Rate Example:**
    ```json
    {
        "amount": 100,
        "base": "USD",
        "quote": "EUR",
        "date": "2023-12-31"
    }
    ```
    
    Returns:
        ConvertResponse with converted amount, formula, and rate info
    
    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    try:
        # Delegate to agent which handles all logic
        result = await agent.handle_convert(req)
        return result
    
    except ValueError as e:
        # Handle validation and business logic errors
        error_msg = str(e)
        
        # Parse error code and message
        if ":" in error_msg:
            code, message = error_msg.split(":", 1)
            code = code.strip()
            message = message.strip()
        else:
            code = "VALIDATION_ERROR"
            message = error_msg
        
        # Determine HTTP status code based on error type
        if code == "CLARIFY":
            status_code = 400
            code = "CLARIFICATION_NEEDED"
        elif code in ["AMOUNT_MUST_BE_POSITIVE", "MISSING_CURRENCY", "INVALID_CURRENCY", "INVALID_DATE"]:
            status_code = 400
        elif code in ["RATE_NOT_FOUND", "PROVIDER_ERROR"]:
            status_code = 503  # Service Unavailable
        else:
            status_code = 400
        
        raise HTTPException(
            status_code=status_code,
            detail={
                "code": code,
                "message": message
            }
        )
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": f"An unexpected error occurred: {str(e)}"
            }
        )


@app.get("/currencies")
async def get_supported_currencies():
    """
    Get list of supported currency codes.
    
    Returns:
        List of 3-letter ISO currency codes
    """
    from backend.agent import SUPPORTED_CURRENCIES
    return {
        "currencies": sorted(list(SUPPORTED_CURRENCIES)),
        "count": len(SUPPORTED_CURRENCIES)
    }


