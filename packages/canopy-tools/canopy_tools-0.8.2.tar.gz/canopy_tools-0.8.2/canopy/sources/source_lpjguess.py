import os
import glob
from typing import Any
from types import MappingProxyType
from canopy.core.field import Field
from canopy.sources.source_abc import Source
from canopy.sources.registry import register_source
from canopy.source_data import get_source_data


@register_source('lpjguess')
class SourceLPJGuess(Source):
    """
    Source object for LPJ-GUESS output
    """

    def __init__(self, path: str, grid_type: str = 'lonlat') -> None:
        """
        Parameters
        ----------
        path: str
            The path of the directory that contains the LPJ-GUESS output
        """
        super().__init__(path, get_source_data('lpjguess'))

        self._field_paths: dict[str,str] = {}
        self._file_formats: dict[str,str] = {}
        self._unknown_formats: dict[str,str] = {}
        self._grid_type = grid_type

        # In LPJ-GUESS each variable is outputted to a different file. The file names
        #   (minus the extension) are the same as the keys used to register the fields
        #   in the JSON model description file.
        paths = glob.glob(path + "/*.out") + glob.glob(path + "/*.out.gz")
        for file_path in paths:
            field_id = os.path.basename(file_path).replace(".gz", "").replace(".out", "")
            if field_id in self.source_data['fields']:
                # I ignore typing errors referring to dynamically set _fields attribute in __init__ method
                self._fields[field_id] = None # type: ignore
                self._field_paths[field_id] = file_path
            else:
                self._unknown_formats[field_id] = file_path

            self._is_loaded[field_id] = False

        if len(self._fields) + len(self._unknown_formats) == 0: # type: ignore
            raise ValueError(f"No data, or no readable data, found in {path}")

        self._fields = dict(sorted(self._fields.items())) # type: ignore
        self._unknown_formats = dict(sorted(self._unknown_formats.items()))

    @property
    def grid_type(self) -> str:
        return self._grid_type

    @property
    def unknown_formats(self) -> MappingProxyType:
        """Contains a list of files in the source folder whose format is unknown."""
        return MappingProxyType(self._unknown_formats)


    def load_field(self, field_id: str, file_format: str | None = None) -> Field:
        """Load a field from this source.

        Parameters
        ----------
        field_id : str
            The field string identifier (coincides with the file name without extensions).
        file_format : str
            If the field metadata is not found in the source data, the file format needs to be
            specified. For known fields this argument is ignored.
        """
        if field_id not in self.fields and field_id not in self.unknown_formats:
            raise KeyError(f"Field '{field_id}' not found in source.")

        if field_id in self.unknown_formats:
            if file_format is None:
                raise ValueError("'file_format' must be specified for unknown format fields.")
            path = self._unknown_formats[field_id]
        else:
            if field_id in self.source_data['fields']:
                file_format = self.source_data['fields'][field_id]['file_format']
            else:
                file_format = self._file_formats[field_id]
            path = self._field_paths[field_id]

        field = Field.from_file(path, file_format=file_format, grid_type = self.grid_type)

        # Check if a field with field_id is registered, and copy the metadata
        if field_id in self.source_data['fields']:
            field.add_md('source', self.source)
            field.set_md('name', self.source_data['fields'][field_id]['name'])
            field.set_md('description', self.source_data['fields'][field_id]['description'])
            field.set_md('units', self.source_data['fields'][field_id]['units'])
        elif field_id in self.unknown_formats:
            # Now the format is known
            # The case where field_id is in unknown_formats and file_format is None has been
            #   already discarded above, but mypy doesn't catch it, hence: ignore
            self._file_formats[field_id] = file_format # type: ignore
            self._field_paths[field_id] = self._unknown_formats.pop(field_id)

        self.is_loaded[field_id] = True
        self._fields[field_id] = field

        return field


    def __str__(self) -> str:
        if len(self.unknown_formats) == 0:
            return super().__str__()
        unknown_formats_str = ["", "Fields with unknown file format: "]
        for field, path in self.unknown_formats.items():
            unknown_formats_str.append(f"      {field} ({path})")
        str_str = '\n'.join(([super().__str__()] + unknown_formats_str))
        return str_str


    def __repr__(self) -> str:
        return self.__str__()
