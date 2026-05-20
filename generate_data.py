import pandas as pd
import random
from datetime import datetime, timedelta

def random_date():
    today = datetime(2026, 5, 9) # Current date based on system time
    start = today - timedelta(days=365) # 1 year ago
    return start + timedelta(days=random.randint(0, 365))

def generate_reviews(product_name, url, templates, count=500):
    data = []
    for i in range(count):
        template = random.choice(templates)
        rating = template["rating"]
        title = random.choice(template["titles"])
        text = random.choice(template["texts"])
        date_str = f"Reviewed in the United States on {random_date().strftime('%d %b %Y')}"
        helpful = random.choice(["", f"{random.randint(1, 100)} people found this helpful"])
        
        data.append({
            "url": url,
            "product_name": product_name,
            "reviewer_name": f"Customer_{random.randint(1000, 9999)}",
            "review_title": title,
            "review_text": text,
            "review_rating": rating,
            "verified_purchase": random.choice(["TRUE", "FALSE"]),
            "review_date": date_str,
            "helpful_count": helpful,
            "uniq_id": f"id-{random.randint(100000, 999999)}",
            "scraped_at": "24/10/23 10:00"
        })
    return pd.DataFrame(data)

# English Review Templates
samsung_templates = [
    {"rating": 5, "titles": ["Amazing phone!", "Best Android", "Stunning display"], "texts": ["The screen is gorgeous and the battery lasts all day.", "Super fast performance and beautiful design. Highly recommended.", "Best smartphone on the market right now."]},
    {"rating": 4, "titles": ["Great but heavy", "Very good", "Nice upgrade"], "texts": ["Overall a fantastic device, but a bit too bulky to hold.", "Camera is great, battery life is decent.", "Solid Android phone, slight learning curve from my old one."]},
    {"rating": 3, "titles": ["It's okay", "Average", "Expected more"], "texts": ["It's fine, but not a huge upgrade from the previous generation.", "Gets a bit warm during gaming. Otherwise okay.", "A bit overpriced for the features it offers."]},
    {"rating": 2, "titles": ["Disappointed", "Battery issues", "Too big"], "texts": ["Battery drains very fast when using 5G.", "Too heavy to hold comfortably with one hand.", "Software feels bloated and laggy at times."]},
    {"rating": 1, "titles": ["Terrible", "Do not buy", "Broke easily"], "texts": ["Screen cracked after a small drop. Very fragile.", "Worst phone I've ever owned. Overheats constantly.", "Customer service was terrible when I tried to return it."]}
]

apple_templates = [
    {"rating": 5, "titles": ["Perfect iPhone", "Love iOS", "Amazing Camera"], "texts": ["Dynamic island is a game changer. Super smooth.", "Best battery life I've seen on an iPhone.", "Video quality is unmatched. I absolutely love it."]},
    {"rating": 4, "titles": ["Solid phone", "Good but expensive", "Nice display"], "texts": ["A reliable phone as always, but costs a fortune.", "Screen is very bright and clear. Good upgrade.", "Works perfectly with my Mac and iPad."]},
    {"rating": 3, "titles": ["Just another iPhone", "Nothing special", "Okay"], "texts": ["Feels exactly like my old iPhone. Not much difference.", "It's a good phone but lightning port is annoying.", "Average experience, wish it had a better refresh rate."]},
    {"rating": 2, "titles": ["Overrated", "Poor battery", "Fragile"], "texts": ["Battery health dropped 5% in two months.", "Back glass shattered despite using a case.", "Too heavy and uncomfortable to hold for long periods."]},
    {"rating": 1, "titles": ["Awful", "Waste of money", "Regret buying"], "texts": ["Overpriced and doesn't offer anything new.", "My screen froze and had to be replaced.", "Apple maps and Siri are still terrible."]}
]

tarte_templates = [
    {"rating": 5, "titles": ["Holy grail!", "Best concealer", "Flawless coverage"], "texts": ["Covers my dark circles perfectly without creasing.", "A little goes a long way. Lasts all day!", "My favorite makeup product ever. Seamless finish."]},
    {"rating": 4, "titles": ["Great coverage", "Really good", "Nice formula"], "texts": ["Very full coverage, but make sure to moisturize first.", "Hides my blemishes well. A bit thick though.", "Good product, but the applicator is a bit too large."]},
    {"rating": 3, "titles": ["Drying", "Okay", "Not for dry skin"], "texts": ["It covers well but looks very dry under my eyes.", "Color match was difficult. Creases after a few hours.", "It's alright, but I think it's overhyped."]},
    {"rating": 2, "titles": ["Too heavy", "Cakey", "Disappointed"], "texts": ["Way too thick and cakey for my liking.", "Made me look older by settling into fine lines.", "Not a fan of the scent or the heavy texture."]},
    {"rating": 1, "titles": ["Terrible", "Broke me out", "Worst purchase"], "texts": ["Caused a massive breakout on my face.", "Extremely drying and looks terrible in natural light.", "Complete waste of money. Do not recommend."]}
]

oysho_templates = [
    {"rating": 5, "titles": ["So comfortable!", "Squat proof", "Love them"], "texts": ["These leggings are buttery soft and stay in place.", "Completely squat proof and very flattering.", "Best gym leggings I own. They shape the body beautifully."]},
    {"rating": 4, "titles": ["Good leggings", "Nice fit", "Great for yoga"], "texts": ["Very comfortable for yoga and pilates.", "Quality is great, but they are a bit long for me.", "Holds everything in. Would buy in another color."]},
    {"rating": 3, "titles": ["Average", "Sizing is weird", "A bit sheer"], "texts": ["They are okay but slightly see-through in bright light.", "The waistband rolls down sometimes during cardio.", "Sizing runs a bit small compared to other brands."]},
    {"rating": 2, "titles": ["Poor quality", "Ripped easily", "Not breathable"], "texts": ["The seam ripped after only two washes.", "Fabric is too thick and makes me sweat excessively.", "Uncomfortable compression, feels too tight on the stomach."]},
    {"rating": 1, "titles": ["Awful", "Do not buy", "Waste of money"], "texts": ["Completely see-through and very poor stitching.", "Lost their shape after the first workout.", "Worst leggings ever. The material is very itchy."]}
]

# Generate and save 500 rows of CSV files for each
generate_reviews("Samsung Galaxy S23 Ultra", "https://amazon.com/dp/SAM1", samsung_templates, 500).to_csv("samsung_phone.csv", index=False)
generate_reviews("Apple iPhone 14 Pro Max", "https://amazon.com/dp/APP1", apple_templates, 500).to_csv("apple_phone.csv", index=False)
generate_reviews("Tarte Shape Tape Concealer", "https://amazon.com/dp/TAR1", tarte_templates, 500).to_csv("tarte_concealer.csv", index=False)
generate_reviews("Oysho Women's Compression Leggings", "https://amazon.com/dp/OYS1", oysho_templates, 500).to_csv("oysho_sports.csv", index=False)

print("Congratulations! 4 English CSV files with 500 rows each have been successfully generated! 🎉")