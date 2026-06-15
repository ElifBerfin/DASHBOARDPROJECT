import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 1. Fetch all products
cursor.execute("SELECT id, name, base_price FROM products;")
products = cursor.fetchall()

for pid, name, base_price in products:
    # Apple and Samsung should remain clean (No manipulation injected)
    if "Apple" in name or "Samsung" in name:
        continue
        
    print(f"Injecting manipulation for: {name}")
    
    # We will inject 5 consecutive days of fake discounts for this product
    # so that the dashboard shows a list of "Suspicious" items, just like Adidas.
    # We choose the seller randomly or we just inject it to Amazon/Trendyol depending on what exists
    
    fake_claimed = base_price * 2.0
    fake_actual = base_price * 1.05
    
    # Find the most recent 5 dates for a random seller
    cursor.execute("SELECT seller, date FROM prices WHERE product_id = ? ORDER BY date DESC LIMIT 10", (pid,))
    rows = cursor.fetchall()
    
    # We will update these rows
    for row in rows[:5]: # Take top 5
        seller = row[0]
        date = row[1]
        
        cursor.execute("""
            UPDATE prices 
            SET claimed_original_price = ?, actual_price = ?
            WHERE product_id = ? AND seller = ? AND date = ?
        """, (fake_claimed, fake_actual, pid, seller, date))

conn.commit()
conn.close()
print("All non-Apple and non-Samsung products have been updated with textbook manipulations!")
