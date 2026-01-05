# 📖 PageVision OCR - Real-time Text Reader with Speech

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**PageVision OCR** is a sophisticated real-time OCR system that captures printed text from a live camera feed and automatically **speaks it aloud** using text-to-speech technology. Perfect for accessibility, document scanning, and hackathon projects!

## ✨ Features

- 🎥 **Real-time Webcam Capture** - Live video feed processing
- 🔍 **Advanced OCR** - Powered by Tesseract for accurate text recognition
- 🗣️ **Text-to-Speech** - Automatic speech output using pyttsx3 (offline)
- 📦 **Bounding Box Detection** - Visual feedback showing detected text regions
- 💾 **Text Export** - Save recognized text to `.txt` files
- 🎯 **Smart Text Detection** - Avoids repeating the same text continuously
- 🖼️ **Advanced Preprocessing** - CLAHE, adaptive thresholding, and noise reduction
- ⌨️ **Interactive Controls** - Keyboard shortcuts for all features
- 🌍 **Multi-language Support** - Structured for easy language expansion (English default)

## 🏗️ Project Structure

```
VisionPage_OCR/
│
├── main.py                      # Main application entry point
│
├── camera/
│   └── camera.py               # Webcam capture and video streaming
│
├── preprocess/
│   └── preprocess.py           # Image preprocessing pipeline
│
├── ocr/
│   └── ocr_engine.py          # Tesseract OCR integration
│
├── speech/
│   └── text_to_speech.py      # Text-to-speech conversion
│
├── utils/
│   └── file_handler.py        # File I/O operations
│
├── ocr_output/                # Auto-generated output directory
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** - Must be installed separately

### Step 1: Install Tesseract OCR

#### Windows:
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (e.g., `tesseract-ocr-w64-setup-5.3.3.exe`)
3. **Important:** Add Tesseract to your system PATH during installation
4. Default installation path: `C:\Program Files\Tesseract-OCR`

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

### Step 2: Verify Tesseract Installation

```bash
tesseract --version
```

You should see output like: `tesseract 5.x.x`

### Step 3: Clone/Download the Project

```bash
cd c:\Users\saksh\Downloads\VisionPage_OCR
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Tesseract Path (Windows Only - If Needed)

If you get a Tesseract not found error, edit [ocr/ocr_engine.py](ocr/ocr_engine.py#L19) and uncomment this line:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Adjust the path to match your Tesseract installation location.

## 🎮 Usage

### Running the Application

```bash
python main.py
```

### Keyboard Controls

| Key | Action |
|-----|--------|
| `S` | **Speak** - Speak the currently detected text |
| `T` | **Save Text** - Save detected text to a file |
| `A` | **Toggle Auto-Speak** - Enable/disable automatic speech |
| `P` | **Toggle Preprocessed View** - Show/hide preprocessing |
| `V` | **List Voices** - Display available TTS voices |
| `Q` | **Quit** - Exit the application |

### Workflow

1. **Launch** the application: `python main.py`
2. **Position** printed text in front of your webcam
3. **Wait** for automatic text detection and speech
4. **Press `S`** to manually trigger speech
5. **Press `T`** to save detected text to file
6. **Press `Q`** to exit

## 🔧 How It Works

### 1. **Camera Capture**
- Captures live video at 1280x720 resolution
- 30 FPS for smooth real-time processing

### 2. **Image Preprocessing**
- **Grayscale Conversion** - Simplify color information
- **Gaussian Blur** - Reduce noise
- **CLAHE Enhancement** - Improve contrast
- **Adaptive Thresholding** - Convert to binary image
- **Morphological Operations** - Clean up noise

### 3. **OCR Processing**
- **Text Extraction** - Tesseract reads the text
- **Bounding Box Detection** - Identifies text regions
- **Confidence Filtering** - Only accepts high-confidence results (>30%)
- **Smart Deduplication** - Avoids repeating identical text

### 4. **Text-to-Speech**
- **Offline Processing** - No internet required
- **Background Execution** - Non-blocking speech
- **Natural Speech** - Adjustable rate and volume
- **Multi-threaded** - Doesn't freeze the UI

## 📝 Configuration

### Adjust OCR Confidence Threshold

Edit [ocr/ocr_engine.py](ocr/ocr_engine.py#L10):

```python
self.confidence_threshold = 30  # Increase for stricter detection (0-100)
```

### Change Speech Rate

Edit [speech/text_to_speech.py](speech/text_to_speech.py#L10):

```python
self.rate = 150  # Words per minute (default: 150)
```

### Modify Camera Resolution

Edit [main.py](main.py#L20):

```python
self.camera = Camera(camera_index=0, width=1280, height=720)
```

### Add Nepali OCR Support

1. Install Nepali language data:
```bash
# Windows - Download from: https://github.com/tesseract-ocr/tessdata
# Place nep.traineddata in: C:\Program Files\Tesseract-OCR\tessdata\

# Linux/Mac
sudo apt install tesseract-ocr-nep
```

2. Change language in [main.py](main.py#L23):
```python
self.ocr_engine = OCREngine(language='nep', confidence_threshold=30)
```

## 🛠️ Troubleshooting

### Issue: "Tesseract not found"
**Solution:** 
- Ensure Tesseract is installed and added to PATH
- On Windows, uncomment and set the path in `ocr_engine.py`

### Issue: "Camera not detected"
**Solution:**
- Check camera permissions
- Try different camera index: `Camera(camera_index=1)`
- Ensure no other application is using the camera

### Issue: "Poor OCR accuracy"
**Solution:**
- Ensure good lighting
- Keep text steady and in focus
- Increase font size of printed text
- Adjust `confidence_threshold` parameter
- Clean the camera lens

### Issue: "No speech output"
**Solution:**
- Check system audio settings
- Verify pyttsx3 installation: `pip install --upgrade pyttsx3`
- Try listing voices: Press `V` in the application

### Issue: "Slow performance"
**Solution:**
- Increase `ocr_interval` in `main.py`: `self.ocr_interval = 30`
- Reduce camera resolution
- Close other applications

## 📊 Performance Tips

- **Optimal Distance:** 15-30 cm from camera
- **Lighting:** Bright, even lighting without glare
- **Text Size:** Minimum 12pt font recommended
- **Background:** Use plain, contrasting backgrounds
- **Stability:** Keep paper steady for best results

## 🔮 Future Enhancements

- [ ] Multi-language switching via keyboard
- [ ] GPU acceleration for faster processing
- [ ] Mobile app version
- [ ] Cloud storage integration
- [ ] Advanced text formatting preservation
- [ ] Batch processing mode
- [ ] Custom TTS voice training
- [ ] Document structure recognition (tables, lists)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📜 License

This project is licensed under the MIT License. Feel free to use it for personal or commercial projects.

## 👨‍💻 Author

Built by sakshyam Bastakoti for accessibility and innovation.

## 🙏 Acknowledgments

- **Tesseract OCR** - Google's powerful OCR engine
- **OpenCV** - Computer vision library
- **pyttsx3** - Cross-platform TTS library
- **Python Community** - For excellent documentation

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**⭐ If you find this project helpful, please give it a star!**

**🎯 Perfect for: Hackathons | Accessibility Projects | Educational Tools | Prototyping**

---

*Last Updated: January 5, 2026*
