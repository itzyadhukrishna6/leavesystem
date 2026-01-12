# College Leave Management System

A Web Application for managing student leave requests, approvals, and admin tracking.

## 🚀 How to Run this Project in VS Code (Beginner Guide)

Follow these simple steps to open and run the project on any computer.

### Step 1: Install Necessary Software
1.  **Download & Install VS Code**: [https://code.visualstudio.com/download](https://code.visualstudio.com/download)
2.  **Download & Install Python**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    *   *Important:* During installation, check the box **"Add Python to PATH"**.

### Step 2: Open the Project
1.  Open **VS Code**.
2.  Go to **File** > **Open Folder...**
3.  Select the `test` folder (where this file is located).

### Step 3: Install Dependencies
1.  In VS Code, open the **Terminal** (Go to **Terminal** > **New Terminal**).
2.  Type the following command and press **Enter**:
    ```bash
    pip install -r requirements.txt
    ```
    *This downloads the required libraries (Flask).*

### Step 4: Run the Application
1.  In the same terminal, type:
    ```bash
    python app.py
    ```
2.  You should see a message saying "Running on http://127.0.0.1:5000".
3.  Open your web browser (Chrome/Edge) and type: `http://127.0.0.1:5000`

---

## 🔑 Login Credentials

### 1. Admin Account
*   **Email**: `admin@college.edu`
*   **Password**: `admin123`
*   *Access*: Manage users, view all leave records.

### 2. Student Account (Test)
*   **Email**: `student@college.edu`
*   **Password**: `password123`
*   *Access*: Apply for leave, view history.

---

## 📂 Project Structure
*   `app.py`: The main file that runs the website.
*   `college_leave.db`: The database file (created automatically).
*   `templates/`: HTML files (the pages you see).
*   `static/`: CSS files (the designs and colors).
