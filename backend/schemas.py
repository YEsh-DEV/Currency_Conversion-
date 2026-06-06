from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as DateType


class ConvertRequest(BaseModel):
    """
    Request schema for currency conversion endpoint.
    
    Two modes of usage:
    1. Explicit mode: Provide amount, base, and quote directly
       Example: {"amount": 100, "base": "USD", "quote": "EUR"}
    
    2. Natural language mode: Provide text for LLM to parse
       Example: {"amount": 0, "text": "Convert 100 USD to EUR"}
    """
    amount: float = Field(default=0, example=100.0, description="Amount to convert")
    base: Optional[str] = Field(None, example="USD", description="Source currency (3-letter ISO code)")
    quote: Optional[str] = Field(None, example="EUR", description="Target currency (3-letter ISO code)")
    date: Optional[DateType] = Field(None, example="2023-12-31", description="Optional historical date (YYYY-MM-DD)")
    text: Optional[str] = Field(None, example="Convert 100 USD to EUR", description="Optional natural language text for LLM parsing")
    user_id: Optional[str] = Field(None, description="Optional user identifier for tracking")


class RateInfo(BaseModel):
    """
    Exchange rate information returned by the provider.
    """
    rate: float = Field(..., example=0.85, description="Exchange rate (base to quote)")
    source: str = Field(..., example="exchangerate.host", description="Data provider name")
    timestamp: str = Field(..., example="2025-11-19T10:30:00Z", description="ISO timestamp when rate was fetched")
    ttl_seconds: Optional[int] = Field(None, example=3600, description="Cache TTL in seconds")


class ConvertResponse(BaseModel):
    """
    Response schema for successful currency conversion.
    """
    converted: float = Field(..., example=85.0, description="Converted amount in target currency")
    formula: str = Field(..., example="100 USD × 0.85 = 85.0 EUR", description="Calculation formula for transparency")
    rate: RateInfo = Field(..., description="Detailed rate information")
    raw: dict = Field(default_factory=dict, description="Additional metadata (e.g., cache hit status)")


class ErrorResponse(BaseModel):
    """
    Standard error response format.
    """
    code: str = Field(..., example="INVALID_CURRENCY", description="Machine-readable error code")
    message: str = Field(..., example="Currency 'XYZ' is not supported", description="Human-readable error message")