"""
Camera Module - Handles webcam capture and video streaming
"""
import cv2
import numpy as np


class Camera:
    """Manages webcam capture and frame processing"""
    
    def __init__(self, camera_index=0, width=1280, height=720):
        """
        Initialize camera with specified parameters
        
        Args:
            camera_index (int): Index of the camera device (default: 0)
            width (int): Frame width in pixels
            height (int): Frame height in pixels
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        
    def start(self):
        """Initialize and start the camera capture"""
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            raise Exception(f"Cannot open camera with index {self.camera_index}")
        
        # Set camera properties for better quality
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print(f"✓ Camera started successfully (Resolution: {self.width}x{self.height})")
        
    def read_frame(self):
        """
        Capture a single frame from the camera
        
        Returns:
            tuple: (success: bool, frame: numpy.ndarray)
        """
        if self.cap is None:
            raise Exception("Camera not started. Call start() first.")
        
        ret, frame = self.cap.read()
        return ret, frame
    
    def release(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            print("✓ Camera released")
    
    def is_opened(self):
        """Check if camera is currently active"""
        return self.cap is not None and self.cap.isOpened()
