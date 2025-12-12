"""Registry functionalily for file readers

This file provides a registry of file reader functions. The registry is a dictonary whose
keys (type str) are file format identifiers (e.g., `'lpjg_annual'`...) and the values are
the file reader functions, which read a file of the specified format and return a DataFrame
conforming to the `Field` specification (see `Field` docs).
"""

import pandas as pd
from typing import Callable
from dataclasses import dataclass


# File reader registry
_file_readers: dict[str, Callable[[str, str], pd.DataFrame]] = {}
_format_descriptions: dict[str, str] = {}


def register_reader(file_reader: Callable[[str, str], pd.DataFrame]) -> Callable[[str, str], pd.DataFrame]:
    """Add the decorated function to the file reader registry."""
    key = file_reader.__name__
    if key in _file_readers:
        raise KeyError(f"File format '{key}' already registered.")
    else:
        _file_readers[key] = file_reader
        _format_descriptions[key] = key

    return file_reader


def register_reader_desc(format_description: str):
    """Add the decorated function to the file reader registry."""
    def decorator(file_reader: Callable[[str, str], pd.DataFrame]) -> Callable[[str, str], pd.DataFrame]:
        key = file_reader.__name__
        if key in _file_readers:
            raise KeyError(f"File format '{key}' already registered.")
        else:
            _file_readers[key] = file_reader
            _format_descriptions[key] = format_description
        return file_reader

    return decorator


def get_reader(format: str) -> Callable[[str, str], pd.DataFrame]:
    """Get a reference to the file reader function identified by the passed parameter 'format'.

    Parameters
    ----------
    format : str
        A string identifier for the requested file reader function (e.g., 'lpjg_annual', 'lpjg_monthly'...)

    Returns
    -------
    A reference to the requested file reader.
    """
    try:
        reader = _file_readers[format]
    except KeyError:
        raise KeyError(f"File format '{format}' not recognized. Available formats: {[k for k in _file_readers]}.")
    return reader


def get_format_description(format: str) -> str:
    """Get a file format longer description.

    Parameters
    ----------
    format : str
        A string identifier for the requested file reader function (e.g., 'lpjg_annual', 'lpjg_monthly'...)

    Returns
    -------
    The file format description stored in the registry.
    """
    try:
        reader = _format_descriptions[format]
    except KeyError:
        raise KeyError(f"File format '{format}' not recognized. Available formats: {[k for k in _file_readers]}.")
    return reader

