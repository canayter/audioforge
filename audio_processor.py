pythonimport librosa
import numpy as np

class AudioProcessor:
    """Class for processing audio files and extracting features."""
    
    def __init__(self, file_path=None, sr=22050):
        self.file_path = file_path
        self.sr = sr  # sample rate
        
    def load(self, file_path=None):
        """Load an audio file."""
        if file_path:
            self.file_path = file_path
        
        if not self.file_path:
            raise ValueError("No file path provided")
            
        y, sr = librosa.load(self.file_path, sr=self.sr)
        return y
    
    def filter_noise(self, y, threshold=0.01):
        """Apply simple noise reduction."""
        mask = np.abs(y) < threshold
        y_filtered = y.copy()
        y_filtered[mask] = 0
        return y_filtered
    
    def trim_silence(self, y, top_db=20):
        """Trim silence from the beginning and end."""
        y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)
        return y_trimmed
    
    def normalize(self, y):
        """Normalize audio to have max amplitude of 1."""
        return librosa.util.normalize(y)