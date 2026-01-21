import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

class AudioVisualizer:
    """Visualize audio data in various formats."""
    
    def __init__(self, figsize=(12, 4)):
        self.figsize = figsize
        
    def plot_waveform(self, y, sr=22050, title="Waveform"):
        """Plot the waveform of an audio signal."""
        plt.figure(figsize=self.figsize)
        plt.plot(np.linspace(0, len(y)/sr, len(y)), y)
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.tight_layout()
        
        return plt
    
    def plot_spectrogram(self, y, sr=22050, title="Spectrogram"):
        """Plot the spectrogram of an audio signal."""
        plt.figure(figsize=self.figsize)
        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
        librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title(title)
        plt.tight_layout()
        
        return plt
    
    def plot_mfcc(self, mfcc, sr=22050, title="MFCC"):
        """Plot the MFCC features."""
        plt.figure(figsize=self.figsize)
        librosa.display.specshow(mfcc, sr=sr, x_axis='time')
        plt.colorbar(format='%+2.0f')
        plt.title(title)
        plt.tight_layout()
        
        return plt
    
    def plot_feature_over_time(self, feature, sr=22050, feature_name="Feature", title=None):
        """Plot a feature over time."""
        if title is None:
            title = f"{feature_name} Over Time"

        plt.figure(figsize=self.figsize)

        # Calculate appropriate time axis
        if len(feature.shape) > 1 and feature.shape[0] > 1:
            # If feature is 2D with multiple rows
            plt.imshow(feature, aspect='auto', origin='lower')
            plt.colorbar(format='%+2.0f')
        else:
            # If feature is 1D or a single row
            feature = feature.flatten()  # Ensure 1D
            time = np.linspace(0, len(feature) / sr, len(feature))
            plt.plot(time, feature)
            plt.xlabel("Time (s)")

        plt.title(title)
        plt.tight_layout()

        return plt


if __name__ == "__main__":
    # Demo: Create sample audio and visualize it
    print("Generating sample audio for visualization demo...")

    # Generate a simple audio signal (combination of sine waves)
    sr = 22050  # Sample rate
    duration = 3  # seconds
    t = np.linspace(0, duration, int(sr * duration))

    # Create a signal with multiple frequencies
    y = (np.sin(2 * np.pi * 440 * t) +  # A4 note
         0.5 * np.sin(2 * np.pi * 880 * t) +  # A5 note
         0.3 * np.sin(2 * np.pi * 220 * t))  # A3 note

    # Add some envelope to make it more interesting
    envelope = np.exp(-t / 2)
    y = y * envelope

    # Create visualizer
    visualizer = AudioVisualizer()

    # Plot waveform
    print("Displaying waveform...")
    visualizer.plot_waveform(y, sr, title="Sample Audio Waveform")
    plt.show()

    # Plot spectrogram
    print("Displaying spectrogram...")
    visualizer.plot_spectrogram(y, sr, title="Sample Audio Spectrogram")
    plt.show()

    # Compute and plot MFCC
    print("Displaying MFCC...")
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    visualizer.plot_mfcc(mfcc, sr, title="Sample Audio MFCC")
    plt.show()

    print("\nDemo complete! All visualizations have been displayed.")