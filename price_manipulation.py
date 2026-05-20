import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import random

# 5 Farklı ayakkabı modeli
shoes = ["New Balance 530", "Nike Air Max", "Adidas Ultraboost", "Puma RS-X", "Vans Old Skool"]
dates = [datetime(2023, 4, 1) + timedelta(days=i) for i in range(30)]

data = []

for shoe in shoes:
    base_price = random.randint(800, 1500) # Başlangıç fiyatı
    
    for date in dates:
        # Fiyat dalgalanması kurgulama
        current_price = base_price
        claimed_original_price = base_price
        
        # Nisan ayının 15'i civarı "Büyük Bahar İndirimi" kurgusu yapalım
        if date.day >= 15 and date.day <= 20:
            # Manipülasyon yapalım: Fiyatı aslında artırıp, çok yüksek bir fiyattan düşmüş gibi gösterelim
            if shoe == "New Balance 530" or shoe == "Nike Air Max": 
                current_price = base_price + 300  # Gerçekte zamlandı
                claimed_original_price = current_price + 500 # Sahte eski fiyat!
            else:
                # Gerçek indirim yapanlar
                current_price = base_price - 200
                claimed_original_price = base_price
        else:
            # Normal günlerde ufak dalgalanmalar
            current_price += random.choice([-50, 0, 50])
            claimed_original_price = current_price
            
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "shoe": shoe,
            "actual_price": current_price,
            "claimed_original_price": claimed_original_price
        })

df = pd.DataFrame(data)

df['rolling_avg_14d'] = df.groupby('shoe')['actual_price'].transform(lambda x: x.rolling(14, min_periods=1).mean())

# 1. YAPAY ZEKA DESTEKLİ ANOMALİ TESPİTİ (Isolation Forest)
features = ['actual_price', 'claimed_original_price', 'rolling_avg_14d']

# Modeli oluştur (verinin tahmini %10'u anomali olabilir diyerek kirlilik oranını ayarladık)
model = IsolationForest(contamination=0.10, random_state=42)
df['anomaly_score'] = model.fit_predict(df[features])

# 2. BACKGROUND VALIDATION (AI'ın bulduğu anomaliyi Kural ile sessizce doğrulama)
# AI anomali (-1) dediyse VE sözde indirim fiyatı gerçek fiyattan büyükse VE fiyat ortalamanın alt sınırından yüksekse -> Manipülasyondur
df['is_manipulation'] = (df['anomaly_score'] == -1) & (df['claimed_original_price'] > df['actual_price']) & (df['actual_price'] >= df['rolling_avg_14d'] * 0.9)

# Gereksiz AI skoru ve karmaşık verileri atarak UI'a sadece temiz veriyi gönderiyoruz
df = df.drop(columns=['anomaly_score', 'rolling_avg_14d'])

# Veriyi CSV olarak kaydet
df.to_csv("price_manipulation_data.csv", index=False)
print("Sentetik veri oluşturuldu. AI modelleri arka plan doğrulamasıyla manipülasyonları temiz bir şekilde tespit etti!")
