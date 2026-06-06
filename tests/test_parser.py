from backend.agent import extract_currency_codes


def test_extract_currency_codes():
    text = "Convert 100 USD to EUR"
    codes = extract_currency_codes(text)
    assert "USD" in codes
    assert "EUR" in codes
