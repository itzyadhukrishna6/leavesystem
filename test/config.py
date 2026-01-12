import os

class Config:
    # Database Configuration
    # SQLite database will be created in the instance folder or current directory
    DB_NAME = 'college_leave.db'
    
    # Secret Key for Sessions
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key_for_college_leave_system'
    
    # Upload Folder
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
