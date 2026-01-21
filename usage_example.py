from audioforge.audio_processor import AudioProcessor
from audioforge.visualizer import AudioVisualizer

# Load and preprocess audio
processor = AudioProcessor('path/to/audio.wav')
audio_data = processor.load()
filtered_audio = processor.filter_noise(audio_data)

# Visualize the audio
visualizer = AudioVisualizer()
visualizer.plot_waveform(filtered_audio)
visualizer.plot_spectrogram(filtered_audio)