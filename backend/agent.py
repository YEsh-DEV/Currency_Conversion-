from typing import Optional
from datetime import datetime
from backend.schemas import ConvertRequest, ConvertResponse, RateInfo
from backend.tools.get_rate import get_rate
from backend.utils.cache import SimpleTTLCache
from backend.llm import LLMClient
from decimal import Decimal, ROUND_HALF_UP


# In-memory cache for exchange rates
_cache = SimpleTTLCache()

# List of supported currencies (expand this as needed)
SUPPORTED_CURRENCIES = {
    "USD", "EUR", "GBP", "JPY", "INR", "AUD", "CAD", "CHF",
    "CNY", "SEK", "NZD", "MXN", "SGD", "HKD", "NOK", "KRW",
    "TRY", "RUB", "BRL", "ZAR", "DKK", "PLN", "THB", "IDR",
    "HUF", "CZK", "ILS", "CLP", "PHP", "AED", "SAR", "MYR"
}


class Agent:
    """
    Main controller that handles currency conversion.
    
    Simple flow:
    1. Get amount, base currency, quote currency from user
    2. If user sent text instead, use LLM to extract details
    3. Validate the currencies
    4. Get exchange rate from API (with caching)
    5. Calculate: amount * rate = converted amount
    6. Return result
    """

    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize agent with LLM client for parsing text."""
        self.llm = llm_client or LLMClient()

    async def handle_convert(self, req: ConvertRequest) -> ConvertResponse:
        """
        Main function to convert currency.
        
        Args:
            req: Request with amount, base, quote (or text to parse)
        
        Returns:
            Response with converted amount and rate info
        """
        
        # STEP 1: Check amount is positive
        if req.amount <= 0:
            raise ValueError("AMOUNT_MUST_BE_POSITIVE: Amount must be greater than 0")

        # STEP 2: If user sent text like "Convert 100 USD to EUR", extract details
        if (not req.base or not req.quote) and req.text:
            parsed = self.llm.extract_entities(req.text)
            
            # Check if LLM needs more info
            if parsed.get("clarify"):
                question = parsed.get("question", "Please specify currencies")
                raise ValueError(f"CLARIFY: {question}")
            
            # Use what LLM found (if we don't already have it)
            if not req.base and parsed.get("base"):
                req.base = parsed.get("base")
            
            if not req.quote and parsed.get("quote"):
                req.quote = parsed.get("quote")
            
            # LLM might find amount in text
            if req.amount == 0 and parsed.get("amount"):
                req.amount = float(parsed.get("amount"))
            
            # LLM might find date
            if not req.date and parsed.get("date"):
                date_str = parsed.get("date")
                try:
                    req.date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    raise ValueError(f"INVALID_DATE: Date '{date_str}' must be YYYY-MM-DD format")

        # STEP 3: Make sure we have both currencies
        if not req.base or not req.quote:
            raise ValueError("MISSING_CURRENCY: Please provide both base and quote currencies")
        
        # Clean up currency codes (make uppercase, remove spaces)
        base = req.base.upper().strip()
        quote = req.quote.upper().strip()
        
        # STEP 4: Check if currencies are valid
        if base not in SUPPORTED_CURRENCIES:
            raise ValueError(f"INVALID_CURRENCY: '{base}' is not supported")
        
        if quote not in SUPPORTED_CURRENCIES:
            raise ValueError(f"INVALID_CURRENCY: '{quote}' is not supported")
        
        # STEP 5: Get exchange rate (check cache first)
        date_str = str(req.date) if req.date else "latest"
        cache_key = f"rate:{base}:{quote}:{date_str}"
        
        # Try cache first
        rate_info = _cache.get(cache_key)
        
        if not rate_info:
            # Not in cache, get from API
            try:
                rate_info = get_rate(base, quote, date=str(req.date) if req.date else None)
                
                # Save to cache
                ttl = int(rate_info.get("ttl_seconds", 3600))
                _cache.set(cache_key, rate_info, ttl)
                
            except ValueError as e:
                # API returned error
                raise e
            except Exception as e:
                # Unexpected error
                raise ValueError(f"PROVIDER_ERROR: Could not fetch rate - {str(e)}")
        
        # STEP 6: DO THE CONVERSION (THIS IS THE MAIN CALCULATION!)
        # Example: 100 USD * 0.85 = 85 EUR
        
        rate = Decimal(str(rate_info["rate"]))  # Exchange rate (e.g., 0.85)
        amount = Decimal(str(req.amount))        # Amount to convert (e.g., 100)
        
        # Multiply and round to 2 decimal places
        converted = (amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        # Create formula string for user
        formula = f"{req.amount} {base} × {rate} = {converted} {quote}"
        
        # STEP 7: Return the result
        rate_obj = RateInfo(
            rate=float(rate),
            source=rate_info.get("source", "unknown"),
            timestamp=rate_info.get("timestamp"),
            ttl_seconds=rate_info.get("ttl_seconds")
        )
        
        return ConvertResponse(
            converted=float(converted),
            formula=formula,
            rate=rate_obj,
            raw={"cached": bool(_cache.get(cache_key))}
        )
