from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

# ... (rest of imports)

# ... (after apply_leave route)


# ... (rest of imports)

# --- Faculty Routes ---
import sqlite3
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Database Connection Helper
def get_db_connection():
    conn = sqlite3.connect(app.config['DB_NAME'])
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

# Login Required Decorator
def login_required(role=None):
    def wrapper(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash('Unauthorized access!', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            conn = get_db_connection()
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            conn.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['role'] = user['role']
                session['full_name'] = user['full_name']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        except Exception as e:
            flash(f"Database Error: {str(e)}", 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'faculty':
        return redirect(url_for('faculty_dashboard'))
    elif role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# --- Student Routes ---
@app.route('/student/dashboard')
@login_required(role='student')
def student_dashboard():
    conn = get_db_connection()
    leaves = conn.execute("SELECT * FROM leave_requests WHERE user_id = ? ORDER BY created_at DESC", (session['user_id'],)).fetchall()
    conn.close()
    return render_template('student_dashboard.html', leaves=leaves)

@app.route('/apply_leave', methods=['POST'])
@login_required(role='student')
def apply_leave():
    print("--- Processing Leave Application ---")
    try:
        user_id = session['user_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        leave_type = request.form['leave_type']
        reason = request.form['reason']
        
        print(f"User: {user_id}, Date: {start_date} to {end_date}, Type: {leave_type}")
        
        file = request.files.get('file')
        filename = None
        if file and file.filename != '':
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(f"File saved: {filename}")

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO leave_requests (user_id, start_date, end_date, leave_type, reason, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, start_date, end_date, leave_type, reason, filename))
        conn.commit()
        conn.close()
        
        flash('Leave application submitted successfully!', 'success')
        print("Database Insert Success")
    except Exception as e:
        print(f"ERROR in apply_leave: {e}")
        flash(f'Error submitting application: {str(e)}', 'danger')
        
    return redirect(url_for('student_dashboard'))

@app.route('/uploads/<filename>')
@login_required()
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Faculty Routes ---
@app.route('/faculty/dashboard')
@login_required(role='faculty')
def faculty_dashboard():
    conn = get_db_connection()
    # Fetch pending leaves. Joined with users to get student name
    pending_leaves = conn.execute("""
        SELECT l.*, u.full_name, u.profile_photo
        FROM leave_requests l 
        JOIN users u ON l.user_id = u.id 
        WHERE l.status = 'Pending' 
        ORDER BY l.created_at ASC
    """).fetchall()
    conn.close()
    return render_template('faculty_dashboard.html', leaves=pending_leaves)

@app.route('/update_leave/<int:id>', methods=['POST'])
@login_required(role='faculty')
def update_leave(id):
    action = request.form['action'] # 'approve' or 'reject'
    remarks = request.form.get('remarks', '')
    status = 'Approved' if action == 'approve' else 'Rejected'

    conn = get_db_connection()
    conn.execute("UPDATE leave_requests SET status = ?, remarks = ? WHERE id = ?", (status, remarks, id))
    conn.commit()
    conn.close()
    
    flash(f'Leave application {status}!', 'success')
    return redirect(url_for('faculty_dashboard'))

# --- Admin Routes ---
@app.route('/admin/dashboard')
@login_required(role='admin')
def admin_dashboard():
    conn = get_db_connection()
    
    # Stats
    student_count = conn.execute("SELECT COUNT(*) FROM users WHERE role='student'").fetchone()[0]
    faculty_count = conn.execute("SELECT COUNT(*) FROM users WHERE role='faculty'").fetchone()[0]
    total_leaves = conn.execute("SELECT COUNT(*) FROM leave_requests").fetchone()[0]
    
    users = conn.execute("SELECT * FROM users").fetchall()
    
    # Fetch all leaves for Admin View
    all_leaves = conn.execute("""
        SELECT l.*, u.full_name 
        FROM leave_requests l 
        JOIN users u ON l.user_id = u.id 
        ORDER BY l.created_at DESC
    """).fetchall()
    
    conn.close()
    return render_template('admin_dashboard.html', 
                           student_count=student_count, 
                           faculty_count=faculty_count,
                           total_leaves=total_leaves,
                           users=users,
                           leaves=all_leaves)

@app.route('/admin/add_user', methods=['POST'])
@login_required(role='admin')
def add_user():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    
    # Handle Profile Photo
    file = request.files.get('profile_photo')
    filename = None
    if file and file.filename != '':
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (full_name, email, password, role, profile_photo) VALUES (?, ?, ?, ?, ?)", 
                       (full_name, email, hashed_password, role, filename))
        conn.commit()
        conn.close()
        flash('User added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding user: {str(e)}', 'danger')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required(role='admin')
def delete_user(user_id):
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_leave/<int:leave_id>', methods=['POST'])
@login_required(role='admin')
def delete_leave(leave_id):
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM leave_requests WHERE id = ?", (leave_id,))
        conn.commit()
        conn.close()
        flash('Leave record deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting leave record: {str(e)}', 'danger')
    return redirect(url_for('admin_dashboard'))

# --- Init DB (For First Run) ---
def init_db():
    """Initializes the database using schema.sql"""
    if os.path.exists(app.config['DB_NAME']):
        return # Already exists
        
    conn = sqlite3.connect(app.config['DB_NAME'])
    with open('schema.sql') as f:
        conn.executescript(f.read())
    
    # Create Default Admin
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = 'admin@college.edu'")
    if not cursor.fetchone():
        pwd = generate_password_hash("admin123")
        cursor.execute("INSERT INTO users (full_name, email, password, role) VALUES ('System Admin', 'admin@college.edu', ?, 'admin')", (pwd,))
        print("Default Admin created: admin@college.edu / admin123")
    
    conn.commit()
    conn.close()
    print("Database Initialized!")

if __name__ == '__main__':
    init_db() # Auto-init on start
    app.run(debug=True, port=5001)
