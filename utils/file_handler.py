"""
File Handler Module - Handles file operations for saving OCR results
"""
import os
from datetime import datetime


class FileHandler:
    """Manages file operations for saving OCR text"""
    
    def __init__(self, output_dir='ocr_output'):
        """
        Initialize file handler
        
        Args:
            output_dir (str): Directory to save output files
        """
        self.output_dir = output_dir
        self.create_output_directory()
        
    def create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ Created output directory: {self.output_dir}")
    
    def save_text(self, text, filename=None):
        """
        Save extracted text to a file
        
        Args:
            text (str): Text to save
            filename (str): Custom filename (optional)
            
        Returns:
            str: Path to the saved file
        """
        if not text or not text.strip():
            print("⚠ No text to save")
            return None
        
        # Generate filename with timestamp if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ocr_text_{timestamp}.txt"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"OCR Text Extraction\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(text)
                f.write("\n\n" + "=" * 60 + "\n")
            
            print(f"✓ Text saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"✗ Error saving file: {e}")
            return None
    
    def append_text(self, text, filename='continuous_ocr.txt'):
        """
        Append text to an existing file (useful for continuous capture)
        
        Args:
            text (str): Text to append
            filename (str): Filename to append to
            
        Returns:
            str: Path to the file
        """
        if not text or not text.strip():
            return None
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"\n[{timestamp}]\n")
                f.write(text)
                f.write("\n" + "-" * 40 + "\n")
            
            print(f"✓ Text appended to: {filepath}")
            return filepath
        except Exception as e:
            print(f"✗ Error appending to file: {e}")
            return None
    
    def save_image(self, image, filename=None):
        """
        Save processed image
        
        Args:
            image (numpy.ndarray): Image to save
            filename (str): Custom filename (optional)
            
        Returns:
            str: Path to the saved image
        """
        import cv2
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ocr_image_{timestamp}.png"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            cv2.imwrite(filepath, image)
            print(f"✓ Image saved to: {filepath}")
            return filepath
        except Exception as e:
            print(f"✗ Error saving image: {e}")
            return None
    
    def read_text(self, filename):
        """
        Read text from a saved file
        
        Args:
            filename (str): Name of the file to read
            
        Returns:
            str: File contents or None if error
        """
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return None
    
    def list_saved_files(self):
        """
        List all saved files in the output directory
        
        Returns:
            list: List of filenames
        """
        try:
            files = os.listdir(self.output_dir)
            return sorted(files, reverse=True)  # Most recent first
        except Exception as e:
            print(f"✗ Error listing files: {e}")
            return []
