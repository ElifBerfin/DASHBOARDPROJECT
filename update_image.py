import sqlite3

def update_db():
    conn = sqlite3.connect('c:/Users/huawe/Desktop/Dashboard/database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET image_url = 'images/loreal1.png' WHERE name = 'L''Oreal True Match Lumi Glotion'")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_db()
