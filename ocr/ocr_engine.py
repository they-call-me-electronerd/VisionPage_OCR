"""
OCR Engine Module - Text extraction using Tesseract OCR
"""
import pytesseract
import cv2
import numpy as np
from datetime import datetime


class OCREngine:
    """Handles OCR operations using Tesseract"""
    
    def __init__(self, language='eng', confidence_threshold=30):
        """
        Initialize OCR engine
        
        Args:
            language (str): Language code for OCR ('eng' for English, 'nep' for Nepali)
            confidence_threshold (int): Minimum confidence score to accept text (0-100)
        """
        self.language = language
        self.confidence_threshold = confidence_threshold
        self.last_text = ""
        self.last_detection_time = None
        
        # Configure Tesseract path (uncomment and modify if needed)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Tesseract configuration for better accuracy
        self.config = f'--oem 3 --psm 6 -l {self.language}'
        
    def extract_text(self, image):
        """
        Extract text from preprocessed image
        
        Args:
            image (numpy.ndarray): Preprocessed binary image
            
        Returns:
            str: Extracted text (cleaned)
        """
        try:
            # Perform OCR
            text = pytesseract.image_to_string(image, config=self.config)
            
            # Clean the extracted text
            text = self.clean_text(text)
            
            return text
        except Exception as e:
            print(f"✗ OCR Error: {e}")
            return ""
    
    def extract_text_with_boxes(self, image):
        """
        Extract text along with bounding box coordinates
        
        Args:
            image (numpy.ndarray): Preprocessed image
            
        Returns:
            list: List of tuples containing (text, confidence, x, y, w, h)
        """
        try:
            # Get detailed OCR data including bounding boxes
            data = pytesseract.image_to_data(image, config=self.config, output_type=pytesseract.Output.DICT)
            
            boxes = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                # Filter by confidence threshold
                confidence = int(data['conf'][i])
                text = data['text'][i].strip()
                
                if confidence > self.confidence_threshold and text:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    boxes.append((text, confidence, x, y, w, h))
            
            return boxes
        except Exception as e:
            print(f"✗ OCR Box Detection Error: {e}")
            return []
    
    def clean_text(self, text):
        """
        Clean and format extracted text
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that are likely OCR errors
        # Keep alphanumeric, spaces, and basic punctuation
        cleaned = ''.join(char for char in text if char.isalnum() or char in ' .,!?;:-()[]"\'')
        
        return cleaned.strip()
    
    def is_new_text(self, current_text, similarity_threshold=0.8):
        """
        Check if the detected text is significantly different from the last detection
        This prevents repeated speech of the same content
        
        Args:
            current_text (str): Current detected text
            similarity_threshold (float): Minimum similarity ratio to consider text as "same"
            
        Returns:
            bool: True if text is new, False otherwise
        """
        if not current_text:
            return False
        
        if not self.last_text:
            self.last_text = current_text
            self.last_detection_time = datetime.now()
            return True
        
        # Simple similarity check
        similarity = self.calculate_similarity(current_text, self.last_text)
        
        if similarity < similarity_threshold:
            self.last_text = current_text
            self.last_detection_time = datetime.now()
            return True
        
        return False
    
    def calculate_similarity(self, text1, text2):
        """
        Calculate similarity ratio between two texts
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity ratio (0.0 to 1.0)
        """
        if not text1 or not text2:
            return 0.0
        
        # Convert to lowercase for comparison
        t1 = text1.lower().split()
        t2 = text2.lower().split()
        
        # Calculate Jaccard similarity
        set1 = set(t1)
        set2 = set(t2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def draw_boxes(self, frame, boxes):
        """
        Draw bounding boxes around detected text on the frame
        
        Args:
            frame (numpy.ndarray): Original frame
            boxes (list): List of bounding boxes from extract_text_with_boxes
            
        Returns:
            numpy.ndarray: Frame with drawn bounding boxes
        """
        output = frame.copy()
        
        for text, confidence, x, y, w, h in boxes:
            # Draw rectangle around text
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add confidence score above the box
            label = f"{confidence}%"
            cv2.putText(output, label, (x, y - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        return output
    
    def set_language(self, language):
        """
        Change OCR language
        
        Args:
            language (str): Language code ('eng', 'nep', etc.)
        """
        self.language = language
        self.config = f'--oem 3 --psm 6 -l {self.language}'
        print(f"✓ OCR language changed to: {language}")
