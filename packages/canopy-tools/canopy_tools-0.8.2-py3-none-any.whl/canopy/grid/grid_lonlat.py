"""Grid with longitude and latitude coordinates.

This grid type has longitude and latutide coordinates. The longitude and latitude intervals are
constant, although they can be different (i.e. dlon != dlat). Reduction operations on this grid
are weighted according to their position on the grid.
"""
import pandas as pd
import numpy as np
import copy
from typing_extensions import Self
from canopy.grid.grid_abc import Grid
from canopy.grid.registry import register_grid, register_gridop, get_gridop
from canopy.core.constants import *


grid_type = 'lonlat'

# ---------------
# GRID DEFINITION
# ---------------

COORD_BOUNDARIES = {'lon': -180., 'lat': -90.}

@register_grid(grid_type)
class GridLonLat(Grid):
    """A Grid type representing a longitude-latitude grid with constant increments."""

    def __init__(self,
                 lon_min: float = np.nan, lon_max: float = np.nan, dlon: float = np.nan,
                 lat_min: float = np.nan, lat_max: float = np.nan, dlat: float = np.nan,
                 lon_gridop: str | None = None, lat_gridop: str | None = None) -> None:
        """
        Parameters
        ----------
        lon_min : float
            Smallest longitude of the represented domain (degrees).
        lon_max : float
            Largest longitude of the represented domain (degrees).
        dlon : float
            Increment in longitude (degrees). 
        lat_min : float
            Smallest latitude of the represented domain (degrees).
        lat_max : float
            Largest latitude of the represented domain (degrees).
        dlat : float
            Increment in latitude (degrees). 
        lon_gridop : str | None
            Grid reduction operation along lon axis. If not None, values of lon_min, lon_max, and dlon are ignored.
        lat_gridop : str | None
            Grid reduction operation along lat axis. If not None, values of lat_min, lat_max, and dlat are ignored.
        """

        if lon_gridop is not None:
            try:
                get_gridop(grid_type, lon_gridop, 'lon')
            except:
                raise ValueError(f"Operation '{lon_gridop}' not registered for axis 'lon'")
        if lat_gridop is not None:
            try:
                get_gridop(grid_type, lat_gridop, 'lat')
            except:
                raise ValueError(f"Operation '{lat_gridop}' not registered for axis 'lat'")

        # TODO: this to ABC?
        if lon_gridop is not None and lat_gridop is not None and lon_gridop != lat_gridop:
            raise ValueError(f"Grid operation must be the same on both axes")

        super().__init__(grid_type, axis0='lon', axis1='lat', gridop0=lon_gridop, gridop1=lat_gridop)
        self.axis_gridop['both'] = None

        self.xmin = {}
        self.xmax = {}
        self.dx = {}
        self.axes = {}

        param_xmin = {'lon': lon_min, 'lat': lat_min}
        param_xmax = {'lon': lon_max, 'lat': lat_max}
        param_dx = {'lon': dlon, 'lat': dlat}
        param_gridop = {'lon': lon_gridop, 'lat': lat_gridop}

        for axis_name in self.axis_names:
            if param_gridop[axis_name] is None:
                if param_dx[axis_name] <= 0:
                    raise ValueError(f"d{axis_name} must be greater than 0.")
                if param_xmin[axis_name] > param_xmax[axis_name]:
                    raise ValueError(f"{axis_name}_min must be smaller or equal than {axis_name}_max.")
                self.axes[axis_name] = np.arange(param_xmin[axis_name],
                                                 param_xmax[axis_name]+0.5*param_dx[axis_name],
                                                 param_dx[axis_name])
                self.xmin[axis_name] = param_xmin[axis_name]
                self.xmax[axis_name] = param_xmax[axis_name]
                self.dx[axis_name] = param_dx[axis_name]
            else:
                self.axes[axis_name] = np.empty(0)
                self.xmin[axis_name] = np.nan
                self.xmax[axis_name] = np.nan
                self.dx[axis_name] = np.nan


    def to_txt(self, fname: str, sep: str = ' ', randomize: bool = False) -> None:
        raise NotImplementedError


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
        An instance of GridLonLat
        """
        grid = copy.deepcopy(self)
        for an in grid.axis_names:
            if axis == an or axis == 'both':
                grid.axis_gridop[an] = gridop
                grid.axes[an] = np.empty(0)
                grid.dx[an] = np.nan
                grid.xmin[an] = np.nan
                grid.xmax[an] = np.nan

        return grid


    def get_sliced_grid(self, axis0_slice: tuple[float,float] | None, axis1_slice: tuple[float,float] | None) -> Grid:
        """Create a new grid, sliced according to the parameters.

        Parameters
        ----------
        axis0_slice : tuple[float, float]
            Specifies an interval on longitude.
        axis1_slice : tuple[float, float]
            Specifies an interval on latitude.

        Returns
        -------
        An instance of the grid subclass.
        """
        xmin = {ax: np.nan for ax in self.axis_names}
        xmax = {ax: np.nan for ax in self.axis_names}
        dx = {ax: np.nan for ax in self.axis_names}
        gridop = {ax: None for ax in self.axis_names}
        for axis_name, axis_slice in zip(self.axis_names, [axis0_slice, axis1_slice]):
            if self.is_reduced(axis_name):
                gridop[axis_name] = self.axis_gridop[axis_name]
                continue
            if axis_slice is None:
                xmin[axis_name] = self.xmin[axis_name]
                xmax[axis_name] = self.xmax[axis_name]
                dx[axis_name] = self.dx[axis_name]
            else:
                xmin[axis_name], xmax[axis_name] = axis_slice
                xmin[axis_name] = self.axes[axis_name][self.axes[axis_name] >= xmin[axis_name]].min()
                xmax[axis_name] = self.axes[axis_name][self.axes[axis_name] <= xmax[axis_name]].max()
                dx[axis_name] = self.dx[axis_name]

        return GridLonLat(lon_min = xmin['lon'], lon_max = xmax['lon'], dlon = dx['lon'],
                          lat_min = xmin['lat'], lat_max = xmax['lat'], dlat = dx['lat'],
                          lon_gridop = gridop['lon'], lat_gridop = gridop['lat'])


    @classmethod
    def from_frame(cls, df: pd.DataFrame) -> Self: 
        """Create a GridLonLat instance from a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            A pandas DataFrame with a valid format (see Field documentation).

        Returns
        -------
        An instance of the grid subclass.
        """
        lon = np.sort(df.index.unique(level='lon').values)
        lat = np.sort(df.index.unique(level='lat').values)

        xmin = {}
        xmax = {}
        dx = {}
        gridop: dict['str', 'str' | None] = {}

        for axis_name, axis_values in zip(['lon', 'lat'], [lon, lat]):
            if len(axis_values) == 1:
                # Is it a reduced DataFrame?
                if isinstance(axis_values[0], str):
                    try:
                        get_gridop(grid_type, axis_values[0], axis_name)
                    except KeyError:
                        raise ValueError(f"Axis value '{axis_values[0]}' is not a spatial reduction.")
                    xmin[axis_name] = np.nan
                    xmax[axis_name] = np.nan
                    dx[axis_name] = np.nan
                    gridop[axis_name] = axis_values[0]
                else:
                    raise ValueError(f"Axis '{axis_name}' must be of size larger than 1.")
            else:
                xmin[axis_name] = axis_values.min()
                xmax[axis_name] = axis_values.max()
                dx[axis_name] = (axis_values[1:] - axis_values[:-1]).min()
                gridop[axis_name] = None

        return cls(lon_min=xmin['lon'], lon_max=xmax['lon'], dlon=dx['lon'],
                   lat_min=xmin['lat'], lat_max=xmax['lat'], dlat=dx['lat'],
                   lon_gridop=gridop['lon'], lat_gridop=gridop['lat'])


    def __add__(self, other):

        if not self.is_compatible(other):
            raise ValueError("Field grids are not compatible.")

        if self.is_reduced('lon') or self.is_reduced('lat'):
            raise NotImplementedError('Reduced grids cannot be combined (for now).')

        if self.is_reduced('lon'):
            lon_min = np.nan
            lon_max = np.nan
            dlon = np.nan
            lon_gridop = self.axis_gridop['lon']
        else:
            lon_min = min(self.xmin['lon'], other.xmin['lon'])
            lon_max = max(self.xmax['lon'], other.xmax['lon'])
            dlon = self.dx['lon']
            lon_gridop = None

        if self.is_reduced('lat'):
            lat_min = np.nan
            lat_max = np.nan
            dlat = np.nan
            lat_gridop = self.axis_gridop['lat']
        else:
            lat_min = min(self.xmin['lat'], other.xmin['lat'])
            lat_max = max(self.xmax['lat'], other.xmax['lat'])
            dlat = self.dx['lat']
            lat_gridop = None

        return GridLonLat(lon_min=lon_min, lon_max=lon_max, dlon=self.dx['lon'],
                          lat_min=lat_min, lat_max=lat_max, dlat=self.dx['lat'])


    def __repr__(self) -> str:
        repr_str = [super().__repr__()]
        if self.is_reduced('lon') or self.is_reduced('both'):
            repr_str.append(f"Longitude: reduced (gridop = {self.axis_gridop['lon']})")
        else:
            repr_str.append(f"Longitude: {self.lon_min} to {self.xmax['lon']} (step: {self.dx['lon']})")
        if self.is_reduced('lat') or self.is_reduced('both'):
            repr_str.append(f"Latitude: reduced (gridop = {self.axis_gridop['lat']})")
        else:
            repr_str.append(f"Latitude: {self.xmin['lat']} to {self.xmax['lat']} (step: {self.dx['lat']})")

        return '\n'.join(repr_str)
    

    def __str__(self) -> str:
        return self.__repr__()


    def is_compatible(self, other: Grid) -> bool:

        if type(other) is not GridLonLat:
            return False

        for axis in ['lon', 'lat']:
            if self.axis_gridop[axis] != other.axis_gridop[axis]:
                return False

            if self.is_reduced(axis):
                continue
            
            if self.dx[axis] != other.dx[axis]:
                return False

            x0_self = self.xmin[axis] - int((self.xmin[axis] - COORD_BOUNDARIES[axis])/self.dx[axis])*self.dx[axis]
            x0_other = other.xmin[axis] - int((other.xmin[axis] - COORD_BOUNDARIES[axis])/other.dx[axis])*other.dx[axis]

            if not np.isclose(x0_self, x0_other, rtol=1.e-7):
                return False

        return True


    @property
    def lon(self):
        return self.axes['lon']

    @property
    def dlon(self):
        return self.dx['lon']

    @property
    def lon_min(self):
        return self.xmin['lon']

    @property
    def lon_max(self):
        return self.xmax['lon']

    @property
    def lat(self):
        return self.axes['lat']

    @property
    def dlat(self):
        return self.dx['lat']

    @property
    def lat_min(self):
        return self.xmin['lat']

    @property
    def lat_max(self):
        return self.xmax['lat']


# ---------------
# GRID OPERATIONS
# ---------------

@register_gridop(grid_type)
def av_lon(df: pd.DataFrame, grid: GridLonLat) -> pd.DataFrame:
    """Average data along the longitude axis.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : Grid
        A GridLonLat object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['lat', 'time']
    df_red = df.groupby(group_levels).mean()

    return df_red


@register_gridop(grid_type)
def av_lat(df: pd.DataFrame, grid: GridLonLat) -> pd.DataFrame:
    """Average data along the latitude axis.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : GridLonLat
        A GridLonLat object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['lon', 'time']
    df_red = df.groupby(group_levels).mean()

    return df_red


@register_gridop(grid_type)
def av_both(df: pd.DataFrame, grid: GridLonLat) -> pd.DataFrame:
    """Average data across the whole domain.

    Each gridcell value is weighted by its corresponding area element:
        da = EARTH_RADIUS**2*dlon*dlat*cos(lat),

    where the angles are in radians.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : GridLonLat
        A GridLonLat object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['time']
    weights = np.cos(df.index.get_level_values('lat').to_numpy()*DEG_TO_RAD)
    df_red = df.multiply(weights, axis='index')
    df_red['w'] = weights
    df_red = df_red.groupby(group_levels).sum()
    df_red = df_red.div(df_red['w'], axis='index')
    df_red.drop('w', axis=1, inplace=True)

    return df_red


@register_gridop(grid_type)
def sum_lon(df: pd.DataFrame, grid: GridLonLat) -> pd.DataFrame:
    """Aggregate data along the longitude axis.

    Parameters
    ----------
    df : pd.DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : GridLonLat
        A GridLonLat object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    if grid.is_reduced('lat'):
        raise ValueError("Cannot calculate 'sum' along 'lon' axis on a field with a reduced 'lat' axis.")
    group_levels = ['lat', 'time']
    weights = EARTH_RADIUS*grid.dlon*DEG_TO_RAD*np.cos(df.index.get_level_values('lat').to_numpy()*DEG_TO_RAD)
    df_red = df.multiply(weights, axis='index').groupby(group_levels).sum()

    return df_red


@register_gridop(grid_type)
def sum_lat(df: pd.DataFrame, grid: GridLonLat) -> pd.DataFrame:
    """Aggregate data along the latitude axis.

    Parameters
    ----------
    df : pandas DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : GridLonLat
        A GridLonLat object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['lon', 'time']
    df_red = (EARTH_RADIUS*grid.dlat*DEG_TO_RAD*df).groupby(group_levels).sum()

    return df_red


@register_gridop(grid_type)
def sum_both(df: pd.DataFrame, grid: GridLonLat) -> pd.DataFrame:
    """Aggregate data across the whole domain.

    Each gridcell value is weighted by its corresponding area element:
        da = EARTH_RADIUS**2*dlon*dlat*cos(lat),
        
    where the angles are in radians.

    Parameters
    ----------
    df: pandas DataFrame
        The pandas DataFrame whose data is to be averaged.
    grid : GridLonLat
        A GridLonLat object.

    Returns
    -------
    A reduced pandas DataFrame
    """
    group_levels = ['time']
    weights = EARTH_RADIUS**2*DEG_TO_RAD**2*grid.dlat*grid.dlon*np.cos(df.index.get_level_values('lat').to_numpy()*DEG_TO_RAD)
    df_red = df.multiply(weights, axis='index')
    df_red = df_red.groupby(group_levels).sum()

    return df_red

