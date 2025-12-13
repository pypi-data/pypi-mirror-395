import torch
import torch.nn as nn
from typing import List, Tuple, Any

LayerInfo = Tuple[str, Tuple[int, ...], Tuple[int, ...]]

def extract_shapes(model: nn.Module,
                   input_tensor: torch.Tensor) -> List[LayerInfo]:
    """
    Performs a forward pass on the model and records the input and output shapes
    for each non-sequential layer.
    """
    layers: List[LayerInfo] = []
    x = input_tensor

    for layer in model.modules():
        if layer == model or isinstance(layer, nn.Sequential):
            continue

        prev_shape = tuple(x.shape)

        try:
            x = layer(x)
        except Exception:
            try:
                if isinstance(layer, nn.Linear) and len(prev_shape) > 2:
                    prev_shape_flattened = tuple(torch.flatten(x, 1).shape)
                    x = torch.flatten(x, 1)
                    x = layer(x)
                    prev_shape = prev_shape_flattened
                else:
                    continue 

            except Exception as e:
                print(f"Warning: Could not pass tensor through {layer.__class__.__name__}. Error: {e}")
                continue

        new_shape = tuple(x.shape)
        layers.append((layer.__class__.__name__, prev_shape, new_shape))

    return layers