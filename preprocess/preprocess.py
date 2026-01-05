"""
Preprocessing Module - Image enhancement for better OCR accuracy
"""
import cv2
import numpy as np


class ImagePreprocessor:
    """Handles image preprocessing pipeline for OCR optimization"""
    
    def __init__(self):
        """Initialize preprocessor with default parameters"""
        self.kernel_size = (5, 5)  # Gaussian blur kernel
        self.block_size = 11       # Adaptive threshold block size
        self.c_value = 2           # Adaptive threshold constant
        
    def preprocess(self, frame):
        """
        Apply full preprocessing pipeline to the input frame
        
        Args:
            frame (numpy.ndarray): Input BGR image from camera
            
        Returns:
            numpy.ndarray: Preprocessed binary image ready for OCR
        """
        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Step 2: Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, self.kernel_size, 0)
        
        # Step 3: Enhance contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(blurred)
        
        # Step 4: Apply adaptive thresholding for better text extraction
        # This works well for varying lighting conditions
        threshold = cv2.adaptiveThreshold(
            enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            self.block_size,
            self.c_value
        )
        
        # Step 5: Morphological operations to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        
        return morph
    
    def denoise(self, image):
        """
        Additional denoising step (optional)
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Denoised image
        """
        return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
    
    def deskew(self, image):
        """
        Deskew the image if text is tilted
        
        Args:
            image (numpy.ndarray): Input binary image
            
        Returns:
            numpy.ndarray: Deskewed image
        """
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Rotate the image to deskew
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    def get_preprocessed_for_display(self, frame):
        """
        Get preprocessed image suitable for display alongside original
        
        Args:
            frame (numpy.ndarray): Input frame
            
        Returns:
            numpy.ndarray: Preprocessed image in BGR format for display
        """
        processed = self.preprocess(frame)
        # Convert back to BGR for consistent display
        return cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
