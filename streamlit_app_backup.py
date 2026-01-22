import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from audio_recorder_streamlit import audio_recorder
import io
import librosa
from vowel_space_recorder import FormantExtractor, VowelSpaceVisualizer
from visualizer import AudioVisualizer
from feature_extractor import FeatureExtractor
from audio_processor import AudioProcessor

# Page configuration
st.set_page_config(
    page_title="AudioForge - Vowel Space Analyzer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = VowelSpaceVisualizer()
if 'recorded_vowels' not in st.session_state:
    st.session_state.recorded_vowels = {}

def save_audio_to_array(audio_bytes, sr=22050):
    """Convert audio bytes to numpy array."""
    audio_file = io.BytesIO(audio_bytes)
    y, _ = librosa.load(audio_file, sr=sr)
    return y

def find_stable_vowel_segment(y, sr, segment_duration=0.3):
    """Find the most stable segment of the recording."""
    segment_samples = int(segment_duration * sr)
    hop_length = segment_samples // 4
    energies = []

    for i in range(0, len(y) - segment_samples, hop_length):
        segment = y[i:i+segment_samples]
        energy = np.sum(segment ** 2)
        energies.append((i, energy))

    if energies:
        best_idx, _ = max(energies, key=lambda x: x[1])
        return y[best_idx:best_idx+segment_samples]
    else:
        mid = len(y) // 2
        return y[mid-segment_samples//2:mid+segment_samples//2]

def main():
    # Header
    st.markdown('<p class="main-header">🎙️ AudioForge - Vowel Space Analyzer</p>', unsafe_allow_html=True)

    st.info("**Welcome!** Record vowel sounds and visualize them on an IPA-style vowel chart.")

    # Sidebar
    st.sidebar.title("⚙️ Settings")
    mode = st.sidebar.radio(
        "Select Mode:",
        ["Vowel Space Analysis", "Audio Visualization", "Feature Extraction"]
    )
    sr = st.sidebar.selectbox("Sample Rate (Hz)", [16000, 22050, 44100], index=1)

    # Main content
    if mode == "Vowel Space Analysis":
        show_vowel_space_mode(sr)
    elif mode == "Audio Visualization":
        show_audio_visualization_mode(sr)
    else:
        show_feature_extraction_mode(sr)

def show_vowel_space_mode(sr):
    """Display vowel space analysis interface."""
    st.markdown('<p class="sub-header">📊 Vowel Space Analysis</p>', unsafe_allow_html=True)

    vowels = {
        "/i/ (ee)": {"example": "as in 'bEEt'", "ipa": "/i/"},
        "/ɪ/ (ih)": {"example": "as in 'bIt'", "ipa": "/ɪ/"},
        "/ɛ/ (eh)": {"example": "as in 'bEt'", "ipa": "/ɛ/"},
        "/æ/ (a)": {"example": "as in 'bAt'", "ipa": "/æ/"},
        "/ɑ/ (ah)": {"example": "as in 'fAther'", "ipa": "/ɑ/"},
        "/ɔ/ (aw)": {"example": "as in 'cAUght'", "ipa": "/ɔ/"},
        "/u/ (oo)": {"example": "as in 'bOOt'", "ipa": "/u/"},
        "/ʌ/ (uh)": {"example": "as in 'bUt'", "ipa": "/ʌ/"},
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎤 Record a Vowel")
        selected_vowel = st.selectbox("Select vowel:", list(vowels.keys()))
        st.info(f"**Example**: {vowels[selected_vowel]['example']}")

        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="3x"
        )

        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")

            if st.button("🔍 Analyze Formants", type="primary"):
                with st.spinner("Analyzing..."):
                    try:
                        y = save_audio_to_array(audio_bytes, sr=sr)
                        segment = find_stable_vowel_segment(y, sr, segment_duration=0.5)
                        extractor = FormantExtractor(sr=sr)
                        formants = extractor.extract_formants(segment, n_formants=3)
                        f1, f2, f3 = formants

                        if f1 and f2:
                            st.success(f"✅ F1: {f1:.0f} Hz | F2: {f2:.0f} Hz" + (f" | F3: {f3:.0f} Hz" if f3 else ""))

                            ipa = vowels[selected_vowel]['ipa']
                            st.session_state.recorded_vowels[ipa] = {'f1': f1, 'f2': f2, 'f3': f3}
                            st.session_state.visualizer.add_vowel(ipa, f1, f2, f3)
                        else:
                            st.error("❌ Could not extract formants. Try again.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with col2:
        st.markdown("### 📝 Recorded Vowels")
        if st.session_state.recorded_vowels:
            for vowel, data in st.session_state.recorded_vowels.items():
                st.markdown(f"**{vowel}**: F1={data['f1']:.0f}Hz, F2={data['f2']:.0f}Hz")
            if st.button("🗑️ Clear All"):
                st.session_state.recorded_vowels = {}
                st.session_state.visualizer = VowelSpaceVisualizer()
                st.rerun()
        else:
            st.info("No vowels recorded yet.")

    if st.session_state.recorded_vowels:
        st.markdown('<p class="sub-header">🗺️ Vowel Space Chart</p>', unsafe_allow_html=True)
        show_reference = st.checkbox("Show reference vowels", value=True)

        fig, ax = st.session_state.visualizer.plot_vowel_space(show_reference=show_reference, figsize=(12, 10))
        st.pyplot(fig)

        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        st.download_button("📥 Download Chart", data=buffer, file_name="vowel_space.png", mime="image/png")

def show_audio_visualization_mode(sr):
    """Display audio visualization interface."""
    st.markdown('<p class="sub-header">📈 Audio Visualization</p>', unsafe_allow_html=True)

    input_method = st.radio("Input:", ["Record Audio", "Upload File"])
    audio_data = None

    if input_method == "Record Audio":
        audio_bytes = audio_recorder(text="Record", icon_name="microphone")
        if audio_bytes:
            st.audio(audio_bytes)
            audio_data = save_audio_to_array(audio_bytes, sr=sr)
    else:
        uploaded_file = st.file_uploader("Upload audio", type=["wav", "mp3", "flac"])
        if uploaded_file:
            audio_data, _ = librosa.load(uploaded_file, sr=sr)
            st.audio(uploaded_file)

    if audio_data is not None:
        processor = AudioProcessor(sr=sr)

        col1, col2 = st.columns(2)
        with col1:
            trim_silence = st.checkbox("Trim silence", value=True)
            normalize = st.checkbox("Normalize", value=True)
        with col2:
            filter_noise = st.checkbox("Filter noise")

        processed = audio_data.copy()
        if trim_silence:
            processed = processor.trim_silence(processed)
        if normalize:
            processed = processor.normalize(processed)
        if filter_noise:
            threshold = st.slider("Noise threshold", 0.0, 0.1, 0.01)
            processed = processor.filter_noise(processed, threshold=threshold)

        tab1, tab2, tab3 = st.tabs(["Waveform", "Spectrogram", "MFCC"])

        with tab1:
            fig = plt.figure(figsize=(12, 4))
            plt.plot(np.linspace(0, len(processed)/sr, len(processed)), processed)
            plt.title("Waveform")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            st.pyplot(fig)

        with tab2:
            fig = plt.figure(figsize=(12, 4))
            D = librosa.amplitude_to_db(np.abs(librosa.stft(processed)), ref=np.max)
            librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
            plt.colorbar(format='%+2.0f dB')
            plt.title("Spectrogram")
            st.pyplot(fig)

        with tab3:
            mfcc = librosa.feature.mfcc(y=processed, sr=sr, n_mfcc=13)
            fig = plt.figure(figsize=(12, 4))
            librosa.display.specshow(mfcc, sr=sr, x_axis='time')
            plt.colorbar()
            plt.title("MFCC")
            st.pyplot(fig)

def show_feature_extraction_mode(sr):
    """Display feature extraction interface."""
    st.markdown('<p class="sub-header">🔬 Feature Extraction</p>', unsafe_allow_html=True)

    input_method = st.radio("Input:", ["Record Audio", "Upload File"])
    audio_data = None

    if input_method == "Record Audio":
        audio_bytes = audio_recorder(text="Record", icon_name="microphone")
        if audio_bytes:
            st.audio(audio_bytes)
            audio_data = save_audio_to_array(audio_bytes, sr=sr)
    else:
        uploaded_file = st.file_uploader("Upload audio", type=["wav", "mp3", "flac"])
        if uploaded_file:
            audio_data, _ = librosa.load(uploaded_file, sr=sr)
            st.audio(uploaded_file)

    if audio_data is not None and st.button("🔍 Extract Features", type="primary"):
        with st.spinner("Extracting..."):
            extractor = FeatureExtractor(sr=sr)
            features = extractor.extract_all_features(audio_data)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### MFCC")
                mfcc_mean = np.mean(features['mfcc'], axis=1)
                st.bar_chart(mfcc_mean)

                st.markdown("#### Spectral Features")
                st.write(f"**Centroid**: {np.mean(features['centroid']):.2f} Hz")
                st.write(f"**Bandwidth**: {np.mean(features['bandwidth']):.2f} Hz")
                st.write(f"**Rolloff**: {np.mean(features['rolloff']):.2f} Hz")

            with col2:
                st.markdown("#### Zero Crossing Rate")
                st.write(f"**Mean ZCR**: {np.mean(features['zcr']):.4f}")
                st.line_chart(features['zcr'])

if __name__ == "__main__":
    main()
