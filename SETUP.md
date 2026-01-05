# PageVision OCR - Installation & Setup Guide

## Quick Start (Windows)

### Step 1: Install Tesseract OCR
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the `.exe` installer
3. **IMPORTANT:** Check "Add to PATH" during installation
4. Default path: `C:\Program Files\Tesseract-OCR`

### Step 2: Verify Tesseract
Open PowerShell or Command Prompt:
```bash
tesseract --version
```

### Step 3: Install Python Dependencies
```bash
cd c:\Users\saksh\Downloads\VisionPage_OCR
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python main.py
```

## Troubleshooting

### If Tesseract is not found:
1. Open `ocr\ocr_engine.py`
2. Find line 19 (around line 19)
3. Uncomment and update the path:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### If camera doesn't work:
- Check camera permissions in Windows Settings
- Try changing camera index in main.py:
```python
self.camera = Camera(camera_index=1)  # Try 1 instead of 0
```

### If speech doesn't work:
- Check Windows audio settings
- Reinstall pyttsx3:
```bash
pip uninstall pyttsx3
pip install pyttsx3
```

## Tips for Best Results

1. **Good Lighting:** Ensure bright, even lighting on the text
2. **Camera Position:** Hold text 15-30cm from camera
3. **Text Size:** Use at least 12pt font
4. **Background:** Plain, contrasting background works best
5. **Stability:** Keep the text steady for 2-3 seconds

## Controls Quick Reference

- `S` - Speak detected text
- `T` - Save text to file
- `A` - Toggle auto-speak on/off
- `Q` - Quit application

## Need Help?

Check the main README.md for detailed documentation and advanced configuration options.
