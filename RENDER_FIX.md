# CRITICAL FIX FOR RENDER DEPLOYMENT

## Problem
Render is using Python 3.13.4, but MediaPipe only supports Python 3.8-3.11.

## Solution 1: Fix runtime.txt (Primary)
The `runtime.txt` file must be in the **root directory** of your repository with this exact content:

```
python-3.11.9
```

## Solution 2: Set Python Version in Render Dashboard (Backup)
If runtime.txt doesn't work:

1. Go to https://dashboard.render.com
2. Select your Web Service
3. Go to **Settings** → **Environment**
4. Add Environment Variable:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.9`
5. Save and redeploy

## Solution 3: Disable Poetry Detection
Render is detecting Poetry. To disable it:

1. Go to **Settings** → **Build & Deploy**
2. Set **Build Command** to:
   ```
   pip install -r requirements.txt
   ```
3. Make sure there's NO `pyproject.toml` or `poetry.lock` in your repo

## Files You Need (All in Root Directory):

1. **runtime.txt** - Contains: `python-3.11.9`
2. **requirements.txt** - Contains all dependencies
3. **Procfile** - Contains start command
4. **.streamlit/config.toml** - Streamlit config

## Verify Before Deploying:

1. ✅ runtime.txt exists in root
2. ✅ runtime.txt contains: `python-3.11.9`
3. ✅ requirements.txt has correct MediaPipe version
4. ✅ No pyproject.toml or poetry.lock files
5. ✅ All files committed and pushed to GitHub

## After Fixing:

1. Commit all changes:
   ```bash
   git add runtime.txt requirements.txt Procfile
   git commit -m "Fix Python version for MediaPipe compatibility"
   git push
   ```

2. Redeploy on Render
3. Check build logs - should show "Installing Python version 3.11.9"

