# User Guide: How to Deploy Your Project (Free)

We will use **Render.com** to deploy your website for free. It is simple and optimized for Python apps.

## Prerequisites
1.  **GitHub Account**: Go to [github.com](https://github.com/) and create a free account.
2.  **Git Installed**: Make sure Git is installed on your computer.

---

## Step 1: Upload Code to GitHub
1.  **Initialize Git**:
    *   Open your project folder in VS Code.
    *   Open Terminal (`Ctrl + ~`).
    *   Run these commands one by one:
        ```bash
        git init
        git add .
        git commit -m "Initial commit"
        ```
2.  **Create Repository on GitHub**:
    *   Go to GitHub and click **New Repository** (+ icon top right).
    *   Name it `college-leave-system`.
    *   Click **Create repository**.
3.  **Push Code**:
    *   Copy the 3 lines shown on GitHub under "…or push an existing repository from the command line".
    *   Paste them into your VS Code terminal and press Enter.

## Step 2: Deploy on Render
1.  Go to [dashboard.render.com](https://dashboard.render.com/) and Sign Up with GitHub.
2.  Click **New +** -> **Web Service**.
3.  Select "Build and deploy from a Git repository".
4.  Connect your `college-leave-system` repository.
5.  **Configure Settings** (Important!):
    *   **Name**: `my-college-app` (or any name).
    *   **Region**: Singapore (or nearest to you).
    *   **Runtime**: **Python 3**.
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
6.  Click **Create Web Service**.

## Step 3: Wait & Visit
*   Render will start building your app. This takes about 2-3 minutes.
*   Once it says **"Live"**, click the URL at the top (e.g., `https://my-college-app.onrender.com`).
*   **Done!** Your website is now on the internet.

---

## ⚠️ Important Note for SQLite
Since we are using **SQLite** (a file-based database):
*   **The database will reset every time you deploy a new update** (because Render wipes disk changes on redeploy).
*   For a real production app that keeps data forever, you would need to switch to **PostgreSQL** (Render offers a free tier for this too), but that requires code changes.
*   For a college project demo, the current **SQLite setup is completely fine**.
