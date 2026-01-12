import sqlite3

try:
    conn = sqlite3.connect('college_leave.db')
    cursor = conn.cursor()
    
    print("Checking if column exists...")
    try:
        cursor.execute("SELECT profile_photo FROM users LIMIT 1")
        print("Column 'profile_photo' already exists.")
    except sqlite3.OperationalError:
        print("Column missing. Adding 'profile_photo' to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN profile_photo TEXT")
        conn.commit()
        print("Column added successfully!")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
