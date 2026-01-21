from pydantic import BaseModel,Field

def fetch_security_data(symbol: str):
    import nsepython
    """
    Get the price, percent_change, pe_ratio and industry for an Indian security, just pass in the ticker symbol.
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

# We need to define arguments of any tool in another Pydantic model, which is then converted to JSON Schema via .model_json_schema() for the LLM.  
class fetch_security_data_args(BaseModel):
    symbol: str = Field(
        ...,
        description="The ticker symbol of the security being fetched, just pass in the ticker symbol and not the full name e.g. INFY, RELIANCE ",
    )