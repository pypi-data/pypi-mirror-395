"""
This module is a registry for Source objects. Source objects are subclasses of the abstract
Source class. They provide an interface to handle data from different sources (model output,
observations...)
"""
from typing import Callable, Any
from canopy.sources.source_abc import Source
from canopy.source_data import get_source_data

_sources = {}

def register_source(source_id: str) -> Callable:
    """
    Register decorated source subclass for source 'source_id'.

    Parameters
    ----------
    source_id : str
        String identifier of the source the decorated Source object is associated with
    """
    try:
        _ = get_source_data(source_id)
    except KeyError:
        raise KeyError(f"Model '{source_id}' not registered")

    def decorator(cls):
        _sources[source_id] = cls
        return cls

    return decorator


def get_source(path: str, source_id: str, **kwargs) -> Source:
    """
    Construct a source object from the data in 'path' for source 'source_id'.

    Parameters
    ----------
    path : str
        The path of the data source (simulation output)
    source_id : str
        String identifier of the source the decorated Source object is associated with
    """
    try:
        _ = get_source_data(source_id)
    except KeyError:
        raise KeyError(f"Model '{source_id}' not registered")

    try:
        return _sources[source_id](path, **kwargs)
    except KeyError:
        raise KeyError(f"No Source object defined for source '{source_id}'")

