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
git clone https://github.com/yourusername/audioforge.git
cd vowel-space-analyzer

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Run the application
python backend/app.py
```

## Usage

1. **Language Selection**: Choose your native language (L1) and target language (L2)
2. **Recording Setup**: Complete optional survey about language experience
3. **Voice Recording**: Record prompted words/phrases (max 20 seconds)
4. **Analysis**: System extracts F1/F2 formants using dual temporal analysis
5. **Visualization**: View interactive vowel quadrangle with reference overlay
6. **Export**: Download formant data as CSV

## Research Applications

- **Second Language Acquisition**: Compare L2 vowel production to native speakers
- **Dialectal Studies**: Analyze regional vowel variations
- **Speech Therapy**: Track vowel production improvements
- **Cross-linguistic Research**: Compare vowel systems across languages

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
  author={Your Name},
  year={2025},
  url={https://github.com/canayter/audioforge}
}
```

## Acknowledgments

- Based on established phonetic analysis methodologies
- Reference vowel data from published acoustic studies
- Inspired by Praat and other acoustic analysis tools
