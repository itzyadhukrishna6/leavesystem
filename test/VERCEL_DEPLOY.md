# Deploy to Vercel

Vercel is a specific platform for frontend frameworks but supports Serverless Python.

## ⚠️ Critical Warning regarding SQLite
You are using `sqlite3` (a file-based database).
- **Vercel is Serverless**: This means the filesystem is **Read-Only** after deployment.
- **Consequence**: You **CANNOT** add new users or apply for leaves on the deployed version. The app will likely crash or error when you try to save data.
- **Solution**: To make this work on Vercel, you must switch to a cloud database like **Vercel Postgres**, **Supabase**, or **Neon**.

If you just want to view the app as a static demo (read-only), follow below.

## Step 1: Configuration (Already Done)
I have added `vercel.json` to your project folder. This tells Vercel how to run your Python app.

## Step 2: Push to GitHub
If you haven't already:
1. Open Terminal in VS Code.
2. Run:
   ```bash
   git add .
   git commit -m "Add Vercel config"
   git push origin main
   ```

## Step 3: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com) and Sign Up/Login.
2. Click **"Add New..."** -> **"Project"**.
3. Import your `college-leave-system` repository.
4. **Environment Variables**:
   - You might need to add `SECRET_KEY` if your app uses sessions (it does).
   - In Vercel Project Settings -> Environment Variables, add:
     - Key: `SECRET_KEY`
     - Value: (generate a random string, e.g., `supersecretkey123`)
5. Click **Deploy**.

## Alternative: Deploy (Command Line)
If you have Vercel CLI installed:
1. Run `npm i -g vercel` to install.
2. Run `vercel` in this folder.
3. Follow the prompts (Login -> Yes -> Select Scope -> Link to existing project? No -> etc.)
