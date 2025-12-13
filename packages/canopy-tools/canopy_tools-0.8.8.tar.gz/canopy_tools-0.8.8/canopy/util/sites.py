"""
Utilities for site-based fields
"""
import numpy as np
import pandas as pd
from canopy.core.field import Field
from canopy.grid import get_grid_type, get_grid


def check_grid_is_sites(field: Field):
    if get_grid_type(field.grid) != 'sites':
        raise ValueError(f"Grid must be of type 'sites' (passed: {get_grid_type(field.grid)}).")


def sel_sites(field: Field, sites: list[tuple[int | float, int | float]], invert: bool = False) -> Field:
    """
    Select sites from a Field

    Parameters
    ----------
    field : Field
        The field to select the sites from
    sites : list[tuple[int | float, int | float]]
        A list of coordinates
    invert : bool
        Invert selection: select sites not in the 'sites' list

    Returns
    -------
    A new Field with the selected sites
    """

    # TODO: select sites by NAME -> GridSites should include names
    check_grid_is_sites(field)

    ax0 = field.data.index.get_level_values(0)
    ax1 = field.data.index.get_level_values(1)

    spatial_index = pd.MultiIndex.from_arrays([ax0, ax1])
    mask = spatial_index.isin(sites)
    if invert:
        mask = np.logical_not(mask)

    data = field.data.loc[mask]
    if data.empty:
        grid = get_grid('empty').from_frame(data)
    else:
        grid = get_grid('sites').from_frame(data)

    field_new = Field(data, grid)

    return field_new
