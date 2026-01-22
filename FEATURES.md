# AudioForge - Complete Feature List

## 🎯 Core Features

### 1. **Vowel Space Analysis Mode** 🎤
The flagship feature for acoustic phonetics research.

#### Capabilities:
- **Browser-based voice recording** - No external software needed
- **Formant extraction** - F1, F2, F3 using LPC analysis
- **IPA vowel chart visualization** - Traditional vowel trapezoid layout
- **Multiple language support** - English, Turkish, Spanish vowel systems
- **Reference vowel overlay** - Compare with native speaker data
- **Real-time formant display** - See exact Hz values for each recording

#### Data Display:
- **Interactive table** showing:
  - Vowel symbol (IPA)
  - F1 frequency (Hz)
  - F2 frequency (Hz)
  - F3 frequency (Hz)
  - Accuracy score (%)

#### Export Options:
- **PNG images** - High-resolution (300 DPI) vowel charts
- **PDF documents** - Publication-quality vector graphics
- **CSV data** - Formant values for statistical analysis
- **JSON sessions** - Complete session data with timestamps

---

### 2. **Practice Mode** 🎯
Interactive vowel pronunciation training with real-time feedback.

#### Features:
- **Target vowel display** - Shows ideal F1/F2 values
- **Accuracy scoring** - Compares your production to native speakers
- **Visual feedback** - Color-coded performance indicators:
  - 🎉 Green (90%+): Excellent
  - 👍 Blue (75-89%): Good
  - 🤔 Yellow (60-74%): Keep practicing
  - 💪 Red (<60%): Try again
- **Progress tracking** - Progress bar shows accuracy
- **Delta display** - Shows +/- Hz difference from target
- **Example sentences** - Context for each vowel

---

### 3. **Multi-Language Support** 🌍

**18 Languages with 134+ Vowels!**

#### European Languages:
- **English (American)** - 10 vowels
- **Spanish** - 5 vowels
- **French** - 10 vowels (including front rounded)
- **German** - 10 vowels (including umlauts)
- **Italian** - 7 vowels
- **Portuguese (Brazilian)** - 7 vowels
- **Russian** - 6 vowels
- **Dutch** - 11 vowels
- **Swedish** - 10 vowels
- **Polish** - 6 vowels
- **Greek** - 5 vowels

#### Asian Languages:
- **Turkish** - 8 vowels (vowel harmony system)
- **Arabic (Modern Standard)** - 3 vowels
- **Mandarin Chinese** - 7 vowels
- **Japanese** - 5 vowels
- **Korean** - 8 vowels
- **Hindi** - 7 vowels
- **Vietnamese** - 8 vowels

#### Each vowel includes:
- IPA symbol
- Example word with translation
- Target F1 formant (Hz)
- Target F2 formant (Hz)
- Pronunciation guide

---

### 4. **Session Management** 💾

#### Save Sessions:
- **JSON export** - Complete session data
- **Automatic naming** - Timestamp-based or custom names
- **Includes**:
  - All recorded vowels
  - Formant values (F1, F2, F3)
  - Accuracy scores
  - Timestamps
  - Language setting

#### Load Sessions:
- **Drag-and-drop** JSON file upload
- **Restore all data** - Recordings, visualizations, settings
- **Continue work** - Add more vowels to existing sessions

---

### 5. **Audio Playback** 🔊
Replay your recordings without re-uploading.

#### Features:
- **Expandable player** for each vowel
- **Inline audio controls** - Play, pause, volume
- **Quick reference** - Compare multiple recordings
- **Quality check** - Verify recordings before analysis

---

### 6. **Audio Visualization Mode** 📈

#### Visualizations:
1. **Waveform**
   - Time-domain representation
   - Amplitude over time
   - Identify clipping or silence

2. **Spectrogram**
   - Frequency content over time
   - dB scale coloring
   - Identify formants visually

3. **MFCC (Mel-Frequency Cepstral Coefficients)**
   - Feature representation
   - Common in speech recognition
   - Pattern analysis

#### Audio Processing Options:
- **Trim silence** - Remove quiet sections
- **Normalize** - Equalize volume
- **Noise filtering** - Adjustable threshold
- **Real-time preview** - See effects immediately

---

### 7. **Feature Extraction Mode** 🔬

#### Extracted Features:
1. **MFCC Features**
   - 13 coefficients
   - Mean values across time
   - Bar chart visualization

2. **Spectral Features**
   - **Centroid** - Brightness measure
   - **Bandwidth** - Spectral spread
   - **Rolloff** - High-frequency content

3. **Zero-Crossing Rate**
   - Voice/unvoiced detection
   - Temporal patterns
   - Line chart display

#### Use Cases:
- Speech recognition research
- Voice quality analysis
- Audio classification
- Machine learning feature input

---

### 8. **Enhanced Vowel Charts** 🗺️

#### Customization:
- **Toggle reference vowels** - Show/hide native speaker data
- **Grid display** - Enable/disable gridlines
- **Chart size** - Adjustable from 8-16 inches
- **Traditional IPA orientation**:
  - F1 (vertical) - Inverted (high = close vowels)
  - F2 (horizontal) - Inverted (right = front vowels)

#### Labels:
- **Corner labels**:
  - CLOSE/HIGH (top)
  - OPEN/LOW (bottom)
  - FRONT (right)
  - BACK (left)

---

### 9. **User Interface Enhancements** ✨

#### Styling:
- **Color-coded badges** - Info, success, warning
- **Responsive design** - Works on desktop, tablet
- **Clean layout** - Wide mode for data tables
- **Professional typography** - Clear, readable fonts

#### Help System:
- **Collapsible help section** in sidebar
- **Recording tips**:
  - Quiet environment
  - Consistent mic distance
  - Sustain vowels 1-2 seconds
  - Clear pronunciation
- **Feature overview** - Quick reference guide

#### Navigation:
- **Mode selection** - 4 distinct modes with icons
- **Settings sidebar** - Centralized configuration
- **Download buttons** - Clear call-to-actions

---

### 10. **Data Export Formats** 📊

#### Export Options:

1. **PNG Images**
   - 300 DPI resolution
   - Transparent background option
   - Perfect for presentations

2. **PDF Documents**
   - Vector graphics
   - Scalable quality
   - Publication-ready

3. **CSV Data**
   - Spreadsheet compatible
   - Headers included
   - Easy statistical analysis

4. **JSON Sessions**
   - Complete data structure
   - Machine-readable
   - Session restoration

---

## 🔧 Technical Features

### Performance:
- **Fast formant extraction** - LPC algorithm optimized
- **Efficient audio processing** - NumPy/SciPy backend
- **Responsive UI** - Streamlit caching
- **Small file sizes** - Compressed audio storage

### Compatibility:
- **Python 3.13** compatible
- **Cross-platform** - Windows, Mac, Linux
- **Cloud deployment** - Streamlit Cloud ready
- **Browser support** - Chrome, Firefox, Edge

### Security:
- **Local processing** - No data uploaded to servers
- **Privacy-first** - Recordings processed in-browser
- **Optional saving** - User controls all exports

---

## 📚 Research Applications

### Linguistics Research:
- Vowel space analysis across languages
- L1 vs L2 pronunciation comparison
- Dialectal variation studies
- Phonetic drift tracking

### Language Learning:
- Pronunciation practice
- Target language comparison
- Progress monitoring
- Self-assessment tools

### Speech Therapy:
- Vowel production tracking
- Articulation improvement
- Pre/post therapy comparison
- Objective measurements

### Education:
- IPA symbol learning
- Acoustic phonetics demonstrations
- Interactive linguistics labs
- Student pronunciation assessment

---

## 🎓 Portfolio Highlights

This project demonstrates:

1. **Full-Stack Development**
   - Python backend (librosa, scipy, numpy)
   - Web frontend (Streamlit)
   - Data visualization (matplotlib, pandas)

2. **Signal Processing**
   - LPC formant extraction
   - Audio filtering
   - Spectral analysis
   - Feature extraction

3. **UX/UI Design**
   - Intuitive interface
   - Multiple modes
   - Export options
   - Help documentation

4. **Domain Expertise**
   - Computational linguistics
   - Phonetics research
   - Language analysis
   - Educational technology

5. **Software Engineering**
   - Modular architecture
   - Session management
   - Error handling
   - Cross-platform deployment

---

## 🚀 Future Enhancements (Roadmap)

- [ ] Real-time formant tracking during recording
- [ ] Diphthong trajectory analysis
- [ ] Pitch contour visualization
- [ ] Database backend for research data
- [ ] Multi-user study mode
- [ ] API for programmatic access
- [ ] Mobile app version
- [ ] Integration with Praat
- [ ] Batch audio processing
- [ ] Advanced statistical analysis

---

## 📖 Documentation

See also:
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - User guide
- [README.md](README.md) - Project overview
- [LICENSE](LICENSE) - MIT License

---

**Built with ❤️ for phonetics research and language learning**

*AudioForge - Where audio meets linguistics*
