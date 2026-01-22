# AUDIOFORGE - Vowel Space Analyzer

A web-based tool for acoustic phonetic analysis that visualizes vowel spaces through formant extraction and comparison with native speaker reference data.

## Features

- **Multi-language Support**: Select L1 (native) and L2 (target) languages
- **Real-time Recording**: Browser-based audio recording with visual prompts
- **Dual Temporal Analysis**: Formant extraction at T1 (1/3) and T2 (2/3) vowel duration
- **Interactive Visualization**: Dynamic vowel quadrangle with F1/F2 plotting
- **Comparative Analysis**: Overlay user data with reference vowel spaces
- **Data Export**: CSV export of formant data and research database integration
- **Privacy-First**: Anonymized data collection and storage

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (Web Audio API)
- **Backend**: Python (Flask/FastAPI)
- **Audio Processing**: Praat-Python, librosa, scipy
- **Visualization**: D3.js, Chart.js
- **Database**: SQLite/PostgreSQL
- **Deployment**: Docker, GitHub Actions

## Project Structure

```
audioforge/
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
├── backend/
│   ├── app.py
│   ├── formant_analysis/
│   ├── database/
│   └── utils/
├── data/
│   ├── reference_vowels/
│   └── language_configs/
├── tests/
├── docs/
├── docker/
├── requirements.txt
├── README.md
└── LICENSE
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- Praat (for formant analysis)

### Setup
```bash
# Clone the repository
git clone https://github.com/canayter/audioforge.git
cd audioforge

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit web app
streamlit run streamlit_app.py

# Or use the provided scripts
# Windows:
run_app.bat

# Mac/Linux:
./run_app.sh
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Web Interface (Recommended)

The Streamlit app provides three modes:

1. **Vowel Space Analysis**
   - Record vowels directly in your browser
   - Extract formants (F1, F2, F3) automatically
   - Visualize on an IPA-style vowel chart
   - Compare with reference vowels
   - Download your vowel space chart

2. **Audio Visualization**
   - Record or upload audio files
   - View waveforms, spectrograms, and MFCCs
   - Apply audio processing (trim, normalize, filter)

3. **Feature Extraction**
   - Extract MFCC, spectral features, and ZCR
   - View feature statistics and visualizations

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for detailed instructions.

### Command-Line Interface

For advanced users, run the Python modules directly:

```python
from vowel_space_recorder import VowelRecorder, VowelSpaceVisualizer

recorder = VowelRecorder()
y = recorder.record_audio()
# ... extract formants and visualize
```

## Research Applications

- **Second Language Acquisition**: Compare L2 vowel production to native speakers
- **Dialectal Studies**: Analyze regional vowel variations
- **Speech Therapy**: Track vowel production improvements
- **Cross-linguistic Research**: Compare vowel systems across languages

## Background

This project draws on my background in computational linguistics and phonetics research, applying similar techniques used in my Master's thesis on Turkish vowel spaces to general audio analysis.

## Data Privacy

- All recordings are processed locally and deleted after analysis
- Only anonymized formant data and metadata are stored
- No personally identifiable information is collected
- Research data export follows ethical guidelines

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{audioforge,
  title={AUDIOFORGE: An Interactive Formant Analysis Tool},
  author={Can Ayter},
  year={2025},
  url={https://github.com/canayter/audioforge}
}
```

## Acknowledgments

- Based on established phonetic analysis methodologies
- Reference vowel data from published acoustic studies
- Inspired by Praat and other acoustic analysis tools