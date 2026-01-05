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
        
        # Document detection parameters
        self.min_contour_area = 50000  # Minimum area for document detection
        self.max_contour_area_ratio = 0.9  # Maximum ratio of frame area
        
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
    
    def detect_document(self, frame):
        """  
        Detect if a document/page is present in the frame
        Uses contour detection to find rectangular objects
        
        Args:
            frame (numpy.ndarray): Input BGR image
            
        Returns:
            tuple: (has_document: bool, largest_contour: numpy.ndarray or None)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return False, None
        
        # Get frame dimensions
        frame_area = frame.shape[0] * frame.shape[1]
        
        # Find the largest rectangular contour
        largest_contour = None
        largest_area = 0
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if area < self.min_contour_area:
                continue
            
            # Skip if contour is too large (likely the whole frame)
            if area > frame_area * self.max_contour_area_ratio:
                continue
            
            # Approximate contour to polygon
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # Check if it's roughly rectangular (4 corners)
            if len(approx) >= 4 and area > largest_area:
                largest_area = area
                largest_contour = contour
        
        # Document detected if we found a valid rectangular contour
        has_document = largest_contour is not None and largest_area > self.min_contour_area
        
        return has_document, largest_contour
    
    def get_text_density(self, processed_image):
        """
        Calculate the density of potential text pixels in the image
        Higher density suggests presence of text
        
        Args:
            processed_image (numpy.ndarray): Binary preprocessed image
            
        Returns:
            float: Text density ratio (0.0 to 1.0)
        """
        # Count white pixels (potential text)
        white_pixels = np.count_nonzero(processed_image == 0)  # Text is black on white
        total_pixels = processed_image.size
        
        density = white_pixels / total_pixels if total_pixels > 0 else 0.0
        
        # Text typically occupies 5-30% of document area
        return density
