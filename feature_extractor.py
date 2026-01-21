import librosa
import numpy as np

class FeatureExtractor:
    """Extract various audio features for analysis."""
    
    def __init__(self, sr=22050):
        self.sr = sr
        
    def extract_mfcc(self, y, n_mfcc=13):
        """Extract MFCC features."""
        mfccs = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=n_mfcc)
        return mfccs
    
    def extract_spectral_features(self, y):
        """Extract spectral features like centroid, bandwidth, etc."""
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=self.sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=self.sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=self.sr)[0]
        
        return {
            'centroid': spectral_centroid,
            'bandwidth': spectral_bandwidth,
            'rolloff': spectral_rolloff
        }
    
    def extract_zero_crossing_rate(self, y):
        """Extract zero crossing rate."""
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        return zcr
    
    def extract_all_features(self, y):
        """Extract all features and return as a dictionary."""
        features = {}
        
        features['mfcc'] = self.extract_mfcc(y)
        features.update(self.extract_spectral_features(y))
        features['zcr'] = self.extract_zero_crossing_rate(y)
        
        return features