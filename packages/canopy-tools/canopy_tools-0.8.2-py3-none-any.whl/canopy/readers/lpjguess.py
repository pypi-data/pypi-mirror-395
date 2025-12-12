"""Reader functions for standard LPJ-GUESS output

This module provides reader functions for the standard, text-based output of LPJ-GUESS.

Registered file formats:
    - lpjg_annual: e.g. anpp.out[.gz], aaet.out[.gz] ...
    - lpjg_monthly: e.g. mnpp.out[.gz], maet.out[.gz] ...
"""

import pandas as pd
from canopy.core.redspec import RedSpec
from canopy.core import frameops
from canopy.grid import get_grid, get_gridop
from canopy.readers.registry import register_reader_desc

# Readers for LPJ-GUESS standard (common) output
# ----------------------------------------------

# Number of rows to load for working out the length of the time series when reading file by chunks
NROWS_PROBE = 2000
# Number of gridcells per chunk when reading file by chunks
NGRIDCELLS_PER_CHUNK = 1000
# Columns to build index
INDEX_COLS = ['Lon', 'Lat', 'Year', ]

def _insert_index_yearly(df: pd.DataFrame) -> None:
    """Insert a MultiIndex for an annual output file

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame
    """
    # Ignore the type of index because the type hints for PeriodIndex are outdated and don't include from_fields
    index = pd.PeriodIndex.from_fields(year=df.Year, month=[1]*len(df), freq='Y') # type: ignore
    df.Year = index
    df.index = pd.MultiIndex.from_frame(df[INDEX_COLS])
    df.drop(INDEX_COLS, axis=1, inplace=True)
    df.sort_index(inplace=True)
    df.index.names = ['lon', 'lat', 'time', ]


def _insert_index_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """Insert a MultiIndex for a monthly output file

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame
    """
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ]
    df.index = pd.MultiIndex.from_frame(df[INDEX_COLS])
    df.drop(INDEX_COLS, axis=1, inplace=True)
    df = df.stack() # type: ignore
    index_list = [(lon, lat, pd.Period(year=y, month=months.index(m)+1, freq='M')) for lon, lat, y, m in df.index.values]
    df.index = pd.MultiIndex.from_tuples(index_list)
    df.sort_index(inplace=True)
    df.index.names = ['lon', 'lat', 'time']
    df = df.to_frame()
    df.columns = ['Data']
    return df


def _chunk_spatial_aggregation(ichunk, chunk, grid_type, preprocess):

    weights = pd.DataFrame([1]*len(chunk.index), index=chunk.index, columns=['w'])
    grid = get_grid(grid_type).from_frame(chunk)
    sumop = get_gridop(grid, 'sum', preprocess.axis)
    chunk = sumop(chunk, grid)
    chunk = frameops.restore_index(chunk, grid, f'c{ichunk}')
    if preprocess.gridop == 'av':
        weights = sumop(weights, grid)
        weights = frameops.restore_index(weights, grid, f'c{ichunk}')
    else:
        weights = None

    return chunk, weights


def read_by_chunks(path: str, preprocess: RedSpec,
                   grid_type: str | None, insert_index):

    #TODO: include reduction info in history?

    if grid_type is None:
        raise ValueError(f"Parameter 'grid_type' must be specified.")

    probe = pd.read_csv(path, nrows=NROWS_PROBE, sep=r'\s+')
    columns = list(probe.columns)
    if preprocess.layers is not None:
        columns = list(set(probe.columns) & set(preprocess.layers))
        if len(columns) == 0:
            raise ValueError("The file does not have any of the requested layers")
        columns += INDEX_COLS

    chunksize = len(probe['Year'].unique()) * NGRIDCELLS_PER_CHUNK

    insert_index(probe)
    probe_grid = get_grid(grid_type).from_frame(probe)

    if preprocess.gridop is not None and preprocess.axis is None:
        preprocess.axis = 'both'

    chunk_list = []
    weight_list = []
    for ichunk, chunk in enumerate(pd.read_csv(path, chunksize=chunksize, sep=r'\s+', usecols=columns)):
        insert_index(chunk)
        # Slice
        if preprocess.lon_slice is not None \
        or preprocess.lat_slice is not None \
        or preprocess.time_slice is not None:
            grid = get_grid(grid_type).from_frame(chunk)
            chunk, _, _ = frameops.sel_slice(chunk, grid,
                                             preprocess.lon_slice,
                                             preprocess.lat_slice,
                                             preprocess.time_slice)
            if chunk.empty:
                continue

        # Time reduction
        if preprocess.timeop is not None:
            chunk, _ = frameops.red_time(chunk, timeop=preprocess.timeop, freq=preprocess.freq)

        # Spatial reduction
        if preprocess.gridop is not None:
            chunk, weights = _chunk_spatial_aggregation(ichunk, chunk, grid_type, preprocess)
            weight_list.append(weights)

        chunk_list.append(chunk)

    if len(chunk_list) == 0:
        raise ValueError("Requested slicing yields empty data.")

    df_red = pd.concat(chunk_list)

    if preprocess.gridop is not None:
        group_levels = ['time']
        if preprocess.axis != 'both':
            group_levels = list(probe_grid.axis_names) + group_levels
            group_levels.remove(preprocess.axis)
    
        df_red = df_red.groupby(group_levels).sum()
        if preprocess.gridop == 'av':
            weights = pd.concat(weight_list).groupby(group_levels).sum()
            values = df_red.values/weights.values
            df_red = pd.DataFrame(values, index=df_red.index, columns=df_red.columns)
        df_red = frameops.restore_index(df_red, probe_grid, preprocess.gridop)

    return df_red


@register_reader_desc('LPJ-GUESS: common output (annual)')
def lpjg_annual(path: str, grid_type: str, preprocess: RedSpec | None = None):
    """Read an annual output file from the standard LPJ-GUESS output."""
    if preprocess is None:
        df = pd.read_csv(path, sep=r'\s+')
        _insert_index_yearly(df)
    else:
        df = read_by_chunks(path, preprocess, grid_type, _insert_index_yearly)
    return df


@register_reader_desc('LPJ-GUESS: common output (monthly)')
def lpjg_monthly(path: str, grid_type: str, preprocess: RedSpec | None = None):
    """Read a monthly output file from the standard LPJ-GUESS output."""
    if preprocess is None:
        df = pd.read_csv(path, sep=r'\s+')
        df = _insert_index_monthly(df)
    else:
        raise NotImplementedError
    return df


