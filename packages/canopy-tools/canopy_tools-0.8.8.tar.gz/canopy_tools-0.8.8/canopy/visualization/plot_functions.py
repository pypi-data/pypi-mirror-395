import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Optional, List, Tuple
import os
import warnings

def select_sites(data: Union[pd.DataFrame, List[Tuple[float, float]]], 
                 sites: Union[bool, List[Tuple[float, float]]] = True) -> pd.DataFrame:
    """
    Select and reorder columns of a DataFrame according to requested sites.
    """
    
    if sites is True:
        # Keep all columns
        df = data.copy()
        df.columns = [f"{c[1]}, {c[2]}" for c in df.columns]
        return df
    
    elif isinstance(sites, list):
        ordered_cols = []
        for lon, lat in sites:
            cols = [c for c in data.columns if np.isclose(c[1], float(lon)) and np.isclose(c[2], float(lat))]
            if not cols:
                raise ValueError(f"Requested site ({lon}, {lat}) not found in data.")
            ordered_cols.extend(cols)
        
        df = data[ordered_cols].copy()
        df.columns = [f"{c[1]}, {c[2]}" for c in ordered_cols]
        return df

def handle_figure_output(fig, output_file=None, return_fig=False, transparent=False) -> Optional[plt.Figure]:
    """
    Figure handler: save, return, or show.
    """
    if output_file and return_fig:
        raise ValueError("Cannot both save (output_file='myimage') and return the figure (return_fig=True). Choose one.")
    elif output_file:
        # Only use bbox_inches='tight' if nothing is out of bounds
        if has_out_of_bounds_artists(fig):
            save_figure_png(output_file, bbox_inches=None, transparent=transparent)
        else:
            save_figure_png(output_file, bbox_inches='tight', transparent=transparent)
        plt.close()
    elif return_fig:
        return fig
    else:
        plt.show()

def has_out_of_bounds_artists(fig):
    # Handle Seaborn FacetGrid/PairGrid
    if hasattr(fig, "axes"):
        axes = fig.axes
        # FacetGrid.axes is a numpy array, flatten it
        if hasattr(axes, "flat"):
            axes = axes.flat
    # Handle matplotlib Figure
    elif hasattr(fig, "get_axes"):
        axes = fig.get_axes()
    else:
        return False

    for ax in axes:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        for line in ax.get_lines():
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            if ((xdata < xlim[0]).any() or (xdata > xlim[1]).any() or
                (ydata < ylim[0]).any() or (ydata > ylim[1]).any()):
                return True
    return False

def save_figure_png(output_file, bbox_inches=None, transparent=False):
    """
    Save the current matplotlib figure as a PNG file.
    """
    # Ensure the extension is .png
    base, _ = os.path.splitext(output_file)
    output_file = f"{base}.png"
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(output_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Save the figure
    plt.savefig(output_file, format="png", dpi=300, bbox_inches=bbox_inches, transparent=transparent)

def get_color_palette(n_classes, palette=None, custom_palette=None):
    """
    Generate a color palette for plotting based on either a ColorBrewer palette or a custom palette file.
    """
    if custom_palette:
        palette_dict = {}
        with open(custom_palette, 'r') as file:
            lines = file.readlines()
            if len(lines) != n_classes:
                raise ValueError(f"Custom palette file has {len(lines)} lines, but {n_classes} classes are required.")
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    label, color = parts
                    palette_dict[label] = color
                else:
                    raise ValueError("Custom palette provided should have two elements maximum per line.")
        
        # Extract colors from the dictionary
        palette = [palette_dict[label] for label in palette_dict]

    else:
        if palette:
            palette = sns.color_palette(palette, n_colors=n_classes)
        else:
            # Get the base tab20 palette (20 colors)
            base_palette = sns.color_palette("tab20", n_colors=20)
            # Loop through the palette if more than 20 classes are needed
            if n_classes > 20:
                warnings.warn(f"Requested {n_classes} classes, but tab20 palette only has 20 colors. Colors will be repeated cyclically. Consider using a custom palette with custom_palette for better distinction.", UserWarning)
            palette = [base_palette[i % 20] for i in range(n_classes)]
        palette_dict = None
    
    return palette, palette_dict

def make_dark_mode(fig, ax, legend_style=None, cbar=None, gridlines=None):
    """
    Apply dark mode styling to the given figure and axis.
    """
    dark_gray = '#1F1F1F'
    fig.patch.set_facecolor(dark_gray)
    ax.set_facecolor(dark_gray)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    if gridlines:
        gridlines.xlabel_style = {'color': 'white'}
        gridlines.ylabel_style = {'color': 'white'}
    
    if cbar:
        cbar.ax.xaxis.label.set_color('white')
        cbar.ax.tick_params(axis='x', colors='white')
        cbar.outline.set_edgecolor('white')
    
    legend = ax.get_legend()
    if legend and legend_style == 'default':
        for text in legend.get_texts():
            text.set_color('white')
    
    return fig, ax

def multiple_figs(fig_list: List[Figure], output_file: Optional[str] = None, 
                   ncols: Optional[int] = 2, dpi: Optional[int] = 150, 
                   dark_mode: Optional[bool] = False, add_letters: Optional[bool] = False,
                   title: Optional[str] = None, title_font_size: Optional[int] = 24):
    """
    Arrange multiple figures into a single figure.

    Parameters
    ----------
    fig_list : list of matplotlib.Figure
        List of figure and axes pairs to combine into a single image.
    output_file : str, optional
        Path to save the combined image
    ncols : int, optional
        Number of columns in the grid
    dpi : int, optional
        Resolution for the output. Default is 150.
    dark_mode : bool, optional
        If True, use dark gray background instead of white
    add_letters : bool, optional
        If True, adds letter labels (a, b, c...) to the bottom left corner of each subfigure
    title : str, optional
        A common title for all figures.
    title_font_size : int, optional
        Font size for the title in points (pt). Default is 24.
    """
    none_indices = [i for i, fig in enumerate(fig_list) if fig is None]
    if none_indices:
        raise ValueError(f"Figures at indices {none_indices} are None. Please check your figure creation.")

    # Save each figure temporarily
    temp_files = []
    for i, fig in enumerate(fig_list):
        # If fig is a seaborn FacetGrid, extract the underlying matplotlib Figure
        if isinstance(fig, matplotlib.figure.Figure):
            current_fig = fig
        elif hasattr(fig, "fig"):  # e.g. seaborn FacetGrid
            current_fig = fig.fig
        else:
            raise TypeError(f"Unsupported figure type: {type(fig)}")

        if add_letters:
            letter = chr(97 + i)  # Convert number to letter (97 is ASCII for 'a')
            current_fig.text(-0.05, -0.05, f"({letter})", 
                    fontsize=12, fontweight='bold',
                    color='white' if dark_mode else 'black',
                    transform=current_fig.transFigure)
        
        temp_file = f"temp_plot_{i}.png"
        current_fig.savefig(temp_file, dpi=dpi, bbox_inches='tight', edgecolor='none')
        temp_files.append(temp_file)
    
    # Load images and combine them
    images = [Image.open(tf) for tf in temp_files]
    
    # Calculate dimensions
    nplots = len(images)
    nrows = (nplots + ncols - 1) // ncols
    
    # Get max dimensions for consistent sizing
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Add space for title if provided
    title_height = 0
    font = None
    if title:
        # Scale font size by DPI for resolution independence. Using 72 as a reference DPI.
        scaled_font_size = int(title_font_size * dpi / 72)
        font = ImageFont.truetype("DejaVuSans.ttf", scaled_font_size)
        
        # Calculate title height
        title_bbox = ImageDraw.Draw(Image.new('RGB', (1,1))).textbbox((0, 0), title, font=font)
        title_width_text = title_bbox[2] - title_bbox[0]
        title_height_text = title_bbox[3] - title_bbox[1]
        title_height = title_height_text + 20  # Add some padding
    
    # Create combined image
    combined_width = ncols * max_width
    combined_height = nrows * max_height + title_height
    bg_color = '#1F1F1F' if dark_mode else 'white'
    combined_image = Image.new('RGB', (combined_width, combined_height), bg_color)
    
    # Draw title if provided
    if title:
        draw = ImageDraw.Draw(combined_image)
        # Recalculate for positioning on the actual image canvas
        title_bbox = draw.textbbox((0, 0), title, font=font)
        title_width_text = title_bbox[2] - title_bbox[0]
        title_height_text = title_bbox[3] - title_bbox[1]
        x_text = (combined_width - title_width_text) // 2
        y_text = (title_height - title_height_text) // 2 - title_bbox[1]

        draw.text((x_text, y_text), title, font=font, fill='white' if dark_mode else 'black')

    # Paste individual images
    for idx, img in enumerate(images):
        row = idx // ncols
        col = idx % ncols
        x = col * max_width
        y = row * max_height + title_height
        
        # Center horizontally, align to bottom vertically
        x_offset = (max_width - img.width) // 2
        y_offset = max_height - img.height
        
        combined_image.paste(img, (x + x_offset, y + y_offset))
    
    # Save or show the result
    if output_file:
        combined_image.save(output_file, dpi=(dpi, dpi))
    else:
        combined_image.show()
    
    # Clean up temporary files
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except:
            pass
    
    return combined_image
