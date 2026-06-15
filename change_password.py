import sqlite3

def change_password():
    new_password = input("Lütfen yeni şifrenizi girin: ")
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE admins SET password = ? WHERE username = 'admin'", (new_password,))
    conn.commit()
    conn.close()
    
    print(f"\nBaşarılı! Şifreniz '{new_password}' olarak güncellendi.")

if __name__ == "__main__":
    change_password()
