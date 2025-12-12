# Minimal trainer — requires PyTorch and some training data (pairs of "ugly" -> "smooth" spectrogram targets).
import torch
from torch import nn, optim
from .transition_model import TransitionModel, load_checkpoint
from .utils import synth_demo_audio, save_checkpoint
import numpy as np


def make_dummy_dataset(n=200):
    X, Y = [], []
    for _ in range(n):
        y, sr = synth_demo_audio()
        # create noisy / shifted versions as dummy "input"
        x = y + 0.01*np.random.randn(*y.shape)
        # target is slightly smoothed tone
        t = np.convolve(y, np.ones(5)/5, mode='same')
        X.append(x)
        Y.append(t)
    return X, Y


def train(epochs=10, lr=1e-3):
    model = TransitionModel()
    if not torch:
        raise RuntimeError("Torch required to train")
    model = model.to('cpu')
    opt = optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    X, Y = make_dummy_dataset()
    for e in range(epochs):
        total_loss = 0.0
        for x, y in zip(X, Y):
            # convert to log-mel or simplified features for toy training
            x_t = torch.from_numpy(np.abs(np.fft.rfft(x, n=2048))[:128]).unsqueeze(0).unsqueeze(0).float()
            y_t = torch.from_numpy(np.abs(np.fft.rfft(y, n=2048))[:128]).float()
            pred = model(x_t)
            loss = loss_fn(pred.squeeze(), y_t)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total_loss += loss.item()
        print(f"Epoch {e+1}/{epochs} loss {total_loss/len(X):.6f}")
    save_checkpoint(model, "models/transition_ckpt.pt")


if __name__ == "__main__":
    train(epochs=3)

