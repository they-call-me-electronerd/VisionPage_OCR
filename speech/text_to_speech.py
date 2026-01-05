"""
Text-to-Speech Module - Converts text to speech using pyttsx3
"""
import pyttsx3
import threading


class TextToSpeech:
    """Handles text-to-speech conversion using pyttsx3 (offline)"""
    
    def __init__(self, rate=150, volume=1.0):
        """
        Initialize TTS engine
        
        Args:
            rate (int): Speech rate (words per minute)
            volume (float): Volume level (0.0 to 1.0)
        """
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume
        self.is_speaking = False
        
        # Configure TTS properties
        self.configure_engine()
        
    def configure_engine(self):
        """Configure TTS engine properties"""
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Try to set a clear English voice
        for voice in voices:
            if 'english' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        print(f"✓ Text-to-Speech initialized (Rate: {self.rate} WPM)")
    
    def speak(self, text, blocking=False):
        """
        Convert text to speech
        
        Args:
            text (str): Text to speak
            blocking (bool): If True, wait for speech to complete. If False, speak in background.
        """
        if not text or not text.strip():
            print("⚠ No text to speak")
            return
        
        if self.is_speaking:
            print("⚠ Already speaking, please wait...")
            return
        
        if blocking:
            # Blocking mode - wait for speech to complete
            self._speak_blocking(text)
        else:
            # Non-blocking mode - speak in background thread
            thread = threading.Thread(target=self._speak_blocking, args=(text,))
            thread.daemon = True
            thread.start()
    
    def _speak_blocking(self, text):
        """
        Internal method to speak text in blocking mode
        
        Args:
            text (str): Text to speak
        """
        try:
            self.is_speaking = True
            print(f"🔊 Speaking: {text[:50]}...")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"✗ TTS Error: {e}")
        finally:
            self.is_speaking = False
    
    def stop(self):
        """Stop current speech"""
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False
            print("✓ Speech stopped")
    
    def set_rate(self, rate):
        """
        Change speech rate
        
        Args:
            rate (int): New speech rate (words per minute)
        """
        self.rate = rate
        self.engine.setProperty('rate', self.rate)
        print(f"✓ Speech rate changed to: {rate} WPM")
    
    def set_volume(self, volume):
        """
        Change volume level
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        self.engine.setProperty('volume', self.volume)
        print(f"✓ Volume changed to: {int(self.volume * 100)}%")
    
    def list_voices(self):
        """List all available voices"""
        voices = self.engine.getProperty('voices')
        print("\n📢 Available voices:")
        for idx, voice in enumerate(voices):
            print(f"  {idx}: {voice.name} - {voice.languages}")
        return voices
    
    def set_voice(self, voice_index):
        """
        Change voice by index
        
        Args:
            voice_index (int): Index of the voice to use
        """
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            print(f"✓ Voice changed to: {voices[voice_index].name}")
        else:
            print(f"✗ Invalid voice index. Available: 0-{len(voices)-1}")
