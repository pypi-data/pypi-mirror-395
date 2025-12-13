# -----------------------------------------------------------------------------
# | Suite of unit tests for spatial reduction operations on the 'lonlat' grid |
# -----------------------------------------------------------------------------

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
        # Annual npp over Spain 1990-2010, gridded
        'anpp_spain': 'tests/test_data/anpp_spain_1990_2010.out.gz',
        }

def get_test_field():
    # Change this to use another test dataframe
    test = 'anpp_spain'
    return Field.from_file(TEST_DATA[test])


def test_red_space_av_lat():
    """Check that lat-mean yields same result as when calc'd with xarray"""
    field = get_test_field()
    df, grid = field._data, field._grid
    # PyGUESS calculation
    # -------------------
    red_df, _, _ = frameops.red_space(df, grid, 'av', 'lat')
    # Drop 'lon' index before converting to xarray for comparison
    red_df.index = red_df.index.droplevel('lat')
    red_df = red_df.to_xarray()
    # Xarray calculation
    # ------------------
    xa = df.to_xarray().sortby('lon').sortby('lat').sortby('time')
    red_xa = xa.mean('lat')
    # Comparison
    # ----------
    xr.testing.assert_allclose(red_xa, red_df)

def test_red_space_av_lon():
    """Check that lon-mean yields same result as when calc'd with xarray"""
    field = get_test_field()
    df, grid = field._data, field._grid
    # PyGUESS calculation
    # -------------------
    red_df, _, _ = frameops.red_space(df, grid, 'av', 'lon')
    # Drop 'lon' index before converting to xarray for comparison
    red_df.index = red_df.index.droplevel('lon')
    red_df = red_df.to_xarray()
    # Xarray calculation
    # ------------------
    xa = df.to_xarray().sortby('lon').sortby('lat').sortby('time')
    red_xa = xa.mean('lon')
    # Compare them
    xr.testing.assert_allclose(red_xa, red_df)

def test_red_space_av_both():
    """Check that both-mean yields same result as when calc'd with xarray"""
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
    weights = np.cos(np.deg2rad(xa.lat))
    xa_weighted = xa.weighted(weights)
    red_xa = xa_weighted.mean(('lon', 'lat'))
    # Compare them
    xr.testing.assert_allclose(red_xa, red_df)

def test_red_space_sum_lat():
    """Check that lat-sum yields same result as when calc'd with xarray"""
    field = get_test_field()
    df, grid = field._data, field._grid
    # PyGUESS calculation
    # -------------------
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'lat')
    # Drop 'lat' index before converting to xarray for comparison
    red_df.index = red_df.index.droplevel('lat')
    red_df = red_df.to_xarray()
    # Xarray calculation
    # ------------------
    xa = df.to_xarray().sortby('lon').sortby('lat').sortby('time')
    red_xa = (xa*EARTH_RADIUS*np.deg2rad(grid.dx['lat'])).sum('lat')
    # Comparison
    # ----------
    xr.testing.assert_allclose(red_xa, red_df)


def test_red_space_sum_lon():
    """Check that lon-sum yields same result as when calc'd with xarray"""
    field = get_test_field()
    df, grid = field._data, field._grid
    # PyGUESS calculation
    # -------------------
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'lon')
    # Drop 'lon' index before converting to xarray for comparison
    red_df.index = red_df.index.droplevel('lon')
    red_df = red_df.to_xarray()
    # Xarray calculation
    # ------------------
    xa = df.to_xarray().sortby('lon').sortby('lat').sortby('time')
    weights = EARTH_RADIUS*np.deg2rad(grid.dx['lon'])*np.cos(np.deg2rad(xa.lat))
    xa_weighted = xa.weighted(weights)
    red_xa = xa_weighted.sum('lon')
    # Comparison
    # ----------
    xr.testing.assert_allclose(red_xa, red_df)


def test_red_space_sum_both():
    """Check that both-sum yields same result as when calc'd with xarray"""
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
    weights = EARTH_RADIUS**2*np.deg2rad(grid.dx['lon'])*np.deg2rad(grid.dx['lat'])*np.cos(np.deg2rad(xa.lat))
    xa_weighted = xa.weighted(weights)
    red_xa = xa_weighted.sum(('lon', 'lat'))
    # Compare them
    xr.testing.assert_allclose(red_xa, red_df)


def test_levels_av_lon():
    """Check that the data frame index still has all levels after averaging in longitude"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'av', 'lon')
    assert red_df.index.names == INDEX_NAMES


def test_levels_av_lat():
    """Check that the data frame index still has all levels after averaging in latitude"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'av', 'lat')
    assert red_df.index.names == INDEX_NAMES

def test_levels_av_both():
    """Check that the data frame index still has all levels after averaging on both axes"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'av', 'both')
    assert red_df.index.names == INDEX_NAMES

def test_levels_sum_lon():
    """Check that the data frame index still has all levels after aggregating in longitude"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'lon')
    assert red_df.index.names == INDEX_NAMES

def test_levels_sum_lat():
    """Check that the data frame index still has all levels after aggregating in latitude"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'lat')
    assert red_df.index.names == INDEX_NAMES

def test_levels_sum_both():
    """Check that the data frame index still has all levels after aggregating on both axes"""
    field = get_test_field()
    df, grid = field._data, field._grid
    red_df, _, _ = frameops.red_space(df, grid, 'sum', 'both')
    assert red_df.index.names == INDEX_NAMES

