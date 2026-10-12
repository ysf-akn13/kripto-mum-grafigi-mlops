import os
import shutil
from sklearn.model_selection import train_test_split

def tum_verileri_birlestir_ve_ayir():
    kaynaklar = {
        "binance": "data/processed/binance_images",
        "kaggle": "data/raw/kaggle_images"
    }
    tum_gorseller = []

    print("Veri setleri alt klasörler taranarak toplanıyor...")
    for kaynak_adi, kaynak_yol in kaynaklar.items():
        if os.path.exists(kaynak_yol):
            sayac = 0
            # os.walk ile alt klasörlerin (ADANIENT, charts vb.) içine derinlemesine iniyoruz
            for kok, klasorler, dosyalar in os.walk(kaynak_yol):
                for dosya in dosyalar:
                    if dosya.lower().endswith(('.png', '.jpg', '.jpeg')):
                        tam_yol = os.path.join(kok, dosya)
                        tum_gorseller.append((kaynak_adi, tam_yol))
                        sayac += 1
            print(f"-> {kaynak_yol} klasöründen {sayac} görsel bulundu ve eklendi.")
        else:
            print(f"Uyarı: {kaynak_yol} klasörü bulunamadı, atlanıyor.")

    if len(tum_gorseller) == 0:
        print("Hata: Hiçbir kaynak klasörde görsel bulunamadı!")
        return

    print(f"Toplamda {len(tum_gorseller)} adet görsel birleştirildi. Eğitim (%70), Doğrulama (%15) ve Test (%15) olarak ayrılıyor...")

    # %70 Train, %30 Geçici (Val + Test)
    train_yollar, gecici_yollar = train_test_split(tum_gorseller, test_size=0.30, random_state=42)
    # Kalan %30'luk kısmı %15 Val ve %15 Test olarak ikiye böl
    val_yollar, test_yollar = train_test_split(gecici_yollar, test_size=0.50, random_state=42)

    dagilim = {
        'train': train_yollar,
        'val': val_yollar,
        'test': test_yollar
    }

    output_base = "data/processed"
    
    # Eski kalıntıları temizleyip temiz bir başlangıç yapalım
    for grup_adi in dagilim.keys():
        grup_klasoru = os.path.join(output_base, grup_adi)
        if os.path.exists(grup_klasoru):
            for f in os.listdir(grup_klasoru):
                fp = os.path.join(grup_klasoru, f)
                if os.path.isfile(fp):
                    os.remove(fp)
        else:
            os.makedirs(grup_klasoru, exist_ok=True)

    # Görselleri isim çakışması olmayacak şekilde kopyala
    for grup_adi, kayit_listesi in dagilim.items():
        grup_klasoru = os.path.join(output_base, grup_adi)
        
        for idx, (kaynak_turu, kaynak_yol) in enumerate(kayit_listesi):
            dosya_uzantisi = os.path.splitext(kaynak_yol)[1]
            yeni_isim = f"{kaynak_turu}_{idx}{dosya_uzantisi}" # Örn: kaggle_12.png veya binance_5.png
            hedef_yol = os.path.join(grup_klasoru, yeni_isim)
            shutil.copy(kaynak_yol, hedef_yol)
            
        print(f"-> data/processed/{grup_adi}/ klasörüne {len(kayit_listesi)} görsel kopyalandı.")

    print("İki veri seti başarıyla birleştirilip oranlı bir şekilde dağıtıldı!")

if __name__ == "__main__":
    tum_verileri_birlestir_ve_ayir()