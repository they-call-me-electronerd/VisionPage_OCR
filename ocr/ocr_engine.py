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
        
        # Stability tracking - text must appear in multiple consecutive frames
        self.text_buffer = []  # Store recent text detections
        self.buffer_size = 3   # Number of frames to check for consistency
        self.stability_threshold = 2  # Minimum consistent appearances
        
        # Meaningful text validation
        self.min_text_length = 3  # Minimum characters for valid text
        self.min_word_length = 2  # Minimum length for a word to be valid
        self.min_words = 1  # Minimum number of words required
        
        # Configure Tesseract path (uncomment and modify if needed)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
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
    
    def is_meaningful_text(self, text):
        """
        Validate if extracted text is meaningful and not random noise
        
        Args:
            text (str): Text to validate
            
        Returns:
            bool: True if text appears meaningful, False otherwise
        """
        if not text or len(text) < self.min_text_length:
            return False
        
        # Split into words
        words = text.split()
        
        if len(words) < self.min_words:
            return False
        
        # Check for valid words (at least min_word_length characters)
        valid_words = [w for w in words if len(w) >= self.min_word_length]
        
        if len(valid_words) < self.min_words:
            return False
        
        # Check if text has reasonable character composition
        # Should have more alphanumeric than special characters
        alnum_count = sum(c.isalnum() for c in text)
        total_non_space = len(text.replace(' ', ''))
        
        if total_non_space == 0:
            return False
        
        alnum_ratio = alnum_count / total_non_space
        
        # Require at least 60% alphanumeric characters
        if alnum_ratio < 0.6:
            return False
        
        # Reject if it's all digits or all special characters
        if text.replace(' ', '').isdigit():
            return len(text.replace(' ', '')) > 3  # Allow long numbers
        
        return True
    
    def add_to_buffer(self, text):
        """
        Add text detection to buffer for stability tracking
        
        Args:
            text (str): Detected text
        """
        self.text_buffer.append(text)
        
        # Keep buffer at fixed size
        if len(self.text_buffer) > self.buffer_size:
            self.text_buffer.pop(0)
    
    def is_stable_text(self, current_text):
        """
        Check if text appears consistently across multiple frames
        This prevents random noise from being spoken
        
        Args:
            current_text (str): Current detected text
            
        Returns:
            bool: True if text is stable across frames
        """
        if not current_text:
            return False
        
        # Add current text to buffer
        self.add_to_buffer(current_text)
        
        # Need enough frames in buffer
        if len(self.text_buffer) < self.buffer_size:
            return False
        
        # Count how many times similar text appears in buffer
        similar_count = 0
        for buffered_text in self.text_buffer:
            similarity = self.calculate_similarity(current_text, buffered_text)
            if similarity >= 0.7:  # 70% similarity threshold
                similar_count += 1
        
        # Text is stable if it appears consistently
        return similar_count >= self.stability_threshold
