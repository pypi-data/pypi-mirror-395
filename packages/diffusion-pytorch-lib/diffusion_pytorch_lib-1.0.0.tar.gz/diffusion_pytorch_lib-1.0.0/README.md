
# UNet-based Denoising Diffusion Probabilistic Model (DDPM) in PyTorch

A **modular and customizable PyTorch implementation** of a **UNet-based Denoising Diffusion Probabilistic Model** for high-quality image generation.  
Supports multiple beta schedules, flexible loss functions (MSE or L1), attention layers, and residual blocks for advanced denoising performance.

## 🚀 Features

- 🌀 **UNet backbone** for efficient denoising and image synthesis

- 📈 **Multiple beta schedules** (`linear`, `cosine`, etc.) for diffusion process customization

- 🔁 **Residual and attention blocks** for better feature preservation

- ⚙️ **Configurable architecture** via channel multipliers and attention resolution

- 🧮 **Loss function options** — Mean Squared Error (MSE) or L1 loss

- 🧪 Clean and modular code for research and experimentation

- 📦 Production-ready with training and sampling APIs

## 📦 Installation

You can access the [PyPI page](https://pypi.org/project/diffusion-pytorch-lib/) or install the package directly.

```bash
pip install diffusion-pytorch-lib

```

## 📁 Project Structure

```bash
diffusion-pytorch-lib/
├── diffusion_pytorch_lib/
│   ├── __init__.py
│   ├── module.py        # All architecture classes and logic
├── pyproject.toml
├── LICENSE
└── README.md

```

## 🚀 Quick Start

### 1. Import and create the model

```python
import torch
from diffusion-pytorch-lib import UNet, Diffusion

# Define UNet
model = UNet(
    dim=64,
    dim_mults=(1, 2, 4, 8),
    channels=3,
)

# Define diffusion process
diffusion = GaussianDiffusion(
    model,
    image_size=256,
    timesteps=1000,
    beta_schedule="linear",  # or 'cosine'
    loss_type="l2"           # 'l2' (MSE) or 'l1'
)

```

### 2. Training step (sample loop)

```python
optimizer = torch.optim.Adam(diffusion.parameters(), lr=1e-4)

def train_step(x):
    diffusion.train()
    optimizer.zero_grad()
    loss = diffusion(x)  # computes diffusion loss internally
    loss.backward()
    optimizer.step()
    return loss.item()

```

### 3. Sampling new images

```python
diffusion.eval()
with torch.no_grad():
    samples = diffusion.sample(batch_size=8)  # (8, 3, 256, 256)

```

## ⚙️ Configuration Options

### 🧩 U-Net Architecture

| Argument | Type | Default | Description |
|--|--|--|--|
| `dim` | `int` | `64` | Base number of feature channels in the first layer. |
| `dim_mults` | `tuple` | `(1, 2, 4, 8)` | Multipliers for feature map dimensions at each U-Net stage. |
| `channels` | `int` | `3` | Number of input/output image channels (e.g., `3` for RGB). |
| `dropout` | `float` | `0.0` | Dropout rate for regularization. |

### 🌀 Diffusion Process

| Argument | Type | Default | Description |
|--|--|--|--|
| `image_size` | `int` | `256` | Target image resolution |
| `timesteps` | `int` | `1000` | Number of diffusion steps (Higher values improve quality but increase training time). |
| `beta_schedule` | `str` | `"linear"` | Noise schedule type (`"linear"`, `"cosine"`, etc.). |
| `loss_type` | `str` | `"mse"` | Loss type (`"mse"` or `"l1"`) |

## 🙋‍♂️ Author

Developed by [Mehran Bazrafkan](mailto:mhrn.bzrafkn.dev@gmail.com)

> Built from scratch for research into diffusion models, with inspiration from modern generative modeling literature.

## ⭐️ Support & Contribute

If you find this project useful, consider:

- ⭐️ Starring the repo

- 🐛 Submitting issues

- 📦 Suggesting improvements

## 🔗 Related Projects

- [variational-autoencoder-pytorch-lib · PyPI (by me)](https://pypi.org/project/variational-autoencoder-pytorch-lib/)

- [Original DDPM Paper (external)](https://arxiv.org/abs/2006.11239)

## 📜 License

This project is licensed under the terms of the [`MIT LICENSE`](https://github.com/MehranBazrafkan/diffusion-pytorch-lib/blob/main/LICENSE).
