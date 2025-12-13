from abc import ABC, abstractmethod
from canopy import Field
from typing import Any
import pathlib
from types import MappingProxyType


class Source(ABC):
    """
    Source abstract base class
    """

    def __init__(self, path: str, source_data: dict) -> None:
        """
        Parameters
        ----------
        path : str
            Path to the data source
        source_data : dict
            The source's metadata dict (see source_data/registry.py for a description)
        """
        super().__setattr__('_fields', {})
        _path = pathlib.Path(path)
        if not _path.exists():
            raise ValueError(f"Path '{path}' does not exist.")
        self._path = _path.resolve()
        self._source_data = source_data
        self._is_loaded: dict[str, bool] = {}


    def __getattr__(self, field_id):
        """
        Attribute-like access to fields
        """
        try:
            if not self._is_loaded[field_id]:
                raise ValueError(f"Field '{field_id}' is not loaded.")
            return self._fields[field_id]
        except KeyError:
            raise AttributeError(f"Field '{field_id}' not found in source.")


    def __setattr__(self, name: str, value: Any):
        """
        Prevent assignment of fields
        """
        if name in self._fields:
            raise AttributeError("Source field cannot be assigned")
        return super().__setattr__(name, value)


    def __getitem__(self, field_id):
        """
        Get-item-like access to fields
        """
        try:
            if not self._is_loaded[field_id]:
                raise ValueError(f"Field '{field_id}' is not loaded.")
            return self._fields[field_id]
        except KeyError:
            raise KeyError(f"Field '{field_id}' not found in source.")


    def __dir__(self):
        """
        Return __dir__() extended with the ids of loaded fields
        """
        attrs = [attr for attr in super().__dir__() if attr[0] != '_']
        attrs.extend([field_id for field_id in self._fields.keys() if self.is_loaded[field_id]])
        return attrs
    

    @property
    def path(self) -> str:
        """str: Stores the path of the source (e.g. the model output folder)."""
        return self._path


    @property
    def source_data(self) -> MappingProxyType:
        """dict: the dict with the registered source data."""
        return MappingProxyType(self._source_data)


    @property
    def source(self) -> str:
        """str: The name of the source."""
        return self._source_data['name']


    @property
    def fields(self) -> MappingProxyType:
        """dict: Stores the source's fields (if not loaded, the field is None)."""
        return MappingProxyType(self._fields)


    @property
    def is_loaded(self) -> dict[str, bool]:
        """dict: Stores the source's fields (if not loaded, the field is None)."""
        return self._is_loaded


    @abstractmethod
    def load_field(self, field_id: str) -> Field:
        """Load a field from the source. To be implemented by the subclasses.

        Parameters
        ----------
        field_id : str
            The string identifier of the field to load.
        """
        pass


    def get_field(self, field_id: str) -> Field | None:
        """
        Get a reference to a field

        Parameters
        ----------
        field_id : str
            The field's key in the _fields dictionary
        """
        try:
            field = self.fields[field_id]
        except KeyError:
            raise KeyError("Field not found in source")
        if field is None:
            field = self.load_field(field_id)
        return field


    def drop_field(self, field_id: str) -> None:
        """
        Drop or 'unload' a field

        Parameters
        ----------
        field_id: str
            The field's key in the _fields dictionary
        """
        if field_id not in self._fields:
            raise KeyError(f"Field {field_id} does not exist in source")
        self._fields[field_id] = None
        self.is_loaded[field_id] = False


    def __str__(self) -> str:

        str_list = [
                f"Source: {self.source}",
                f"Path: {self.path}",
                "",
                ]
        descr_list = []
        units_list = []
        
        for fid in self.fields:
            
            if fid in self.source_data['fields']:
                description = self.source_data['fields'][fid]['description']
                units = self.source_data['fields'][fid]['units']
            else:
                description = '[no description]'
                units = '[no units]'
            descr_list.append(description)
            units_list.append(units)

        max_field_len = max([len(fid) for fid in self.fields])
        max_field_len = max(5, max_field_len) # Header "Field" is 5 characters long
        max_descr_len = max([len(descr) for descr in descr_list])
        max_descr_len = max(11, max_descr_len) # Header "Description" is 11 characters long

        field_list = []
        for fid, descr, units in zip(self.fields, descr_list, units_list):
            is_loaded_indicator = u'\u2713' if self.is_loaded[fid] else ' '
            is_modified_indicator = ' '
            if self.is_loaded[fid]:
                # self.fields[fid] is either a Field or None. The line below will make mypy complain because None
                # doesn't have a 'modified' attribute. But if is_loaded[fid], fields[fid] cannot be None. I prefer
                # to ignore the error to checking if fields[fid] is none.
                if self.fields[fid].modified: # type: ignore
                    is_modified_indicator = u'\u2713'
            field_list.append(f"{is_loaded_indicator}  {is_modified_indicator}  {fid:{max_field_len}}  {descr:{max_descr_len}}  ({units})")
        max_str_len = max([len(x) for x in field_list])
        field_header = [
                f"L  M  {'Field':{max_field_len}}  {'Description':{max_descr_len}}  {'(units)'}",
                f"{'-'*max_str_len}",
                ]
        str_list += field_header + field_list
        str_str = '\n'.join(str_list)
        return str_str
                

    def __repr__(self) -> str:
        return self.__str__()
    
