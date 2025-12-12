"""Registry functionality for grids and grid operations.

This module provides:

- A registry of different Grid types: A dictionary where the keys are string identifiers for each
  type of grid (e.g. `'sites'`, `'lonlat'`...) and the values are the corresponding subclass of Grid
  (e.g. `GridSites`, `GridLonLat`...)
- A registry of spatial reduction operations on the different grids: A dictionary where the keys are
  tuples of the form `(grid_type, operation, axis)`, and the values are the functions that perform the
  operation on the dataframe. In the key, `grid_type` is the string identifier of the grid (`'sites'`, `'lonlat'`...),
  `operation` is a string identifying the reduction operation, and `axis` is the axis name as it appears
  on the DataFrame index.

Examples
--------
Suppose we want to register a cartesian grid and its associated operations. The first step is to
create a new file in the grid/ folder. This file will contain the grid description and the supported
grid operations. Let's assume the file is grid/grid_xy.py. The code described below goes in this file.

We first define a new class, GridXY, inheriting from the Grid abstract base class. This class
will be registered with the string identifier passed to the register_grid class decorator:

.. code-block::

    from canopy.grid.grid_abc import Grid
    grid_type = 'xy' # String used to register this grid type.
    @register_grid(grid_type)
    class GridXY(Grid):
        super().__init__(axis0 = 'x', axis1 = 'y')
        ...

The Grid object's documentation details the mandatory abstract methods to implement.

we define the operations that are allowed on this grid, and register them with the
register_gridop decorator. This decorator will use the name of the function to form a key to
identify the operation. The name of the function must be of the format `operation_axis`.
For example, to register an averaging operation along the x axis, we would do:

.. code-block::

    @register_gridop(grid_type)
    def av_x(df: pd.DataFrame, grid: Grid) -> pd.DataFrame:
        ...

Note that grid operations have all the same signature.

Lastly, we need to add the new file, grid/grid_xy.py, to grid/__init.py__:

    import canopy.grid.grid_xy

If all went well, the new grid type and grid operations will be available. For example, the
following should work:

.. code-block::

    from canopy.field import Field
    field = Field.from_file(path, grid_type='xy')
    field.red_space('av', 'x', inplace=True)
    print(field)
"""

import pandas as pd
from typing import Callable, Type
from canopy.grid.grid_abc import Grid

# Grid type registry
_grids: dict[str, Type[Grid]] = {}

# Grid operations registry
_grid_operations: dict[tuple[str, str, str], Callable[[pd.DataFrame, Grid], pd.DataFrame]] = {}


def register_grid(grid_type: str) -> Callable:
    """Add decorated Grid subclass to the grid registry.

    Parameters
    ----------
    grid_type : str
        A string that identifies the type of Grid being registered.

    Returns
    -------
    A decorator to register the class with the provided identifier.
    """
    def decorator(cls: Type[Grid]) -> Type[Grid]:
        if grid_type in _grids:
            raise KeyError(f"Grid type {grid_type} is already registered.")
        else:
            _grids[grid_type] = cls
        return cls

    return decorator


def create_grid(grid_type: str, **kwargs) -> Grid:
    """Create an instance of a Grid object of the specified type.

    Parameters
    ----------
    grid_type : str
        The string identifying the grid type to create.
    **kwargs
        The keyword arguments are forwarded to the selected grid's constructor.

    Returns
    -------
    An instance of a subclass of Grid, specified by the grid_type parameter.
        
    Examples
    --------
    .. code-block::
    
        # Create a 'lonlat' type grid
        from canopy.grid import create_grid
        grid = create_grid('lonlat',
                           lon_min = -12.25, lon_max = 10.75, dlon = 0.5,
                           lat_min = 20.25, lat_max = 40.25, dlat = 0.5)
    """
    try:
        grid = _grids[grid_type](**kwargs)
    except KeyError:
        raise KeyError(f"Grid must be one of {[_ for _ in _grids]}")

    return grid


def get_grid(grid_type: str) -> Type[Grid]:
    """Get a reference to the uninstantiated Grid subclass of the specified type.

    Parameters
    ----------
    grid_type : str
        The grid type identifier (e.g., 'lonlat, 'sites')

    Returns
    -------
    The Grid subclass type registered under the specified grid_type string.
    """
    try:
        grid = _grids[grid_type]
    except KeyError:
        raise KeyError(f"Grid must be one of {[_ for _ in _grids]}")
    return grid


def get_grid_type(grid: Grid) -> str:
    """Get the grid type string identifier of the passed Grid instance.

    Parameters
    ----------
    grid : Grid
        An instance of a Grid subclass.
    
    Returns
    -------
    The grid type's string identifier.
    """
    for k, v in _grids.items():
        if isinstance(grid, v):
            return k
    raise ValueError("Grid type not found in registry.")


def register_gridop(grid_type: str):
    """Add decorated function to the grid operations registry.

    Parameters
    ----------
    grid_type : str
        The grid type string identifier.

    Returns
    -------
    A decorator to register a grid grid operation.

    Notes
    -----
    The decorator forms the registry key (the tuple `(grid_type, operation, axis)`) from the
    argument `grid_type`, supplied to the decorator, and the name of the decorated function,
    which must be of the form `operation_axis`.

    The name of the operation can be any string. But it should make sense and be consistent
    with all the other gridops (for example, if you want to register averaging operations for
    axes `'x'` and `'y'`, don't use `mean_x` and `av_y`).

    The names of the axes, however, must be the consistent with the names of the indices on
    the DataFrame that the operation is meant to act on.
    """
    def decorator(gop):
        op, axis = gop.__name__.split('_')
        key = (grid_type, op, axis)
        if key in _grid_operations:
            raise KeyError(f"Grid operation {key} is already registered.")
        else:
            _grid_operations[key] = gop
        return gop
    return decorator


def get_gridop(grid: str | Grid, gridop: str, axis: str) -> Callable[[pd.DataFrame, Grid], pd.DataFrame]:
    """Retrieve a grid operation function from the registry.
    
    Parameters
    ----------
    grid : str | Grid
        An instance of the Grid object describing the grid type.
    gridop : str
        The string identifying the grid operation (e.g., 'av' for average).
    axis : str
        The name of the axis along which the operation is performed (e.g. 'lon')

    Returns
    -------
    The function that performs the selected grid operation.
    """
    if isinstance(grid, Grid):
        grid_type = get_grid_type(grid)
    elif isinstance(grid, str):
        grid_type = grid
    try:
        return _grid_operations[(grid_type, gridop, axis)]
    except KeyError:
        raise KeyError(f"Operation '{gridop}' on axis '{axis}' is not defined for grid type '{grid_type}'.")

