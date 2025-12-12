"""Utilities for creating publication-ready matplotlib figures.

This module provides tools for scaling figures and setting rcParams so that
figures have journal-friendly fonts, font sizes, and DPI, and are imported
correctly by different vector graphics editors (Figma, Adobe, Affinity, etc.).
"""

import contextlib
import importlib.resources
from contextvars import ContextVar
from pathlib import Path

import matplotlib as mpl
import matplotlib.style.core as _msc
from matplotlib import _api, _rc_params_in_file, rcParamsDefault

# Module-level context variable for scaling factor
_scaling_ctx: ContextVar[float] = ContextVar("scaling", default=1.0)


def scale(
    *values: int | float | tuple[int | float, ...], scaling_factor: float | None = None
) -> int | float | tuple[int | float, ...]:
    """Scale input value(s) according to the current context, or by `scaling_factor`.

    Preserves the input type: scalar returns scalar, tuple returns tuple.
    Also accepts multiple positional arguments.

    Parameters
    ----------
    *values : int, float, or tuple of int/float
        A single number, tuple of numbers, or multiple numbers to scale.
    scaling_factor : float, optional
        The scaling factor to apply. If None, reads from the current context.
        Defaults to 1.0 if no context is set.

    Returns
    -------
    int, float, or tuple of int/float
        Scaled value(s) in the same type as input.
    """
    if scaling_factor is None:
        scaling_factor = _scaling_ctx.get()

    if len(values) == 1:
        values = values[0]
        if isinstance(values, tuple):
            return tuple(v * scaling_factor for v in values)
        else:
            return values * scaling_factor
    else:
        return tuple(v * scaling_factor for v in values)


def _get_scalable_rc_params_keys() -> dict[str, float]:
    """Get the rcParams keys that should be scaled in order to preserve figure
    appearance when the figsize is scaled.

    Returns
    -------
    list of str
        A list of rcParams keys that should be scaled.
    """
    scalable_params = {
        "axes.labelpad": 4.0,
        "axes.linewidth": 0.8,
        "axes.titlepad": 6.0,
        "boxplot.boxprops.linewidth": 1.0,
        "boxplot.capprops.linewidth": 1.0,
        "boxplot.flierprops.linewidth": 1.0,
        "boxplot.flierprops.markeredgewidth": 1.0,
        "boxplot.flierprops.markersize": 6.0,
        "boxplot.meanprops.linewidth": 1.0,
        "boxplot.meanprops.markersize": 6.0,
        "boxplot.medianprops.linewidth": 1.0,
        "boxplot.whiskerprops.linewidth": 1.0,
        "boxplot.whiskers": 1.5,
        "figure.constrained_layout.h_pad": 0.04167,
        "figure.constrained_layout.hspace": 0.02,
        "figure.constrained_layout.w_pad": 0.04167,
        "figure.constrained_layout.wspace": 0.02,
        "grid.linewidth": 0.8,
        "hatch.linewidth": 1.0,
        "lines.linewidth": 1.5,
        "lines.markeredgewidth": 1.0,
        "lines.markersize": 6.0,
        "patch.linewidth": 1.0,
        "xtick.major.pad": 3.5,
        "xtick.major.size": 3.5,
        "xtick.major.width": 0.8,
        "xtick.minor.pad": 3.4,
        "xtick.minor.size": 2.0,
        "xtick.minor.width": 0.6,
        "ytick.major.pad": 3.5,
        "ytick.major.size": 3.5,
        "ytick.major.width": 0.8,
        "ytick.minor.pad": 3.4,
        "ytick.minor.size": 2.0,
        "ytick.minor.width": 0.6,
    }  # Default values shown for convenience.
    return list(scalable_params.keys())


def get_rc_params(destination: str) -> tuple[dict, callable]:
    """Get matplotlib rcParams and a scaling factor for publication-ready figures.

    Returns rcParams so that figures have journal-friendly fonts, font sizes, and
    DPI, and are imported correctly by different vector graphics editors.

    Parameters
    ----------
    destination : str
        The vector graphics application into which the figure will be imported.
        "figma" requires special scaling. Anything else ("adobe", "affinity",
        "inkscape") does not.

    Returns
    -------
    rc_params : dict
        A dictionary of rcParams to set for matplotlib.
    scaler : callable
        A function that scales input values according to the selected destination,
        regardless of context.

    Notes
    -----
    **Figma-specific scaling factor explanation**

    *Text scaling:*

    - 1 pt = 1/72 inch virtually everywhere except for Figma,
      where 1pt = 1 CSS pixel = 1/96 inch.
    - Figma attempts to correct for this by scaling up text by 96/72, so an
      SVG with 5pt font will import with 6.66pt font in Figma.
    - The only way to specify a frame size in Figma is in pixels (pts), so if
      you want an 8.5x11" figure at 300ppi, you make a frame that is
      8.5*300 x 11*300 pixels (which is 2550 x 3300 pixels).
    - Thus, assuming a 300ppi frame, font which should print at 5pt needs to
      appear in Figma as 5 * (300 / 72) = 20.833pt, but you must account for
      Figma's (96/72) scaling, so the font must be specified in the SVG as
      5 * (72/96) * (300/72) = 300/96 = 15.625pt.

    *Figure size:*

    - When you write an SVG using matplotlib, the figure size is specified in pts
      (savefig.dpi has no bearing on the SVG created. It is ignored.), using the
      convention that 1pt = 1/72 inch. So if you request a 2"x2" figure, it will
      be saved as 144pt x 144pt.
    - As with text, Figma will scale up these pts by 96/72, so your SVG will get
      imported as 192x192 pixels. If you are using a 300dpi frame, this means
      your figure will actually be 192/300 = 0.64" wide instead of 2" wide.
    - Therefore, to get a figure that is actually 2" wide at 300dpi, you need to
      ask matplotlib to create a figure that is 2 * (300/96) = 6.25" wide, which
      will be saved as 450pt wide, and then imported into Figma as 600 pixels
      wide, which is 600/300 = 2" wide.
    """
    if destination == "figma":
        scaling = 300 / 96
    else:
        scaling = 1.0

    rc_params = {
        "font.family": "sans-serif",  # Essential
        "font.sans-serif": ["Arial"],  # Essential
        "font.size": 6 * scaling,
        "axes.titlesize": 6 * scaling,
        "axes.labelsize": 6 * scaling,
        "xtick.labelsize": 5 * scaling,
        "ytick.labelsize": 5 * scaling,
        "legend.fontsize": 6 * scaling,
        "figure.titlesize": 7 * scaling,
        "figure.labelsize": 7 * scaling,
        "figure.dpi": 150 / scaling,  # Controls display size in notebooks
        "figure.autolayout": True,  # Pre-emptively apply tight_layout
        "savefig.dpi": 300,
        "savefig.format": "svg",
        "svg.fonttype": "none",  # Essential
        "pdf.fonttype": 42,
    }

    def _scale(
        *values: int | float | tuple[int | float, ...],
    ) -> int | float | tuple[int | float, ...]:
        return scale(*values, scaling_factor=scaling)

    return rc_params, _scale


def resolve_styles(style: str | dict | Path | list | None) -> dict:
    """Resolve style(s) into a single rcParams dictionary.
    Based on `matplotlib.pyplot.style.use()`.

    Parameters
    ----------
    style : str, dict, Path, list, or None
        A style specification. See `matplotlib.pyplot.style.use()` for details.
        If None, return the current style.

    Returns
    -------
    dict
        A dictionary of rcParams resulting from applying the specified styles.
    """
    # Deprecation warnings were already handled when creating
    # rcParamsDefault, no need to reemit them here.
    with _api.suppress_matplotlib_deprecation_warning():
        # don't trigger RcParams.__getitem__('backend')
        filtered = {
            k: mpl.rcParams[k] for k in mpl.rcParams if k not in _msc.STYLE_BLACKLIST
        }

    if style is None:
        return filtered

    if isinstance(style, (str, Path)) or hasattr(style, "keys"):
        # If name is a single str, Path or dict, make it a single element list.
        styles = [style]
    else:
        styles = style

    style_alias = {"mpl20": "default", "mpl15": "classic"}

    for style in styles:
        if isinstance(style, str):
            style = style_alias.get(style, style)
            if style == "default":
                # Deprecation warnings were already handled when creating
                # rcParamsDefault, no need to reemit them here.
                with _api.suppress_matplotlib_deprecation_warning():
                    # don't trigger RcParams.__getitem__('backend')
                    style = {
                        k: rcParamsDefault[k]
                        for k in rcParamsDefault
                        if k not in _msc.STYLE_BLACKLIST
                    }
            elif style in mpl.style.library:
                style = mpl.style.library[style]
            elif "." in style:
                pkg, _, name = style.rpartition(".")
                try:
                    path = (
                        importlib.resources.files(pkg)
                        / f"{name}.{_msc.STYLE_EXTENSION}"
                    )
                    style = _rc_params_in_file(path)
                except (ModuleNotFoundError, OSError, TypeError):
                    # There is an ambiguity whether a dotted name refers to a
                    # package.style_name or to a dotted file path.  Currently,
                    # we silently try the first form and then the second one;
                    # in the future, we may consider forcing file paths to
                    # either use Path objects or be prepended with "./" and use
                    # the slash as marker for file paths.
                    pass
        if isinstance(style, (str, Path)):
            try:
                style = _rc_params_in_file(style)
            except OSError as err:
                raise OSError(
                    f"{style!r} is not a valid package style, path of style "
                    f"file, URL of style file, or library style name (library "
                    f"styles are listed in `style.available`)"
                ) from err
        for k in style:  # don't trigger RcParams.__getitem__('backend')
            if k in _msc.STYLE_BLACKLIST:
                _api.warn_external(
                    f"Style includes a parameter, {k!r}, that is not "
                    f"related to style.  Ignoring this parameter."
                )
            else:
                filtered[k] = style[k]
    return filtered


@contextlib.contextmanager
def destination(
    destination: str = "default",
    style: str | dict | Path | list | None = None,
    style_scaling: bool = True,
):
    """Context manager for publication-ready matplotlib figures.

    Sets matplotlib rcParams so that figures have journal-friendly fonts, font
    sizes, DPI, etc., and are imported correctly by different vector graphics
    editors ("destinations"). Also sets an appropriate figure (or text) size
    scaling factor. Within this context, `scale()` will automatically use the
    appropriate scaling factor without needing to pass it explicitly.

    Parameters
    ----------
    destination : str, optional
        The vector graphics application into which the figure will be imported.
        "figma" applies special scaling (300/96). Anything else ("adobe",
        "affinity", "inkscape") does not. Default is "default".
    style : str, dict, Path, list, or None, optional
        Matplotlib style(s), as one would pass to `plt.style.use()`, to apply before
        destination-specific params. The destination-specific scaling factor will be
        applied to these styles, if applicable (see `_get_scalable_rc_params_keys()`),
        unless `style_scaling` is set to False.
        If `style` is None (default), uses the current rcParams.

    Yields
    ------
    None

    See Also
    --------
    get_rc_params : Get the rcParams dictionary and scaler function directly.
    scale : Scale values according to the current context.
    resolve_styles : Resolve style(s) into a single rcParams dictionary.

    Examples
    --------
    >>> with destination("figma"):
    ...     fig, ax = plt.subplots(figsize=scale(2, 2))
    ...     # scale() automatically uses figma scaling (300/96)
    ...     # Current rcParams are also scaled, where appropriate.

    >>> with destination("figma", style="ggplot"):
    ...     fig, ax = plt.subplots(figsize=scale(2, 2))
    ...     # scale() automatically uses figma scaling (300/96)
    ...     # 'ggplot' style is applied and rcParams are scaled, where appropriate.

    >>> with destination("figma", style_scaling=False):
    ...     fig, ax = plt.subplots(figsize=scale(2, 2))
    ...     # scale() automatically uses figma scaling (300/96)
    ...     # Does NOT apply scaling to most current rcParams, only to
    ...     # destination-specific rcParams.

    """
    rc_params = resolve_styles(style)
    dest_params, scaler = get_rc_params(destination)
    rc_params.update(dest_params)

    if style_scaling:
        scalable_keys = _get_scalable_rc_params_keys()
        assert not set(scalable_keys) & set(dest_params.keys()), (
            "scalable_keys and dest_params.keys() overlap; this may cause double scaling."
        )
        rc_params = {
            k: (scaler(v) if k in scalable_keys else v) for k, v in rc_params.items()
        }

    token = _scaling_ctx.set(scaler(1.0))
    try:
        with mpl.rc_context(rc_params):
            yield
    finally:
        _scaling_ctx.reset(token)
