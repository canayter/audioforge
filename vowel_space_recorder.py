import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy import signal
from scipy.linalg import solve_toeplitz
import sounddevice as sd
import time
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class FormantExtractor:
    """Extract formant frequencies from audio signals using LPC analysis."""

    def __init__(self, sr=22050):
        self.sr = sr

    def extract_formants(self, y, n_formants=3, lpc_order=12):
        """
        Extract formant frequencies using Linear Predictive Coding (LPC).

        Parameters:
        -----------
        y : array
            Audio signal
        n_formants : int
            Number of formants to extract (default: 3)
        lpc_order : int
            Order of LPC analysis (default: 12, typically 2 + number of formants * 2)

        Returns:
        --------
        formants : list
            List of formant frequencies in Hz
        """
        # Pre-emphasis to boost higher frequencies
        pre_emphasis = 0.97
        y_emphasized = np.append(y[0], y[1:] - pre_emphasis * y[:-1])

        # Compute LPC coefficients
        lpc_coeffs = self._lpc(y_emphasized, lpc_order)

        # Find roots of the LPC polynomial
        roots = np.roots(lpc_coeffs)

        # Keep only roots inside the unit circle
        roots = roots[np.abs(roots) < 1]

        # Get angles of the roots
        angles = np.arctan2(roots.imag, roots.real)

        # Convert to frequencies
        freqs = angles * (self.sr / (2 * np.pi))

        # Keep only positive frequencies
        freqs = freqs[freqs > 0]

        # Sort by frequency
        freqs = np.sort(freqs)

        # Return the first n_formants
        formants = freqs[:n_formants].tolist()

        # Pad with None if not enough formants found
        while len(formants) < n_formants:
            formants.append(None)

        return formants

    def _lpc(self, y, order):
        """
        Compute Linear Predictive Coding coefficients.

        Parameters:
        -----------
        y : array
            Input signal
        order : int
            LPC order

        Returns:
        --------
        a : array
            LPC coefficients
        """
        # Compute autocorrelation
        r = np.correlate(y, y, mode='full')
        r = r[len(r)//2:]

        # Solve Yule-Walker equations
        R = r[:order]
        r_rest = r[1:order+1]

        try:
            a = solve_toeplitz(R, r_rest)
            return np.concatenate([[1], -a])
        except:
            # If solution fails, return identity
            return np.concatenate([[1], np.zeros(order)])


class VowelRecorder:
    """Record vowel sounds and extract formants."""

    def __init__(self, sr=22050, duration=1.5):
        self.sr = sr
        self.duration = duration
        self.formant_extractor = FormantExtractor(sr=sr)

    def record_audio(self, prompt="Recording..."):
        """
        Record audio from the microphone.

        Parameters:
        -----------
        prompt : str
            Message to display during recording

        Returns:
        --------
        y : array
            Recorded audio signal
        """
        print(f"\n{prompt}")
        print(f"Recording for {self.duration} seconds...")
        print("3...")
        time.sleep(1)
        print("2...")
        time.sleep(1)
        print("1...")
        time.sleep(1)
        print("GO! (say the vowel now)")

        # Record audio
        recording = sd.rec(int(self.duration * self.sr),
                          samplerate=self.sr,
                          channels=1,
                          dtype='float32')
        sd.wait()

        print("Recording complete!")

        # Convert to 1D array
        y = recording.flatten()

        return y

    def find_stable_vowel_segment(self, y, segment_duration=0.3):
        """
        Find the most stable segment of the recording (likely the vowel).

        Parameters:
        -----------
        y : array
            Audio signal
        segment_duration : float
            Duration of segment to extract in seconds

        Returns:
        --------
        segment : array
            Most stable audio segment
        """
        segment_samples = int(segment_duration * self.sr)

        # Compute energy in windows
        hop_length = segment_samples // 4
        energies = []

        for i in range(0, len(y) - segment_samples, hop_length):
            segment = y[i:i+segment_samples]
            energy = np.sum(segment ** 2)
            energies.append((i, energy))

        # Find segment with highest energy (likely the vowel)
        if energies:
            best_idx, _ = max(energies, key=lambda x: x[1])
            return y[best_idx:best_idx+segment_samples]
        else:
            # Fallback to middle segment
            mid = len(y) // 2
            return y[mid-segment_samples//2:mid+segment_samples//2]


class VowelSpaceVisualizer:
    """Visualize vowel formants on an IPA-style vowel chart."""

    def __init__(self):
        # Reference formant values for standard vowels (approximate, based on adult male)
        # Format: vowel: (F1, F2, IPA_symbol, position_description)
        self.reference_vowels = {
            'i': (240, 2400, 'i', 'close front'),      # as in "beat"
            'ɪ': (400, 2000, 'ɪ', 'near-close front'), # as in "bit"
            'e': (450, 2300, 'e', 'close-mid front'),  # as in "bait"
            'ɛ': (550, 1800, 'ɛ', 'open-mid front'),   # as in "bet"
            'æ': (700, 1700, 'æ', 'near-open front'),  # as in "bat"
            'ɑ': (750, 1100, 'ɑ', 'open back'),        # as in "father"
            'ɔ': (600, 900, 'ɔ', 'open-mid back'),     # as in "caught"
            'o': (450, 800, 'o', 'close-mid back'),    # as in "boat"
            'ʊ': (400, 1000, 'ʊ', 'near-close back'),  # as in "book"
            'u': (250, 700, 'u', 'close back'),        # as in "boot"
            'ʌ': (650, 1200, 'ʌ', 'open-mid central'), # as in "but"
            'ə': (500, 1500, 'ə', 'mid central'),      # as in "about"
        }

        self.recorded_vowels = []

    def add_vowel(self, label, f1, f2, f3=None):
        """
        Add a recorded vowel to the collection.

        Parameters:
        -----------
        label : str
            Label for the vowel (e.g., "my /i/")
        f1, f2, f3 : float
            Formant frequencies in Hz
        """
        self.recorded_vowels.append({
            'label': label,
            'F1': f1,
            'F2': f2,
            'F3': f3
        })

    def plot_vowel_space(self, show_reference=True, figsize=(12, 10)):
        """
        Plot the vowel space with recorded vowels and optional reference vowels.

        Parameters:
        -----------
        show_reference : bool
            Whether to show reference vowel positions
        figsize : tuple
            Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Plot reference vowels if requested
        if show_reference:
            ref_f1 = [v[0] for v in self.reference_vowels.values()]
            ref_f2 = [v[1] for v in self.reference_vowels.values()]
            ref_labels = [v[2] for v in self.reference_vowels.values()]

            ax.scatter(ref_f2, ref_f1, c='lightgray', s=200, alpha=0.5,
                      marker='o', label='Reference vowels', zorder=1)

            for f1, f2, label in zip(ref_f1, ref_f2, ref_labels):
                ax.annotate(label, (f2, f1), fontsize=12, ha='center',
                           va='center', color='gray', weight='bold')

        # Plot recorded vowels
        if self.recorded_vowels:
            rec_f1 = [v['F1'] for v in self.recorded_vowels]
            rec_f2 = [v['F2'] for v in self.recorded_vowels]
            rec_labels = [v['label'] for v in self.recorded_vowels]

            ax.scatter(rec_f2, rec_f1, c='red', s=300, alpha=0.8,
                      marker='*', label='Your vowels', zorder=2,
                      edgecolors='darkred', linewidth=2)

            for f1, f2, label in zip(rec_f1, rec_f2, rec_labels):
                ax.annotate(label, (f2, f1), fontsize=10, ha='right',
                           va='bottom', color='darkred', weight='bold',
                           xytext=(5, 5), textcoords='offset points')

        # Invert axes (traditional vowel space orientation)
        ax.invert_xaxis()
        ax.invert_yaxis()

        # Labels and formatting
        ax.set_xlabel('F2 (Hz)', fontsize=14, weight='bold')
        ax.set_ylabel('F1 (Hz)', fontsize=14, weight='bold')
        ax.set_title('Vowel Space (IPA Chart Style)', fontsize=16, weight='bold')

        # Add descriptive labels for the dimensions
        ax.text(0.02, 0.98, 'CLOSE/HIGH', transform=ax.transAxes,
               fontsize=10, va='top', ha='left', style='italic', color='blue')
        ax.text(0.02, 0.02, 'OPEN/LOW', transform=ax.transAxes,
               fontsize=10, va='bottom', ha='left', style='italic', color='blue')
        ax.text(0.98, 0.98, 'FRONT', transform=ax.transAxes,
               fontsize=10, va='top', ha='right', style='italic', color='blue')
        ax.text(0.02, 0.98, 'BACK', transform=ax.transAxes,
               fontsize=10, va='top', ha='left', style='italic', color='blue',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        # Grid
        ax.grid(True, alpha=0.3, linestyle='--')

        # Legend
        if show_reference or self.recorded_vowels:
            ax.legend(loc='upper left', fontsize=12)

        plt.tight_layout()

        return fig, ax


def main():
    """Main application for recording vowels and creating vowel space."""

    print("=" * 60)
    print("VOWEL SPACE RECORDER")
    print("=" * 60)
    print("\nThis application will record you saying different vowels")
    print("and plot them on an IPA-style vowel chart.")
    print("\nTips for best results:")
    print("  - Use a quiet environment")
    print("  - Speak clearly and sustain the vowel sound")
    print("  - Keep the same volume for all vowels")
    print("  - Position yourself the same distance from the mic")
    print("\n" + "=" * 60)

    # Setup
    recorder = VowelRecorder(sr=22050, duration=2.0)
    visualizer = VowelSpaceVisualizer()

    # Define vowels to record
    vowels_to_record = [
        ("ee", "as in 'bEEt' or 'sEE'", "/i/"),
        ("ih", "as in 'bIt' or 'sIt'", "/ɪ/"),
        ("eh", "as in 'bEt' or 'sEt'", "/ɛ/"),
        ("aa", "as in 'fAther' or 'pAlm'", "/ɑ/"),
        ("aw", "as in 'bOUght' or 'cAUght'", "/ɔ/"),
        ("oo", "as in 'bOOt' or 'fOOd'", "/u/"),
        ("uh", "as in 'bUt' or 'cUp'", "/ʌ/"),
    ]

    print("\nYou will record the following vowels:")
    for i, (name, example, ipa) in enumerate(vowels_to_record, 1):
        print(f"  {i}. {ipa} - {example}")

    input("\nPress Enter when ready to start recording...")

    # Record each vowel
    for name, example, ipa in vowels_to_record:
        print(f"\n{'=' * 60}")
        print(f"Recording vowel: {ipa}")
        print(f"Example: {example}")
        print(f"{'=' * 60}")

        # Record
        y = recorder.record_audio(f"Get ready to say {ipa}")

        # Find stable segment
        segment = recorder.find_stable_vowel_segment(y, segment_duration=0.5)

        # Extract formants
        formants = recorder.formant_extractor.extract_formants(segment, n_formants=3)
        f1, f2, f3 = formants

        if f1 and f2:
            print(f"\nFormants detected:")
            print(f"  F1: {f1:.0f} Hz")
            print(f"  F2: {f2:.0f} Hz")
            if f3:
                print(f"  F3: {f3:.0f} Hz")

            # Add to visualizer
            visualizer.add_vowel(ipa, f1, f2, f3)
        else:
            print(f"\nWarning: Could not extract formants for {ipa}")

        # Ask if user wants to re-record
        if input("\nRe-record this vowel? (y/n): ").lower() == 'y':
            print("Let's try again...")
            # Repeat this iteration
            y = recorder.record_audio(f"Get ready to say {ipa}")
            segment = recorder.find_stable_vowel_segment(y, segment_duration=0.5)
            formants = recorder.formant_extractor.extract_formants(segment, n_formants=3)
            f1, f2, f3 = formants

            if f1 and f2:
                print(f"\nFormants detected:")
                print(f"  F1: {f1:.0f} Hz")
                print(f"  F2: {f2:.0f} Hz")
                if f3:
                    print(f"  F3: {f3:.0f} Hz")

                # Remove previous attempt and add new one
                visualizer.recorded_vowels = [v for v in visualizer.recorded_vowels if v['label'] != ipa]
                visualizer.add_vowel(ipa, f1, f2, f3)

    # Plot results
    print("\n" + "=" * 60)
    print("Recording complete! Generating vowel space chart...")
    print("=" * 60)

    visualizer.plot_vowel_space(show_reference=True)
    plt.show()

    print("\nThank you for using Vowel Space Recorder!")
    print("Your vowel positions have been plotted against reference IPA vowels.")


if __name__ == "__main__":
    main()
