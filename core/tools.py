from pydantic import BaseModel,Field

def fetch_security_data(symbol: str):
    import nsepython
    """
    Get the price, percent_change, pe_ratio and industry for a security, just pass in the ticker symbol.
    """
    try:
        # Get quote from NSE directly
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        data = nsepython.nsefetch(url)

        price, percent_change, pe_ratio, industry = (
            data["priceInfo"]["lastPrice"],
            data["priceInfo"]["pChange"],
            data["metadata"]["pdSymbolPe"],
            data["info"]["industry"],
        )
        return round(price, 2), round(percent_change, 2), pe_ratio, industry
    except Exception as e:
        print(f"Error: {e}")
        return None
    
class GetFetchPriceArgs(BaseModel):
    symbol: str = Field(
        ...,
        description="The ticker symbol of the security being fetched, just pass in the ticker symbol and not the full name e.g. INFY, RELIANCE ",
    )