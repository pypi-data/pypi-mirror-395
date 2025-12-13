import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon

BLOCK_COLORS = {
    "Conv2d": "#4e79a7",
    "Linear": "#59a14f",
    "MaxPool2d": "#f28e2b",
    "ReLU": "#bab0ac"
}
GAP = 3
CENTER_Y = 10


def draw_block_3d(ax, x: float, y: float, width: float, height: float, depth: float = 0.8, color: str = "#4e79a7"):
    """
    Draws a 3D block representation on the matplotlib Axes.
    Returns: The total width and height of the drawn 3D block.
    """
    dx = depth
    dy = depth

    front = Rectangle((x, y), width, height,
                      edgecolor="black", facecolor=color, linewidth=1.0)
    ax.add_patch(front)

    top = Polygon([
        (x, y + height),
        (x + dx, y + height + dy),
        (x + width + dx, y + height + dy),
        (x + width, y + height)
    ], closed=True, facecolor=color, edgecolor="black", alpha=0.9)
    ax.add_patch(top)

    side = Polygon([
        (x + width, y),
        (x + width + dx, y + dy),
        (x + width + dx, y + height + dy),
        (x + width, y + height)
    ], closed=True, facecolor=color, edgecolor="black", alpha=0.7)
    ax.add_patch(side)

    return width + dx, height + dy


def draw_arrow(ax, x1: float, y1: float, x2: float, y2: float):
    """
    Draws a connecting arrow between two points.
    """
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle="->", mutation_scale=12, linewidth=1)
    ax.add_patch(arr)


def draw_block(ax, x: float, shape: tuple, layer_name: str) -> tuple[float, float]:
    """
    Calculates block size based on input shape and draws the block with its label.
    Size heuristic: width ~ channels, height ~ log(spatial dimensions).
    Returns: The effective width and height of the block (including 3D depth).
    """
    c, h, w = 1, 1, 1
    if len(shape) >= 2:
        if len(shape) == 4:
            _, c, h, w = shape
        elif len(shape) == 3:
            c, h, w = shape
        elif len(shape) == 2:
            h = shape[1]
            c = 1
        else:
            h = shape[0]
            c = 1

    width = min(max(1.5, c / 32),15)
    height = min(max(1.0, math.log(h + 1) * 2),15)

    y = CENTER_Y - height / 2

    color = BLOCK_COLORS.get(layer_name, "#cccccc")
    effective_width, effective_height = draw_block_3d(
        ax, x, y, width, height, color=color
    )

    ax.text(x + (width) / 2, y - 3,
            layer_name,
            ha="center", va="center", fontsize=9)

    shape_str = f"({', '.join(map(str, shape[1:]))})" if len(shape) > 1 else f"({shape[0]})"
    ax.text(x + (width*1.4) / 2, y + height + 2,
            shape_str,
            ha="center", va="center", fontsize=6, color="#666666")

    return effective_width, effective_height