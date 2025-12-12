from dataclasses import dataclass
import json
import os
from canopy.core.field import Field

@dataclass
class TestDataInfo:
    description: str = ""
    file_format: str = ""
    grid_type: str = ""
    source: str = ""

_test_data_info = {}


def _load_test_data_registry():

    with open(f'{os.path.dirname(__file__)}/registry.json') as f:
        test_data = json.load(f)
    for fname, data in test_data.items():
        td = TestDataInfo(description=data['description'],
                          file_format=data['file_format'],
                          grid_type=data['grid_type'],
                          source=data['source']
                          )
        _test_data_info[fname] = td


def get_test_data(fname: str | None = None) -> Field | None:
    '''Load a test data field

    Parameters
    ----------
    fname : str | None
        The name of the data file to load. If None, a list of available test data files is printed, and the function returns None

    Returns
    -------
        Either a Field object derived from the data file or None.
    '''

    if fname is None:
        msg = [
                "Available test data:",
                "--------------------",
                ]

        for fname, info in _test_data_info.items():
            msg.append(f"{fname}: {info.description}")

        print("\n".join(msg))
        return None

    path = f'{os.path.dirname(__file__)}'
    tdi = _test_data_info[fname]
    field = Field.from_file(f'{path}/{fname}', grid_type=tdi.grid_type, source=tdi.source)

    return field


_load_test_data_registry()


