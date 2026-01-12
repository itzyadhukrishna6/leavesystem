import sqlite3
from werkzeug.security import generate_password_hash

try:
    conn = sqlite3.connect('college_leave.db')
    cursor = conn.cursor()
    
    email = 'student@college.edu'
    password = 'password123'
    hashed = generate_password_hash(password)
    
    # Check if exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        print("User already exists. Updating password...")
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed, email))
    else:
        print("Creating new student...")
        cursor.execute("""
            INSERT INTO users (full_name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, ('Test Student', email, hashed, 'student'))
        
    conn.commit()
    conn.close()
    print(f"SUCCESS: User {email} is ready with password: {password}")
except Exception as e:
    print(f"Error: {e}")
