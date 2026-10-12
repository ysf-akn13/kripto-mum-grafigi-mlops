import os
import pandas as pd
from binance.client import Client

def fetch_crypto_ohlcv(symbol="BTCUSDT", interval="1h", limit=1000):
    client = Client()
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    
    df = pd.DataFrame(klines, columns=[
        'Open_time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close_time', 'Quote_asset_volume', 'Number_of_trades',
        'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'
    ])
    
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/{symbol}_{interval}.csv"
    df.to_csv(file_path, index=False)
    print(f"Veri kaydedildi: {file_path}")

if __name__ == "__main__":
    fetch_crypto_ohlcv("BTCUSDT", "1h", 10000)