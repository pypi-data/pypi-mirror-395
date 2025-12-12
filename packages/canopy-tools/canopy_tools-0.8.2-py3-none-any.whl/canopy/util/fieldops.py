import numpy as np
import pandas as pd
import regionmask
import copy
from typing import Optional, Hashable, Type, cast
from canopy import RedSpec, Raster, Field
from canopy.grid import get_grid_type
from pandas.api.types import is_string_dtype
from canopy.util.checks import check_spatial_coords_match

# Make raster
# -----------
def gcidx(x: float, xmin: float, dx: float) -> int:
    return int((x-(xmin-0.5*dx))/dx)
get_coord_index = np.vectorize(gcidx)

def make_raster(field: Field, layer: str) -> Raster:
    """Produce a Raster object from a Field

    Parameters
    ----------
    field : Field
        The field object from which to create the Raster
    layer : str
        The field layer to rasterize
    """

    data = field.data
    grid = field.grid

    # This is to avoid mypy errors.
    # TODO: find a better solution. Maybe Rasterizable Grid?
    grid_type = get_grid_type(grid) 
    if grid_type != 'lonlat':
        raise ValueError("make_raster currently supports only 'lonlat' grid type.")
    from canopy.grid.grid_lonlat import GridLonLat
    grid  = cast(GridLonLat, grid)

    ilon = get_coord_index(data.index.get_level_values('lon').to_numpy(), grid.lon_min, grid.dlon)
    ilat = get_coord_index(data.index.get_level_values('lat').to_numpy(), grid.lat_min, grid.dlat)

    # Create Raster
    xx, yy = np.meshgrid(grid.lon, grid.lat)

    vmap = np.empty([grid.lat.size, grid.lon.size], dtype=float)
    vmap[:] = np.nan
    dtype = data.dtypes[layer]
    if is_string_dtype(dtype):
        labels = dict(enumerate(data[layer].unique()))
        labels_r = {v: k for (k, v) in labels.items()}
        values = np.vectorize(labels_r.get)(data[layer].values)
        vmap[ilat,ilon] = values
    else:
        labels = None
        vmap[ilat,ilon] = data[layer].values
    
    return Raster(xx, yy, vmap, labels)


# Make lines
# ----------
def make_lines(field: Field, axis: str = 'time') -> pd.DataFrame:
    """Create a pandas DataFrame with the field's data unstacked along the specified axis

    This DataFrame is much easier to use to plot lines (e.g. with df.plot())

    Parameters
    ----------
    field : Field
        The field from which to create the DataFrame
    axis: str
        The axis along which to unstack the data
    """

    df = field._data.copy()
                         
    if field._grid.is_reduced('lon'):
        df.index = df.index.droplevel('lon')
    if field._grid.is_reduced('lat'):
        df.index = df.index.droplevel('lat')

    levels = cast(Hashable, [x for x in df.index.names if not x == axis])
    return cast(pd.DataFrame, df.unstack(level=levels))


# Concatenate two fields
# ----------------------

def concat2(field1: Field, field2: Field) -> Field:
    """Concatenate two fields along the time axis.

    The fields must have matching grids and compatible ('concatenable') time series.

    Parameters
    ----------
    field1 : Field
        The first field to concatenate
    field2 : Field
        The second field to concatenate

    Returns
    -------
    A Field object with the concatenated data
    """

    # These will always be MultiIndex
    index1 = cast(pd.MultiIndex, field1._data.index)
    index2 = cast(pd.MultiIndex, field2._data.index)
    columns1 = field1._data.columns.sort_values()
    columns2 = field2._data.columns.sort_values()

    # Check that fields have the same layers
    try:
        layers_match = (columns1 == columns2).all()
    # If layer number doesn't match, the above comparison will fail
    except ValueError:
        layers_match = False
    if not layers_match:
        raise ValueError(f"The fields have different layers (field1: {columns1}; field2: {columns2}).")

    # Check that temporal frequencies match
    freq1 = index1.levels[-1].dtype
    freq2 = index2.levels[-1].dtype
    if freq1 != freq2:
        raise ValueError(f"The time indices of the fields have different frequencies (field1: {freq1}; field2: {freq2}).")

    # Check that time series are concatenable
    period1 = index1.droplevel(['lon', 'lat']).drop_duplicates()[-1]
    period2 = index2.droplevel(['lon', 'lat']).drop_duplicates()[0]
    if period1 + 1 != period2:
        raise ValueError(f"Time series are not consecutive (last period of field1: {period1}; first period of field2: {period2}).")

    check_spatial_coords_match(field1, field2)

    grid = copy.deepcopy(field1._grid)

    df = pd.concat([field1._data, field2._data]).sort_index()
    return Field(df, grid)


# Merge fields
def merge_fields(field_list: list[Field]) -> Field:
    """Merge fields defined in compatible grids.

    The fields must have compatible grids and contain the same layers.

    Parameters
    ----------
    field_list: list[Field]
        List of fields to merge

    Returns
    -------
    A new Field with the merged data.
    """

    # Check that layers are the same for all fields
    layers = field_list[0].layers
    for field in field_list[1:]:
        if field.layers != layers:
            raise ValueError("Fields must contain the same layers")

    # Combine all the grids
    grids = [field.grid for field in field_list]
    grid = sum(grids[1:], start=grids[0])

    # Concatente data along index axes
    data = pd.concat([field.data for field in field_list])

    # Remove rows with duplicated indices
    data = data.loc[~data.index.duplicated(keep='first'), :]

    return Field(data, grid)

# Filter data by region
# ---------------------

def filter_region(field: Field, region: str, region_type: str = "country") -> Field:
    """Filter a Field to retain only rows whose lon/lat fall inside a named region.
    
    Parameters
    ----------
    field : Field
        The field to filter
    region : str
        Region identifier understood by the chosen region set.
        For example: Names for countries, or region names for Giorgi/SREX/AR6.
    region_type: str
        Which predefined region set to use:
        - "country": natural_earth_v5_0_0.countries_10
        - "giorgi": Giorgi regions
        - "SREX"/"srex": IPCC SREX regions
        - "AR6"/"ar6": IPCC AR6 regions

    Returns
    -------
    A new Field instance containing only rows whose coordinates are inside the region.
    """
    
    # Select which region set to use based on region_type
    region_type_norm = region_type.lower()
    if region_type_norm == "country":
        regionmask_type = regionmask.defined_regions.natural_earth_v5_0_0.countries_10
    elif region_type_norm == "giorgi":
        regionmask_type = regionmask.defined_regions.giorgi
    elif region_type_norm == "srex":
        regionmask_type = regionmask.defined_regions.srex
    elif region_type_norm == "ar6":
        regionmask_type = regionmask.defined_regions.ar6.all
    else:
        raise ValueError("Unsupported region_type; expected one of {'country','giorgi','SREX','AR6'}")

    # Select region
    try:
        region_key = regionmask_type.map_keys(region)
    except KeyError:
        raise ValueError(f"Unknown region '{region}' for region_type '{region_type}'.")
    region_idx = regionmask_type[[region_key]]

    # Compute region mask on the 2D lon-lat grid
    region_mask = region_idx.mask(field.grid.lon, field.grid.lat)
    region_mask = region_mask.assign_coords(lat=field.grid.lat, lon=field.grid.lon)

    # Retrieve field data and coordinates
    data = field.data
    lons = data.index.get_level_values("lon")
    lats = data.index.get_level_values("lat")

    # Get the region_mask coordinate arrays
    mask_lats = region_mask.lat.values
    mask_lons = region_mask.lon.values

    # Find nearest indices (to avoid precision errors)
    lat_indices = np.searchsorted(mask_lats, lats.to_numpy())
    lon_indices = np.searchsorted(mask_lons, lons.to_numpy())

    # Clip to valid range
    lat_indices = np.clip(lat_indices, 0, len(mask_lats) - 1)
    lon_indices = np.clip(lon_indices, 0, len(mask_lons) - 1)

    # Index directly into the region_mask array
    is_in_region = region_mask.values[lat_indices, lon_indices]

    # Add column mask to data
    data["mask"] = np.isfinite(is_in_region) # convert nan to False and 121 to True

    # Apply the boolean mask to keep only rows inside the region
    filtered_field = field.filter("mask == True")

    # Add log message
    filtered_field.log(f"Filter data with region: '{region}'")

    return filtered_field
