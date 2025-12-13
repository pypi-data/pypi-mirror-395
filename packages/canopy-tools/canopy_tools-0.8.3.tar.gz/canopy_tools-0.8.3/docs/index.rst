.. canopy documentation master file, created by
   sphinx-quickstart on Wed Apr  2 11:25:16 2025.

Welcome to canopy's documentation!
==================================

**canopy** is an open source python project designed to support research in the field of vegetation dynamics and climate modelling by providing tools for **analysing** and **visualising** Dynamic Global Vegetation Model (**DGVM**) and Land Surface Models (**LSM**) **outputs**.

To find our gallery website, go to https://canopy.imk-ifu.kit.edu/

The gallery is an **interactive website** showcasing figures created with **canopy**, where each image links to the code that generated it. Users can also submit their own canopy code (Python or JSON) and figure to be featured, helping build a collection of examples that make learning canopy easy and inspiring.

Example data
------------

All the data files used in this documentation can be downloaded from `Zenodo <https://zenodo.org/records/17601589>`_. 

To use the example data, download the archive and unpack it in your working directory:

.. code-block:: bash

   tar -xzf example_data.tar.gz

After unpacking, you will have an ``example_data`` folder containing all the data files. Make sure to run the examples from the directory where you unpacked the data, or adjust the file paths accordingly.

.. toctree::
   :maxdepth: 2

   quick_start
   data_model
   data_manipulation
   visualization
   json
   technical_documentation
   API_reference
