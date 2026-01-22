import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from audio_recorder_streamlit import audio_recorder
import io
import librosa
import pandas as pd
import json
from datetime import datetime
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

# Enhanced CSS
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
    .formant-table {
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    .success-badge {
        background-color: #d4edda;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .info-badge {
        background-color: #e8f4f8;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = VowelSpaceVisualizer()
if 'recorded_vowels' not in st.session_state:
    st.session_state.recorded_vowels = {}
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = {}
if 'session_name' not in st.session_state:
    st.session_state.session_name = f"Session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if 'language_mode' not in st.session_state:
    st.session_state.language_mode = "English"

# Comprehensive vowel systems for major world languages
# Formant values based on published acoustic phonetics research
VOWEL_SYSTEMS = {
    "English (American)": {
        "/i/ (ee)": {"example": "as in 'bEEt'", "ipa": "/i/", "target_f1": 280, "target_f2": 2250},
        "/ɪ/ (ih)": {"example": "as in 'bIt'", "ipa": "/ɪ/", "target_f1": 400, "target_f2": 2000},
        "/ɛ/ (eh)": {"example": "as in 'bEt'", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1800},
        "/æ/ (a)": {"example": "as in 'bAt'", "ipa": "/æ/", "target_f1": 700, "target_f2": 1700},
        "/ɑ/ (ah)": {"example": "as in 'fAther'", "ipa": "/ɑ/", "target_f1": 750, "target_f2": 1100},
        "/ɔ/ (aw)": {"example": "as in 'cAUght'", "ipa": "/ɔ/", "target_f1": 600, "target_f2": 900},
        "/u/ (oo)": {"example": "as in 'bOOt'", "ipa": "/u/", "target_f1": 300, "target_f2": 870},
        "/ʊ/ (u)": {"example": "as in 'bOOk'", "ipa": "/ʊ/", "target_f1": 400, "target_f2": 1000},
        "/ʌ/ (uh)": {"example": "as in 'bUt'", "ipa": "/ʌ/", "target_f1": 650, "target_f2": 1200},
        "/ə/ (uh)": {"example": "as in 'About'", "ipa": "/ə/", "target_f1": 500, "target_f2": 1500},
    },
    "Spanish": {
        "/i/": {"example": "sí, mi (yes, my)", "ipa": "/i/", "target_f1": 240, "target_f2": 2400},
        "/e/": {"example": "té, de (tea, of)", "ipa": "/e/", "target_f1": 450, "target_f2": 2300},
        "/a/": {"example": "la, casa (the, house)", "ipa": "/a/", "target_f1": 700, "target_f2": 1200},
        "/o/": {"example": "no, sol (no, sun)", "ipa": "/o/", "target_f1": 450, "target_f2": 800},
        "/u/": {"example": "tú, luz (you, light)", "ipa": "/u/", "target_f1": 300, "target_f2": 700},
    },
    "French": {
        "/i/": {"example": "si, vie (if, life)", "ipa": "/i/", "target_f1": 250, "target_f2": 2300},
        "/e/": {"example": "été (summer)", "ipa": "/e/", "target_f1": 400, "target_f2": 2100},
        "/ɛ/": {"example": "mère (mother)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1800},
        "/a/": {"example": "chat (cat)", "ipa": "/a/", "target_f1": 700, "target_f2": 1300},
        "/ɔ/": {"example": "port (port)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 900},
        "/o/": {"example": "beau (beautiful)", "ipa": "/o/", "target_f1": 400, "target_f2": 850},
        "/u/": {"example": "tout (all)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
        "/y/": {"example": "tu (you)", "ipa": "/y/", "target_f1": 250, "target_f2": 2000},
        "/ø/": {"example": "feu (fire)", "ipa": "/ø/", "target_f1": 400, "target_f2": 1500},
        "/œ/": {"example": "peur (fear)", "ipa": "/œ/", "target_f1": 550, "target_f2": 1400},
    },
    "German": {
        "/i/": {"example": "Biene (bee)", "ipa": "/i/", "target_f1": 250, "target_f2": 2300},
        "/ɪ/": {"example": "bitte (please)", "ipa": "/ɪ/", "target_f1": 400, "target_f2": 2000},
        "/e/": {"example": "Tee (tea)", "ipa": "/e/", "target_f1": 450, "target_f2": 2200},
        "/ɛ/": {"example": "Bett (bed)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1750},
        "/a/": {"example": "Hand (hand)", "ipa": "/a/", "target_f1": 700, "target_f2": 1300},
        "/ɔ/": {"example": "Gott (god)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 900},
        "/o/": {"example": "Boot (boat)", "ipa": "/o/", "target_f1": 400, "target_f2": 850},
        "/ʊ/": {"example": "Mutter (mother)", "ipa": "/ʊ/", "target_f1": 400, "target_f2": 1050},
        "/u/": {"example": "Schuh (shoe)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
        "/y/": {"example": "über (over)", "ipa": "/y/", "target_f1": 250, "target_f2": 1850},
        "/ø/": {"example": "schön (beautiful)", "ipa": "/ø/", "target_f1": 450, "target_f2": 1500},
    },
    "Italian": {
        "/i/": {"example": "vino (wine)", "ipa": "/i/", "target_f1": 240, "target_f2": 2400},
        "/e/": {"example": "mese (month)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/ɛ/": {"example": "bello (beautiful)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1800},
        "/a/": {"example": "casa (house)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/ɔ/": {"example": "cosa (thing)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 900},
        "/o/": {"example": "nome (name)", "ipa": "/o/", "target_f1": 450, "target_f2": 850},
        "/u/": {"example": "nudo (naked)", "ipa": "/u/", "target_f1": 300, "target_f2": 750},
    },
    "Portuguese (Brazilian)": {
        "/i/": {"example": "vi (I saw)", "ipa": "/i/", "target_f1": 250, "target_f2": 2350},
        "/e/": {"example": "vê (sees)", "ipa": "/e/", "target_f1": 450, "target_f2": 2150},
        "/ɛ/": {"example": "pé (foot)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1850},
        "/a/": {"example": "má (bad)", "ipa": "/a/", "target_f1": 700, "target_f2": 1300},
        "/ɔ/": {"example": "pó (dust)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 950},
        "/o/": {"example": "vô (grandpa)", "ipa": "/o/", "target_f1": 450, "target_f2": 900},
        "/u/": {"example": "nu (naked)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
    },
    "Turkish": {
        "/i/": {"example": "ip (thread)", "ipa": "/i/", "target_f1": 240, "target_f2": 2400},
        "/y/": {"example": "gül (rose)", "ipa": "/y/", "target_f1": 240, "target_f2": 2100},
        "/ɯ/": {"example": "kız (girl)", "ipa": "/ɯ/", "target_f1": 300, "target_f2": 1400},
        "/u/": {"example": "kum (sand)", "ipa": "/u/", "target_f1": 250, "target_f2": 700},
        "/e/": {"example": "el (hand)", "ipa": "/e/", "target_f1": 500, "target_f2": 2300},
        "/ø/": {"example": "göl (lake)", "ipa": "/ø/", "target_f1": 500, "target_f2": 1600},
        "/a/": {"example": "at (horse)", "ipa": "/a/", "target_f1": 700, "target_f2": 1200},
        "/o/": {"example": "kol (arm)", "ipa": "/o/", "target_f1": 450, "target_f2": 800},
    },
    "Arabic (Modern Standard)": {
        "/i/": {"example": "بيت (house)", "ipa": "/i/", "target_f1": 270, "target_f2": 2300},
        "/a/": {"example": "باب (door)", "ipa": "/a/", "target_f1": 750, "target_f2": 1200},
        "/u/": {"example": "سوق (market)", "ipa": "/u/", "target_f1": 320, "target_f2": 850},
    },
    "Russian": {
        "/i/": {"example": "мир (world)", "ipa": "/i/", "target_f1": 250, "target_f2": 2300},
        "/ɨ/": {"example": "мыло (soap)", "ipa": "/ɨ/", "target_f1": 350, "target_f2": 1600},
        "/e/": {"example": "это (this)", "ipa": "/e/", "target_f1": 500, "target_f2": 2000},
        "/a/": {"example": "мама (mom)", "ipa": "/a/", "target_f1": 700, "target_f2": 1200},
        "/o/": {"example": "дом (house)", "ipa": "/o/", "target_f1": 500, "target_f2": 900},
        "/u/": {"example": "ум (mind)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
    },
    "Mandarin Chinese": {
        "/i/": {"example": "一 yī (one)", "ipa": "/i/", "target_f1": 250, "target_f2": 2400},
        "/y/": {"example": "鱼 yú (fish)", "ipa": "/y/", "target_f1": 250, "target_f2": 1900},
        "/ɯ/": {"example": "四 sì (four)", "ipa": "/ɯ/", "target_f1": 300, "target_f2": 1400},
        "/u/": {"example": "五 wǔ (five)", "ipa": "/u/", "target_f1": 300, "target_f2": 850},
        "/ɤ/": {"example": "饿 è (hungry)", "ipa": "/ɤ/", "target_f1": 450, "target_f2": 1200},
        "/o/": {"example": "波 bō (wave)", "ipa": "/o/", "target_f1": 450, "target_f2": 900},
        "/a/": {"example": "八 bā (eight)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
    },
    "Japanese": {
        "/i/": {"example": "い (i)", "ipa": "/i/", "target_f1": 250, "target_f2": 2400},
        "/e/": {"example": "え (e)", "ipa": "/e/", "target_f1": 450, "target_f2": 2200},
        "/a/": {"example": "あ (a)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/o/": {"example": "お (o)", "ipa": "/o/", "target_f1": 450, "target_f2": 900},
        "/ɯ/": {"example": "う (u)", "ipa": "/ɯ/", "target_f1": 300, "target_f2": 1400},
    },
    "Korean": {
        "/i/": {"example": "이 (i)", "ipa": "/i/", "target_f1": 250, "target_f2": 2350},
        "/e/": {"example": "에 (e)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/ɛ/": {"example": "애 (ae)", "ipa": "/ɛ/", "target_f1": 600, "target_f2": 1900},
        "/a/": {"example": "아 (a)", "ipa": "/a/", "target_f1": 750, "target_f2": 1250},
        "/ʌ/": {"example": "어 (eo)", "ipa": "/ʌ/", "target_f1": 550, "target_f2": 1100},
        "/o/": {"example": "오 (o)", "ipa": "/o/", "target_f1": 450, "target_f2": 850},
        "/u/": {"example": "우 (u)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
        "/ɯ/": {"example": "으 (eu)", "ipa": "/ɯ/", "target_f1": 350, "target_f2": 1300},
    },
    "Hindi": {
        "/i/": {"example": "सी (si)", "ipa": "/i/", "target_f1": 270, "target_f2": 2300},
        "/e/": {"example": "से (se)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/ɛ/": {"example": "है (hai)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1850},
        "/a/": {"example": "का (ka)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/ɔ/": {"example": "और (aur)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 950},
        "/o/": {"example": "को (ko)", "ipa": "/o/", "target_f1": 450, "target_f2": 900},
        "/u/": {"example": "सू (su)", "ipa": "/u/", "target_f1": 300, "target_f2": 850},
    },
    "Dutch": {
        "/i/": {"example": "zien (to see)", "ipa": "/i/", "target_f1": 250, "target_f2": 2300},
        "/ɪ/": {"example": "dit (this)", "ipa": "/ɪ/", "target_f1": 400, "target_f2": 2000},
        "/e/": {"example": "zee (sea)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/ɛ/": {"example": "bed (bed)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1800},
        "/a/": {"example": "man (man)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/ɔ/": {"example": "pot (pot)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 900},
        "/o/": {"example": "boot (boat)", "ipa": "/o/", "target_f1": 450, "target_f2": 850},
        "/ʊ/": {"example": "put (pit)", "ipa": "/ʊ/", "target_f1": 400, "target_f2": 1000},
        "/u/": {"example": "hoed (hat)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
        "/y/": {"example": "huis (house)", "ipa": "/y/", "target_f1": 250, "target_f2": 2000},
        "/ø/": {"example": "neus (nose)", "ipa": "/ø/", "target_f1": 450, "target_f2": 1500},
    },
    "Swedish": {
        "/i/": {"example": "vi (we)", "ipa": "/i/", "target_f1": 250, "target_f2": 2350},
        "/e/": {"example": "se (see)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/ɛ/": {"example": "häst (horse)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1800},
        "/a/": {"example": "mat (food)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/ɑ/": {"example": "tak (roof)", "ipa": "/ɑ/", "target_f1": 700, "target_f2": 1100},
        "/ɔ/": {"example": "hål (hole)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 900},
        "/o/": {"example": "bro (bridge)", "ipa": "/o/", "target_f1": 450, "target_f2": 850},
        "/u/": {"example": "mus (mouse)", "ipa": "/u/", "target_f1": 300, "target_f2": 800},
        "/y/": {"example": "hus (house)", "ipa": "/y/", "target_f1": 250, "target_f2": 1950},
        "/ø/": {"example": "röd (red)", "ipa": "/ø/", "target_f1": 450, "target_f2": 1500},
    },
    "Polish": {
        "/i/": {"example": "mił (nice)", "ipa": "/i/", "target_f1": 270, "target_f2": 2300},
        "/ɨ/": {"example": "ty (you)", "ipa": "/ɨ/", "target_f1": 350, "target_f2": 1600},
        "/ɛ/": {"example": "sen (dream)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1850},
        "/a/": {"example": "las (forest)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/ɔ/": {"example": "kot (cat)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 950},
        "/u/": {"example": "but (shoe)", "ipa": "/u/", "target_f1": 300, "target_f2": 850},
    },
    "Greek": {
        "/i/": {"example": "νύχτα (night)", "ipa": "/i/", "target_f1": 260, "target_f2": 2300},
        "/e/": {"example": "γέρος (old)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/a/": {"example": "μάτι (eye)", "ipa": "/a/", "target_f1": 700, "target_f2": 1250},
        "/o/": {"example": "χρόνος (time)", "ipa": "/o/", "target_f1": 450, "target_f2": 900},
        "/u/": {"example": "κούκλα (doll)", "ipa": "/u/", "target_f1": 300, "target_f2": 850},
    },
    "Vietnamese": {
        "/i/": {"example": "tí (little)", "ipa": "/i/", "target_f1": 250, "target_f2": 2400},
        "/e/": {"example": "té (to fall)", "ipa": "/e/", "target_f1": 450, "target_f2": 2100},
        "/ɛ/": {"example": "kẹ (candy)", "ipa": "/ɛ/", "target_f1": 550, "target_f2": 1850},
        "/a/": {"example": "ta (we)", "ipa": "/a/", "target_f1": 700, "target_f2": 1300},
        "/ɔ/": {"example": "ó (oh)", "ipa": "/ɔ/", "target_f1": 550, "target_f2": 950},
        "/o/": {"example": "tô (bowl)", "ipa": "/o/", "target_f1": 450, "target_f2": 900},
        "/u/": {"example": "tú (you)", "ipa": "/u/", "target_f1": 300, "target_f2": 850},
        "/ɯ/": {"example": "tư (thought)", "ipa": "/ɯ/", "target_f1": 300, "target_f2": 1400},
    },
}

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

def calculate_vowel_accuracy(f1, f2, target_f1, target_f2):
    """Calculate how close the recorded vowel is to target."""
    # Euclidean distance in formant space
    distance = np.sqrt((f1 - target_f1)**2 + (f2 - target_f2)**2)
    # Convert to similarity score (0-100%)
    max_distance = 1000  # Maximum expected distance
    accuracy = max(0, 100 - (distance / max_distance * 100))
    return accuracy, distance

def save_session_to_json():
    """Export session data as JSON for download."""
    session_data = {
        "session_name": st.session_state.session_name,
        "timestamp": datetime.now().isoformat(),
        "language": st.session_state.language_mode,
        "recordings": []
    }

    for vowel, data in st.session_state.recorded_vowels.items():
        session_data["recordings"].append({
            "vowel": vowel,
            "f1": float(data['f1']),
            "f2": float(data['f2']),
            "f3": float(data['f3']) if data['f3'] else None
        })

    return json.dumps(session_data, indent=2)

def load_session_from_json(json_str):
    """Load session data from JSON."""
    try:
        data = json.loads(json_str)
        st.session_state.session_name = data.get("session_name", "Loaded Session")
        st.session_state.language_mode = data.get("language", "English")
        st.session_state.recorded_vowels = {}
        st.session_state.visualizer = VowelSpaceVisualizer()

        for recording in data.get("recordings", []):
            vowel = recording["vowel"]
            st.session_state.recorded_vowels[vowel] = {
                'f1': recording['f1'],
                'f2': recording['f2'],
                'f3': recording.get('f3')
            }
            st.session_state.visualizer.add_vowel(
                vowel, recording['f1'], recording['f2'], recording.get('f3')
            )
        return True
    except Exception as e:
        st.error(f"Error loading session: {str(e)}")
        return False

def main():
    # Header
    st.markdown('<p class="main-header">🎙️ AudioForge - Vowel Space Analyzer</p>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("⚙️ Settings")

    # Mode selection
    mode = st.sidebar.radio(
        "Select Mode:",
        ["🎤 Vowel Space Analysis", "📈 Audio Visualization", "🔬 Feature Extraction", "🎯 Practice Mode"]
    )

    # Session management in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Session")
    st.session_state.session_name = st.sidebar.text_input(
        "Session Name",
        value=st.session_state.session_name
    )

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("💾 Save", help="Download session as JSON"):
            json_data = save_session_to_json()
            st.download_button(
                label="Download Session",
                data=json_data,
                file_name=f"{st.session_state.session_name}.json",
                mime="application/json"
            )

    with col2:
        uploaded_file = st.file_uploader("📂 Load", type=['json'], label_visibility="collapsed")
        if uploaded_file:
            json_str = uploaded_file.read().decode('utf-8')
            if load_session_from_json(json_str):
                st.sidebar.success("Session loaded!")
                st.rerun()

    # Language selection
    st.sidebar.markdown("---")
    st.session_state.language_mode = st.sidebar.selectbox(
        "🌍 Language",
        list(VOWEL_SYSTEMS.keys()),
        index=list(VOWEL_SYSTEMS.keys()).index(st.session_state.language_mode)
    )

    sr = st.sidebar.selectbox("🎚️ Sample Rate (Hz)", [16000, 22050, 44100], index=1)

    # Show help
    with st.sidebar.expander("ℹ️ Help & Tips"):
        st.markdown("""
        **Recording Tips:**
        - Use a quiet environment
        - Keep consistent distance from mic
        - Sustain vowel for 1-2 seconds
        - Speak clearly

        **Features:**
        - Record multiple vowels
        - Save/load sessions
        - Compare languages
        - Export data
        - Practice mode with scoring
        """)

    # Main content
    if mode == "🎤 Vowel Space Analysis":
        show_vowel_space_mode(sr)
    elif mode == "📈 Audio Visualization":
        show_audio_visualization_mode(sr)
    elif mode == "🔬 Feature Extraction":
        show_feature_extraction_mode(sr)
    else:
        show_practice_mode(sr)

def show_vowel_space_mode(sr):
    """Enhanced vowel space analysis interface."""
    st.markdown('<p class="sub-header">📊 Vowel Space Analysis</p>', unsafe_allow_html=True)

    vowels = VOWEL_SYSTEMS[st.session_state.language_mode]

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎤 Record a Vowel")
        selected_vowel = st.selectbox("Select vowel:", list(vowels.keys()))

        st.markdown(f"""
        <div class="info-badge">
        <b>Example:</b> {vowels[selected_vowel]['example']}<br>
        <b>IPA Symbol:</b> {vowels[selected_vowel]['ipa']}<br>
        <b>Target F1:</b> ~{vowels[selected_vowel]['target_f1']} Hz |
        <b>Target F2:</b> ~{vowels[selected_vowel]['target_f2']} Hz
        </div>
        """, unsafe_allow_html=True)

        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e74c3c",
            neutral_color="#3498db",
            icon_name="microphone",
            icon_size="3x"
        )

        if audio_bytes:
            st.audio(audio_bytes, format="audio/wav")

            # Store audio data
            ipa = vowels[selected_vowel]['ipa']
            st.session_state.audio_data[ipa] = audio_bytes

            if st.button("🔍 Analyze Formants", type="primary"):
                with st.spinner("Analyzing..."):
                    try:
                        y = save_audio_to_array(audio_bytes, sr=sr)
                        segment = find_stable_vowel_segment(y, sr, segment_duration=0.5)
                        extractor = FormantExtractor(sr=sr)
                        formants = extractor.extract_formants(segment, n_formants=3)
                        f1, f2, f3 = formants

                        if f1 and f2:
                            # Calculate accuracy
                            accuracy, distance = calculate_vowel_accuracy(
                                f1, f2,
                                vowels[selected_vowel]['target_f1'],
                                vowels[selected_vowel]['target_f2']
                            )

                            st.markdown(f"""
                            <div class="success-badge">
                            <b>✅ Formants Detected!</b><br>
                            <b>F1:</b> {f1:.0f} Hz | <b>F2:</b> {f2:.0f} Hz{f' | <b>F3:</b> {f3:.0f} Hz' if f3 else ''}<br>
                            <b>Accuracy:</b> {accuracy:.1f}% (Distance: {distance:.0f} Hz)
                            </div>
                            """, unsafe_allow_html=True)

                            st.session_state.recorded_vowels[ipa] = {
                                'f1': f1, 'f2': f2, 'f3': f3,
                                'accuracy': accuracy,
                                'timestamp': datetime.now().isoformat()
                            }
                            st.session_state.visualizer.add_vowel(ipa, f1, f2, f3)
                        else:
                            st.error("❌ Could not extract formants. Try again.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with col2:
        st.markdown("### 📝 Recorded Vowels")
        if st.session_state.recorded_vowels:
            # Create DataFrame for better display
            data = []
            for vowel, info in st.session_state.recorded_vowels.items():
                data.append({
                    "Vowel": vowel,
                    "F1 (Hz)": f"{info['f1']:.0f}",
                    "F2 (Hz)": f"{info['f2']:.0f}",
                    "F3 (Hz)": f"{info['f3']:.0f}" if info['f3'] else "—",
                    "Accuracy": f"{info.get('accuracy', 0):.1f}%"
                })

            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Audio playback for recordings
            st.markdown("**🔊 Playback:**")
            for vowel in st.session_state.recorded_vowels.keys():
                if vowel in st.session_state.audio_data:
                    with st.expander(f"Play {vowel}"):
                        st.audio(st.session_state.audio_data[vowel])

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📊 Export CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        f"{st.session_state.session_name}.csv",
                        "text/csv"
                    )

            with col_b:
                if st.button("🗑️ Clear All"):
                    st.session_state.recorded_vowels = {}
                    st.session_state.visualizer = VowelSpaceVisualizer()
                    st.session_state.audio_data = {}
                    st.rerun()
        else:
            st.info("No vowels recorded yet. Start recording to see your vowel space!")

    # Vowel space visualization
    if st.session_state.recorded_vowels:
        st.markdown('<p class="sub-header">🗺️ Vowel Space Chart</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col2:
            show_reference = st.checkbox("Show reference vowels", value=True)
            show_grid = st.checkbox("Show grid", value=True)
            chart_size = st.slider("Chart size", 8, 16, 12)

        with col1:
            fig, ax = st.session_state.visualizer.plot_vowel_space(
                show_reference=show_reference,
                figsize=(chart_size, chart_size*0.8)
            )

            if not show_grid:
                ax.grid(False)

            st.pyplot(fig)

            # Download options
            col_a, col_b = st.columns(2)
            with col_a:
                buffer = io.BytesIO()
                fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
                buffer.seek(0)
                st.download_button(
                    "📥 Download PNG",
                    data=buffer,
                    file_name=f"{st.session_state.session_name}_vowel_chart.png",
                    mime="image/png"
                )

            with col_b:
                buffer_pdf = io.BytesIO()
                fig.savefig(buffer_pdf, format='pdf', bbox_inches='tight')
                buffer_pdf.seek(0)
                st.download_button(
                    "📄 Download PDF",
                    data=buffer_pdf,
                    file_name=f"{st.session_state.session_name}_vowel_chart.pdf",
                    mime="application/pdf"
                )

def show_practice_mode(sr):
    """Practice mode with scoring."""
    st.markdown('<p class="sub-header">🎯 Practice Mode</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-badge">
    Practice producing vowels and get real-time feedback on accuracy!
    Try to match the target formant values as closely as possible.
    </div>
    """, unsafe_allow_html=True)

    vowels = VOWEL_SYSTEMS[st.session_state.language_mode]

    selected_vowel = st.selectbox("Select vowel to practice:", list(vowels.keys()))
    ipa = vowels[selected_vowel]['ipa']

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Target")
        target_f1 = vowels[selected_vowel]['target_f1']
        target_f2 = vowels[selected_vowel]['target_f2']

        st.metric("Target F1", f"{target_f1} Hz")
        st.metric("Target F2", f"{target_f2} Hz")
        st.info(f"**Example:** {vowels[selected_vowel]['example']}")

    with col2:
        st.markdown("### 🎤 Your Recording")
        audio_bytes = audio_recorder(
            text="Record your attempt",
            icon_name="microphone"
        )

        if audio_bytes:
            st.audio(audio_bytes)

            if st.button("📊 Check Accuracy", type="primary"):
                with st.spinner("Analyzing..."):
                    try:
                        y = save_audio_to_array(audio_bytes, sr=sr)
                        segment = find_stable_vowel_segment(y, sr)
                        extractor = FormantExtractor(sr=sr)
                        formants = extractor.extract_formants(segment, n_formants=2)
                        f1, f2, _ = formants

                        if f1 and f2:
                            accuracy, distance = calculate_vowel_accuracy(
                                f1, f2, target_f1, target_f2
                            )

                            st.metric("Your F1", f"{f1:.0f} Hz",
                                     delta=f"{f1-target_f1:+.0f} Hz")
                            st.metric("Your F2", f"{f2:.0f} Hz",
                                     delta=f"{f2-target_f2:+.0f} Hz")

                            # Score display
                            if accuracy >= 90:
                                st.success(f"🎉 Excellent! Accuracy: {accuracy:.1f}%")
                            elif accuracy >= 75:
                                st.info(f"👍 Good! Accuracy: {accuracy:.1f}%")
                            elif accuracy >= 60:
                                st.warning(f"🤔 Keep practicing! Accuracy: {accuracy:.1f}%")
                            else:
                                st.error(f"💪 Try again! Accuracy: {accuracy:.1f}%")

                            # Progress bar
                            st.progress(accuracy / 100)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

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
