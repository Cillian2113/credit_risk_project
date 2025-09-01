import yfinance as yf
import numpy as np
import pandas as pd
from openpyxl import load_workbook

def fetch_balance_sheet(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    balance_sheet = ticker.balance_sheet.T 
        
    if balance_sheet is None or balance_sheet.empty:
        return pd.DataFrame({"Error": [f"No balance sheet data found for '{ticker_symbol}'."]})
                
    return balance_sheet


if __name__ == "__main__":

    wb = load_workbook('portfolio.xlsx')
    input = wb['Input']      
    ticker_symbol = input['B1'].value
    df = fetch_balance_sheet(ticker_symbol)
    df.index = df.index.astype(str)
    df.to_csv(f"{ticker_symbol}_balance_sheet.csv")

    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="2y", interval="1d")

    try:
        market_cap = ticker.info['currentPrice'] * ticker.info['sharesOutstanding']
    except:
        print("error calculating market cap")
        market_cap = "must be found"

    try:
        data['LogReturn'] = np.log(data['Close'] / data['Close'].shift(1))
        data = data.dropna()
        equity_volatility = data['LogReturn'].std() * np.sqrt(252)
    except:
        print("error calculating equity volatility")
        equity_volatility = "must be found"
    
    print(f"Market Cap: {market_cap}")
    print(f"Equity Volatility: {equity_volatility}")


    











