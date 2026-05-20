import pandas as pd
from datetime import datetime, timedelta
import random

def generate_price_data():
    products = [
        {"name": "Samsung Galaxy S23 Ultra", "base_price": 1200, "manipulated": True, "seller": "ElectroWorld"},
        {"name": "Apple iPhone 14 Pro Max", "base_price": 1100, "manipulated": False, "seller": "AppleStore"},
        {"name": "Tarte Shape Tape Concealer", "base_price": 30, "manipulated": True, "seller": "BeautyCosmetics"},
        {"name": "Oysho Women's Compression Leggings", "base_price": 50, "manipulated": False, "seller": "SportFit"},
        {"name": "Adidas Running Shoes", "base_price": 60, "manipulated": True, "seller": "ShoeCenter"},
        {"name": "New Balance Sneakers", "base_price": 85, "manipulated": False, "seller": "UrbanKicks"}
    ]
    
    today = datetime(2026, 5, 9)
    data = []
    
    for p in products:
        eski_fiyat = p["base_price"]
        # Every product gets a campaign period to test real vs fake discounts
        campaign_start = random.randint(10, 20)
        campaign_end = campaign_start + 6
        
        for i in range(30):
            date = today - timedelta(days=29-i)
            is_manip = False
            seller = p["seller"]
            
            if campaign_start <= i <= campaign_end:
                if p["manipulated"]:
                    indirimli_fiyat = eski_fiyat * 1.5
                    claimed_price = eski_fiyat * 2.0
                    seller = "ScamSeller_1"
                else:
                    indirimli_fiyat = eski_fiyat * 0.8
                    claimed_price = eski_fiyat
                
                # KONTROL MANTIĞI: (Sizin belirttiğiniz kural)
                if indirimli_fiyat >= eski_fiyat:
                    is_manip = True # Şüpheli durum (Sahte İndirim)
                elif indirimli_fiyat < eski_fiyat:
                    is_manip = False # Normal / Gerçek İndirim
                    
                current_price = indirimli_fiyat
            else:
                current_price = eski_fiyat
                claimed_price = current_price
                
                if random.random() > 0.7:
                    current_price += random.choice([-1, 1]) * (eski_fiyat * 0.01) # Small realistic fluctuations
                    claimed_price = current_price
                
            data.append({"date": date.strftime("%Y-%m-%d"), "product_name": p["name"], "seller": seller, "actual_price": round(current_price, 2), "claimed_original_price": round(claimed_price, 2), "is_manipulation": is_manip, "real_old_price": round(eski_fiyat, 2)})
            
    pd.DataFrame(data).to_csv("price_manipulation_data.csv", index=False)
    print("Great! 1 month of realistic price data (price_manipulation_data.csv) has been successfully generated! 🎉")

if __name__ == "__main__":
    generate_price_data()