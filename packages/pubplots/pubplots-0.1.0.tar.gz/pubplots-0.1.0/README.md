# pubplots

Utilities for creating publication-ready matplotlib figures.

This package provides tools for scaling figures and setting rcParams so that figures have journal-friendly fonts, font sizes, and DPI, and are imported correctly by different vector graphics editors (Figma, Adobe, Affinity, Inkscape, etc.).

## Installation

```bash
pip install pubplots
```

Or with uv:

```bash
uv add pubplots
```

## Usage

```python
import matplotlib.pyplot as plt
import pubplots as pp

# Use the context manager to set up publication-ready rcParams
with pp.destination("figma"):
    fig, ax = plt.subplots(figsize=pp.scale(3, 2))  # 3" x 2" figure
    ax.plot([0, 1, 2], [0, 1, 4])
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    fig.savefig("my_figure.svg")
```

The `scale()` function automatically uses the appropriate scaling factor for the current context. You can also scale multiple values:

```python
with pp.destination("figma"):
    width, height, margin = pp.scale(3, 2, 0.5)
```

For non-Figma destinations (Adobe Illustrator, Affinity Designer, Inkscape), use any other string (e.g. `"default"`):

```python
with pp.destination("default"):
    fig, ax = plt.subplots(figsize=pp.scale(3, 2))
    # No special scaling applied
```

### Using Styles

You can apply matplotlib styles using the `style` parameter. Styles can be specified in any format that `plt.style.use()` accepts:

- A style name from `plt.style.available` (e.g., `"ggplot"`, `"seaborn-v0_8"`)
- A `Path` to a `.mplstyle` file
- A dictionary of rcParams
- A list of any of the above (styles are composed left-to-right, just like `plt.style.use()`)

```python
# Use a built-in style
with pp.destination("figma", style="ggplot"):
    fig, ax = plt.subplots(figsize=pp.scale(3, 2))
    ax.plot([0, 1, 2], [0, 1, 4])
    fig.savefig("ggplot_figure.svg")

# Use a custom style file
from pathlib import Path
with pp.destination("figma", style=Path("my_custom_style.mplstyle")):
    fig, ax = plt.subplots(figsize=pp.scale(3, 2))
    ax.plot([0, 1, 2], [0, 1, 4])
    fig.savefig("custom_figure.svg")

# Compose multiple styles (applied left-to-right)
with pp.destination("figma", style=["ggplot", {"lines.linewidth": 2.0}]):
    fig, ax = plt.subplots(figsize=pp.scale(3, 2))
    ax.plot([0, 1, 2], [0, 1, 4])
    fig.savefig("composed_figure.svg")
```

### Style Scaling

By default, when using `destination("figma")`, certain rcParams (line widths, marker sizes, padding, etc.) are automatically scaled along with the figure size to preserve the visual appearance. If you want to disable this behavior and only scale the figure size and font sizes, set `style_scaling=False`:

```python
# Disable automatic scaling of style parameters
with pp.destination("figma", style="ggplot", style_scaling=False):
    fig, ax = plt.subplots(figsize=pp.scale(3, 2))
    # Only figure size and font sizes are scaled; line widths, marker sizes,
    # tick sizes, etc. retain their original values from the style.
    ax.plot([0, 1, 2], [0, 1, 4])
    fig.savefig("no_style_scaling.svg")
```

## Font Configuration

The rcParams ensure that **text is output as text** (not as paths), which allows you to edit text directly in your vector graphics editor. This requires **Arial** to be installed on your system.

If matplotlib is not finding the font even after installing Arial, try clearing the matplotlib cache directory:

```python
import matplotlib as mpl
print(mpl.get_cachedir())
```

Then remove the cache:

```bash
rm -rf ~/.cache/matplotlib
```

The default font and other parameters can be made configurable upon request.

## Figma-Specific Scaling

Figma uses non-standard scaling that requires special handling when importing SVG figures.

### Text Scaling

- 1 pt = 1/72 inch virtually everywhere except for Figma, where 1pt = 1 CSS pixel = 1/96 inch.
- Figma attempts to correct for this by scaling up text by 96/72, so an SVG with 5pt font will import with 6.66pt font in Figma.
- The only way to specify a frame size in Figma is in pixels (pts), so if you want an 8.5×11" figure at 300ppi, you make a frame that is 8.5×300 × 11×300 pixels (which is 2550 × 3300 pixels).
- Thus, assuming a 300ppi frame, font which should print at 5pt needs to appear in Figma as 5 × (300 / 72) = 20.833pt, but you must account for Figma's (96/72) scaling, so the font must be specified in the SVG as 5 × (72/96) × (300/72) = 300/96 = 15.625pt.

### Figure Size

- When you write an SVG using matplotlib, the figure size is specified in pts (savefig.dpi has no bearing on the SVG created—it is ignored), using the convention that 1pt = 1/72 inch. So if you request a 2"×2" figure, it will be saved as 144pt × 144pt.
- As with text, Figma will scale up these pts by 96/72, so your SVG will get imported as 192×192 pixels. If you are using a 300dpi frame, this means your figure will actually be 192/300 = 0.64" wide instead of 2" wide.
- Therefore, to get a figure that is actually 2" wide at 300dpi, you need to ask matplotlib to create a figure that is 2 × (300/96) = 6.25" wide, which will be saved as 450pt wide, and then imported into Figma as 600 pixels wide, which is 600/300 = 2" wide.

This package handles all of this scaling automatically when you use `pubplots.destination("figma")`.
