"""Grid associated to site-based data.

This Grid type actually represents the absence of a grid. It is meant to describe a
collection of unrelated sites or locations. Spatial reduction operations are only defined
for both axes (axis = 'both').
"""

import numpy as np
import pandas as pd
import copy
from typing import Optional, Sequence, Tuple, SupportsFloat
from canopy.grid.grid_abc import Grid
from canopy.grid.grid_empty import GridEmpty
from canopy.grid.registry import register_grid, register_gridop, get_gridop
import random

grid_type = 'sites'

def _setindex(grid: 'GridSites', new_index: Sequence):
    grid.sites.index = new_index
    grid.sites.index.name = "Key"
    grid.sites.sort_index(inplace=True)

@register_grid(grid_type)
class GridSites(Grid):
    """A subclass of Grid used to represent a collection of sites.

    Parameters
    ----------
    sites
        The site locations are arranged in rows. For example:
        .. code-block::
        
            [[12.25, -4.75],
             [-27.75, 45.25],
             [-50.25, 73.25]]
    axis0 : str
        Name of first axis (default: 'lon').
    axis1 : str
        Name of second axis (default: 'lat').
    """

    def __init__(self, sites: np.ndarray | None, names: Sequence[str | None] | None = None, axis0: str = 'lon', axis1: str = 'lat', gridop: str | None = None) -> None:
        super().__init__(grid_type, axis0=axis0, axis1=axis1)

        if gridop is None and sites is None:
            raise ValueError("'sites' and 'gridop' cannot be both None")

        if sites is None:
            self.sites = None
            get_gridop(self.grid_type, gridop, 'both') # KeyError if gridop doesn't exist
            self.axis_gridop['both'] = gridop
            self.axis_gridop[self.axis_names[0]] = gridop
            self.axis_gridop[self.axis_names[1]] = gridop
        else:
            self.axis_gridop['both'] = None
            if not isinstance(sites, np.ndarray):
                raise ValueError("'sites' must be a numpy array")
            if sites.shape[1] != 2:
                raise ValueError("'sites' must have exactly two columns, corresponding to the spatial axes")
            if len(sites) < 1:
                raise ValueError("'sites' must have at least one row")
            sites = sites.astype(float) # Will fail if not numbers
            index = []
            if names is None:
                for site in sites:
                    index.append(tuple(site))
            else:
                if len(sites) != len(names):
                    raise ValueError("The number of rows of the 'sites' array and the length of the 'names' list must be equal.")
                for name, site in zip(names, sites):
                    index.append(str(name) if not name is None else tuple(site))

            self.sites = pd.DataFrame(sites, dtype=float, columns=[axis0, axis1])
            _setindex(self, index)


    @classmethod
    def from_frame(cls, df):
        """Create a GridSites instance from a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            A pandas DataFrame with a valid format (see Field documentation).

        Returns
        -------
        An instance of the grid subclass.
        """
        index = df.index
        axis0, axis1 = index.names[:2]
        sites = np.array(list(index.droplevel('time').drop_duplicates().values))
        return cls(axis0 = axis0, axis1 = axis1, sites=sites)


    def to_txt(self, fname: str, sep: str = ' ', randomize: bool = False) -> None:
        lines = []
        for key, coords in zip(self.sites.index, self.sites.values):
            coord0 = str(coords[0])
            coord1 = str(coords[1])
            line = coord0 + sep + coord1
            if isinstance(key, str):
                line += sep + key
            line += '\n'
            lines.append(line)

        if randomize:
            random.shuffle(lines)

        with open(fname, 'w') as f:
            f.writelines(lines)


    def get_reduced_grid(self, gridop: str, axis: str) -> Grid:
        """Create a new grid, reduced according to the parameters

        Parameters
        ----------
        gridop : str
            The reduction operation
        axis : str
            The axis to be reduced

        Returns
        -------
        An instance of GridSites
        """
        get_gridop(self.grid_type, gridop, axis) # Will raise a KeyError if it doesn't exist
        return GridSites(sites = None, gridop = gridop, axis0 = self.axis_names[0], axis1 = self.axis_names[1])


    def get_sliced_grid(self,
                        axis0_slice: Optional[tuple[float,float]] = None,
                        axis1_slice: Optional[tuple[float,float]] = None) -> Grid:
        """Create a new grid, sliced according to the parameters.

        Parameters
        ----------
        axis0_slice : tuple[float,float]
            Specifies an interval on axis0.
        axis1_slice : tuple[float,float]
            Specifies an interval on axis1.

        Returns
        -------
        An instance of the grid subclass.
        """
        sites = self.sites
        if axis0_slice is not None:
            x0min, x0max = axis0_slice
            ax0 = self.axis_names[0]
            sites = sites[(sites[ax0] >= x0min) & (sites[ax0] <= x0max)]
        if axis1_slice is not None:
            x1min, x1max = axis1_slice
            ax1 = self.axis_names[1]
            sites = sites[(sites[ax1] >= x1min) & (sites[ax1] <= x1max)]

        if sites.empty:
            return GridEmpty()
        else:
            names = [x if isinstance(x,str) else None for x in sites.index]
            return GridSites(sites.values, names = names, axis0 = self.axis_names[0], axis1 = self.axis_names[1])
        

    def is_compatible(self, other) -> bool:

        if self.grid_type != other.grid_type:
            return False

        if self.axis_gridop != other.axis_gridop:
            return False

        return True


    def __add__(self, other):

        if not self.is_compatible(other):
            raise ValueError("Non-compatible grids cannot be aggregated.")

        if self.is_reduced('both'):
            raise ValueError("Reduced grids cannot be added.")

        sites = pd.concat([self.sites, other.sites])
        sites = sites[~sites.index.duplicated(keep='first')]
        names = [x if isinstance(x,str) else None for x in sites.index]

        return GridSites(sites.values, names=names, axis0=self.axis_names[0], axis1=self.axis_names[0])


    def __repr__(self) -> str:
        repr_str = [super().__repr__()]
        if self.is_reduced('both'):
            repr_str.append(f"Grid is reduced (gridop: '{self.axis_gridop['both']}').")
        else:
            repr_str.append(f"Gridlist:\n{str(self.sites)}")
        return '\n'.join(repr_str)


    def __str__(self) -> str:
        return self.__repr__()


    def assign_names(self, names_dict: dict[Tuple[SupportsFloat],str], atol=1.e-6, rtol=0) -> None:
        """Assign names to sites based on their coordinates

        Parameters
        ----------
        names_dict: dict
            A dictionary whose keys are tuples representing the coordinates of a site,
            and whose values (strings) are the names to assign to those sites
        atol: float
            Absolute tolerance for the coordinate comparison, as in numpy's allclose function.
        rtol: float
            Relative tolerance for the coordinate comparison, as in numpy's allclose function.
        """
        named_coords = []
        for k, v in names_dict.items():
            coord1 = np.array(k, dtype=float).flatten()
            if coord1.size != 2:
                raise ValueError(f"Key {k} cannot be interpreted as a coordinate")
            named_coords.append(coord1)

        new_index = []
        for old_key, coord2 in zip(self.sites.index, self.sites.values):
            for coord1, name in zip(named_coords, names_dict.values()):
                found = False
                if np.allclose(coord1, coord2, atol=atol, rtol=rtol):
                    new_index.append(str(name))
                    found = True
                    break
            if not found:
                new_index.append(old_key)

        _setindex(self, new_index)
                    

@register_gridop(grid_type)
def av_both(df: pd.DataFrame, grid: Grid) -> pd.DataFrame:
    """Spatially average the data.
    
    On this 'grid', all sites count the same for the average.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : GridSites
        A GridSites object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['time']
    df_red = df.groupby(group_levels).mean()
    #df_red = _restore_index(df_red, 'av')

    return df_red


@register_gridop(grid_type)
def sum_both(df: pd.DataFrame, grid: Grid) -> pd.DataFrame:
    """Spatially aggregate the data.

    On this 'grid', all sites count the same for the sum.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame whose data is to be aggregated.
    grid : GridSites
        A GridSites object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['time']
    df_red = df.groupby(group_levels).sum()
    #df_red = _restore_index(df_red, 'sum')

    return df_red

