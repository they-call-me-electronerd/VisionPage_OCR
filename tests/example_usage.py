"""
Example Usage of PageVision OCR Components
This file demonstrates how to use individual modules
"""

# Example 1: Test Camera
def test_camera():
    from camera.camera import Camera
    import cv2
    
    print("Testing camera...")
    cam = Camera(camera_index=0)
    cam.start()
    
    for i in range(30):  # Capture 30 frames
        ret, frame = cam.read_frame()
        if ret:
            cv2.imshow('Test Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cam.release()
    cv2.destroyAllWindows()


# Example 2: Test Preprocessing
def test_preprocessing():
    from camera.camera import Camera
    from preprocess.preprocess import ImagePreprocessor
    import cv2
    
    print("Testing preprocessing...")
    cam = Camera()
    cam.start()
    preprocessor = ImagePreprocessor()
    
    ret, frame = cam.read_frame()
    if ret:
        processed = preprocessor.preprocess(frame)
        cv2.imshow('Original', frame)
        cv2.imshow('Preprocessed', processed)
        cv2.waitKey(0)
    
    cam.release()
    cv2.destroyAllWindows()


# Example 3: Test OCR
def test_ocr():
    from camera.camera import Camera
    from preprocess.preprocess import ImagePreprocessor
    from ocr.ocr_engine import OCREngine
    import cv2
    
    print("Testing OCR...")
    cam = Camera()
    cam.start()
    preprocessor = ImagePreprocessor()
    ocr = OCREngine()
    
    ret, frame = cam.read_frame()
    if ret:
        processed = preprocessor.preprocess(frame)
        text = ocr.extract_text(processed)
        print(f"Detected text: {text}")
    
    cam.release()


# Example 4: Test Text-to-Speech
def test_tts():
    from speech.text_to_speech import TextToSpeech
    
    print("Testing TTS...")
    tts = TextToSpeech()
    tts.speak("Hello! This is a test of the text to speech system.", blocking=True)
    print("Speech completed!")


# Example 5: Test File Handler
def test_file_handler():
    from utils.file_handler import FileHandler
    
    print("Testing file handler...")
    handler = FileHandler()
    
    test_text = "This is a test OCR output.\nLine 2 of the text.\nEnd of test."
    filepath = handler.save_text(test_text)
    print(f"Saved to: {filepath}")
    
    # List all files
    files = handler.list_saved_files()
    print(f"Saved files: {files}")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("PageVision OCR - Component Testing")
    print("=" * 60)
    print()
    print("Select a test to run:")
    print("1. Test Camera")
    print("2. Test Preprocessing")
    print("3. Test OCR")
    print("4. Test Text-to-Speech")
    print("5. Test File Handler")
    print("0. Exit")
    print()
    
    choice = input("Enter your choice (0-5): ")
    
    if choice == '1':
        test_camera()
    elif choice == '2':
        test_preprocessing()
    elif choice == '3':
        test_ocr()
    elif choice == '4':
        test_tts()
    elif choice == '5':
        test_file_handler()
    else:
        print("Exiting...")
