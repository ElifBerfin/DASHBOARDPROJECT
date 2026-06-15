import pandas as pd
import random
from datetime import datetime, timedelta

def generate_loreal_reviews(num_reviews=500):
    product_name = "L'Oreal True Match Lumi Glotion"
    
    # Review templates (rating, title, text)
    templates = [
        # Positive
        (5, "Absolutely love the glow!", "This glotion is amazing. It gives me such a natural, radiant glow without looking greasy. I use it under my foundation."),
        (5, "Holy grail product", "I have repurchased this three times. It makes my skin look so healthy. Better than expensive high-end alternatives!"),
        (4, "Very nice, subtle glow", "It's a great product, easily blendable. Taking one star off because the tube is a bit small, but a little goes a long way."),
        (5, "Perfect for no-makeup days", "When I don't want to wear foundation, I just put this on and it blurs imperfections while making my skin shine beautifully."),
        (4, "Good product", "I like how it looks on my skin. Doesn't cause breakouts for me. The color match is pretty decent."),
        
        # Neutral
        (3, "It's okay", "It gives a nice glow but it doesn't last all day. It tends to fade after a few hours on my oily skin."),
        (3, "Not bad, but not for me", "The glow is a bit too sparkly for my taste. I was expecting a more natural dewy finish."),
        (3, "Average glow lotion", "It does what it says, but I feel like I could get the same effect from mixing a liquid highlighter with my moisturizer."),
        
        # Negative
        (2, "Made me break out", "Unfortunately, this clogged my pores and caused a breakout on my cheeks. Might not be suitable for acne-prone skin."),
        (1, "Too glittery", "This isn't a 'natural glow'. It has visible chunks of glitter in it. I look like a disco ball. Returning it."),
        (2, "Greasy feeling", "It just sat on top of my skin and felt very heavy and greasy. Did not blend well with my other skincare products."),
        (1, "Terrible packaging", "The product exploded when I opened it. So much wasted product. The formula is okay but the tube is badly designed.")
    ]
    
    data = []
    end_date = datetime(2026, 5, 20)
    
    for i in range(num_reviews):
        # 70% chance of positive, 20% neutral, 10% negative
        r = random.random()
        if r < 0.7:
            rating, title, text = random.choice([t for t in templates if t[0] >= 4])
        elif r < 0.9:
            rating, title, text = random.choice([t for t in templates if t[0] == 3])
        else:
            rating, title, text = random.choice([t for t in templates if t[0] <= 2])
            
        review_date = end_date - timedelta(days=random.randint(0, 365))
        date_str = f"Reviewed in the United States on {review_date.strftime('%B %d, %Y')}"
        
        data.append({
            "product_name": product_name,
            "reviewer_name": f"User_{random.randint(1000, 9999)}",
            "review_title": title,
            "review_text": text,
            "review_rating": f"{rating}.0 out of 5 stars",
            "verified_purchase": "Verified Purchase",
            "review_date": date_str,
            "helpful_count": f"{random.randint(0, 50)} people found this helpful" if random.random() > 0.5 else ""
        })
        
    df = pd.DataFrame(data)
    df.to_csv("c:/Users/huawe/Desktop/Dashboard/loreal_lumi.csv", index=False)
    print("loreal_lumi.csv created successfully with 500 reviews.")

if __name__ == "__main__":
    generate_loreal_reviews()
