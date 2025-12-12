import numpy as np
import pandas as pd
from canopy.core.field import Field
import canopy.core.frameops as frameops


def check_field_contains_layers(field: Field, layers: str | list[str], name: str = 'field'):
    """Check if field contains required layers

    Parameters
    ----------
    field : Field
        The field whose layers to check
    layers : str | list[str]
        A string or a list of strings, identifying the required layer(s)
    name: str = 'field'
        The name of the field for message printing purposes
    """
    if isinstance(layers, str):
        layers = [layers]

    not_found = []
    for layer in layers:
        if layer not in field.layers:
            not_found.append(layer)

    if len(not_found):
        raise ValueError(f"Layers {not_found} not found in {name}'s layers ({field.layers}).")


def check_spatial_coords_match(field1: Field, field2: Field, atol: float = 1.e-6, rtol: float = 0.):
    """Check if spatial coordinates of two fields match up to given tolerance

    Parameters
    ----------
    field1 : Field
        The first of the two fields whose coordinates to compare
    field2 : Field
        The second of the two fields whose coordinates to compare
    atol : float
        Absolute tolerance to apply in the comparison
    rtol : float
        Relative tolerance to apply in the comparison

    Notes
    -----
    Absolute and relative tolerances are defined as in Numpy, i.e., two numbers a and b are equivalent if the following
    equation is fulfilled:

        absolute(a - b) <= (atol + rtol * absolute(b))

    See https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose
    """

    gridlist1 = np.array(field1.data.index.droplevel('time').drop_duplicates().to_frame())
    gridlist2 = np.array(field2.data.index.droplevel('time').drop_duplicates().to_frame())
    try:
        gridlists_match = np.allclose(gridlist1, gridlist2, atol=atol, rtol=rtol)
    # If gridlists don't have the same length, the above comparison will fail
    except ValueError:
        gridlists_match = False
    if not gridlists_match:
        raise ValueError("Gridlists do not match.")


def check_indices_match(field1: Field, field2: Field, atol: float = 1.e-6, rtol: float = 0.):
    """Check if the indices of the DataFrames of two fields match up to a given tolerance

    Parameters
    ----------
    field1 : Field
        The first of the two fields whose coordinates to compare
    field2 : Field
        The second of the two fields whose coordinates to compare
    atol : float
        Absolute tolerance to apply in the comparison
    rtol : float
        Relative tolerance to apply in the comparison

    Notes
    -----
    Absolute and relative tolerances are defined as in Numpy, i.e., two numbers a and b are equivalent if the following
    equation is fulfilled:

        absolute(a - b) <= (atol + rtol * absolute(b))

    See https://numpy.org/doc/stable/reference/generated/numpy.isclose.html#numpy.isclose
    """

    frameops.check_indices_match(field1.data, field2.data, atol, rtol)


