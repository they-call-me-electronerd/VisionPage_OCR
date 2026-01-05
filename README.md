# 📄 PageVision OCR - Real-time Text Reader

A real-time OCR (Optical Character Recognition) system with text-to-speech that reads printed text from your webcam with **advanced false positive elimination**.

## ✨ Key Features

- 🎥 **Real-time OCR** from webcam feed
- 🔊 **Automatic Text-to-Speech** for hands-free reading
- 🛡️ **5-Layer Validation System** - eliminates false positives and noise
- 📦 **Multi-language Support** (English, Nepali, and more)
- 💾 **Save extracted text** to files with timestamps
- 🎨 **Visual feedback** with bounding boxes and document detection
- ⚡ **Offline processing** - no internet required

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Webcam
- Tesseract OCR

### Installation

1. **Install Tesseract OCR:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to: `C:\Program Files\Tesseract-OCR\`

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python tests/test_dependencies.py
   ```

### Running the Application

```bash
python main.py
```

## ⌨️ Keyboard Controls

| Key | Action |
|-----|--------|
| `S` | Speak current detected text |
| `T` | Save text to file |
| `A` | Toggle auto-speak mode |
| `P` | Toggle preprocessed view |
| `V` | List available TTS voices |
| `Q` | Quit application |

## 🛡️ Advanced False Positive Protection

This system uses **5 layers of validation** to ensure only real text is detected and spoken:

### Layer 1: Document Detection
- Detects physical pages using contour detection
- Shows "Document: DETECTED" or "Document: NO PAGE" status

### Layer 2: Text Density Validation
- Analyzes pixel density to verify meaningful content
- Filters out blank frames and pure noise

### Layer 3: Meaningful Text Validation
- Requires minimum character count and valid words
- Rejects gibberish and random characters
- Requires 30%+ actual letters in the text

### Layer 4: Stability Tracking
- Text must appear consistently across multiple frames
- Prevents random flickering noise from being spoken

### Layer 5: New Text Detection
- Only speaks text that differs from previous detection
- Prevents repetition of the same content

**Result:** No more random words from noise, backgrounds, or empty frames!

## 📁 Project Structure

```
VisionPage_OCR/
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── SETUP.md               # Detailed setup instructions
├── LICENSE                # MIT License
├── camera/                # Camera capture module
│   ├── __init__.py
│   └── camera.py
├── ocr/                   # OCR engine module
│   ├── __init__.py
│   └── ocr_engine.py
├── preprocess/            # Image preprocessing module
│   ├── __init__.py
│   └── preprocess.py
├── speech/                # Text-to-speech module
│   ├── __init__.py
│   └── text_to_speech.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── file_handler.py
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md
│   ├── GETTING_STARTED.md
│   ├── VISUAL_GUIDE.md
│   └── FALSE_POSITIVE_SOLUTION.md
├── tests/                 # Test scripts
│   ├── test_dependencies.py
│   └── example_usage.py
└── ocr_output/           # Saved text files
```

## 🔧 Configuration

### Adjust Tesseract Path
Edit `ocr/ocr_engine.py` line 27:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Adjust Detection Sensitivity

**Document Detection** (`preprocess/preprocess.py`):
```python
self.min_contour_area = 10000  # Lower = detect smaller documents
```

**Text Stability** (`ocr/ocr_engine.py`):
```python
self.buffer_size = 2           # More frames = more stable (slower)
self.stability_threshold = 1   # Higher = stricter validation
```

**Processing Speed** (`main.py`):
```python
self.ocr_interval = 10  # Lower = faster processing, higher CPU usage
```

## 🎯 Usage Tips

### For Best Results:
- ✅ Use good lighting
- ✅ Hold the page steady
- ✅ Use printed text (not handwritten)
- ✅ Keep text at comfortable reading distance
- ✅ Ensure page is flat and in focus

### Common Issues:
- **"No document detected"** → Ensure page has clear borders
- **"Text not stable"** → Hold the page steadier
- **"Text rejected as noise"** → Improve lighting or text quality
- **Gibberish detected** → Clean the camera lens, improve focus

## 📚 Documentation

- [Setup Guide](SETUP.md) - Detailed installation instructions
- [Getting Started](docs/GETTING_STARTED.md) - Tutorial for beginners
- [Architecture](docs/ARCHITECTURE.md) - Technical documentation
- [Visual Guide](docs/VISUAL_GUIDE.md) - Screenshots and examples
- [False Positive Solution](docs/FALSE_POSITIVE_SOLUTION.md) - Validation system details

## 🧪 Testing

Test individual components:
```bash
python tests/example_usage.py
```

Check dependencies:
```bash
python tests/test_dependencies.py
```

## 📋 Requirements

See `requirements.txt`:
- opencv-python
- pytesseract
- pyttsx3
- numpy
- pillow

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 🙏 Acknowledgments

- **Tesseract OCR** - Google's OCR engine
- **OpenCV** - Computer vision library
- **pyttsx3** - Text-to-speech library

## 📞 Support

If you encounter issues:
1. Check the [FALSE_POSITIVE_SOLUTION.md](docs/FALSE_POSITIVE_SOLUTION.md) for troubleshooting
2. Verify all dependencies are installed
3. Ensure Tesseract is properly configured

---

**Version:** 2.0  
**Last Updated:** January 6, 2026  
**Status:** ✅ Production Ready
