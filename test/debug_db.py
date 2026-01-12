import sqlite3
try:
    conn = sqlite3.connect('college_leave.db')
    cursor = conn.cursor()
    
    print("--- Tables ---")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    
    print("\n--- Users ---")
    try:
        cursor.execute("SELECT id, email, role FROM users")
        print(cursor.fetchall())
    except Exception as e:
        print(f"Error checking users: {e}")
        
    conn.close()
except Exception as e:
    print(f"Connection error: {e}")
