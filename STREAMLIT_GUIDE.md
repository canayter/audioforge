# AudioForge Streamlit App Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the App

```bash
streamlit run streamlit_app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## Features

### 🎤 Vowel Space Analysis
- **Record vowels** directly in your browser
- **Extract formants** (F1, F2, F3) using LPC analysis
- **Visualize** your vowel space on an IPA-style chart
- **Compare** with reference vowels
- **Download** your vowel space chart

### 📈 Audio Visualization
- **Record or upload** audio files
- **View waveforms** in time domain
- **Analyze spectrograms** in frequency domain
- **Examine MFCC** features
- **Process audio** with trimming, normalization, and filtering

### 🔬 Feature Extraction
- Extract **MFCC** coefficients
- Calculate **spectral features** (centroid, bandwidth, rolloff)
- Analyze **zero-crossing rate**
- View feature statistics and visualizations

## Using Voice Recording

### Browser Permissions
When you first click the microphone icon, your browser will ask for microphone permission. Click "Allow" to enable recording.

### Supported Browsers
- Chrome/Edge (recommended)
- Firefox
- Safari (may have limited support)

### Recording Tips
1. **Quiet environment** - Minimize background noise
2. **Consistent distance** - Stay the same distance from the mic
3. **Sustained vowels** - Hold the vowel sound steadily for 1-2 seconds
4. **Clear articulation** - Pronounce vowels clearly

## Vowel Recording Guide

### IPA Vowels Included
- **/i/** - as in "bEEt" (high front)
- **/ɪ/** - as in "bIt" (near-high front)
- **/ɛ/** - as in "bEt" (mid front)
- **/æ/** - as in "bAt" (low front)
- **/ɑ/** - as in "fAther" (low back)
- **/ɔ/** - as in "cAUght" (mid back)
- **/u/** - as in "bOOt" (high back)
- **/ʌ/** - as in "bUt" (mid central)

## Troubleshooting

### Microphone Not Working
1. Check browser permissions in settings
2. Ensure no other app is using the microphone
3. Try refreshing the page
4. Use Chrome/Edge for best compatibility

### Formant Extraction Fails
- Record longer (2-3 seconds)
- Speak louder and clearer
- Reduce background noise
- Try the upload option instead

### App Won't Start
```bash
# Upgrade streamlit
pip install --upgrade streamlit

# Check Python version (3.8+ required)
python --version
```

## Advanced Options

### Custom Sample Rate
Adjust in the sidebar:
- 16000 Hz - Lower quality, faster processing
- 22050 Hz - Default, good balance
- 44100 Hz - High quality, slower processing

### Audio Processing
- **Trim Silence** - Remove quiet sections
- **Normalize** - Equalize volume levels
- **Filter Noise** - Remove low-amplitude noise

## Deployment

### Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repository
4. App will be live at `yourapp.streamlit.app`

### Local Network Access
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```
Access from other devices: `http://YOUR_IP:8501`

## Research Applications

- **Phonetics Research** - Analyze vowel production
- **Language Learning** - Compare L1 and L2 vowels
- **Speech Therapy** - Track pronunciation improvements
- **Dialectology** - Study regional variations
- **Acoustic Analysis** - Extract and visualize audio features

## Support

For issues or questions:
- GitHub Issues: [https://github.com/canayter/audioforge/issues](https://github.com/canayter/audioforge/issues)
- Documentation: See README.md

## Citation

If you use this tool in research, please cite:

```bibtex
@software{audioforge,
  title={AUDIOFORGE: An Interactive Formant Analysis Tool},
  author={Can Ayter},
  year={2025},
  url={https://github.com/canayter/audioforge}
}
```
