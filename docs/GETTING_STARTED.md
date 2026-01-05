# 🎯 GETTING STARTED - PageVision OCR

## Welcome! Follow these steps to get your OCR system running.

---

## ⚡ QUICK START (5 Minutes)

### ✅ Step 1: Install Tesseract OCR

**Windows:**
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest installer (e.g., `tesseract-ocr-w64-setup-5.3.3.exe`)
3. Run the installer
4. ✅ **IMPORTANT:** Check "Add to PATH" during installation
5. Restart your terminal/PowerShell

**Verify Installation:**
```powershell
tesseract --version
```

You should see: `tesseract 5.x.x`

---

### ✅ Step 2: Install Python Dependencies

Open PowerShell in this directory and run:

```powershell
pip install -r requirements.txt
```

**What gets installed:**
- ✅ opencv-python (Computer Vision)
- ✅ pytesseract (OCR Python wrapper)
- ✅ pyttsx3 (Text-to-Speech)
- ✅ numpy (Array operations)
- ✅ Pillow (Image processing)

---

### ✅ Step 3: Test Your Installation

Run the dependency checker:

```powershell
python test_dependencies.py
```

You should see all green checkmarks ✓

---

### ✅ Step 4: RUN THE APPLICATION! 🚀

```powershell
python main.py
```

---

## 🎮 HOW TO USE

1. **Position Your Text**
   - Place printed text in front of your webcam
   - Distance: 15-30 cm from camera
   - Keep it steady for 2-3 seconds

2. **Wait for Detection**
   - Green bounding boxes will appear around detected text
   - The system will automatically speak the text (if auto-speak is ON)

3. **Use Keyboard Controls**
   - Press **S** to speak current text
   - Press **T** to save text to file
   - Press **A** to toggle auto-speak on/off
   - Press **Q** to quit

---

## ❓ TROUBLESHOOTING

### Problem: "Tesseract not found"

**Solution 1:** Add to PATH manually
1. Find your Tesseract installation: `C:\Program Files\Tesseract-OCR`
2. Add to Windows PATH environment variable

**Solution 2:** Edit the code
1. Open `ocr\ocr_engine.py`
2. Find line 19 (commented out)
3. Uncomment and update the path:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

### Problem: "Cannot open camera"

**Solutions:**
- Check if another app is using the camera
- Grant camera permissions in Windows Settings
- Try different camera index:
  - Open `main.py`
  - Change line 21 from `camera_index=0` to `camera_index=1`

---

### Problem: "Poor text detection"

**Solutions:**
- ✅ Improve lighting (bright, even light)
- ✅ Increase text size (at least 12pt font)
- ✅ Use matte paper (not glossy)
- ✅ Keep text parallel to camera
- ✅ Use high contrast (black text on white paper)

---

### Problem: "No speech output"

**Solutions:**
1. Check system volume
2. Verify audio drivers
3. Reinstall pyttsx3:
```powershell
pip uninstall pyttsx3
pip install pyttsx3
```
4. Press **V** in the app to list available voices

---

## 🎓 FIRST-TIME USER TUTORIAL

### Scenario: Reading a Book Page

1. **Start the app:**
   ```powershell
   python main.py
   ```

2. **Open a book** to any page with text

3. **Position the book** in front of your webcam
   - About 20cm distance
   - Make sure the page is well-lit
   - Keep it steady

4. **Wait 2-3 seconds**
   - You'll see green boxes around the text
   - The app will automatically read it aloud!

5. **Save the text** (optional)
   - Press **T** on your keyboard
   - Check the `ocr_output/` folder for saved file

6. **Exit**
   - Press **Q** to quit

---

## 📚 LEARNING MORE

After getting started, explore these files:

- **README.md** - Complete documentation
- **ARCHITECTURE.md** - System design and diagrams
- **config.py** - Customize settings
- **example_usage.py** - Test individual components

---

## 💡 PRO TIPS

✨ **For Best Accuracy:**
- Use books, documents, or printed papers
- Avoid handwritten text (not supported well)
- Keep lighting bright and even
- Hold text steady for 2-3 seconds

✨ **Performance Tips:**
- Increase `OCR_INTERVAL` in config.py for faster performance
- Reduce camera resolution if laggy
- Close other camera apps

✨ **Customization:**
- Edit `config.py` to change speech rate, OCR language, etc.
- Adjust `confidence_threshold` for stricter/looser detection
- Change speech rate in config (default: 150 WPM)

---

## 🌟 WHAT YOU CAN DO

✅ Read books aloud
✅ Scan documents
✅ Assist visually impaired users
✅ Learn new languages (change OCR language)
✅ Quick text digitization
✅ Build accessibility tools
✅ Create educational applications

---

## 🆘 STILL STUCK?

1. Run the test script: `python test_dependencies.py`
2. Check the troubleshooting section above
3. Review error messages carefully
4. Ensure all prerequisites are installed

---

## 🎉 YOU'RE READY!

Start the application and point your camera at any printed text!

```powershell
python main.py
```

**Happy OCR-ing! 📖➡️🔊**

---

*Need help? Check README.md for detailed documentation.*
