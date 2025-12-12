"""
Simple PyTorch model for spectral transition smoothing.

This file provides:

 - TransitionModel: a tiny CNN that operates on log-mel spectrogram patches

 - load_checkpoint(path): loads weights if available

 - neural_transition(audio, sr, checkpoint_path=None): applies model, or fallback smoothing if missing
"""

import os
import numpy as np
import soundfile as sf
import librosa

# Try import torch but let code work without it
try:
    import torch
    import torch.nn as nn
    TORCH = True
except Exception:
    TORCH = False


class TransitionModel(nn.Module if TORCH else object):
    def __init__(self, n_mels=128):
        if TORCH:
            super().__init__()
            self.net = nn.Sequential(
                nn.Conv2d(1, 16, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Conv2d(16, 32, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1,1)),
                nn.Flatten(),
                nn.Linear(32, n_mels),
                nn.Tanh()
            )
        else:
            # dummy placeholder
            self.net = None

    def forward(self, x):
        if not TORCH:
            raise RuntimeError("Torch not available")
        return self.net(x)


def load_checkpoint(path):
    """Return a TransitionModel with weights if available. Returns None if not."""
    if not TORCH:
        return None
    if path is None or not os.path.exists(path):
        return None
    model = TransitionModel()
    model.load_state_dict(torch.load(path, map_location='cpu'))
    model.eval()
    return model


def _spectrogram(audio, sr, n_mels=128, hop_length=512):
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels, hop_length=hop_length)
    logS = librosa.power_to_db(S, ref=np.max)
    return logS


def neural_transition(audio, sr, checkpoint_path=None):
    """
    If a checkpoint exists and torch is available, run the tiny model to generate
    a per-frame smoothing mask and apply it to a short region to make transitions smoother.
    Otherwise fallback to deterministic spectral smoothing (Gaussian smoothing).
    Returns audio array and sr.
    """
    # if torch + checkpoint available -> use model
    if TORCH and checkpoint_path and os.path.exists(checkpoint_path):
        model = load_checkpoint(checkpoint_path)
        if model is not None:
            # run model on log-mel spectrogram patches and reconstruct
            S = _spectrogram(audio, sr)
            import torch
            x = torch.from_numpy(S).unsqueeze(0).unsqueeze(0).float()  # [1,1,n_mels,frames]
            with torch.no_grad():
                out = model(x).cpu().numpy().squeeze()  # simplistic
            # Map output to a smoothing curve; here we scale and apply as soft mask:
            mask = np.interp(np.mean(out, axis=0) if out.ndim>1 else out, (out.min(), out.max()), (0.85,1.15))
            # naive apply: multiply overlapping frames on original waveform via STFT
            y_stft = librosa.stft(audio)
            mag, phase = np.abs(y_stft), np.angle(y_stft)
            # resize mask to match frames
            mask_resized = np.interp(np.linspace(0,1,mag.shape[1]), np.linspace(0,1,mask.size), mask)
            mag2 = mag * mask_resized[np.newaxis, :]
            y2 = librosa.istft(mag2 * np.exp(1j*phase))
            return y2, sr
    
    # fallback deterministic smoothing:
    import scipy.ndimage
    # convert to mono if stereo
    if audio.ndim > 1:
        audio = librosa.to_mono(audio)
    # small gaussian smoothing on short windows near high-energy changes
    energy = librosa.feature.rms(y=audio)[0]
    energy_smooth = scipy.ndimage.gaussian_filter1d(energy, sigma=2)
    # identify regions to smooth (where energy changes rapidly)
    diff = np.abs(np.gradient(energy_smooth))
    thresh = np.mean(diff) + np.std(diff)
    frames = np.where(diff > thresh)[0]
    y_out = audio.copy()
    for f in frames:
        # frame -> sample index (approx)
        center = int(f * 512)
        l = max(0, center - 2048)
        r = min(len(y_out), center + 2048)
        y_out[l:r] = scipy.ndimage.gaussian_filter1d(y_out[l:r], sigma=3)
    return y_out, sr

