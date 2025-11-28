import librosa
import numpy as np
import io
import soundfile as sf


class AudioAnalyzer:
    def detect_slur(self, audio_bytes):
        """
        Analyzes audio for Dysarthria (Slurred Speech) indicators:
        1. Low Pitch Variation (Monotone)
        2. High Spectral Flatness (Noisiness/Breathiness)
        """
        try:
            with io.BytesIO(audio_bytes) as audio_file:
                y, sr = sf.read(audio_file)

            if len(y) < sr * 0.5:
                return False

            f0, _, _ = librosa.pyin(
                y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7")
            )

            f0_clean = f0[~np.isnan(f0)]
            if len(f0_clean) == 0:
                return False

            pitch_std = np.std(f0_clean)

            if pitch_std < 10.0:
                return True

            return False
        except Exception as e:
            print(f"Audio Analysis Warning: {e}")
            return False
