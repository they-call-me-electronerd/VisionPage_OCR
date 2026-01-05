"""
Configuration File for PageVision OCR
Modify these settings to customize the application behavior
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================
CAMERA_INDEX = 0           # Camera device index (0 for default, 1 for external)
CAMERA_WIDTH = 1280        # Frame width in pixels
CAMERA_HEIGHT = 720        # Frame height in pixels
CAMERA_FPS = 30            # Frames per second

# ============================================================================
# OCR SETTINGS
# ============================================================================
OCR_LANGUAGE = 'eng'       # Language code: 'eng' for English, 'nep' for Nepali
OCR_CONFIDENCE = 30        # Minimum confidence threshold (0-100)
OCR_INTERVAL = 15          # Perform OCR every N frames (higher = faster, less accurate)

# Tesseract path (uncomment and set if Tesseract is not in PATH)
# TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSERACT_PATH = None

# ============================================================================
# PREPROCESSING SETTINGS
# ============================================================================
GAUSSIAN_KERNEL_SIZE = (5, 5)   # Kernel size for Gaussian blur
ADAPTIVE_BLOCK_SIZE = 11         # Block size for adaptive thresholding
ADAPTIVE_C_VALUE = 2             # Constant for adaptive thresholding
CLAHE_CLIP_LIMIT = 2.0          # Contrast enhancement limit
CLAHE_TILE_SIZE = (8, 8)        # Tile grid size for CLAHE

# ============================================================================
# TEXT-TO-SPEECH SETTINGS
# ============================================================================
TTS_RATE = 150             # Speech rate in words per minute (50-300)
TTS_VOLUME = 1.0           # Volume level (0.0 to 1.0)
TTS_VOICE_INDEX = None     # Voice index (None for default, 0-N for specific)

# ============================================================================
# FILE HANDLER SETTINGS
# ============================================================================
OUTPUT_DIRECTORY = 'ocr_output'  # Directory for saved files
AUTO_SAVE = False                 # Automatically save all detected text
SAVE_WITH_TIMESTAMP = True        # Include timestamp in filenames

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
AUTO_SPEAK_ENABLED = True         # Enable automatic speech on text detection
SHOW_BOUNDING_BOXES = True        # Show boxes around detected text
SHOW_CONFIDENCE_SCORES = True     # Display confidence scores on boxes
SIMILARITY_THRESHOLD = 0.8        # Text similarity threshold (0.0-1.0)
WINDOW_NAME = 'PageVision OCR - Live Feed'  # Main window title

# ============================================================================
# UI SETTINGS
# ============================================================================
INFO_PANEL_OPACITY = 0.6          # Transparency of info panel (0.0-1.0)
TEXT_COLOR_PRIMARY = (0, 255, 255)    # BGR color for title
TEXT_COLOR_SECONDARY = (255, 255, 0)  # BGR color for status
TEXT_COLOR_INFO = (255, 255, 255)     # BGR color for info
BBOX_COLOR = (0, 255, 0)              # BGR color for bounding boxes
BBOX_THICKNESS = 2                     # Thickness of bounding boxes

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================
ENABLE_MULTITHREADING = True      # Use threading for TTS
MAX_TEXT_LENGTH = 1000            # Maximum text length for display
ENABLE_DENOISE = False            # Enable additional denoising (slower)
ENABLE_DESKEW = False             # Enable automatic deskewing (slower)

# ============================================================================
# DEBUG SETTINGS
# ============================================================================
DEBUG_MODE = False                # Enable debug output
SAVE_PROCESSED_FRAMES = False     # Save preprocessed frames to disk
SHOW_FPS = False                  # Display FPS counter
LOG_OCR_RESULTS = True            # Print OCR results to console

# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================
KEY_SPEAK = 's'          # Speak current text
KEY_SAVE = 't'           # Save text to file
KEY_TOGGLE_AUTO = 'a'    # Toggle auto-speak
KEY_TOGGLE_VIEW = 'p'    # Toggle preprocessed view
KEY_VOICES = 'v'         # List available voices
KEY_QUIT = 'q'           # Quit application

# ============================================================================
# ADVANCED SETTINGS (Don't modify unless you know what you're doing)
# ============================================================================
OCR_CONFIG = '--oem 3 --psm 6'   # Tesseract configuration
MORPH_KERNEL_SIZE = (2, 2)        # Morphological operation kernel
MIN_TEXT_LENGTH = 3                # Minimum text length to consider valid
