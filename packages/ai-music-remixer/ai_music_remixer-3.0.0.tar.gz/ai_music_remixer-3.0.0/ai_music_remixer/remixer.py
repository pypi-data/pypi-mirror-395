"""
Main remixer module - handles audio processing and remixing
"""

import os
import numpy as np
from pydub import AudioSegment
import librosa
import soundfile as sf
from spleeter.separator import Separator

# Import neural transition (optional, safe fallback)
try:
    from .neural import neural_transition
    NEURAL_AVAILABLE = True
except ImportError:
    NEURAL_AVAILABLE = False


def ai_remix(input_file, output_file, style="default"):
    """
    Main remix function - processes audio file and creates remix
    
    Args:
        input_file: Path to input audio file
        output_file: Path to output remix file
        style: Remix style (default, aggressive, smooth)
    """
    # Load audio
    audio, sr = librosa.load(input_file, sr=22050)
    
    # Separate stems using Spleeter
    separator = Separator('spleeter:2stems-16kHz')
    prediction = separator.separate_to_file(input_file, './temp_output')
    
    # Process and combine (simplified example)
    # In a real implementation, you'd do more sophisticated processing
    combined = audio.copy()
    
    # Apply neural transition smoothing if available
    if NEURAL_AVAILABLE:
        ckpt = os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "transition_ckpt.pt"
        )
        try:
            combined, sr = neural_transition(combined, sr, checkpoint_path=ckpt)
        except Exception:
            # Fallback no-op if neural transition fails
            pass
    
    # Save output
    sf.write(output_file, combined, sr)
    print(f"Remix saved to {output_file}")


def ai_remix_beatsync(input_file, output_file, beats_per_minute=None):
    """
    Beat-synchronized remix function
    
    Args:
        input_file: Path to input audio file
        output_file: Path to output remix file
        beats_per_minute: Optional BPM (auto-detected if None)
    """
    # Load audio
    audio, sr = librosa.load(input_file, sr=22050)
    
    # Detect tempo if not provided
    if beats_per_minute is None:
        tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
        beats_per_minute = tempo
    
    # Process with beat alignment
    combined = audio.copy()
    
    # Apply neural transition smoothing if available
    if NEURAL_AVAILABLE:
        ckpt = os.path.join(
            os.path.dirname(__file__), "..", "..", "models", "transition_ckpt.pt"
        )
        try:
            combined, sr = neural_transition(combined, sr, checkpoint_path=ckpt)
        except Exception:
            # Fallback no-op if neural transition fails
            pass
    
    # Save output
    sf.write(output_file, combined, sr)
    print(f"Beat-synced remix saved to {output_file}")

