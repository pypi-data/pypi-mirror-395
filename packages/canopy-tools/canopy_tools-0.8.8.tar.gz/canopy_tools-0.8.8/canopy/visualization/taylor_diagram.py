import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import geocat.viz as gv
import warnings
from typing import Optional, List
import canopy as cp
from canopy.visualization.plot_functions import get_color_palette, make_dark_mode, handle_figure_output, select_sites

def make_taylor_diagram(fields: cp.Field | List[cp.Field], obs: cp.Field,
                        output_file: Optional[str] = None,
                        sites: Optional[bool | List[tuple]] = False,
                        gridop: Optional[str] = None,
                        title: Optional[str] = None,
                        field_labels: Optional[List[str]] = None,
                        palette: Optional[str] = None,
                        custom_palette: Optional[str] = None,
                        dark_mode: Optional[bool] = False,
                        transparent: Optional[bool] = False,
                        marker_size: Optional[float] = 100,
                        marker: Optional[str] = 'o',
                        fontsize: Optional[int] = 16,
                        x_fig: Optional[float] = 12, y_fig: Optional[float] = 10,
                        return_fig: Optional[bool] = False, **kwargs) -> Optional[plt.Figure]:
    """
    Create a Taylor diagram (https://pcmdi.llnl.gov/staff/taylor/CV/Taylor_diagram_primer.pdf) 
    comparing model data against observations.

    Parameters
    ----------
    fields : cp.Field or List[cp.Field]
        Model data Field(s) to compare against observations. If a list is provided,
        multiple fields will be plotted with one point per field.
    obs : cp.Field
        Observation/reference data Field (typically the "truth").
    output_file : str, optional
        File path for saving the plot.
    sites : bool or List[Tuple], optional
        Control site-level plotting. Default is False.
        If False, space reduction is applied to get a single point per field.
        If True, all sites are used. If provided with a list of (lon, lat) tuples, only select those sites.
    gridop : str, optional
        If provided, the grid reduction operation. Either None, 'sum' or 'av'. Default is None.
    title : str, optional
        Title of the plot.
    field_labels : List[str], optional
        Labels for each field when multiple fields are provided. Required when field is a list.
    palette : str, optional
        Seaborn color palette to use (https://seaborn.pydata.org/tutorial/color_palettes.html).
    custom_palette : str, optional
        Path of custom color palette .txt file to use. Names should match site labels.
    dark_mode : bool, optional
        Whether to apply dark mode styling to the plot.
    transparent : bool, optional
        If True, makes the background of the figure transparent.
    marker_size : float, optional
        Size of the markers. Default is 100.
    marker : str, optional
        Marker shape. Default is 'o' (circle).
    fontsize : int, optional
        Font size for labels. Default is 16.
    x_fig : float, optional
        Width of the figure in inches. Default is 12.
    y_fig : float, optional
        Height of the figure in inches. Default is 12.
    return_fig : bool, optional
        If True, returns the figure object that can be used by multiple_figs().
        Default is False.
    **kwargs
        Additional keyword arguments are passed directly to `taylor.add_model_set`. This allows
        customization of plot features such as `linestyle`, `linewidth`, etc.
    """
    # Force field to be a list
    if not isinstance(fields, list):
        fields = [fields]
    
    # Check that all fields have exactly one layer #TODO: add ability to select a layer
    for i, field in enumerate(fields):
        if len(field.layers) != 1:
            raise ValueError(f"All fields must have exactly one layer. Found: field[{i}]={len(field.layers)}")
    if len(obs.layers) != 1:
        raise ValueError(f"Obs must have exactly one layer. Found: obs={len(obs.layers)}")
        
    # Check sites parameter and warn if needed for multiple fields
    if len(fields) > 1 and sites:
        warnings.warn("Multiple fields doesn't work with multiple sites. Setting sites=False and gridop='av'", UserWarning)
        sites = False
        gridop = 'av'
    
    # Require field_labels for multiple fields
    if len(fields) > 1:
        if field_labels is None:
            raise ValueError("field_labels must be provided when multiple fields are provided")
        if len(field_labels) != len(fields):
            raise ValueError(f"field_labels length ({len(field_labels)}) must match number of fields ({len(fields)})")

    # Handle space reduction when sites is False
    if not sites and gridop is None:
        warnings.warn("Neither gridop nor sites provided. Setting gridop='av' by default to reduce space to a single point.", UserWarning)
        gridop = 'av'
    
    # Apply grid reduction to obs if needed
    if gridop:
        obs_red = obs.red_space(gridop)
    
    # Convert obs to DataFrame
    df_obs = cp.make_lines(obs_red if gridop else obs)
    
    # Compute statistics
    if sites:
        # Single field, multiple sites
        if gridop:
            fields_red = fields[0].red_space(gridop)
        
        df_field = cp.make_lines(fields_red if gridop else fields[0])

        # Force sites to be a list
        if not isinstance(sites, bool) and not isinstance(sites, list):
            sites = [sites]

        # Select sites
        df_field_sites = select_sites(df_field, sites)
        df_obs_sites = select_sites(df_obs, sites)
        site_names = list(df_field_sites.columns)
        
        stddev_norm, corrcoef, valid_site_names = [], [], []
        for site in site_names:
            std_norm, corr = compute_stats(df_field_sites[site], df_obs_sites[site])
            if std_norm is not None:
                stddev_norm.append(std_norm)
                corrcoef.append(corr)
                valid_site_names.append(site)
            else:
                print(f"Warning: Skipping site {site}: insufficient data or zero obs std dev")
        
        if len(stddev_norm) == 0:
            raise ValueError("No valid sites found with sufficient data for Taylor diagram")
        site_names = valid_site_names
    else:
        # Process all fields: one point per field
        stddev_norm, corrcoef, valid_labels = [], [], []
        
        for i, field in enumerate(fields):
            # Apply grid reduction to this field (returns a new Field without modifying original)
            if gridop:
                field_red = field.red_space(gridop)
            else:
                field_red = field
            
            df_field = cp.make_lines(field_red)
            
            std_norm, corr = compute_stats(df_field.iloc[:, 0], df_obs.iloc[:, 0])
            if std_norm is not None:
                stddev_norm.append(std_norm)
                corrcoef.append(corr)
                if field_labels:
                    valid_labels.append(field_labels[i])
            else:
                label = field_labels[i]
                print(f"Warning: Skipping {label}: insufficient data or zero obs std dev")
        
        if len(stddev_norm) == 0:
            raise ValueError("No valid fields found with sufficient data for Taylor diagram")
        
        # Update site_names
        site_names = valid_labels
        if not site_names: site_names = ["LPJ-GUESS"]
    
    # Create figure and Taylor Diagram instance
    fig = plt.figure(figsize=(x_fig, y_fig))
    taylor = gv.TaylorDiagram(fig=fig, label='observed')
    ax = plt.gca()

    # Get colors and plot points
    n_points = len(site_names) if site_names else 1
    colors, _ = get_color_palette(n_points, palette=palette, custom_palette=custom_palette)
    legend_handles = []
    
    # Plot points
    for i, (std, corr, label) in enumerate(zip(stddev_norm, corrcoef, site_names)):
        color = colors[i]
        
        # Base arguments
        plot_kwargs = {
            "color": color,
            "model_outlier_on": True,
            "annotate_on": False,
            "marker": marker,
            "facecolors": color,
            "s": marker_size
        }
        
        # Update with user-provided kwargs
        plot_kwargs.update(kwargs)
        
        taylor.add_model_set([std], [corr], **plot_kwargs)
        legend_handles.append(mlines.Line2D([0], [0], marker=marker, color='w',
                            markerfacecolor=color, markeredgecolor=color, markersize=8,
                            label=label, linestyle='None'))

    # Add reference point (obs vs obs = perfect match)
    taylor.add_model_set([1.0], [1.0], color='black', facecolors='black', s=marker_size, annotate_on=False)

    # Add taylor contours
    taylor.add_contours(levels=np.arange(0, 1.1, 0.25), colors='lightgrey', linewidths=0.5)
    taylor.add_corr_grid(np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.99]))
    
    if legend_handles:
        ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(0.95, 0.75), 
                  frameon=False, fontsize=fontsize)
    
    # Add figure title
    if title:
        plt.title(title, size=26, pad=45)
    
    # Apply dark mode if requested
    if dark_mode:
        fig, ax = make_dark_mode(fig, ax)
    
    return handle_figure_output(fig, output_file=output_file, return_fig=return_fig, transparent=transparent)

def compute_stats(model_ts, obs_ts):
    """
    Helper function to compute statistics from aligned time series
    """
    model_ts, obs_ts = model_ts.align(obs_ts, join='inner')
    valid = model_ts.notna() & obs_ts.notna()
    model_ts, obs_ts = model_ts[valid], obs_ts[valid]
    
    if len(model_ts) < 2:
        return None, None
    std_model, std_obs = float(model_ts.std()), float(obs_ts.std())
    if std_obs == 0:
        return None, None
    return std_model / std_obs, float(np.corrcoef(model_ts.values, obs_ts.values)[0, 1])
