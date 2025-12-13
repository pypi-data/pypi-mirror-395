import torch
import matplotlib.pyplot as plt
from typing import Optional
from .extractor import extract_shapes, LayerInfo
from .visualization import draw_block, draw_arrow, GAP, CENTER_Y

def plot_architecture(
    model: torch.nn.Module, 
    input_shape: tuple[int, int, int] = (3, 227, 227),
    batch_size: int = 1,
    save_path: str = "architecture.png", 
    skip_layers: Optional[list[str]] = None
):
    """
    Generates and saves a visual diagram of the PyTorch model architecture.

    Args:
        model: The PyTorch nn.Module to visualize.
        input_shape: The (C, H, W) shape of the input tensor.
        batch_size: The batch size to use for the forward pass.
        save_path: The filename to save the resulting plot to.
        skip_layers: A list of layer names (strings) to exclude from the plot (e.g., ['ReLU']).
    """
    skip_layers = skip_layers or ["ReLU"]

    input_tensor = torch.randn(batch_size, *input_shape)
    layers: list[LayerInfo] = extract_shapes(model, input_tensor)

    plottable_layers = [l for l in layers if l[0] not in skip_layers]
    
    fig, ax = plt.subplots(figsize=(len(plottable_layers) * 1.5, 7))
    ax.axis("off")
    ax.set_title(f"{model.__class__.__name__} Architecture", fontsize=12, pad=10)

    x = 0
    input_shape_full = (batch_size, *input_shape)
    draw_block(ax, x, input_shape_full, "Input")
    x += draw_block(ax, x, input_shape_full, "Input")[0] + GAP
    
    for i, (layer_name, in_shape, out_shape) in enumerate(layers):
        if layer_name in skip_layers: 
            continue 

        width, height = draw_block(ax, x, in_shape, layer_name)

        if i < len(layers) - 1:
            draw_arrow(
                ax,
                x + width,
                CENTER_Y,
                x + width + GAP,
                CENTER_Y
            )

        x += width + GAP

    ax.set_xlim(0, x + 3)
    ax.set_ylim(0, CENTER_Y * 2)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Architecture diagram saved to: {save_path}")