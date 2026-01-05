"""
PageVision OCR - Real-time OCR with Text-to-Speech
Main Application File

This application captures live video from a webcam, performs OCR on printed text,
and automatically speaks the detected text aloud.
"""

import cv2
import sys
import time
from camera.camera import Camera
from preprocess.preprocess import ImagePreprocessor
from ocr.ocr_engine import OCREngine
from speech.text_to_speech import TextToSpeech
from utils.file_handler import FileHandler


class PageVisionOCR:
    """Main application class for real-time OCR with TTS"""
    
    def __init__(self):
        """Initialize all components"""
        print("=" * 60)
        print("🚀 Initializing PageVision OCR System...")
        print("=" * 60)
        
        # Initialize components
        self.camera = Camera(camera_index=0, width=1280, height=720)
        self.preprocessor = ImagePreprocessor()
        self.ocr_engine = OCREngine(language='eng', confidence_threshold=30)
        self.tts = TextToSpeech(rate=150, volume=1.0)
        self.file_handler = FileHandler(output_dir='ocr_output')
        
        # Application state
        self.current_text = ""
        self.auto_speak = True  # Auto-speak when new text is detected
        self.show_processed = False  # Toggle to show preprocessed view
        self.frame_count = 0
        self.ocr_interval = 10  # Perform OCR every N frames for performance (faster processing)
        
        # Document detection state
        self.document_detected = False
        self.frames_without_document = 0
        self.max_frames_without_document = 10  # Reset buffer if no document for N frames
        
        print("✓ All components initialized successfully!\n")
    
    def display_instructions(self):
        """Display keyboard controls and instructions"""
        print("=" * 60)
        print("⌨️  KEYBOARD CONTROLS")
        print("=" * 60)
        print("  S  →  Speak current detected text")
        print("  T  →  Save text to file")
        print("  A  →  Toggle auto-speak mode")
        print("  P  →  Toggle preprocessed view")
        print("  V  →  List available TTS voices")
        print("  Q  →  Quit application")
        print("=" * 60)
        print()
    
    def add_overlay_text(self, frame, text, position, font_scale=0.6, color=(0, 255, 0), thickness=2):
        """
        Add text overlay to frame
        
        Args:
            frame: Input frame
            text: Text to display
            position: (x, y) coordinates
            font_scale: Size of the font
            color: Text color in BGR
            thickness: Text thickness
        """
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, color, thickness)
    
    def create_info_panel(self, frame):
        """
        Create an information panel on the frame
        
        Args:
            frame: Input frame
            
        Returns:
            Frame with info panel
        """
        height, width = frame.shape[:2]
        
        # Create semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (width - 10, 180), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # Add status information
        y_offset = 35
        line_height = 25
        
        self.add_overlay_text(frame, "PageVision OCR - Real-time Text Reader", 
                            (20, y_offset), 0.7, (0, 255, 255), 2)
        y_offset += line_height
        
        # Document detection status
        doc_status = "DETECTED" if self.document_detected else "NO PAGE"
        doc_color = (0, 255, 0) if self.document_detected else (0, 0, 255)
        self.add_overlay_text(frame, f"Document: {doc_status}", 
                            (20, y_offset), 0.5, doc_color, 1)
        y_offset += line_height
        
        status = "ON" if self.auto_speak else "OFF"
        color = (0, 255, 0) if self.auto_speak else (0, 165, 255)
        self.add_overlay_text(frame, f"Auto-Speak: {status}", 
                            (20, y_offset), 0.5, color, 1)
        y_offset += line_height
        
        self.add_overlay_text(frame, f"Language: {self.ocr_engine.language.upper()}", 
                            (20, y_offset), 0.5, (255, 255, 0), 1)
        y_offset += line_height
        
        # Display current text (truncated)
        if self.current_text:
            display_text = self.current_text[:60] + "..." if len(self.current_text) > 60 else self.current_text
            self.add_overlay_text(frame, f"Text: {display_text}", 
                                (20, y_offset), 0.5, (255, 255, 255), 1)
        
        # Add keyboard hint
        self.add_overlay_text(frame, "Press 'Q' to quit | 'S' to speak | 'T' to save", 
                            (20, height - 20), 0.5, (200, 200, 200), 1)
        
        return frame
    
    def process_frame(self, frame):
        """
        Process a single frame for OCR with multi-layer validation
        
        Args:
            frame: Input frame from camera
            
        Returns:
            Processed frame with annotations
        """
        # Create a copy for display
        display_frame = frame.copy()
        
        # Perform OCR at intervals for better performance
        if self.frame_count % self.ocr_interval == 0:
            # LAYER 1: Document Detection - Check if a page/document is present
            has_document, document_contour = self.preprocessor.detect_document(frame)
            self.document_detected = has_document
            
            # Draw document boundary if detected
            if has_document and document_contour is not None:
                cv2.drawContours(display_frame, [document_contour], -1, (0, 255, 0), 3)
                self.frames_without_document = 0
            else:
                self.frames_without_document += 1
                # Reset OCR buffer if no document detected for too long
                if self.frames_without_document > self.max_frames_without_document:
                    self.ocr_engine.text_buffer = []
                    # Don't print reset message every time
            
            # Proceed with OCR even if document detection is uncertain (more lenient)
            if True:  # Changed from 'if has_document:' to allow OCR even without perfect document detection
                # Preprocess the frame
                processed = self.preprocessor.preprocess(frame)
                
                # LAYER 2: Text Density Check - Verify there's meaningful content
                text_density = self.preprocessor.get_text_density(processed)
                
                if 0.01 < text_density < 0.7:  # Wider text density range for better detection
                    # Extract text with bounding boxes
                    boxes = self.ocr_engine.extract_text_with_boxes(processed)
                    
                    # Draw bounding boxes
                    display_frame = self.ocr_engine.draw_boxes(display_frame, boxes)
                    
                    # Extract full text
                    full_text = self.ocr_engine.extract_text(processed)
                    
                    # LAYER 3: Meaningful Text Validation
                    if full_text and self.ocr_engine.is_meaningful_text(full_text):
                        # LAYER 4: Stability Check - Text must be consistent across frames
                        if self.ocr_engine.is_stable_text(full_text):
                            # Update current text
                            self.current_text = full_text
                            print(f"\n📄 Detected STABLE text: {full_text}")
                            
                            # LAYER 5: New Text Check - Only speak if text is new
                            if self.auto_speak and self.ocr_engine.is_new_text(full_text):
                                print("🔊 Auto-speaking detected text...")
                                self.tts.speak(full_text, blocking=False)
                        else:
                            print("⚠ Text not stable enough (noise filtered)")
                    else:
                        if full_text:
                            print(f"⚠ Text rejected as noise: '{full_text}'")
                else:
                    print(f"⚠ Invalid text density: {text_density:.3f} (likely noise or no text)")
        
        # Add info panel
        display_frame = self.create_info_panel(display_frame)
        
        return display_frame
    
    def run(self):
        """Main application loop"""
        try:
            # Start camera
            self.camera.start()
            
            # Display instructions
            self.display_instructions()
            
            print("✓ Starting real-time OCR... Point camera at printed text.\n")
            
            while True:
                # Read frame from camera
                ret, frame = self.camera.read_frame()
                
                if not ret:
                    print("✗ Failed to read frame from camera")
                    break
                
                # Process frame
                self.frame_count += 1
                processed_frame = self.process_frame(frame)
                
                # Display the frame
                cv2.imshow('PageVision OCR - Live Feed', processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    # Quit
                    print("\n👋 Quitting application...")
                    break
                
                elif key == ord('s') or key == ord('S'):
                    # Speak current text
                    if self.current_text:
                        print(f"\n🔊 Speaking: {self.current_text}")
                        self.tts.speak(self.current_text, blocking=False)
                    else:
                        print("\n⚠ No text detected yet")
                
                elif key == ord('t') or key == ord('T'):
                    # Save text to file
                    if self.current_text:
                        filepath = self.file_handler.save_text(self.current_text)
                        print(f"\n💾 Text saved successfully!")
                    else:
                        print("\n⚠ No text to save")
                
                elif key == ord('a') or key == ord('A'):
                    # Toggle auto-speak
                    self.auto_speak = not self.auto_speak
                    status = "enabled" if self.auto_speak else "disabled"
                    print(f"\n🔊 Auto-speak {status}")
                
                elif key == ord('p') or key == ord('P'):
                    # Toggle preprocessed view
                    self.show_processed = not self.show_processed
                    print(f"\n👁 Preprocessed view: {'ON' if self.show_processed else 'OFF'}")
                
                elif key == ord('v') or key == ord('V'):
                    # List available voices
                    print()
                    self.tts.list_voices()
        
        except KeyboardInterrupt:
            print("\n\n⚠ Interrupted by user")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Cleanup
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\n" + "=" * 60)
        print("🧹 Cleaning up resources...")
        print("=" * 60)
        
        self.camera.release()
        cv2.destroyAllWindows()
        self.tts.stop()
        
        print("✓ Cleanup complete")
        print("=" * 60)
        print("Thank you for using PageVision OCR! 👋")
        print("=" * 60)


def main():
    """Entry point for the application"""
    # Create and run the application
    app = PageVisionOCR()
    app.run()


if __name__ == "__main__":
    main()
