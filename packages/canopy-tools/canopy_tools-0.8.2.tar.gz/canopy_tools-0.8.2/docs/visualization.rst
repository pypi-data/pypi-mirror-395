.. _visualization:

Visualization
=============

**canopy** includes high-level functions to make figures directly from a ``Field`` object using `Seaborn <https://seaborn.pydata.org/index.html>`_ and `Cartopy <https://scitools.org.uk/cartopy/docs/latest/>`_ libraries.

Make a map
----------

.. currentmodule:: canopy.visualization.map

Using a ``Field`` object, you can make a simple map with :func:`make_simple_map`:

.. code-block:: python

    # Load your Field object first
    run_ssp1 = cp.get_source("example_data/ssp1A/","lpjguess")
    run_ssp1.load_field("cpool")

    cp.visualization.make_simple_map(field=run_ssp1.cpool, layer="Total")

.. image:: _static/ssp1_cpool_map.png
    :alt: Example map output
    :align: center
    :width: 60%

**You can check the different arguments available in the API reference:** :func:`make_simple_map`. 

.. note::

    ``make_simple_map`` is using a ``Field`` to produce a figure. 
    
    By doing so, the rasterisation with ``make_raster`` is included in the function.

.. warning::

    In certain configurations, the use of "EuroPP" as projection will introduce a bug that will produce undesired polygons on the ocean.

    This originates from **Cartopy** and is being discussed in their `github issues <https://github.com/SciTools/cartopy/issues/1685>`_.

    If you encounter such issues, please use "TransverseMercator", an adapted projection for the Europe region.

    .. code-block:: python

        cp.visualization.make_simple_map(field=myfield, layer="Total", projection="TransverseMercator")

You can also make a difference map between two ``Field`` objects using :func:`make_diff_map`:

.. code-block:: python

    cp.visualization.make_diff_map(field_a=run_ssp1.cpool, field_b=run_ssp3.cpool, layer="Total")

Every time you call :func:`make_diff_map` or :func:`make_simple_map` with a `output_file`, a histogram of your data is produced in a separated file.

.. image:: _static/ssp1_cpool_map_hist.png
    :alt: Example histogram output
    :align: center
    :width: 60%

This graph helps you see the distribution of the values and the colour classification (on the background) applied to it.

Explore different data classification methods with the argument ``classification``, more information can be found on `this tutorial <https://gisgeography.com/choropleth-maps-data-classification/>`_.

Make a time-series
------------------

.. currentmodule:: canopy.visualization.time_series

Using a ``Field`` object, you can make a time-series with :func:`make_time_series`:

.. code-block:: python

    cp.visualization.make_time_series(fields=run_ssp1.cpool)

.. image:: _static/ssp1_cpool_ts.png
    :alt: Example time-series output
    :align: center
    :width: 50%

**You can check the different arguments available in the API reference:** :func:`make_time_series`. 

.. note::

    ``make_time_series`` is using a ``Field`` to produce a figure. 
    
    By doing so, the linearization with ``make_lines`` is included in the function.

In addition, you can use kwargs arguments from the `seaborn.lineplot <https://seaborn.pydata.org/generated/seaborn.lineplot.html>`_ and `matplotlib.lines.Line2D <https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html>`_ functions. This allows customization of line aesthetics such as `linewidth`, `linestyle`, `alpha`, etc.

.. code-block:: python

    cp.visualization.make_time_series(fields=run_ssp1.cpool, layers="Total", linewidth=3, linestyle='-', alpha=0.3)

.. warning::

    Kwargs arguments are only available for single time series (not multiple), and without the ``rolling_mean`` argument.

If you want to compare multiple time-series on the same figure, the function argument ``fields`` also accepts a list of ``Field`` objects:

.. code-block:: python

    import canopy.visualization as cv

    # Let's load first multiple Field objects
    run_hist = cp.get_source("example_data/hist/","lpjguess")
    run_ssp1 = cp.get_source("example_data/ssp1A/","lpjguess")
    run_ssp3 = cp.get_source("example_data/ssp3A/","lpjguess")
    run_hist.load_field("cpool")
    run_ssp1.load_field("cpool")
    run_ssp3.load_field("cpool")

    # Make a list of your loaded Field objects
    fields = [run_hist.cpool,run_ssp1.cpool,run_ssp3.cpool]

    cv.make_time_series(fields=fields,
                        layers=["Total","VegC","SoilC"],
                        field_labels=["hist","ssp1","ssp3"])

.. image:: _static/all_cpool_ts.png
    :alt: Example multiple time-series output
    :align: center
    :width: 50%

In this case, the function argument ``field_labels``, the list of labels for the time series, is mandatory.

By default, each time-series will get a different colour, and each layer will get a different line styles (solid, dashed, etc.). 

If you want to invert this behavior, you can use the function argument ``reverse_hue_style``:

.. code-block:: python

    cv.make_time_series(fields=fields, 
                        layers=["Total","VegC","SoilC"],
                        field_labels=["hist","ssp1","ssp3"],
                        reverse_hue_style=True)

Make a static plot
------------------

.. currentmodule:: canopy.visualization.static_plot

You can produce a scatter plot with regression lines and r-scores to compare two ``Field`` objects (which can be reduced spatially, temporally, or both beforehand) with :func:`make_static_plot`:

.. code-block:: python

    cp.visualization.make_static_plot(field_a=run_a, field_b=run_b, 
                                      layers=["Abi_alb","Bet_pen","Bet_pub","Que_rob","C3_gr"],
                                      field_a_label="With land-use",
                                      field_b_label="Without land-use",
                                      unit_a="kgC/m²",
                                      unit_b="kgC/m²",
                                      title="Actual GPP over Europe",
                                      palette="tab10",
                                      move_legend=True,
                                      dark_mode=True,
                                      x_fig=10,
                                      y_fig=10
                                      )

.. image:: _static/static_plot.png
    :alt: Example static output
    :align: center
    :width: 50%

**You can check the different arguments available in the API reference:** :func:`make_static_plot`. 

In addition, you can use kwargs arguments from the `seaborn.regplot <https://seaborn.pydata.org/generated/seaborn.regplot.html>`_ function.

These two fields can be, for example, the same variable from two different runs, or two different variables from the same run.

Make a distribution plot
------------------------

.. currentmodule:: canopy.visualization.distribution_plot

You can compare a list of ``Field`` objects (for example, different runs) with :func:`make_distribution_plot`: 

.. code-block:: python

    cp.visualization.make_distribution_plot(fields=[model_a, model_b], 
                                          plot_type="box", 
                                          layers="Total"
                                          layers=["Abi_alb","Bet_pen","Bet_pub","Que_rob","C3_gr"],
                                          field_labels=["Unmodified", "Modified"],
                                          yaxis_label="NPP",
                                          unit="kgC/m²",
                                          title="plot_type = 'box'",
                                          palette="tab10",
                                          x_fig=10,
                                          y_fig=7
                                          )

.. image:: _static/comparison_plot.png
    :alt: Example static output
    :align: center
    :width: 60%

**You can check the different arguments available in the API reference:** :func:`make_distribution_plot`. 

This function can generate boxplot ("box"), strip plot, swarm plot, violin plot, boxen plot, point plot, bar plot, histogram plot ("hist"), KDE plot ("kde"), or ECDF plot ("ecdf") based on the ``plot_type`` argument.

In addition, you can use kwargs arguments from the `seaborn.catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ function (for categorical plots) or `seaborn.displot <https://seaborn.pydata.org/generated/seaborn.displot.html>`_ function (for distribution plots).

.. note::

    ``make_distribution_plot`` accepts any form of reduced ``Field`` objects. 
    
    You can reduce spatially, temporally, or both your ``Field`` objects beforehand.

Make a Taylor diagram
---------------------

.. currentmodule:: canopy.visualization.taylor_diagram

You can create a `Taylor diagram <https://doi.org/10.1029/2000JD900719>`_ to evaluate the performance of model data against observations using :func:`make_taylor_diagram`. A Taylor diagram is a specialized polar plot that visually summarizes how well different models reproduce observed data by displaying their correlation coefficient, normalized standard deviation, and root-mean-square error (RMSE) in a single plot.

.. code-block:: python

    import canopy as cp
    import canopy.visualization as cv

    # Import FLUXNET data (observations)
    fnet_data = cp.get_source('fluxnet/selection', 'fluxnet2015')
    # Import LPJ-GUESS run (model)
    lpjg_data = cp.get_source('lpjg_output', 'lpjguess', grid_type='sites')

    # Load fields
    mlath_fnet = fnet_data.load_field('LE_MM')
    maet_lpjg = lpjg_data.load_field('maet')

    # Processing FLUXNET and LPJ-GUESS data to create filtered fields
    # (see fluxnet_demo.ipynb for detailed processing steps)

    # Create Taylor diagram
    cv.make_taylor_diagram(
        fields=maet_lpjg_filtered,
        obs=maet_fnet_filtered,
        x_fig=7, y_fig=7
    )

.. image:: _static/taylor_diagram.png
    :alt: Example Taylor diagram output
    :align: center
    :width: 60%

**You can check the different arguments available in the API reference:** :func:`make_taylor_diagram`.

.. note::

    ``make_taylor_diagram`` requires an observations field to compare against model data. Currently, only FLUXNET data is usable as observations. For detailed information on how to use and process FLUXNET data, refer to the `FLUXNET demo notebook <https://codebase.helmholtz.cloud/canopy/notebooks/-/blob/main/fluxnet_demo.ipynb?ref_type=heads>`_.

You can also compare multiple model fields against observations by providing a list of fields:

.. code-block:: python

    cv.make_taylor_diagram(
        fields=[model_a, model_b, model_c],
        obs=observations,
        field_labels=["Model A", "Model B", "Model C"],
        gridop='av'
    )

In addition, you can use kwargs arguments from `geocat.viz.TaylorDiagram.add_model_set <https://geocat-viz.readthedocs.io/en/latest/user_api/generated/geocat.viz.taylor.TaylorDiagram.html#geocat.viz.taylor.TaylorDiagram.add_model_set>`_ to customize plot features such as `annotate_on`, `model_outlier_on`, etc.

Save figure and multiple plots in one figure
--------------------------------------------

So far, the examples provided generate figures using Matplotlib's interactive mode. However, if you are using **canopy** in a non-graphical environment (such as a terminal session) or wish to save your figures directly to files (e.g., as ``.png`` images), you can use the ``output_file`` argument in any visualization functions:

.. code-block:: python

    cp.visualization.make_simple_map(field=run_ssp1.cpool, layer="Total", output_file="ssp1_cpool_map.png")

This will save the generated map to ``ssp1_cpool_map.png`` instead of displaying it interactively.

.. currentmodule:: canopy.visualization.plot_functions

Similar to R's ``ggarrange``, you can combine several figures into a single image using :func:`multiple_figs`:

.. code-block:: python

    import canopy as cp
    import canopy.visualization as cv

    agpp = cp.Field.from_file("example_data/david/agpp.out")
    agpp_nolc = cp.Field.from_file("example_data/david/agpp_nolc.out")

    fig1 = cv.make_diff_map(field_a=agpp, field_b=agpp_nolc, layer="Total", 
                            return_fig=True)

    fig2 = cv.make_time_series(fields=[agpp,agpp_nolc], layers="Total", field_labels=["with", "without"], 
                               return_fig=True)

    fig3 = cv.make_distribution_plot(fields=[agpp,agpp_nolc], layers="Total", field_labels=["with", "without"], 
                                   return_fig=True)

    fig4 = cv.make_static_plot(field_a=agpp,field_b=agpp_nolc, layers="Total", 
                               return_fig=True)

    cv.multiple_figs([fig1, fig2, fig3, fig4], ncols=2, output_file="combined_figures.png")

This will arrange the four plots into a 2-column layout and save the combined image as ``combined_figures.png``. Make sure to generate each figure with ``return_fig=True`` so that the figure objects are returned instead of being displayed.

.. warning::

    The ``multiple_figs`` function manipulates image files, not the original figure objects, due to Cartopy limitations. As a result, some features—such as sharing a common legend across plots—are not supported in combined images.
