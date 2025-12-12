import pandas as pd
import canopy as cp
import canopy.visualization as cv
from canopy.json.json_registry import register_json
import os

@register_json
def map_simple(json_config):
    fields = preprocess_data(json_config)
    if len(fields)==2:
        fields = [cp.concat2(fields[0],fields[1])]
    elif len(fields)>2:
        raise ValueError("A maximum of two input files (to concat) can be used in the JSON mode.")
    
    cv.make_simple_map(field=fields[0],
                       layer=json_config.get('layer'),
                       categorical=json_config.get('categorical', False),
                       output_file=json_config.get('output_file'),
                       timeop=json_config.get('timeop', 'av'),
                       cb_label=json_config.get('cb_label'), 
                       title=json_config.get('title'),
                       unit=json_config.get('unit'), 
                       n_classes=json_config.get('n_classes', 4),
                       classification=json_config.get('classification', 'linear'),
                       palette=json_config.get('palette'), 
                       custom_palette=json_config.get('custom_palette'),
                       orientation=json_config.get('orientation', 'horizontal'),
                       extend=json_config.get('extend', 'neither'),
                       proj=json_config.get('proj', 'Robinson'),
                       force_zero=json_config.get('force_zero', False),
                       dark_mode=json_config.get('dark_mode', False),
                       transparent=json_config.get('transparent', False),
                       stats_annotation=json_config.get('stats_annotation', False),
                       x_fig=json_config.get('x_fig', 10),
                       y_fig=json_config.get('y_fig', 10))

@register_json
def map_diff(json_config):
    fields = preprocess_data(json_config)
    if len(fields)!=2:
        raise ValueError("Requires exactly two input files to use map diff.")
    
    cv.make_diff_map(field_a=fields[0], 
                     field_b=fields[1], 
                     layer=json_config.get('layer'),
                     output_file=json_config.get('output_file'), 
                     timeop=json_config.get('timeop', 'av'),
                     cb_label=json_config.get('cb_label'),
                     title=json_config.get('title'),
                     unit=json_config.get('unit'), 
                     n_classes=json_config.get('n_classes', 4), 
                     classification=json_config.get('classification', 'linear'),
                     palette=json_config.get('palette'), 
                     custom_palette=json_config.get('custom_palette'),
                     orientation=json_config.get('orientation', 'horizontal'),
                     extend=json_config.get('extend', 'neither'),
                     proj=json_config.get('proj', 'Robinson'),
                     force_zero=json_config.get('force_zero', False),
                     dark_mode=json_config.get('dark_mode', False),
                     transparent=json_config.get('transparent', False),
                     stats_annotation=json_config.get('stats_annotation', False),
                     x_fig=json_config.get('x_fig', 10),
                     y_fig=json_config.get('y_fig', 10),
                     percentage=json_config.get('percentage', False),
                     nonsig=json_config.get('nonsig', False))


@register_json
def time_series(json_config):
    fields = preprocess_data(json_config)

    cv.make_time_series(fields=fields,
                        output_file=json_config.get('output_file'),
                        layers=json_config.get('layers'),
                        gridop=json_config.get('gridop', 'av'),
                        make_diff=json_config.get('make_diff', False),
                        yaxis_label=json_config.get('yaxis_label'),
                        title=json_config.get('title'),
                        field_labels=json_config.get('field_labels'),
                        unit=json_config.get('unit'),
                        palette=json_config.get('palette'),
                        custom_palette=json_config.get('custom_palette'),
                        move_legend=json_config.get('move_legend', False),
                        legend_style=json_config.get('legend_style', 'default'),
                        reverse_hue_style=json_config.get('reverse_hue_style', False),
                        max_labels_per_col=json_config.get('max_labels_per_col', 15),
                        baseline=json_config.get('baseline', False),
                        rolling_size=json_config.get('rolling_size'),
                        stacked=json_config.get('stacked', False),
                        relative=json_config.get('relative', False),
                        dark_mode=json_config.get('dark_mode', False),
                        transparent=json_config.get('transparent', False),
                        no_style=json_config.get('no_style', False),
                        yaxis_lim=json_config.get('yaxis_lim'),
                        x_fig=json_config.get('x_fig', 10),
                        y_fig=json_config.get('y_fig', 10))

@register_json
def static(json_config):
    fields = preprocess_data(json_config)

    cv.make_static_plot(field_a=fields[0],
                        field_b=fields[1],
                        output_file=json_config.get('output_file'),
                        layers=json_config.get('layers'),
                        field_a_label=json_config.get('field_a_label'),
                        field_b_label=json_config.get('field_b_label'),
                        unit_a=json_config.get('unit_a'),
                        unit_b=json_config.get('unit_b'),
                        scatter_size=json_config.get('scatter_size', 6),
                        scatter_alpha=json_config.get('scatter_alpha', 0.1),
                        title=json_config.get('title'),
                        palette=json_config.get('palette'),
                        custom_palette=json_config.get('custom_palette'),
                        move_legend=json_config.get('move_legend', False),
                        dark_mode=json_config.get('dark_mode', False),
                        transparent=json_config.get('transparent', False),
                        x_fig=json_config.get('x_fig', 10),
                        y_fig=json_config.get('y_fig', 10),
                        **json_config.get('kwargs', {}))
    
@register_json
def distribution(json_config):
    fields = preprocess_data(json_config)

    cv.make_distribution_plot(fields=fields,
                            output_file=json_config.get('output_file'),
                            plot_type=json_config.get('plot_type', 'box'),
                            layers=json_config.get('layers'),
                            gridop=json_config.get('gridop'),
                            yaxis_label=json_config.get('yaxis_label'),
                            field_labels=json_config.get('field_labels'),
                            unit=json_config.get('unit'),
                            title=json_config.get('title'),
                            palette=json_config.get('palette'),
                            custom_palette=json_config.get('custom_palette'),
                            horizontal=json_config.get('horizontal', False),
                            vertical_xlabels=json_config.get('vertical_xlabels', False),
                            dark_mode=json_config.get('dark_mode', False),
                            transparent=json_config.get('transparent', False),
                            x_fig=json_config.get('x_fig', 10),
                            y_fig=json_config.get('y_fig', 10),
                            **json_config.get('kwargs', {}))

def preprocess_data(json_config):
    """
    Preprocess data based on configuration settings provided in a JSON object.

    This includes loading a field, applying reductions, and optionally transforming or dropping layers.
    """
    # Be sure to create directory if not existing
    if json_config.get('output_file'):
        output_dir = os.path.dirname(json_config.get('output_file'))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    # Extract the input file(s) from the configuration
    input_files = json_config.get('input_file')

    # Initialize reduction_kwargs
    reduction_kwargs = {}

    # Update reduction_kwargs using the helper function
    update_reduction_kwargs(reduction_kwargs, json_config, 'time_slice')
    update_reduction_kwargs(reduction_kwargs, json_config, 'lat_slice')
    update_reduction_kwargs(reduction_kwargs, json_config, 'lon_slice')

    # Create a RedSpec object from reduction_kwargs
    redspec = cp.RedSpec(**reduction_kwargs)

    # Make input_files a list
    if not isinstance(input_files, list):
        input_files = [input_files]
    fields = []

    # Open fields
    for input_file in input_files:
        field = cp.Field.from_file(
            input_file, grid_type=json_config.get('grid_type'), source=json_config.get('source')
            )

        # Apply the region filtering
        if json_config.get('region'):
                field = cp.filter_region(
                    field, region=json_config['region'], region_type=json_config.get('region_type', 'country')
                    )

        # Apply the reduction to the field
        field.reduce(redspec, inplace=True)
        
        # Optionally drop specified data fields
        if json_config.get('drop_layers'):
            field.drop_layers(layers=json_config['drop_layers'], inplace=True)

        # Optionally apply red_layers transformation
        if json_config.get('red_layers'):
            for red_layer in json_config['red_layers']: # Handle multiple red_layers
                field.red_layers(redop=red_layer['redop'], layers=red_layer.get('layers'),
                                 name=red_layer.get('name'), drop=red_layer.get('drop', False),
                                 inplace=True)

        # Apply unit convertion
        if json_config.get('convert_units'):
            convert_units_config = json_config['convert_units']
            if isinstance(convert_units_config, list) and len(convert_units_config) == 2:
                factor, units = convert_units_config
                field.convert_units(factor, units, inplace=True)
            else:
                raise ValueError("convert_units must be a list with exactly two elements: [factor, units]")

        # Apply filtering
        if json_config.get('filter'):
            field.filter(query=json_config['filter'], inplace=True)

        fields.append(field)

    # Handle merge_fields parameter
    if json_config.get('merge_fields'):
        interval = json_config.get('merge_interval', len(fields))
        merged_fields = []
        for i in range(0, len(fields), interval):
            merged_fields.append(cp.merge_fields(fields[i:i+interval]))
        return merged_fields
    
    return fields

def update_reduction_kwargs(reduction_kwargs, json_config, key):
    """
    Helper function to check if a key exists in json_config and update reduction_kwargs.
    """
    if key in json_config:
        reduction_kwargs[key] = json_config[key]
