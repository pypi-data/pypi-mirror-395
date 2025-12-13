import json
from canopy.json.json_registry import get_json_function
import difflib

EXPECTED_KEYS = {
    'figure', 'output_file', 'input_file', 'grid_type', 'time_slice', 'lat_slice', 'lon_slice',
    'drop_layers', 'red_layers', 'layer', 'categorical', 'redop', 'timeop', 'gridop',
    'cb_label', 'title', 'scatter_size', 'scatter_alpha',
    'unit', 'n_classes', 'classification', 'palette', 'custom_palette', 'orientation',
    'extend', 'proj', 'force_zero', 'dark_mode', 'transparent', 'x_fig', 'y_fig',
    'percentage', 'layers', 'make_diff', 'yaxis_label', 'field_labels', 'move_legend',
    'legend_style', 'reverse_hue_style', 'max_labels_per_col', 'baseline', 'rolling_size',
    'stacked', 'relative', 'no_style', 'field_a_label', 'field_b_label', 'unit_a',
    'unit_b', 'plot_type', 'field_labels', 'horizontal', 'vertical_xlabels' 'kwargs',
    'stats_annotation', 'nonsig', 'source', 'convert_units', 'filter', 'yaxis_lim',
    'merge_fields', 'merge_interval', 'region', 'region_type'
}

def run_json(config_file):
    """
    Run a function based on the JSON configuration file.

    Parameters
    ----------
    config_file : str
        Path to the JSON configuration file.

    Notes
    -----
    This function loads the configuration from the specified JSON file,
    retrieves the appropriate function from the registry, and executes it
    with the configuration as an argument.
    """

    # Load the configuration from the JSON file
    json_config = load_json_config(config_file)

    # Check if any JSON keys are not exepcted
    warn_unused_keys(json_config, EXPECTED_KEYS)

    # Get the appropriate function from the registry and call it
    json_function = get_json_function(json_config)
    json_function(json_config)

def load_json_config(file_path):
    with open(file_path) as f:
        return json.load(f)

def warn_unused_keys(json_config, expected_keys):
    for key in json_config:
        if key not in expected_keys:
            suggestion = difflib.get_close_matches(key, expected_keys, n=1)
            if suggestion:
                print(f"Warning: The parameter '{key}' is not recognized. Did you mean '{suggestion[0]}'?")
            else:
                print(f"Warning: The parameter '{key}' in your JSON will not be used.")
