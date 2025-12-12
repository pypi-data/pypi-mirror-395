.. _json:

JSON
====

The JSON mode allows you to use high-level visualization functions to easily and quickly create figures.

What you can do
---------------

You can generate the following types of figures by specifying the ``figure`` key in your JSON file:

.. currentmodule:: canopy.visualization

+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| "figure" key   | Function reference                           | JSON example file                                                                                                       | Remark                                               |
+================+==============================================+=========================================================================================================================+======================================================+
| map_simple     | :func:`map.make_simple_map`                  | `simple_map.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/simple_map.json>`_           | Can concatenate up to two fields (see example below) |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| map_diff       | :func:`map.make_diff_map`                    | `diff_map.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/diff_map.json>`_               | Compute the difference between two fields            |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| time_series    | :func:`time_series.make_time_series`         | `time_series.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/time_series.json>`_         |                                                      |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| static         | :func:`static_plot.make_static_plot`         | `static_plot.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/static_plot.json>`_         |                                                      |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+
| distribution   | :func:`distribution_plot.make_distribution_plot` | `distribution_plot.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/distribution_plot.json>`_ |                                                      |
+----------------+----------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------+

For a complete list of available arguments, refer to the documentation for each function, and consult the corresponding JSON example file for practical usage.

.. currentmodule:: canopy.visualization.map

With ``"figure": "map_simple"``, you can concatenate two fields and visualize them in a single map. For example:

.. code-block:: python

    {
        "figure": "map_simple",
        "input_file": ["example_data/hist/anpp.out.gz","example_data/ssp1A/anpp.out.gz"],
        ...
    }

You can also merge multiple fields together using the ``merge_fields`` and ``merge_interval`` keys. Set ``"merge_fields": true`` to enable merging, and optionally specify ``"merge_interval": 5`` to merge every 5 fields. If no interval is specified, all fields are merged together. For example:

.. code-block:: python

    {
        "figure": "map_simple",
        "input_file": ["grid1_ssp1.out.gz", "grid2_ssp1.out.gz", "grid1_ssp3.out.gz", "grid2_ssp3.out.gz"],
        "merge_fields": true,
        "merge_interval": 2,
        ...
    }

.. currentmodule:: canopy.core.field

**Other features**

- **Grid types and source:** You can specify which ``grid_type`` and ``source`` (to retrieve metadata) to use from the :meth:`Field.from_file` arguments.
- **Slice reduction:** You can reduce data along ``time``, ``lat``, or ``lon`` dimensions using the ``time_slice``, ``lat_slice``, or ``lon_slice`` keys.
- **Drop layers:** Remove unwanted layers from your data using the ``drop_layers`` key (accept a list).
- **Transform layers:** Apply transformations to layers using the ``red_layers`` key and the :meth:`Field.red_layers` function (accept a dictionary, see `stacked_time_series.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/stacked_time_series.json>`_ for an example).
- **Convert units:** Convert the units of your data using the ``convert_units`` key. This accepts a list with exactly two elements: the conversion factor (a number) and the new units string. For example, to convert from kg to GtC, use ``"convert_units": [1e-12, "GtC"]``. See `multiple_time_series.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/multiple_time_series.json>`_ for an example.
- **Filter data:** Filter your data using the ``filter`` key with a query string. For example, to filter for values where Total > 0.4 and Que_rob < 0.15, use ``"filter": "Total > 0.4 and Que_rob < 0.15"``. See `time_series.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/time_series.json>`_ for an example.
- **Filter region:** Filter your data by a named geographical region using the ``region`` and optional ``region_type`` keys. Supported ``region_type`` values are ``country`` (Natural Earth), ``giorgi``, ``SREX`` (IPCC SREX), and ``AR6`` (IPCC AR6). See `region_filter_map.json <https://codebase.helmholtz.cloud/canopy/canopy/-/blob/main/json_examples/region_filter_map.json>`_ for an example.
- **Merge fields:** Merge multiple input files defined on compatible grids into fewer series using ``merge_fields`` and optional ``merge_interval``. When ``merge_fields`` is ``true``, inputs are merged in the provided order; if ``merge_interval`` is set (e.g., ``5``), every N files are merged together. Ensure that ``field_labels`` length matches the number of merged groups.

What you cannot do
------------------

.. currentmodule:: canopy.visualization.plot_functions

- **No multiple figures function:** You cannot use the :func:`multiple_figs` function.
- **No function keyword arguments as JSON keys:** You cannot specify function keyword arguments (``kwargs``) directly as JSON keys.
