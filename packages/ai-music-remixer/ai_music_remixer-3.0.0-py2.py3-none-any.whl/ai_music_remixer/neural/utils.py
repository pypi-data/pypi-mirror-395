"""
Utilities: save_checkpoint, synth_demo_audio
"""

import os
import numpy as np
try:
    import torch
except Exception:
    torch = None


def save_checkpoint(model, path):
    if torch is None:
        raise RuntimeError("Torch not installed")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path)


def synth_demo_audio(duration_sec=4, sr=22050):
    t = np.linspace(0, duration_sec, int(sr*duration_sec))
    tone = 0.2 * np.sin(2*np.pi*220*t)  # simple sine tone
    return tone, sr

