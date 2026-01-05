# 🗂️ VisionPage OCR - File Organization Guide

## 📁 Directory Structure

```
VisionPage_OCR/
├── 📄 main.py                  # Main application entry point
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md               # Main documentation (START HERE)
├── 📄 SETUP.md                # Detailed setup guide
├── 📄 LICENSE                 # MIT License
│
├── 📁 camera/                 # Camera capture module
│   ├── __init__.py
│   └── camera.py              # Webcam interface
│
├── 📁 ocr/                    # OCR processing module
│   ├── __init__.py
│   └── ocr_engine.py          # Tesseract OCR wrapper with validation
│
├── 📁 preprocess/             # Image preprocessing module
│   ├── __init__.py
│   └── preprocess.py          # Image enhancement & document detection
│
├── 📁 speech/                 # Text-to-speech module
│   ├── __init__.py
│   └── text_to_speech.py     # pyttsx3 TTS wrapper
│
├── 📁 utils/                  # Utility functions
│   ├── __init__.py
│   └── file_handler.py        # File saving utilities
│
├── 📁 docs/                   # Documentation
│   ├── ARCHITECTURE.md        # Technical architecture
│   ├── GETTING_STARTED.md     # Beginner tutorial
│   ├── VISUAL_GUIDE.md        # Visual examples
│   └── FALSE_POSITIVE_SOLUTION.md  # Validation system details
│
├── 📁 tests/                  # Testing utilities
│   ├── test_dependencies.py   # Dependency checker
│   └── example_usage.py       # Component examples
│
└── 📁 ocr_output/            # Output directory for saved text files
```

## 🚀 Quick Reference

### To Run the Application:
```bash
python main.py
```

### To Test Dependencies:
```bash
python tests/test_dependencies.py
```

### To Test Individual Components:
```bash
python tests/example_usage.py
```

## 📚 Documentation Map

| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** | Main overview & quick start | First time setup |
| **SETUP.md** | Detailed installation guide | Having installation issues |
| **docs/GETTING_STARTED.md** | Step-by-step tutorial | Learning how to use |
| **docs/ARCHITECTURE.md** | Technical details | Understanding the code |
| **docs/VISUAL_GUIDE.md** | Screenshots & examples | Visual learners |
| **docs/FALSE_POSITIVE_SOLUTION.md** | Validation system explained | Tuning detection |

## 🔧 Key Configuration Files

### OCR Engine Configuration
**File:** `ocr/ocr_engine.py`
- Line 27: Tesseract path
- Lines 18-23: Validation thresholds

### Main Application Settings
**File:** `main.py`
- Line 35: OCR interval (processing speed)
- Lines 38-41: Document detection settings

### Preprocessing Settings
**File:** `preprocess/preprocess.py`
- Lines 10-11: Document detection thresholds

## 📝 Key Files to Edit

### For Basic Configuration:
1. `ocr/ocr_engine.py` - OCR settings
2. `main.py` - Application behavior

### For Advanced Tuning:
1. `preprocess/preprocess.py` - Image processing
2. `ocr/ocr_engine.py` - Text validation
3. `speech/text_to_speech.py` - TTS settings

## 🗑️ Removed Files (No Longer Needed)

The following files were removed during cleanup:
- ❌ `config.py` - Settings now in respective modules
- ❌ `CHECKLIST.md` - Consolidated into documentation
- ❌ `INDEX.md` - Replaced by this file
- ❌ `PROJECT_SUMMARY.md` - Information in README.md

## 📊 Module Dependencies

```
main.py
├── camera/camera.py
├── preprocess/preprocess.py
├── ocr/ocr_engine.py
├── speech/text_to_speech.py
└── utils/file_handler.py
```

## 🎯 Common Tasks

### Change OCR Language:
Edit `main.py` line 30:
```python
self.ocr_engine = OCREngine(language='nep')  # For Nepali
```

### Adjust Processing Speed:
Edit `main.py` line 35:
```python
self.ocr_interval = 5  # Lower = faster, more CPU usage
```

### Change Tesseract Path:
Edit `ocr/ocr_engine.py` line 27:
```python
pytesseract.pytesseract.tesseract_cmd = r'YOUR_PATH_HERE'
```

## 🔍 Finding Code

### Where to find specific functionality:

| Functionality | File | Function/Method |
|--------------|------|-----------------|
| Camera capture | `camera/camera.py` | `read_frame()` |
| Image preprocessing | `preprocess/preprocess.py` | `preprocess()` |
| Document detection | `preprocess/preprocess.py` | `detect_document()` |
| OCR text extraction | `ocr/ocr_engine.py` | `extract_text()` |
| Text validation | `ocr/ocr_engine.py` | `is_meaningful_text()` |
| Text stability | `ocr/ocr_engine.py` | `is_stable_text()` |
| Text-to-speech | `speech/text_to_speech.py` | `speak()` |
| Save text file | `utils/file_handler.py` | `save_text()` |

---

**Last Updated:** January 6, 2026  
**Organization Version:** 2.0
