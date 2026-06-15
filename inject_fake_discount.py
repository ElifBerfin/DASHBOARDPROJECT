import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Find Adidas product ID
cursor.execute("SELECT id, base_price FROM products WHERE name LIKE '%Adidas%';")
row = cursor.fetchone()
if not row:
    print("Adidas not found.")
    conn.close()
    exit()

pid = row[0]
base_price = row[1]

# Inject a fake discount for Amazon 2 days ago
# Fake discount means: They claim original price was 2x, but actual price is same as base_price (no real drop).
fake_claimed = base_price * 2.0
fake_actual = base_price * 1.05  # slightly higher or same

cursor.execute("""
    UPDATE prices 
    SET claimed_original_price = ?, actual_price = ?
    WHERE product_id = ? AND seller = 'Amazon' AND date IN (
        SELECT date FROM prices WHERE product_id = ? AND seller = 'Amazon' ORDER BY date DESC LIMIT 5
    )
""", (fake_claimed, fake_actual, pid, pid))

conn.commit()
conn.close()
print("Successfully injected a textbook fake discount into the SQLite database for Adidas!")
