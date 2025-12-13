import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Rectangle
from scipy.stats import t as t_distribution
import cartopy.feature as feature
import cartopy.crs as ccrs
import seaborn as sns
import jenkspy
from typing import Optional, List
from pathlib import Path
import canopy as cp
from canopy.visualization.projections import projections
from canopy.visualization.plot_functions import handle_figure_output, save_figure_png, get_color_palette, make_dark_mode
import warnings

def make_simple_map(field: cp.Field, layer: str,  categorical: Optional[bool] = False, 
                    output_file: Optional[str] = None, timeop: Optional[str] = 'av',
                    cb_label: Optional[str] = None, title: Optional[str] = None, unit: Optional[str] = None,
                    n_classes: Optional[int] = 4, classification: List[float] | str = "linear", palette: Optional[str] = None,
                    custom_palette: Optional[str] = None, orientation: Optional[str] = 'horizontal', 
                    extend: Optional[str] = "neither", proj: Optional[str] = "Robinson",
                    force_zero: Optional[bool] = False, dark_mode: Optional[bool] = False, 
                    transparent: Optional[bool] =  False, stats_annotation: Optional[bool] = False, 
                    x_fig: Optional[float] = 10, y_fig: Optional[float] = 10, return_fig: Optional[bool] = False) -> Optional[plt.Figure]:
    """
    Create a map from a given Field object (apply time reduction) and save it to a file.

    Parameters
    ----------
    field : cp.Field
        Field object.
    layer : str
        Layer name to display.
    categorical : bool, optional
        Set to True for categorical data mapping. Default False.
    output_file : str, optional
        File path for saving the plot.
    timeop : str, optional
        The reduction operation. Either 'sum' or 'av'. Default is 'av'.
    cb_label : str, optional
        Label of the colour bar, if not provided canopy will try to 
        retrieve the name of the variable in the metadata.
    unit : str, optional
        Unit of the variable, if not provided canopy will try to retrieve 
        the unit of the variable in the metadata.
    title : str, optional
        Title of the map.
    n_classes : int, optional
        Number of discrete color classes to use. Default is 4.
    classification : List[float] | str, optional
        Method to classify the data into different classes. 
        One of 'linear', 'quantile', 'jenks', 'std'
        (https://gisgeography.com/choropleth-maps-data-classification/) 
        or a list, e.g. [0,2,4,8]. 
        Default is 'linear'.
    palette : str, optional
        Seaborn color palette to use for the line colors 
        (https://seaborn.pydata.org/tutorial/color_palettes.html, 
        recommended palette are in https://colorbrewer2.org).
    custom_palette : str, optional
        Path of custom color palette .txt file to use.
    orientation: str, optional
        Orientation of the legend. Either 'horizontal' or 'vertical'. 
        Default is 'horizontal'.
    extend : str, optional
        Extend colourbar to maximum and minimum value. One of 'neither', 
        'min', 'max' or 'both'. Default is 'neither'.
    proj : str, optional
        Cartopy projection to use for the map 
        (https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html).
        Default is 'Robinson'.
    force_zero : bool, optional
        If True, force the first (or the closest in diff_map) bin to zero. 
        Default is False.
    dark_mode : bool, optional
        If True, apply dark mode styling. Default is False.
    transparent: bool, optional
        If True, make the figure transparent. Default is False.
    stats_annotation : bool, optional
        If True, adds a text box annotation on the bottom-left of the map
        displaying the mean and standard deviation of the raster values
        over the entire domain. Default is False.
    x_fig : float, optional
        Width of the figure in inches. Default is 10.
    y_fig : float, optional
        Height of the figure in inches. Default is 10.
    return_fig : bool, optional
        If True, returns the figure object that can be usuable by multiple_figs().
        Default is False.
    """
    # Retrieve metadata
    cb_label, unit = get_metadata(field, cb_label, unit)

    # If classification is provided as a list, update n_classes to match its length minus one
    if isinstance(classification, list) and len(classification)-1 != n_classes:
        n_classes = len(classification) - 1

    # Data processing pipeline (if an error can be raised because a time average field 
    # or a raster is being used, continue with those)
    if categorical:
        raster = safe_make_raster(field, layer)
        n_classes = len(raster.labels)
        bins = np.arange(n_classes)
        labels = raster.labels
    else:
        field_red = safe_red_time(field, timeop)
        raster = safe_make_raster(field_red, layer)
        bins = calculate_bins(raster.vmap, n_classes, classification, force_zero)
        labels = False

    fig = plot_map(raster.xx, raster.yy, raster.vmap, labels, output_file,
                   cb_label, title, unit, n_classes, bins, palette, custom_palette, 
                   orientation, extend, proj, dark_mode, transparent, 
                   stats_annotation, x_fig, y_fig, nonsig_mask=None, hist=not categorical)
    
    return handle_figure_output(fig, output_file=output_file, return_fig=return_fig, transparent=transparent)

def make_diff_map(field_a: cp.Field, field_b: cp.Field, layer: str, output_file: Optional[str] = None, timeop: Optional[str] = 'av',
                  cb_label: Optional[str] = None, title: Optional[str] = None, unit: Optional[str] = None,
                  n_classes: Optional[int] = 4, classification: List[float] | str = "linear", palette: Optional[str] = None,
                  custom_palette: Optional[str] = None, orientation: Optional[str] = 'horizontal', extend: Optional[str] = "neither", 
                  proj: Optional[str] = "Robinson", force_zero: Optional[bool] = False, dark_mode: Optional[bool] = False, 
                  transparent: Optional[bool] =  False, stats_annotation: Optional[bool] = False, x_fig: Optional[float] = 10, 
                  y_fig: Optional[float] = 10, return_fig: Optional[bool] = False, 
                  percentage: Optional[bool] = False, nonsig: Optional[bool] = False) -> Optional[plt.Figure]:
    """
    Create a difference map from two fields

    Parameters
    ----------
    field_a, field_b : cp.Field
        First and second Field objects for computing the difference.
    percentage : bool, optional
        If True, compute proportional difference in %. Default is False.
    nonsig : bool, optional
        If True, overlay hatched areas to indicate regions where 
        differences between the two fields are not statistically 
        significant (p-value >= 0.05). These are areas where the 
        observed differences could be explained by interannual 
        variability rather than representing a true difference 
        between the two climate runs. Default is False.
    """
    # Retrieve metadata
    cb_label, unit = get_metadata(field_a, cb_label, unit)

    # If classification is provided as a list, update n_classes to match its length minus one
    if isinstance(classification, list) and len(classification)-1 != n_classes:
        n_classes = len(classification) - 1

    # Apply space reduction to both fields
    field_a_red = safe_red_time(field_a, timeop)
    field_b_red = safe_red_time(field_b, timeop)
    raster_a = safe_make_raster(field_a_red, layer)
    raster_b = safe_make_raster(field_b_red, layer)

    # Compute the difference
    if percentage:
        with np.errstate(divide='ignore', invalid='ignore'):
            diff = np.where(raster_a.vmap != 0, (raster_b.vmap - raster_a.vmap) / raster_a.vmap * 100, 0)
    else:
        diff = raster_b.vmap - raster_a.vmap

    # Compute hatched areas
    nonsig_mask = None
    if nonsig:
        nonsig_mask = calculate_significance_mask(field_a, field_b, layer, raster_a)

    # Calculate bins for the difference map
    bins = calculate_bins(np.abs(diff), n_classes, classification, force_zero, diff_map=True)

    # Plot the map
    fig = plot_map(raster_a.xx, raster_a.yy, diff, False, output_file, cb_label, title, unit,
                   n_classes, bins, palette, custom_palette, orientation, extend, proj, 
                   dark_mode, transparent, stats_annotation, x_fig, y_fig, nonsig_mask, hist=True)
    
    return handle_figure_output(fig, output_file=output_file, return_fig=return_fig, transparent=transparent)

def get_metadata(field, cb_label, unit):
    """
    Safely retrieve metadata (name and units) from a Field or Raster object.
    Returns (cb_label, unit), using provided values if metadata is not available.
    """
    try:
        if not cb_label and getattr(field, 'metadata', None) and field.metadata['name'] != "[no name]":
            cb_label = field.metadata['name']
        if hasattr(field, 'metadata'):
            unit = unit or field.metadata['units']
    except AttributeError as e:
        if "'Raster' object has no attribute 'metadata'" in str(e):
            print("can't retrieve metadata from raster")
            cb_label, unit = "Unknown"
        else:
            raise
    return cb_label, unit

def safe_red_time(field, timeop):
    """
    Safely apply red_time to a Field, or return the object if not available (e.g., Raster).
    Handles AttributeError and ValueError for unsupported frequency.
    """
    try:
        return field.red_time(timeop, inplace=False)
    except AttributeError as e:
        if "'Raster' object has no attribute 'red_time'" in str(e):
            return field
        else:
            raise
    except ValueError as e:
        if str(e) == "Data must have yearly or monthly frequency.":
            return field
        else:
            raise

def safe_make_raster(field, layer):
    """
    Safely create a raster from a Field or return the object if it is already a Raster.
    Handles AttributeError if the object has no 'data' attribute (i.e., is already a Raster).
    """
    try:
        return cp.make_raster(field, layer)
    except AttributeError as e:
        if "'Raster' object has no attribute 'data'" in str(e):
            return field
        raise

def calculate_bins(raster, n_classes, classification, force_zero=False, diff_map=False):
    """
    Calculate bin edges based on the maximum value and desired scales.
    """
    def center_zero(bins): # take the closest bin to zero and force it to be zero
        bins = np.array(bins)
        bins[np.argmin(np.abs(bins))] = 0
        return bins

    max_val = np.nanmax(raster)
    min_val = np.nanmin(raster)

    if max_val == 0:
        raise ValueError("Maximum value is 0, raster likely empty.")
    if diff_map and n_classes % 2 != 0:
        raise ValueError("with diff_map, n_classes should be an even number.")

    if isinstance(classification, list):
        bin_edges = np.array(classification)

    elif classification == "linear":
        # Linear classification
        scale = 10 ** np.floor(np.log10(max_val))  # Find the largest power of 10 less than or equal to max_value
        bin_max = scale * np.ceil(max_val / scale)  # Round up to the nearest multiple of scale
        if bin_max - max_val > scale / 2:
            bin_max -= scale / 2  # Adjust by subtracting half the scale
        
        bin_edges = np.linspace(min_val, bin_max, n_classes + 1)

    elif classification == "quantile":
        bin_edges = np.nanpercentile(raster, np.linspace(0, 100, n_classes + 1))
        # Ensure strictly increasing bin edges by nudging duplicates
        bin_edges = bin_edges.astype(float)
        data_range = max_val - min_val
        # Choose an epsilon relative to data range; fall back to a tiny constant if range is 0
        eps = 1e-12 if data_range == 0 or not np.isfinite(data_range) else max(1e-12, 1e-9 * data_range)
        adjusted = False
        for i in range(1, len(bin_edges)):
            if not np.isfinite(bin_edges[i-1]):
                continue
            if not np.isfinite(bin_edges[i]) or bin_edges[i] <= bin_edges[i-1]:
                bin_edges[i] = bin_edges[i-1] + eps
                adjusted = True
        if adjusted:
            warnings.warn(
                "Edges were adjusted slightly to ensure monotonicity.", UserWarning
            )

    elif classification == "jenks":
        flat = raster[np.isfinite(raster)].flatten()
        bin_edges = jenkspy.jenks_breaks(flat, n_classes)

    elif classification == "std":
        mean = np.nanmean(raster)
        std = np.nanstd(raster)
        if n_classes % 2 != 0:
            raise ValueError("n_classes should be even for 'std' classification.")
        half = n_classes // 2
        bin_edges = [mean + i * std for i in range(-half, half + 1)]

    else:
        raise ValueError("Invalid classification. Use 'linear', 'quantile', 'jenks', 'std', or a list.")

    if diff_map and force_zero:
        bin_edges = center_zero(bin_edges)
    if force_zero:
        bin_edges[0] = 0

    return np.array(bin_edges)

def calculate_significance_mask(field_a, field_b, layer, raster_a):
        """
        Compute a mask indicating areas where differences between two fields 
        are not statistically significant (p-value >= 0.05).
        """
        # Extract and align time series
        df_a = field_a.data[layer].unstack(level='time')
        df_b = field_b.data[layer].unstack(level='time')
        df_a_aligned, df_b_aligned = df_a.align(df_b, join='inner')
        
        # Calculate statistics
        mean_a, mean_b = df_a_aligned.mean(axis=1), df_b_aligned.mean(axis=1)
        var_a, var_b = df_a_aligned.var(axis=1, ddof=1), df_b_aligned.var(axis=1, ddof=1)
        
        # Calculate t-statistics and p-values
        s_p = np.sqrt((var_a + var_b)/2)
        t_stat = (mean_a - mean_b) / s_p
        p_values = 2 * (1 - t_distribution.cdf(np.abs(t_stat), df=2*len(cp.make_lines(field_a).index)-2))
        
        # Convert to grid format
        p_grid = pd.Series(p_values, index=mean_a.index).reset_index().pivot(index='lat', columns='lon', values=0).reindex(
            index=raster_a.yy[:, 0], columns=raster_a.xx[0, :]).values
        
        # Create significance mask (p < 0.05 is significant, mask shows non-significant areas)
        return p_grid >= 0.05

def plot_map(xx, yy, raster, labels, output_file, cb_label, title, unit,
             n_classes, bins, palette, custom_palette, orientation, extend, 
             proj, dark_mode, transparent, stats_annotation, x_fig, y_fig, nonsig_mask, hist):
    """
    Creates and saves a map plot.
    """
    # Check if raster is 2D
    if not isinstance(raster, np.ndarray) or raster.ndim != 2:
        raise ValueError("raster must be a 2D NumPy array")
    
    # Extend palette if needed
    if extend != "neither":
        if extend == "both":
            n_classes += 2
        else:
            n_classes += 1

    # Create a colormap based on the provided palette
    palette, palette_dict = get_color_palette(n_classes, palette=palette, custom_palette=custom_palette)
    cmap = colors.ListedColormap(palette)
    
    # Discretize the data into bins
    norm = colors.BoundaryNorm(boundaries=bins, ncolors=n_classes, extend=extend)
    
    # Create histogram
    if hist is True and output_file:
        plot_palette_hist(raster, output_file, cb_label, unit, bins, palette, dark_mode)

    # Create the figure and axis with projection
    fig = plt.figure(figsize=[x_fig, y_fig], constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1, projection=projections[proj]())

    # Plot data
    filled = ax.pcolormesh(xx, yy, raster, cmap=cmap, norm=norm, shading='auto',
                           transform=ccrs.PlateCarree())

    # Add title, map features, colorbar, and colorbar label
    if title:
        ax.set_title(title, fontsize="xx-large", pad=15)

    ax, gridlines = add_map_features(ax)

    if labels is False: # Quantitative map
        cbar = add_colorbar_quant(fig, ax, filled, bins, orientation, extend)
        cbar_label = f"{cb_label} (in {unit})" if unit != "[no units]" else cb_label
        cbar.set_label(cbar_label, fontsize=16, labelpad=10)
        cbar.ax.xaxis.set_label_position('top')

    else:               # Qualitative map
        cbar = add_colorbar_quali(fig, ax, filled, bins, orientation, labels)

    # Add statistics annotation
    if stats_annotation:
        # Compute mean and std of non-NaN values
        mean_val = np.nanmean(raster)
        std_val = np.nanstd(raster)
        stat_text = f"Mean: {mean_val:.2f} {unit}\nσ: {std_val:.2f} {unit}"

        # Add text in axes coordinates (bottom left)
        ax.text(0.02, 0.02, stat_text, transform=ax.transAxes, fontsize=12, 
                verticalalignment='bottom', horizontalalignment='left',
                bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

    if nonsig_mask is not None:
        ax.contourf(xx, yy, nonsig_mask, levels=[0.5, 1.5], hatches=['///'], alpha=0, transform=ccrs.PlateCarree())

    # Dark mode
    if dark_mode is True:
        fig, ax = make_dark_mode(fig, ax, cbar=cbar, gridlines=gridlines)

    return fig

def plot_palette_hist(raster, output_file, cb_label, unit, bins, palette, dark_mode):
    """
    Creates and saves an histogram plot of the raster compared to the palette choosen.
    """
    # Make 2d raster, 1d
    flattened_raster = raster.flatten()

    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1)

    # Dark mode
    if dark_mode is True:
        fig, ax = make_dark_mode(fig, ax)

    # Add colored rectangles for each bin
    for i in range(len(bins) - 1):
        ax.add_patch(Rectangle((bins[i], 0), bins[i + 1] - bins[i], 1, 
                     color=palette[i], alpha=0.3, transform=ax.get_xaxis_transform()))
    
    ax.set_xticks(bins)
    ax.set_xticklabels(format_numbers(bins))

    # Create the histogram
    sns.histplot(flattened_raster, kde=False, ax=ax)

    # Add labels
    ax.set_ylabel("Frequency", fontsize="large")
    title = f"{cb_label} (in {unit})" if unit != "[no units]" else cb_label
    ax.set_title(title, fontsize=16)

    output_path = Path(output_file)
    output_file_modified = output_path.with_stem(output_path.stem + "_hist")
    save_figure_png(output_file_modified)

    plt.close()

def add_map_features(ax):
    """
    Add land, coastlines, and gridlines to the map.
    """
    # Draw land and ocean
    ax.add_feature(feature.LAND, facecolor="silver")
    ax.coastlines(linewidth=0.5, color='black')
    # Gridlines labels
    gridlines = ax.gridlines(draw_labels={"top": True, "left": True, "right": False, "bottom": False})

    return ax, gridlines

def add_colorbar_quant(fig, ax, filled, bins, orientation, extend):
    """
    Add a quantitative colorbar to the map.
    """    
    cbar = fig.colorbar(filled, ax=ax, orientation=orientation, ticks=bins, shrink=0.7, pad=0.01, extend=extend)
    cbar.set_ticklabels(format_numbers(bins))
    
    return cbar

def add_colorbar_quali(fig, ax, filled, bins, orientation, labels):
    """
    Add a qualitative colorbar to the map.
    """
    cbar = fig.colorbar(filled, ax=ax, orientation=orientation, shrink=0.7, pad=0.03)
    midpoints = (bins[:-1] + bins[1:]) / 2
    tick_labels = [labels.get(i, '') for i in range(len(bins) - 1)]
    cbar.set_ticks(midpoints)
    cbar.set_ticklabels(tick_labels)
    # Hide the colorbar edges ticks
    cbar.ax.xaxis.set_ticks_position('none')
    
    return cbar

def format_numbers(numbers):
    """
    Format bin values for better readability
    """
    formatted_numbers = []
    for value in numbers:
        if value == 0:
            formatted_numbers.append('0')
        elif abs(value) > 999 or abs(value) < 0.01:
            # Use scientific notation for values > 999 or < 0.01
            formatted_numbers.append(f'{value:.1e}')
        else:
            # Round rest values to 2 decimal places
            rounded_value = round(value, 2)
            if rounded_value.is_integer():
                formatted_numbers.append(f'{int(rounded_value)}')
            else:
                formatted_numbers.append(f'{rounded_value:.2f}')
    
    return formatted_numbers
