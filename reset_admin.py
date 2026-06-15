import sqlite3

def reset_admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='admins'")
    if not cursor.fetchone():
        print("Admins table does not exist.")
        return
        
    # Delete all existing admins
    cursor.execute("DELETE FROM admins;")
    
    # Insert default admin
    cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?);", ("admin", "admin123"))
    
    conn.commit()
    conn.close()
    print("Admin credentials reset successfully to admin / admin123")

if __name__ == "__main__":
    reset_admin()
