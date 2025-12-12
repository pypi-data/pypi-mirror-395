.. _data_model:

The canopy data model
=====================

The Field object
----------------

.. currentmodule:: canopy.core.field

In **canopy**, land surface data from different sources is cast onto a common, self-describing data object called a :class:`Field`. A :class:`Field` is meant to contain/describe one single quantity (e.g., stored C, GPP...), which can have multiple *layers* (e.g, for GPP the different layers could represent different PFTs, for stored C they could be the different carbon pools...) A :class:`Field` is essentially made up of:

.. currentmodule:: canopy.grid.grid_abc

* The data, stored in a **multi-indexed pandas DataFrame**. The multi-index has three levels: the first two are spatial coordinates (`lon` and `lat`), and the third one is time, encoded as `pandas Period objects <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Period.html>`_ .
* A :class:`Grid` object describing the grid associated to the data.
* A metadata dictionary, holding information such as the name and the units of the field.
* An interface to facilitate basic manipulation operations, as well as input/output functionalities (e.g. save the data to different formats).



.. note::

  **Canopy** borrows some names and concepts from `DGVM tools <https://github.com/MagicForrest/DGVMTools>`_, a similarly-purposed R package developed by Matthew Forrest, which inspired us to start developing **canopy**.


The Grid object
---------------

.. currentmodule:: canopy.grid.grid_abc

A :class:`Grid` object contains information about the type of grid specific data may be associated with. The grid type determines how spatial reduction operations are performed on the data. It is also useful to, for example, produce spatial graphics of the data. Currently, supported grids include

* ``lonlat``: A geographical grid with constant spacing along each axis. Spatial reduction operations on this grid are described here: :ref:`lonlat_gridops`.
* ``sites``: A Grid object describing the absence of a proper grid, meant to store specific sites individually. Spatial operations are only allowed on both axes (e.g., mean across sites), but not on longitude or latitude only.


Creating a Field
----------------

.. currentmodule:: canopy.core.field

In order to gain insight into the structure of a :class:`Field` object, we will create one from scratch. We encourage you to try this example on your own. This is, of course, a dummy example with randomly generated data. Normally, the Field is created by data-reader functions from model output files or from an observational dataset. See :ref:`reading_files` and :ref:`data_sources`.
   
First we need a multi-indexed DataFrame. Let's create one purporting to hold plant annual transpiration (in mm) by PFT, in mm, for a small 2x2 gridcells domain between 1999 and 2001 on a **lonlat** grid.

.. code-block:: python

   import pandas as pd
   import numpy as np
   import canopy as cp

   pfts = ['Conifer', 'Broadleaf', 'Grass', ]
   years = [pd.Period(year=x, freq='Y') for x in [1999, 2000, 2001]]
   lons = [13.25, 13.75]
   lats = [40.75, 41.25]
   index = pd.MultiIndex.from_product([lons, lats, years], names=['lon', 'lat', 'time'])
   np.random.seed(10)
   data = 200*np.random.random(len(index)*len(pfts)).reshape([len(index), len(pfts)])
   data = pd.DataFrame(data, index=index, columns=pfts)
   print(data)

.. code-block:: console

                         Conifer   Broadleaf       Grass
    lon   lat   time                                    
    13.25 40.75 1999  154.264129    4.150390  126.729647
                2000  149.760777   99.701402   44.959329
                2001   39.612573  152.106142   33.822167
          41.25 1999   17.667963  137.071964  190.678669
                2000    0.789653  102.438453  162.524192
                2001  122.505213  144.351063   58.375214
    13.75 40.75 1999  183.554825  142.915157  108.508874
                2000   28.434010   74.668152  134.826723
                2001   88.366635   86.802799  123.553396
          41.25 1999  102.627649  130.079436  120.207791
                2000  161.044639  104.329430  181.729776
                2001   63.847218   18.091870   60.140011

.. currentmodule:: canopy.grid.grid_abc

Now, let's create a :class:`Grid` object associated with this data. The grid specifications can be inferred from the DataFrame of interests by invoking the :meth:`Grid.from_frame` constructor as follows:

.. code-block:: python

   grid = cp.grid.get_grid('lonlat').from_frame(data)
   print(grid)

.. code-block:: console

    Longitude: 
    13.25 to 13.75 (step: 0.5)
    Latitude: 
    40.75 to 41.25 (step: 0.5)


Finally, we construct the Field object. It looks like not much is going on, but the Field constructor will verify the DataFrame to ensure that the data conforms to the **canopy** data model described above.

.. code-block:: python

   # Annual transpiration
   aaet = cp.Field(grid, data)
   print(aaet)

.. code-block:: console

   Data
   ----
   name: [no name]
   units: [no units]
   description: [no description]

   Grid: lonlat
   ------------
   Longitude: 
   13.25 to 13.75 (step: 0.5)
   Latitude: 
   40.75 to 41.25 (step: 0.5)

   Time series
   -----------
   Span: 1999-01-01 00:00:00 - 2001-12-31 23:59:59.999999999
   Frequency: Y-DEC

   History
   -------

To examine the Field's data, one can use:

.. code-block:: python

   print(f"Field's layers: {aaet.layers}")
   print("Field's data:")
   print(aaet.data)


.. code-block:: console

   Field's layers: ['Conifer', 'Broadleaf', 'Grass']
   Field's data:
                        Conifer   Broadleaf       Grass
   lon   lat   time                                    
   13.25 40.75 1999  154.264129    4.150390  126.729647
               2000  149.760777   99.701402   44.959329
               2001   39.612573  152.106142   33.822167
         41.25 1999   17.667963  137.071964  190.678669
               2000    0.789653  102.438453  162.524192
               2001  122.505213  144.351063   58.375214
   13.75 40.75 1999  183.554825  142.915157  108.508874
               2000   28.434010   74.668152  134.826723
               2001   88.366635   86.802799  123.553396
         41.25 1999  102.627649  130.079436  120.207791
               2000  161.044639  104.329430  181.729776
               2001   63.847218   18.091870   60.140011


Notice that our created-by-hand Field does not yet have metadata. In normal **canopy** workflow, the metadata is added upon reading from disk by the reader function or the `Source` object (see :ref:`data_manipulation`), as long as the data source is registered. Metadata can be added or reset manually as follows:

.. code-block:: python

   # Fails because the entry 'name' already exists by default in every Field.
   #aaet.add_md('name', 'aaet')
   # For existing entries, like the three default ones, we use Field.set_md()
   aaet.set_md('name', 'aaet')
   aaet.set_md('description', 'Annual transpiration by PFT')
   aaet.set_md('units', 'mm')
   # We can add any metadata we want with Field.add_md()
   aaet.add_md('scenario', 'SSP1-2.6')
   # We can also manually add entries to the history log
   aaet.log('Field created manually with bogus data')
   print(aaet)

.. code-block:: console

   Data
   ----
   name: aaet
   units: mm
   description: Annual transpiration by PFT
   scenario: SSP1-2.6

   Grid: lonlat
   ------------
   Longitude: 
   13.25 to 13.75 (step: 0.5)
   Latitude: 
   40.75 to 41.25 (step: 0.5)

   Time series
   -----------
   Span: 1999-01-01 00:00:00 - 2001-12-31 23:59:59.999999999
   Frequency: Y-DEC

   History
   -------
   2025-05-12 19:20:48: Field created manually with bogus data

