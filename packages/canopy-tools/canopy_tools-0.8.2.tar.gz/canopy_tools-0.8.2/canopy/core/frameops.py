import pandas as pd
import janitor
import copy
from typing import Optional, Union, Type, Literal, SupportsFloat, cast
from canopy.core.redspec import RedSpec
from canopy.grid.grid_abc import Grid
from canopy.grid import get_gridop, create_grid
from canopy.core.constants import *

# Implemented time reduction operations
TIME_REDOPS = ['av', 'std', 'sum', ] #'av_m', 'std_m', ]
# Dataframe frequencies
YEARLY_FREQ = pd.Period('2000', freq='Y').freq
MONTHLY_FREQ = pd.Period('2000', freq='M').freq
# Allowed frequncy units for time reductions
TIME_RED_FREQS = ['M', 'Y', ]
# Valid number of months for time reduction
N_MONTHS_RED = [2, 3, 4, 6, 12]


def check_indices_match(df1: pd.DataFrame, df2: pd.DataFrame, atol: float = 1.e-6, rtol: float = 0.):

    index1 = df1.index
    index2 = df2.index

    if len(index1) != len(index2):
        raise ValueError("Indices have different lenghts.")

    # Check spatial axes
    indices_match = []
    for i in range(2):
        axis1 = index1.get_level_values(i)
        axis2 = index2.get_level_values(i)
        if axis1.dtype != axis2.dtype:
            indices_match.append(False)
            continue
        if isinstance(axis1[0], str) and axis1[0] == axis2[0]:
            indices_match.append(True)
        elif isinstance(axis1[0], str) and axis1[0] != axis2[0]:
            indices_match.append(False)
        else:
            try:
                indices_match.append(np.allclose(axis1, axis2, atol=atol, rtol=rtol))
            except ValueError:
                indices_match.append(False)

    # Check time axis
    timeax1 = index1.get_level_values('time')
    timeax2 = index2.get_level_values('time')
    try:
        indices_match.append(bool((timeax1 == timeax2).all()))
    except ValueError:
        indices_match.append(False)

    if not all(indices_match):
        non_matching = list(np.where(np.logical_not(indices_match))[0])
        raise ValueError(f"Field indices {non_matching} do not match.")


def is_yearly_freq(df) -> bool:
    return df.index.get_level_values('time').freq == YEARLY_FREQ


def is_monthly_freq(df) -> bool:
    return df.index.get_level_values('time').freq == MONTHLY_FREQ


def parse_timeop(timeop: str) -> str:
    if not timeop.lower() in TIME_REDOPS:
        raise ValueError(f"Time timeop must be one of {TIME_REDOPS} (got '{timeop}').")
    return timeop.lower()


def get_time_index(df: pd.DataFrame) -> pd.PeriodIndex:

    index = cast(pd.MultiIndex, df.index)
    return cast(pd.PeriodIndex, index.levels[-1])


def get_base_freq(idx) -> str:

    for freq_str, base_freq in zip(['Month', 'Year'], ['M', 'Y']):
        if freq_str in str(idx.freq.base):
            break

    return base_freq


def parse_freq(freq: str) -> tuple[int, str]:

    if freq[:-1] == '':
        n_periods = 1
    else:
        try:
            n_periods = int(freq[:-1])
        except ValueError:
            raise ValueError(f"Specified number of periods '{freq[:-1]}' is not a number.")

    freq_unit = freq[-1]
    if not freq_unit in TIME_RED_FREQS:
        raise ValueError(f"Frequency unit must be one of {TIME_RED_FREQS} (got '{freq_unit}').")

    return n_periods, freq_unit


def red_time(df, timeop: str, freq: str | None) -> tuple[pd.DataFrame, list[str]]:

    timeop = parse_timeop(timeop)

    # TODO: why? Now I can only read monthly and yearly files, but should work for daily,
    # hourly... => generalize time series resampling
    if not is_yearly_freq(df) and not is_monthly_freq(df):
        raise ValueError("Data must have yearly or monthly frequency.")

    if freq is None:
        idx = get_time_index(df)
        base_freq = cast(pd.offsets.YearEnd, idx.freq)
        n_periods = base_freq.n * len(idx)
        freq_unit = get_base_freq(idx)
    else:
        n_periods, freq_unit = parse_freq(freq)

        if is_yearly_freq(df) and n_periods == 1 and freq_unit == 'Y':
            raise ValueError("Frequency is already 1 year.")

        if is_monthly_freq(df) and n_periods == 1 and freq_unit == 'M':
            raise ValueError("Frequency is already 1 month.")

        if is_monthly_freq(df) and freq_unit == 'M' and not n_periods in N_MONTHS_RED :
            raise ValueError(f"The number of months for reduction:{timeop} must be one of {N_MONTHS_RED}.")

    freq_grouper = f'{n_periods}{freq_unit}S'
    freq_new_period = f'{n_periods}{freq_unit}'

    # - Conversion to timestamp is necessary because resampling with PeriodIndex is not supported as of Pandas 2.2.3
    # TODO: Check this in future Pandas versions
    # - Coversion to datetime64[s] is necessary because Pandas timestamps have a resolution of
    # nanoseconds. This can cause the grouper to overflow. See https://stackoverflow.com/questions/78454291
    index_orig = df.index
    df.index = df.index.set_levels(df.index.levels[2].to_timestamp().astype('datetime64[s]'), level=2)

    if timeop == 'av':
        df_ya = df.groupby(['lon', 'lat', pd.Grouper(freq=freq_grouper, level='time')]).mean()
    elif timeop == 'sum':
        df_ya = df.groupby(['lon', 'lat', pd.Grouper(freq=freq_grouper, level='time')]).sum()
    elif timeop == 'std':
        df_ya = df.groupby(['lon', 'lat', pd.Grouper(freq=freq_grouper, level='time')]).std()

    df_ya.index = df_ya.index.set_levels(df_ya.index.levels[2].to_period(freq=freq_new_period), level=2)
    df.index = index_orig

    if freq is None:
        freq_str = "whole time series"
    else:
        freq_str = freq
    log_msg = [f"Time reduction: {timeop}, {freq_str}"]

    return df_ya, log_msg


def restore_index(df: pd.DataFrame, grid: Grid, gridop: str) -> pd.DataFrame:
    """Restore MultiIndex to a sorted MultiIndex with ['lon', 'lat', 'time'] levels

    Parameters
    ----------
    df : pd.DataFrame
        The (reduced) pandas dataframe whose index is to be restored.
    grid : Grid
        The Grid object associated to the reduced frame.
    gridop : str
        A string describing the grid reduction operation carried out.

    Returns
    -------
    A pandas DataFrame with a restored index
    """
    axes_to_restore = [x for x in grid.axis_names if x not in df.index.names]
    levels = []
    for axis in axes_to_restore:
        df[axis] = gridop
        levels.append(axis)
    df.set_index(levels, append=True, inplace=True)
    df = df.reorder_levels(list(grid.axis_names) + ['time'])
    if not df.index.is_monotonic_increasing:
        df.sort_index(inplace=True)

    return df


def red_space(df, grid: Grid, gridop: str, axis: str) -> tuple[pd.DataFrame, Grid, list[str]]:

    # Check that relevant axes haven't been reduced already
    if grid.is_reduced(axis):
        raise ValueError(f"Axis '{axis}' is already reduced (gridop = {grid.axis_gridop[axis]}).")

    df_red = get_gridop(grid, gridop, axis)(df, grid)
    df_red = restore_index(df_red, grid, gridop)

    # Create new grid
    grid_red = grid.get_reduced_grid(gridop, axis)

    # Create log message
    log_msg = [f"Spatial reduction: '{gridop}', '{axis}'"]

    return df_red, grid_red, log_msg


def get_selection_tuple(lon_slice: tuple[int | float, int | float] | None,
                        lat_slice: tuple[int | float, int | float] | None,
                        time_slice: tuple[int | pd.Period, int | pd.Period] | None)\
                        -> tuple[slice, ...]:

    # Convert time slice to Periods
    if not time_slice is None:
        ts0 = time_slice[0]
        ts1 = time_slice[1]
        if isinstance(ts0, (int, float)):
            ts0 = pd.Period(year=ts0, freq='Y')
        if isinstance(ts1, (int, float)):
            ts1 = pd.Period(year=ts1, freq='Y')
        time_slice = (ts0, ts1)

    selection_tuple = []
    for arg in [lon_slice, lat_slice, time_slice]:
        if arg is None:
            selection_tuple += [slice(None)]
        else:
            selection_tuple += [slice(arg[0], arg[1])]

    return tuple(selection_tuple)


def sel_slice(df: pd.DataFrame,
              grid: Grid,
              lon_slice: Optional[tuple[float,float]] = None,
              lat_slice: Optional[tuple[float,float]] = None,
              time_slice: Optional[tuple[int,int]] = None) -> tuple[pd.DataFrame, Grid, list[str]]:

    if lon_slice is None and lat_slice is None and time_slice is None:
        raise ValueError("At least one of the slices should be other than None")

    # Check that the spatial dimensions are not collapsed
    if (not lon_slice is None and grid.is_reduced('lon')) \
    or (not lat_slice is None and grid.is_reduced('lat')):
        raise ValueError("Cannot slice a reduced dimension.")

    selection_tuple = get_selection_tuple(lon_slice, lat_slice, time_slice)
    df_sliced = df.loc[selection_tuple,:]
    index = cast(pd.MultiIndex, df_sliced.index)
    df_sliced.index = index.remove_unused_levels()

    if df_sliced.empty:
        grid_sliced = create_grid('empty')
    else:
        grid_sliced = grid.get_sliced_grid(lon_slice, lat_slice)

    log_msg = []
    if lon_slice is not None:
        log_msg.append(f"Sliced 'lon': {lon_slice}")
    if lat_slice is not None:
        log_msg.append(f"Sliced 'lat': {lat_slice}")
    if time_slice is not None:
        log_msg.append(f"Sliced 'time': {time_slice}")
    if df_sliced.empty:
        log_msg.append("Field was sliced to empty!")

    return df_sliced, grid_sliced, log_msg


def apply_reduction(df: pd.DataFrame, grid: Grid, redspec: RedSpec) -> tuple[pd.DataFrame, Grid, list[str]]:

    df_red, grid_red = df, grid
    log_msg = []

    # Select layers
    if not redspec.layers is None:
        df_red = df_red[redspec.layers]

    # Slice data
    if not redspec.lon_slice is None \
    or not redspec.lat_slice is None \
    or not redspec.time_slice is None:
        df_red, grid_red, lm = sel_slice(df_red, grid_red,
                                     lon_slice = redspec.lon_slice,
                                     lat_slice = redspec.lat_slice,
                                     time_slice = redspec.time_slice)
        log_msg.extend(lm)

    # Apply time reduction
    if redspec.timeop is not None:
        if redspec.freq is None:
            raise ValueError(f"A frequency for time reduction operation '{redspec.timeop}' must be specified.")
        df_red, lm = red_time(df_red, redspec.timeop, freq=redspec.freq)
        log_msg.extend(lm)

    # Apply spatial reduction
    if redspec.gridop is not None:
        df_red, grid_red, lm = red_space(df_red, grid_red, redspec.gridop, axis = redspec.axis)
        log_msg.extend(lm)

    return df_red, grid_red, log_msg


def check_columns(df: pd.DataFrame, layers: list[str]):

    s1 = set(df.columns)
    s2 = set(layers)
    if not s2.issubset(s1):
        raise ValueError("Field does not have specified layers.")


def apply_sum(df: pd.DataFrame, operand: SupportsFloat | list[str], layers: list[str]) -> None:

    check_columns(df, layers)

    if isinstance(operand, SupportsFloat):
        operand1 = np.array(float(operand))
    else:
        check_columns(df, operand)
        operand1 = df[operand].values

    df[layers] = operand1 + df[layers].values


def apply_mul(df: pd.DataFrame, operand: SupportsFloat | list[str], layers: list[str]) -> None:

    check_columns(df, layers)

    if isinstance(operand, SupportsFloat):
        operand1 = np.array(float(operand))
    else:
        check_columns(df, operand)
        operand1 = df[operand].values

    df[layers] = operand1 * df[layers].values


def apply_sub(df: pd.DataFrame, operand: SupportsFloat | list[str], layers: list[str], how: Literal['left', 'right']) -> None:

    if how not in ['left', 'right']:
        raise ValueError("'how' must be either 'left' or 'right'")

    check_columns(df, layers)

    if isinstance(operand, SupportsFloat):
        operand1 = np.array(float(operand))
    else:
        check_columns(df, operand)
        operand1 = df[operand].values

    if how == 'right':
        df[layers] = operand1 - df[layers].values
    else:
        df[layers] = df[layers].values - operand1


def apply_div(df: pd.DataFrame, operand: SupportsFloat | list[str], layers: list[str], how: Literal['left', 'right']) -> None:

    if how not in ['left', 'right']:
        raise ValueError("'how' must be either 'left' or 'right'")

    check_columns(df, layers)

    if isinstance(operand, SupportsFloat):
        operand1 = np.array(float(operand))
    else:
        check_columns(df, operand)
        operand1 = df[operand].values

    if how == 'right':
        df[layers] = operand1 / df[layers].values
    else:
        df[layers] = df[layers].values / operand1
        

def apply_function(df: pd.DataFrame, layers: list[str], function) -> None:

    check_columns(df, layers)
    function = np.vectorize(function)
    df[layers] = function(df[layers].values)
    


