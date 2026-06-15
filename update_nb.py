import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("UPDATE products SET image_url='images/newbalance1.png,images/newbalance2.png,images/newbalance3.png' WHERE name LIKE '%New Balance%'")
conn.commit()
conn.close()
