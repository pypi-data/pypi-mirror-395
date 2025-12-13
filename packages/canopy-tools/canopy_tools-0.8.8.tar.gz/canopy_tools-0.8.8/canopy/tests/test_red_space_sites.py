# ----------------------------------------------------------------------------
# | Suite of unit tests for spatial reduction operations on the 'sites' grid |
# ----------------------------------------------------------------------------

import numpy as np
import pandas as pd
import pytest
import canopy.core.frameops as frameops
from canopy.core.constants import *
from canopy import Field
import xarray as xr

INDEX_NAMES = ['lon', 'lat', 'time', ]

# The test fields must follow the Field specification, i.e.;
# - field._data is a pandas DataFrame with multiindex with levels 'lon', 'lat', 'time'
# - field._grid must be consistent with the data
TEST_DATA = {
        # AAET for the global gridlist shipped with LPJ-GUESS (data/gridlists/gridlist_global.txt)
        'aaet_global_sites': 'tests/test_data/aaet_global_sites.out.gz',
        }

def get_test_field():
    # Change this to use another test dataframe
    test = 'aaet_global_sites'
    return Field.from_file(TEST_DATA[test], grid_type = 'sites')


# TESTS for red_space(df, axis: str, redop: str)
# ----------------------------------------------

# Check that lat-mean raises invalid operation error
def test_red_space_av_lat():
    field = get_test_field()
    with pytest.raises(KeyError) as e_info:
        df, grid = field._data, field._grid
        red_df, _, _ = frameops.red_space(df, grid, 'av', 'lat')

    assert e_info.value.args[0] == f"Operation 'av' on axis 'lat' is not defined for grid type 'sites'."

# Check that lon-mean raises invalid operation error
def test_red_space_av_lon():
    field = get_test_field()
    with pytest.raises(KeyError) as e_info:
        df, grid = field._data, field._grid
        red_df, _, _ = frameops.red_space(df, grid, 'av', 'lon')

    assert e_info.value.args[0] == f"Operation 'av' on axis 'lon' is not defined for grid type 'sites'."

# Check that both-mean yields same result as when calc'd with xarray
def test_red_space_av_both():
    field = get_test_field()
    df, grid = field._data, field._grid
    # PyGUESS calculation
    # -------------------
    red_df, grid, _ = frameops.red_space(df, grid, 'av', 'both')
    # Drop 'lon' and 'lat' indices before converting to xarray for comparison
    red_df.index = red_df.index.droplevel(['lon','lat'])
    red_df = red_df.to_xarray()
    # Xarray calculation
    # ------------------
    xa = df.to_xarray().sortby('lon').sortby('lat').sortby('time')
    red_xa = xa.mean(('lon', 'lat'))
    # Compare them
    xr.testing.assert_allclose(red_xa, red_df)

# Check that lat-sum raises invalid operation error
def test_red_space_sum_lat():
    field = get_test_field()
    with pytest.raises(KeyError) as e_info:
        df, grid = field._data, field._grid
        red_df, _, _ = frameops.red_space(df, grid, 'sum', 'lat')

    assert e_info.value.args[0] == f"Operation 'sum' on axis 'lat' is not defined for grid type 'sites'."


# Check that lon-sum yields same result as when calc'd with xarray
def test_red_space_sum_lon():
    field = get_test_field()
    with pytest.raises(KeyError) as e_info:
        df, grid = field._data, field._grid
        red_df, _, _ = frameops.red_space(df, grid, 'sum', 'lon')

    assert e_info.value.args[0] == f"Operation 'sum' on axis 'lon' is not defined for grid type 'sites'."


# Check that both-sum yields same result as when calc'd with xarray
def test_red_space_sum_both():
    field = get_test_field()
    df, grid = field._data, field._grid
    # PyGUESS calculation
    # -------------------
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'both')
    # Drop 'lon' and 'lat' indices before converting to xarray for comparison
    red_df.index = red_df.index.droplevel(['lon','lat'])
    red_df = red_df.to_xarray()
    # Xarray calculation
    # ------------------
    xa = df.to_xarray().sortby('lon').sortby('lat').sortby('time')
    red_xa = xa.sum(('lon', 'lat'))
    # Compare them
    xr.testing.assert_allclose(red_xa, red_df)


def test_levels_av_both():
    """Check that the data frame index still has all levels after aggregating on both axes"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'av', 'both')
    assert red_df.index.names == INDEX_NAMES


def test_levels_sum_both():
    """Check that the data frame index still has all levels after aggregating on both axes"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'both')
    assert red_df.index.names == INDEX_NAMES

