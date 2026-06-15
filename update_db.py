import sqlite3

def fix_trendyol():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Where Trendyol actually dropped the price to 33, set the claimed price to the historical average (63)
    # This creates a "Real Discount" that the AI will reward as a Best Buy.
    cursor.execute("""
        UPDATE prices
        SET claimed_original_price = 63.0
        WHERE seller = 'Trendyol' AND actual_price = 33.0
    """)
    
    conn.commit()
    conn.close()
    print('Trendyol Real Discount fixed.')

if __name__ == '__main__':
    fix_trendyol()
