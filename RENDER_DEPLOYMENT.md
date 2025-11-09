# Render Deployment Guide

## Start Command Configuration

### Option 1: Using Procfile (Automatic - Recommended)
Render will automatically detect the `Procfile` in the root directory. No manual configuration needed.

### Option 2: Manual Start Command in Render Dashboard

If you need to set it manually in Render:

1. Go to your Render Dashboard
2. Select your Web Service
3. Go to **Settings** → **Build & Deploy**
4. Scroll down to **Start Command**
5. Enter:
   ```
   streamlit run drowsiness_dashboard/app.py --server.port=$PORT --server.address=0.0.0.0
   ```
6. Click **Save Changes**

## Important Notes

- **Port**: Render automatically sets the `$PORT` environment variable. Always use `$PORT` in your start command.
- **Address**: Use `0.0.0.0` to bind to all network interfaces (required for Render).
- **Path**: The command assumes `app.py` is in the `drowsiness_dashboard/` subdirectory.

## Render Service Settings

### Build Command (if needed)
Leave empty or use:
```
pip install -r requirements.txt
```

### Environment
- **Python Version**: Specified in `runtime.txt` as Python 3.11.9 (required for MediaPipe compatibility)
- **Note**: MediaPipe does not support Python 3.12+ or 3.13+, so Python 3.11 is required

### Environment Variables (Optional)
No environment variables required for basic deployment.

## Files Required for Deployment

1. **Procfile** - Contains the start command
2. **requirements.txt** - Python dependencies
3. **runtime.txt** - Python version (3.11.9 for MediaPipe compatibility)
4. **.streamlit/config.toml** - Streamlit configuration
5. **drowsiness_dashboard/app.py** - Main application file

## Troubleshooting

1. **MediaPipe installation fails**: 
   - Ensure `runtime.txt` specifies Python 3.11 (MediaPipe doesn't support Python 3.12+)
   - Check that `runtime.txt` is in the root directory

2. **Service fails to start**: 
   - Check that the path to `app.py` is correct in the start command
   - Verify the Procfile is in the root directory

3. **Port errors**: 
   - Ensure `$PORT` is used (not a hardcoded port number)
   - Check that `--server.address=0.0.0.0` is in the start command

4. **Import errors**: 
   - Verify all dependencies are in `requirements.txt`
   - Check Python version compatibility with all packages

