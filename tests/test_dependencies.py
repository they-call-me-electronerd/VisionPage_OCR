# Quick Test Script for PageVision OCR
# This script tests if all dependencies are properly installed

import sys

print("=" * 60)
print("PageVision OCR - Dependency Check")
print("=" * 60)
print()

dependencies = {
    'opencv-python': 'cv2',
    'pytesseract': 'pytesseract',
    'pyttsx3': 'pyttsx3',
    'numpy': 'numpy',
    'PIL': 'PIL'
}

all_installed = True

for package, import_name in dependencies.items():
    try:
        __import__(import_name)
        print(f"✓ {package:20s} - Installed")
    except ImportError:
        print(f"✗ {package:20s} - NOT INSTALLED")
        all_installed = False

print()
print("=" * 60)

# Check Tesseract
print("Checking Tesseract OCR...")
try:
    import pytesseract
    version = pytesseract.get_tesseract_version()
    print(f"✓ Tesseract OCR - Version {version}")
except Exception as e:
    print(f"✗ Tesseract OCR - NOT FOUND")
    print(f"  Error: {e}")
    print(f"  Please install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
    all_installed = False

print("=" * 60)
print()

if all_installed:
    print("🎉 All dependencies are installed correctly!")
    print("✓ You can now run: python main.py")
else:
    print("⚠ Some dependencies are missing.")
    print("✗ Please run: pip install -r requirements.txt")
    print("✗ And install Tesseract OCR manually")

print()
print("=" * 60)
