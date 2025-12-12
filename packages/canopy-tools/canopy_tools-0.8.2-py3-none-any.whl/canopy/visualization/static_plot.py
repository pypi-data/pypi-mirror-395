import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
from tqdm import tqdm
from typing import Optional, List
import canopy as cp
from canopy.visualization.plot_functions import get_color_palette, make_dark_mode, handle_figure_output, select_sites

def make_static_plot(field_a: cp.Field, field_b: cp.Field, kind: Optional[str] = 'scatter', 
                     output_file: Optional[str] = None, layers: Optional[List[str] | str] = None,
                     field_a_label: Optional[str] = None, field_b_label: Optional[str] = None,
                     unit_a: Optional[str] = None, unit_b: Optional[str] = None,
                     sites: Optional[bool | List[tuple]] = False,
                     scatter_size: Optional[float] = 6, scatter_alpha: Optional[float] = 0.5,
                     title: Optional[str] = None, palette: Optional[str] = None,
                     custom_palette: Optional[str] = None, move_legend: Optional[bool] = False, 
                     dark_mode: Optional[bool] = False, transparent: Optional[bool] = False, 
                     x_fig: Optional[float] = 10, y_fig: Optional[float] = 10, 
                     return_fig: Optional[bool] = False, **kwargs) -> Optional[plt.Figure]:
    """
    This function generates a scatter plot with regression lines and r-scores from two input fields 
    (which can be reduced spatially, temporally or both).

    Parameters
    ----------
    field_a, field_b : cp.Field
        Input data Field to display.
    kind : str, optional
        Kind of plot to draw. Default is 'scatter', which uses `seaborn.regplot` (supports multiple layers).
        Other options ('kde', 'hist', 'hex') use `seaborn.jointplot` (supports only one layer).
    output_file : str, optional
        File path for saving the plot.
    layers : List[str] or str, optional
        Layers to plot from the input data.
    field_a_label, field_b_label : str, optional
        Labels for the data series, if not provided canopy will try to retrieve the name of the variable in the metadata.
    unit_a, unit_b : str, optional
        Units for the data series, if not provided canopy will try to retrieve the unit of the variable in the metadata.
    sites : bool or List[Tuple], optional
        Control site-level plotting instead of spatial reduction. Default is False. True = all sites,
        if provided with a list, only select the sites in the list.
    scatter_size : float, optional
        Marker size for scatter points. Default is 6.
    scatter_alpha : float, optional
        Transparency (alpha) for scatter points. Default is 0.1.
    title : str, optional
        Title of the plot.
    palette : str, optional
        Seaborn color palette to use for the line colors (https://seaborn.pydata.org/tutorial/color_palettes.html, 
        recommended palette are in https://colorbrewer2.org).
    custom_palette : str, optional
        Path of custom color palette .txt file to use. Names should match label names.
    move_legend : bool, optional
        Location of the legend ('in' or 'out'). Default is False.
    dark_mode : bool, optional
        Whether to apply dark mode styling to the plot.
    transparent : bool, optional
        If True, makes the background of the figure transparent.
    x_fig : float, optional
        Width of the figure in inches. Default is 10.
    y_fig : float, optional
        Height of the figure in inches. Default is 10.
    return_fig : bool, optional
        If True, returns the figure object that can be usuable by multiple_figs().
        Default is False.
    **kwargs
        Additional keyword arguments are passed directly to `seaborn.regplot` (if `kind='scatter'`)
        or `seaborn.jointplot` (if `kind` is other). This allows customization of plot features.
    """
    # Check for some initial conditions
    if layers and sites:
        raise ValueError("layers and sites argument cannot be used simultanuously. Only one layer for multiple sites.")

    # Force variables to be a list
    if isinstance(layers, str):
        layers = [layers]
    if not isinstance(sites, bool) and not isinstance(sites, list):
        sites = [sites]

    # Retrieve metadata
    field_a_label = field_a_label or field_a.metadata['name']
    field_b_label = field_b_label or field_b.metadata['name']
    unit_a = field_a.metadata['units'] if unit_a is None else unit_a
    unit_b = field_b.metadata['units'] if unit_b is None else unit_b
    layers = layers or field_a.layers

    df_a = cp.make_lines(field_a)
    df_b = cp.make_lines(field_b)

    if sites: # If sites, flatten data
        df_a = select_sites(df_a, sites)
        df_b = select_sites(df_b, sites)
        layers = df_a.columns
    
    # Determine if we should use jointplot based on kind parameter
    use_jointplot = (kind != 'scatter')
    
    # Check jointplot constraint after layers are determined (including after sites processing)
    if use_jointplot and len(layers) > 1:
        raise ValueError(f"{kind} currently supports only one layer at a time.")

    # Prepare axis labels (used by both paths)
    xlabel = f"{field_a_label} (in {unit_a})" if unit_a != "[no units]" else field_a_label
    ylabel = f"{field_b_label} (in {unit_b})" if unit_b != "[no units]" else field_b_label

    # Colour palette
    colors, _ = get_color_palette(len(layers), palette=palette, custom_palette=custom_palette)

    # Use jointplot - only supports single layer
    if use_jointplot:
        layer = layers[0]
        x1d, y1d = to_aligned_1d(df_a[layer], df_b[layer])
        if len(x1d) < 2 or x1d.nunique() <= 1 or y1d.nunique() <= 1:
            raise ValueError(f"Insufficient valid data for correlation in layer {layer}")
        r_value = float(np.corrcoef(x1d.values, y1d.values)[0, 1])

        plot_kwargs = {
            "data": pd.DataFrame({field_a_label: x1d, field_b_label: y1d}),
            "x": field_a_label,
            "y": field_b_label,
            "color": colors[0],
            "kind": kind,
            "height": y_fig,
            "ratio": 5,
            "space": 0.2,
        }

        plot_kwargs.update(kwargs)

        g = sns.jointplot(**plot_kwargs)
        ax, fig = g.ax_joint, g.fig
        
        # Hide marginal distributions by default
        g.ax_marg_x.set_visible(False)
        g.ax_marg_y.set_visible(False)

        # Add discrete colorbar with classes
        if kind in ['hex', 'hist']:
            collection = g.ax_joint.collections[0]
            bins = np.linspace(collection.norm.vmin, collection.norm.vmax, 6, dtype=int)
            cbar = fig.colorbar(collection, ax=ax, shrink=0.5, boundaries=bins, ticks=bins)
            cbar.set_label('Count density', fontsize=12, labelpad=5)
        
        plot_title = f"{title} (R={r_value:.2f})" if title else f"R={r_value:.2f}"
    # Use regplot - supports multiple layers
    else:
        fig, ax = plt.subplots(figsize=(x_fig, y_fig))

        for i, layer in enumerate(tqdm(layers, desc="Plotting layers")):
            x1d, y1d = to_aligned_1d(df_a[layer], df_b[layer])
            if len(x1d) < 2 or x1d.nunique() <= 1 or y1d.nunique() <= 1:
                print(f"Skipping {layer}: insufficient valid data for correlation")
                continue
            r_value = float(np.corrcoef(x1d.values, y1d.values)[0, 1])

            plot_kwargs = {
                "x": x1d, "y": y1d, "color": colors[i],
                "label": f"{layer} (R={r_value:.2f})",
                "scatter_kws": {'s': scatter_size, 'alpha': scatter_alpha},
                "ax": ax
            }
            plot_kwargs.update(kwargs)
            sns.regplot(**plot_kwargs)
        
        # Calculate axis limits from all layers
        min_val = min(df_a[layers].min().min(), df_b[layers].min().min())
        max_val = max(df_a[layers].max().max(), df_b[layers].max().max())
        plot_title = title

        # Make legend
        leg = ax.legend(loc='best')
        if move_legend:
            sns.move_legend(ax, "center left", bbox_to_anchor=(1, 0.85))
            leg = ax.get_legend()
        if leg is not None:
            for handle in leg.legend_handles:
                if hasattr(handle, 'set_alpha'):
                    handle.set_alpha(1.0)

    # Common formatting (applied to both paths)
    if use_jointplot:
        min_val, max_val = min(x1d.min(), y1d.min()), max(x1d.max(), y1d.max())
    ax.set_xlim([min_val, max_val])
    ax.set_ylim([min_val, max_val])
    ax.plot([min_val, max_val], [min_val, max_val], color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_title(plot_title, fontsize=18)

    # Apply dark mode if requested
    if dark_mode:
        fig, ax = make_dark_mode(fig, ax)

    return handle_figure_output(fig, output_file=output_file, return_fig=return_fig, transparent=transparent)

def to_aligned_1d(x_obj, y_obj):
    """Return pairwise-valid, aligned 1D Series for x and y (handles Series/DataFrame)."""
    xs = x_obj.stack(future_stack=True) if isinstance(x_obj, pd.DataFrame) else x_obj
    ys = y_obj.stack(future_stack=True) if isinstance(y_obj, pd.DataFrame) else y_obj
    xs, ys = xs.align(ys, join='inner')

    if isinstance(xs, pd.DataFrame):
        xs = xs.stack(future_stack=True)
    if isinstance(ys, pd.DataFrame):
        ys = ys.stack(future_stack=True)

    valid = xs.notna() & ys.notna()

    if isinstance(valid, pd.DataFrame):
        valid = valid.to_numpy().ravel()
        xs = pd.Series(xs.to_numpy().ravel())
        ys = pd.Series(ys.to_numpy().ravel())
        
    return xs[valid], ys[valid]
