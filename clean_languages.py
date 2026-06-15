import sqlite3
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Get all reviews
cursor.execute("SELECT id, review_text FROM reviews")
rows = cursor.fetchall()

to_delete = []
for r_id, text in rows:
    try:
        # Check if text is valid enough
        if len(text.strip()) < 3:
            continue
            
        lang = detect(text)
        if lang != 'en':
            to_delete.append((r_id,))
    except LangDetectException:
        pass # If language cannot be detected, just keep it

print(f"Found {len(to_delete)} non-English reviews. Deleting them...")

if to_delete:
    cursor.executemany("DELETE FROM reviews WHERE id = ?", to_delete)
    conn.commit()

print("Cleaned up non-English reviews successfully.")
conn.close()
