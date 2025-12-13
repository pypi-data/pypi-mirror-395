"""
This module provides a registry for metadata associated to different data sources. (e.g.,
metadata for model output, observations...). The data is provided as .json files. Some data is
shipped with the software, but additional sources can be registered. See `register_source_data`
docstring for an example of json file.
"""
import os
import glob
import json
from typing import Any

_source_data = {}

def register_source_data(file: str) -> None:
    """
    Register source data.

    Parameters
    ----------
    file:
        A .json file describing the source data.

    Notes
    -----
    The .json file name (minus the extension) is used as the key to store the data
    in the registry. In order for it to work with the Source class, it needs to have,
    at least:
        - A "name" key, with value a string containing the name of the model.
        - A "fields" key, with value a dictionary of dictionaries. 
        - Each key in the "fields" dictionary of dictionaries is the name of a field. The
          value is a dictionary with string-string key-value pairs describing the field's
          metadata. In the metadata, "description" and "units" are mandatory.

    Example
    -------
    A description file for LPJ-GUESS (in file, say, 'sources/data/lpjguess.json'):
        {
            "name": "LPJ-GUESS",
            "fields": {
                "agpp": {
                    "name": "Annual GPP",
                    "description": "Annual gross primary production",
                    "units": "kgC m^-2 year^-1"
                },
                "anpp": {
                    "name": "Annual NPP",
                    "description": "Annual net primary production",
                    "units": "kgC m^-2 year^-1"
                }
            },
            "pfts": {
                "TeNE": "Temperate Needleleaved Evergreen Tree",
                "TeBE": "Temperate Broadleaved Evergreen Tree"
            }
        }

    To register the source:
    register_source('lpjguess.json')
    """
    # The name of the file is taken as the registry key
    source_id = os.path.basename(file).replace('.json','')
    if source_id in _source_data:
        raise KeyError(f"Model '{source_id}' has already been registered")
    with open(file, 'r', encoding="utf-8") as f:
        _source_data[source_id] = json.load(f)


def get_source_data(source_id: str) -> dict[str, Any]:
    """
    Get a reference to source 'source_id' data in the registry
    """
    try:
        return _source_data[source_id]
    except KeyError:
        raise KeyError(f"Source '{source_id}' not registered")
    

# Load pre-configured sources
for file in glob.glob(f'{os.path.dirname(__file__)}/data/*.json'):
    register_source_data(file)

