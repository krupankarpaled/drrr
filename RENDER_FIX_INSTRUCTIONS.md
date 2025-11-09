# 🔴 CRITICAL FIX - Render Python Version Issue

## Problem
Render is using Python 3.13.4, but MediaPipe requires Python 3.8-3.11.

## ✅ SOLUTION - Do These Steps:

### Step 1: Set Python Version in Render Dashboard (REQUIRED)

1. Go to https://dashboard.render.com
2. Click on your Web Service
3. Go to **Settings** tab
4. Scroll down to **Environment Variables** section
5. Click **Add Environment Variable**
6. Add:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.9`
7. Click **Save Changes**

### Step 2: Disable Poetry (if detected)

1. In Render Dashboard, go to **Settings** → **Build & Deploy**
2. Find **Build Command** field
3. Set it to:
   ```
   pip install -r requirements.txt
   ```
4. Click **Save Changes**

### Step 3: Verify Files Are Committed

Make sure these files are in your repository root:
- ✅ `runtime.txt` (contains: `3.11.9`)
- ✅ `requirements.txt` (with correct dependencies)
- ✅ `Procfile` (with start command)
- ✅ `.streamlit/config.toml`

### Step 4: Commit and Push

```bash
git add runtime.txt requirements.txt Procfile .python-version
git commit -m "Fix Python version to 3.11.9 for MediaPipe"
git push
```

### Step 5: Manual Redeploy

1. In Render Dashboard, click **Manual Deploy** → **Deploy latest commit**
2. Watch the build logs
3. Should see: "Installing Python version 3.11.9" (NOT 3.13.4)

## Alternative: If runtime.txt Still Doesn't Work

If Render still ignores runtime.txt, use ONLY the environment variable method (Step 1) and delete runtime.txt.

## Files Status:

✅ `runtime.txt` - Contains `3.11.9`
✅ `.python-version` - Contains `3.11.9` (backup)
✅ `requirements.txt` - Updated with compatible versions
✅ `Procfile` - Correct start command

## After Fix:

Your build logs should show:
```
==> Installing Python version 3.11.9...
==> Using Python version 3.11.9
```

NOT:
```
==> Installing Python version 3.13.4...
```

