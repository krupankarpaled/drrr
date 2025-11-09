# 🚨 URGENT FIX - Render Python 3.13.4 Issue

## Problem:
Render is using Python 3.13.4, but MediaPipe requires Python 3.8-3.11.

## ✅ SOLUTION - DO THIS NOW:

### Step 1: Set Python Version in Render Dashboard (REQUIRED)

1. Go to https://dashboard.render.com
2. Click on your "drowsing1" Web Service
3. Go to **Settings** tab
4. Scroll to **Environment Variables** section
5. Click **Add Environment Variable** button
6. Add this EXACT variable:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.9`
7. Click **Save Changes**

### Step 2: Disable Poetry Detection

1. In the same **Settings** tab
2. Go to **Build & Deploy** section
3. Find **Build Command** field
4. Clear it or set to:
   ```
   pip install -r requirements.txt
   ```
5. Click **Save Changes**

### Step 3: Verify Start Command

1. In **Settings** → **Build & Deploy**
2. Find **Start Command** field
3. Should be:
   ```
   streamlit run drowsiness_dashboard/app.py --server.port=$PORT --server.address=0.0.0.0
   ```
   OR if app.py is in root:
   ```
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
4. Click **Save Changes**

### Step 4: Manual Redeploy

1. After saving all changes
2. Click **Manual Deploy** button (top right)
3. Select **Deploy latest commit**
4. Watch the build logs

### Expected Result:

Build logs should show:
```
==> Installing Python version 3.11.9...
==> Using Python version 3.11.9 (default)
```

NOT:
```
==> Installing Python version 3.13.4...
```

## Why runtime.txt isn't working:

Render is detecting Poetry automatically, which overrides `runtime.txt`. 
The environment variable method (Step 1) is the MOST RELIABLE way to fix this.

## Files to commit:

Make sure these are committed and pushed:
- `runtime.txt` (contains: `3.11.9`)
- `requirements.txt`
- `Procfile`
- `.streamlit/config.toml`

