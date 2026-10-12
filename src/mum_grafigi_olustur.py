import os
import matplotlib
matplotlib.use('Agg') # Ekranda pencere açmadan doğrudan dosyaya kaydetmesi için backend ayarı
import pandas as pd
import mplfinance as mpf

def generate_images(csv_path, window_size=30, output_dir="data/processed/binance_images"):
    df = pd.read_csv(csv_path)
    df['Open_time'] = pd.to_datetime(df['Open_time'])
    df.set_index('Open_time', inplace=True)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Renkleri ayarlıyoruz ve eksenleri gizliyoruz
    mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
    s = mpf.make_mpf_style(
        marketcolors=mc, 
        rc={'axes.grid': False, 'xtick.bottom': False, 'ytick.left': False, 'xtick.labelbottom': False, 'ytick.labelleft': False}
    )
    
    saved_count = 0
    for i in range(len(df) - window_size):
        sub_df = df.iloc[i:i+window_size]
        file_name = os.path.join(output_dir, f"chart_{i}.png")
        
        mpf.plot(
            sub_df,
            type='candle',
            style=s,
            axisoff=True,
            savefig=dict(fname=file_name, dpi=100, bbox_inches='tight', pad_inches=0),
            figsize=(2.24, 2.24) # 224x224 px boyutu için
        )
        saved_count += 1
        
    print(f"{output_dir} içerisine {saved_count} adet görsel başarıyla oluşturuldu.")

if __name__ == "__main__":
    generate_images("data/raw/BTCUSDT_1h.csv")