## PyTorch Architecture Plotter

This is a professional, modular utility for visualizing the architecture of a PyTorch `nn.Module`. It generates a clear, longitudinal diagram where the size and color of each block (representing a layer) are scaled according to its input shape (channels and spatial dimensions).

The package is designed for clarity, reusability, and professional integration into any PyTorch project.

### Features

  * **Modular Design:** Code is separated into `visualization`, `arch_extractor`, and `plotter` modules.
  * **Dynamic Shape Extraction:** Performs a real forward pass to accurately determine input and output shapes for every layer, correctly handling transitions like **Flattening** before Linear layers.
  * **3D Visualization:** Layers are rendered as **3D cuboids** for enhanced visual appeal and depth perception.

  * **Scaling Heuristic:** Block width is scaled by the **number of channels** and height is scaled logarithmically by the **spatial dimensions** ($H \times W$), providing an intuitive representation of feature map changes.
  * **Configurable:** Easily skip layers like `ReLU` to declutter the diagram.


### Installation

To use this utility, you should have PyTorch and Matplotlib installed.

1.  Clone or download the `arch_plotter` directory.

2.  Install the package in editable mode from the root directory:

    ```bash
    pip install -e .
    ```

###  Usage Example

You can import the main function and use it on any standard PyTorch `nn.Module`.

```python
import torch.nn as nn
from torchvisualizer import plot_architecture

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
        )
        self.classifier = nn.Sequential(
            nn.Linear(32 * 8 * 8, 10), # Assuming 32x32 input
        )

    def forward(self, x):
        x = self.features(x)
        x = x.flatten(1)
        x = self.classifier(x)
        return x

# Instantiate the model
model = SimpleCNN()

# Generate and save the diagram
plot_architecture(
    model=model,
    input_shape=(3, 32, 32),            # (C, H, W) of the input image
    save_path="simple_cnn_diagram.png",
    skip_layers=["ReLU"]                # Skip ReLU for a cleaner look
)
# Output:  Architecture diagram saved to: simple_cnn_diagram.png
```

### 🔧 API Reference

#### `plot_architecture(model, input_shape, batch_size=1, save_path="architecture.png", skip_layers=None)`

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `model` | `torch.nn.Module` | - | **The PyTorch model** to visualize. |
| `input_shape` | `tuple` | `(3, 227, 227)` | The expected **(C, H, W)** dimensions of the input tensor. |
| `batch_size` | `int` | `1` | Batch size to use for the dummy forward pass. |
| `save_path` | `str` | `"architecture.png"` | The filename for the output image. |
| `skip_layers` | `list[str]` | `["ReLU"]` | List of layer class names to exclude from the plot. |


### 🛠️ Development & Customization

The core visualization logic is found in:

  * **`arch_plotter/visualization.py`**: Modify drawing style, color schemes, and size scaling heuristics here.
  * **`arch_plotter/arch_extractor.py`**: Customize how shapes are extracted, especially for complex or custom layer types.