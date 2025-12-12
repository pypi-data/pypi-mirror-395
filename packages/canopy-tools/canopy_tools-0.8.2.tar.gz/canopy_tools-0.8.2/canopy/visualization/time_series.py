import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
import canopy as cp
from canopy.visualization.plot_functions import handle_figure_output, get_color_palette, make_dark_mode, select_sites
import warnings

# Define a custom warning format to show only the message
def custom_warning_format(message, category, filename, lineno, line=None):
    return f"{category.__name__}: {message}\n"
warnings.formatwarning = custom_warning_format
warnings.filterwarnings("ignore", message="Ignoring `palette` because no `hue` variable has been assigned.")

def make_time_series(fields: cp.Field | List[cp.Field], output_file: Optional[str] = None, 
                     layers: Optional[List[str] | str] = None, gridop: Optional[str] = 'av',
                     make_diff: Optional[bool] = False, yaxis_label: Optional[str] = None, 
                     sites: Optional[bool | List[tuple]] = False, yaxis_lim: Optional[List[float]] = None,
                     field_labels: Optional[List[str]] = None, unit: Optional[str] = None, 
                     title: Optional[str] = None, palette: Optional[str] = None,
                     custom_palette: Optional[str] = None, move_legend: Optional[bool] = False, 
                     legend_style: Optional[str] = 'default', reverse_hue_style: Optional[bool] = False, 
                     max_labels_per_col: Optional[int] = 15, baseline: Optional[bool] = False,
                     rolling_size: Optional[int] = None, stacked: Optional[bool] = False, 
                     relative: Optional[bool] = False, dark_mode: Optional[bool] = False, 
                     transparent: Optional[bool] = False, no_style: Optional[bool] = False,
                     x_fig: Optional[float] = 10, y_fig: Optional[float] = 10, 
                     return_fig: Optional[bool] = False, **kwargs) -> Optional[plt.Figure]:
    """
    Create a time-series plot from the given fields.

    Parameters
    ----------
    fields : cp.Field or List[cp.Field]
        Input data Field or list of Fields to display.
    output_file : str, optional
        File path for saving the plot.
    layers : List[str] or str, optional
        List of layer names to display.
    gridop : str, optional
        The reduction operation. Either 'sum' or 'av'. Default is 'av'.
    sites : bool or List[Tuple], optional
        Control site-level plotting instead of spatial reduction. Default is False. True = all sites,
        if provided with a list, only select the sites in the list.
    make_diff : bool, optional
        Option to make the difference between two time-series. Default is False.
    yaxis_label : str, optional
        Y-axis label, if not provided canopy will try to retrieve the name of the variable in the metadata.
    yaxis_lim : List[float], optional
        List of y-axis limits.
    field_labels : List[str], optional
        List of labels for the time series.
    unit : str, optional
        Unit of the y-axis variable, if not provided canopy will try to retrieve 
        the unit of the variable in the metadata.
    title : str, optional
        Title of the plot.
    palette : str, optional
        Seaborn color palette to use for the line colors (https://seaborn.pydata.org/tutorial/color_palettes.html, 
        recommended palette are in https://colorbrewer2.org).
    custom_palette : str, optional
        Path of custom color palette .txt file to use. Names should match label names.
    move_legend : bool, optional
        Move the the legend outside of plot. Default is False.
    legend_style : str or None, optional
        Style of the legend ('default', 'highlighted', 'end-of-line', 'hidden'). 
        If 'hidden', the legend will not be shown.
    reverse_hue_style : bool, optional
        Reverse how seaborn uses hue for different time series and style for different layers. Default is False.
    max_labels_per_col : int, optional
        Maximum number of labels per layer in the legend. Default is 15.
    baseline : bool, optional
        Option to add a y=0 dotted line. Default is False.
    rolling_size : int, optional
        Window of rolling mean.
    stacked : bool, optional
        Option to create a stacked plot. Default is False.
    relative : bool, optional
        Option to plot relative values. Default is False.
    dark_mode : bool, optional
        Option to use dark mode. Default is False.
    transparent: bool, optional
        Option to use a transparent background. Default is False.
    no_style : bool, optional
        Option to not use line styles in multiple time series. Default is False.
    x_fig : float, optional
        Width of the figure in inches. Default is 10.
    y_fig : float, optional
        Height of the figure in inches. Default is 10.
    return_fig : bool, optional
        If True, returns the figure object that can be usuable by multiple_figs().
        Default is False.
    **kwargs
        Additional keyword arguments are passed directly to `seaborn.lineplot`. This allows customization of
        line aesthetics such as `linewidth`, `linestyle`, `alpha`, etc.
    """
    # Check for some initial conditions
    if layers and sites:
        raise ValueError("Layers and sites cannot be used simultanuously. Only one layer for multiple sites.")

    # Force variables to be a list
    if not isinstance(fields, list):
        fields = [fields]
    if isinstance(layers, str):
        layers = [layers]
    if not isinstance(sites, bool) and not isinstance(sites, list):
        sites = [sites]

    # Retrieve metadata
    yaxis_label = yaxis_label or fields[0].metadata['name']
    unit = unit or fields[0].metadata['units']
    layers = layers or fields[0].layers

    # Make space reduction of the different fields...
    fields_red = []
    for field in fields:
        # ... (pass if already reduced or is sites)
        if not field.grid.is_reduced('lat') and not field.grid.is_reduced('lon') and not sites:
            fields_red.append(field.red_space(gridop))
        else:
            fields_red.append(field)

    # Make line objects
    time_series = []
    for field in fields_red:
        df = cp.make_lines(field)
        
        if sites: # If sites, flatten data
            df = select_sites(df, sites=sites)
            layers = list(df.columns) # Update layers

        time_series.append(df)
    
    # Make the difference between the lines (second minus first)
    if make_diff == True:
        if len(time_series) == 2:
            time_series = [time_series[1] - time_series[0]]
        else:
            raise ValueError("make_diff is True, but the number of time_series is not equal to 2.")

    # Check for valid inputs
    if any(ts.empty for ts in time_series):
        raise ValueError('One or more time_series are empty')
    if len(time_series) > 1:
        if field_labels is None:
            raise ValueError("field_labels must be defined for multiple time-series.")
        elif len(field_labels) != len(time_series):
            raise ValueError("field_labels should be of the same size as the number of time series.")
        
    # Check for different conditions
    if len(time_series) > 1:
        # Check that the selected layers exist in all time series
        layers_set = set(layers) if isinstance(layers, list) else {layers}
        for ts in time_series:
            ts_cols = set(ts.columns)
            missing_layers = layers_set - ts_cols
            if missing_layers:
                raise ValueError(
                    f'Time series is missing the following selected layer(s): {missing_layers}. '
                    'Tip: use field.rename_layers() method or select layers that exist in all time series.'
                    )
        if legend_style not in ['default', 'hidden'] and no_style == False and len(layers)>1:
            warnings.warn("Legend style for multiple time series can only be 'default.'", UserWarning)
            legend_style = 'default'
        if rolling_size is True:
            warnings.warn("Rolling mean is only available for one time series.'", UserWarning)
            rolling_size = None
        if stacked is True:
            raise ValueError("Stacked plot is only available for one time series.")
    if legend_style not in ['default', 'hidden']:
        if move_legend is True:
            warnings.warn("Legend_style with move_legend can only be 'default.'", UserWarning)
            legend_style = 'default'
        if stacked is True:
            warnings.warn("Legend style in stacked plot can only be 'default.'", UserWarning)
            legend_style = 'default'
    if rolling_size:
        if stacked is True:
            warnings.warn("Rolling mean is not available for stacked plot.", UserWarning)
        if kwargs:
            warnings.warn("Rolling mean is not available with custom lineplot kwargs.", UserWarning)

    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(x_fig, y_fig))

    # Make layers of time series relative values
    if relative is True:
        for ts in time_series:
            ts[layers] = ts[layers].div(ts[layers].sum(axis=1), axis=0) * 100
        if unit != "%":
            warnings.warn("Unit will be changed to '%' for relative values.", UserWarning)
            unit = "%"

    # Set colour palette
    n_classes = len(layers)
    # Use time series count if multiple series exist and hue not reversed or single layer.
    if len(time_series) > 1 and (reverse_hue_style is False or len(layers) == 1):
        n_classes = len(time_series)
    colors, palette_dict = get_color_palette(n_classes, palette=palette, custom_palette=custom_palette)
    if custom_palette: # reorder the palette to match the order of the layers
        colors = [palette_dict[col] for col in layers if col in palette_dict]
    
    # Convert PeriodIndex to DatetimeIndex if necessary
    for ts in time_series:
        if isinstance(ts.index, pd.PeriodIndex):
            ts.index = ts.index.to_timestamp()

    # Plot
    if stacked is False:
        fig, ax = plot_time_series(fig, ax, time_series, layers, reverse_hue_style, field_labels, colors, 
                                   move_legend, legend_style, max_labels_per_col, rolling_size, no_style, **kwargs)
    else:
        ax = plot_stacked_time_series(ax, time_series, layers, colors, max_labels_per_col, legend_style)

    # Set axis style
    set_axis_style(ax, yaxis_label, title, unit)
    ax.set_xlim(min(ts.index.min() for ts in time_series), max(ts.index.max() for ts in time_series))

    if relative is True:     # Set y-axis limits if specified
        ax.set_ylim([0, 100])
    elif yaxis_lim is not None:
        ax.set_ylim(yaxis_lim)

    # Dark mode
    if dark_mode is True:
        fig, ax = make_dark_mode(fig, ax, legend_style)

    # Add y=0 line
    if baseline is True:
        ax.axhline(0, color="black", linestyle="--", linewidth=1)

    return handle_figure_output(fig, output_file=output_file, return_fig=return_fig, transparent=transparent)

def plot_time_series(fig, ax, time_series, layers, reverse_hue_style, field_labels, 
                     colors, move_legend, legend_style, max_labels_per_col, rolling_size, 
                     no_style, **kwargs):
    """
    Plot each line from the given DataFrame(s) (time_series)
    """
    # Handle multiple time series
    if len(time_series) > 1:
        # Combine the DataFrames into a single DataFrame with an additional layer            
        combined_ts = pd.concat([df.assign(DataFrame=label) for df, label in zip(time_series, field_labels)])

        # Reshape the DataFrame
        time_series = combined_ts.reset_index().melt(
            id_vars=['time', 'DataFrame'], value_vars=layers, var_name='Column', value_name='Value'
            )
        
        # Base arguments common to all multiple time series cases
        plot_kwargs = {
            "data": time_series,
            "x": 'time',
            "y": 'Value',
            "palette": colors,
            "legend": bool(legend_style)
        }
        
        # Set hue and style based on conditions
        is_single_layer = isinstance(layers, str) or (isinstance(layers, list) and len(layers) == 1)
        if is_single_layer:
            plot_kwargs["hue"] = 'DataFrame'
            if reverse_hue_style:
                plot_kwargs["style"] = 'DataFrame'
        else:
            if reverse_hue_style:
                plot_kwargs["hue"] = 'Column'
                plot_kwargs["style"] = None if no_style else 'DataFrame'
            else:
                plot_kwargs["hue"] = 'DataFrame'
                plot_kwargs["style"] = 'Column'
        
        # Update with user-provided kwargs
        plot_kwargs.update(kwargs)
        ax = sns.lineplot(**plot_kwargs)
    
    # Or only one time series
    else:
        # Base arguments common to all single time series cases
        base_kwargs = {
            "palette": colors,
            "ax": ax
        }
        
        if rolling_size:
            rolling_mean = time_series[0][layers].rolling(window=rolling_size).mean()
            
            # Original data (dashed)
            plot_kwargs_orig = {**base_kwargs, "data": time_series[0][layers], 
                                "legend": False, "dashes": [(1, 1)] * len(layers)}
            plot_kwargs_orig.update(kwargs)
            sns.lineplot(**plot_kwargs_orig)
            
            # Rolling mean (solid)
            plot_kwargs_rolling = {**base_kwargs, "data": rolling_mean[layers], 
                                   "legend": bool(legend_style), "dashes": False}
            plot_kwargs_rolling.update(kwargs)
            sns.lineplot(**plot_kwargs_rolling)
        else:
            plot_kwargs = {**base_kwargs, "data": time_series[0][layers], 
                          "legend": bool(legend_style), "dashes": False}
            plot_kwargs.update(kwargs)
            sns.lineplot(**plot_kwargs)

    # Apply the legend style
    apply_legend_style(ax, legend_style, max_labels_per_col, move_legend)

    return fig, ax

def plot_stacked_time_series(ax, time_series, layers, colors, max_labels_per_col, legend_style):
    """
    Same as plot_time_series but for stacked plot.
    """
    # Plot each line in time_series
    ax.stackplot(time_series[0].index, time_series[0][layers].T.values, colors=colors, linewidth=0.75)

    if legend_style != 'hidden':
        # Add legend with reversed order
        ncols = (len(layers) + max_labels_per_col - 1) // max_labels_per_col  # Ceiling division
        ax.legend(layers, loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, 
                  fontsize=14, reverse=True, ncols=ncols)

    return ax

def apply_legend_style(plot, legend_style, max_labels_per_col, move_legend):
    """
    Apply the selected legend style to the figure.
    If legend_style is 'hidden', the legend will not be shown.
    """
    if legend_style == 'hidden':
        plot.legend().set_visible(False)
        return
    # Estimate the number of layers based on the number of legend entries
    num_labels = len(plot.get_legend_handles_labels()[1])
    ncols = max(1, (num_labels + max_labels_per_col - 1) // max_labels_per_col)  # Ceiling division

    if legend_style == 'default':
        # Handles are to remove all labels from the legend
        handles, labels = plot.get_legend_handles_labels()
        new_labels = [label for label in labels if label not in ['Column', 'DataFrame']]
        new_handles = [handle for handle, label in zip(handles, labels) if label not in ['Column', 'DataFrame']]
        plot.legend(handles=new_handles, labels=new_labels, loc='best', frameon=False, fontsize=14, ncols=ncols)

    elif legend_style == 'highlighted':
        plot.legend(handlelength=0, handletextpad=0, labelcolor='linecolor', loc='best', 
                    frameon=False, fontsize=14, ncols=ncols)
        
    elif legend_style == 'end-of-line':
        plot.legend().set_visible(False)
        lines = plot.get_lines()
        for idx, col in enumerate(plot.get_legend().get_texts()):
            label = col.get_text()
            x_data = lines[idx].get_xdata()
            y_data = lines[idx].get_ydata()
            if len(x_data) > 0 and len(y_data) > 0:
                plt.text(x_data[-1], y_data[-1], ' ' + label, color=lines[idx].get_color(), 
                         verticalalignment='center', fontsize=14)
    else:
        raise ValueError("Invalid legend_style. Choose from 'default', 'highlighted', 'end-of-line', or 'hidden'.")
    
    if move_legend is True:
            sns.move_legend(plot, "center left", bbox_to_anchor=(1, 0.85), ncols=ncols)

def set_axis_style(ax, yaxis_label, title, unit):
    """
    Set the axis labels, yaxis_label, tick parameters, and spine visibility for a given axis.
    """
    # Add title
    if title:
        ax.set_title(title, fontsize=18, pad=20)
    # Add labels
    ax.set_xlabel("Year", fontsize=14)
    ylabel = f"{yaxis_label} (in {unit})" if unit != "[no units]" else yaxis_label
    ax.set_ylabel(ylabel, fontsize=16)
    # Increase font size for ticks
    ax.tick_params(axis='both', labelsize=12)
    # Remove the top and right spines
    sns.despine(ax=ax)
