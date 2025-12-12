import copy
import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime
from types import MappingProxyType
from typing import Optional, Union, Sequence, Callable, Literal, SupportsFloat, cast
from typing_extensions import Self
from canopy.readers.registry import get_reader, get_format_description
from canopy.grid import get_grid, get_grid_type
from canopy.grid.grid_abc import Grid
from canopy.grid.grid_empty import GridEmpty
from canopy.core.redspec import RedSpec
from canopy.source_data import get_source_data
import canopy.core.frameops as frameops
import janitor


class FieldData:
    """Validator class for the data parameter passed to Field"""

    private_name = '_data'

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, data):
        # Protect data from resetting
        if self.private_name in vars(obj):
            raise AttributeError("'Field.data' cannot be set.")
        self.validate(data)
        setattr(obj, self.private_name, data)

    def validate(self, data):
        # The data must be an instance of pandas DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("'data' must be a Pandas DataFrame object.")
        # The index must be a MultiIndex
        if not isinstance(data.index, pd.MultiIndex):
            raise ValueError("'data' must have a MultiIndex.")
        # MultiIndex must have at least 3 levels
        if len(data.index.names) < 3:
            raise ValueError("data's MultiIndex must have at least 3 levels.")
        # The first and second levels of the MultiIndex must be of numeric type
        # TODO: This doesn't work for reduced lon/lat. Think about this problem
        #for ilevel in range(2):
        #    if not pd.api.types.is_numeric_dtype(data.index.get_level_values(ilevel).dtype):
        #        raise ValueError(f"Level {ilevel} of data's MultiIndex must be of numeric dtype.")
        # The third level's name must be "time"
        if data.index.names[2] != 'time':
            raise ValueError("The name of the third level of data's MultiIndex must be 'time'.")
        # 'time' level must be of type PeriodIndex
        if not isinstance(data.index.get_level_values(2), pd.PeriodIndex):
            raise ValueError("Level 'time' of data's Index must be of PeriodIndex type.")


class Field:
    """Container for data derived from model output or observations

    This object contains model output or observation data and associated
    grid information. It allows for basic data manipulation, such as 
    time- and spatial reductions and slicing. The Field object is canopy's
    elemental interface between data and user.
    """

    data = FieldData()

    def __init__(self, data: pd.DataFrame, grid: Grid, modified: bool = False, source: str | None = None) -> None:
        """
        Parameters
        ----------
        data : pd.DataFrame
            Pandas DataFrame containing the Field's data (see specification below).
        grid : Grid
            A canopy Grid object (see Grid object documentation).
        modified : bool
            Whether the field being created has been modified (e.g. reduced).
        source : str
            The source to retrieve the file's metadata. The format for this argument is 'source:field'. For example, to read
            an LPJ-GUESS file and add metadata corresponding to Annual GPP:

            agpp = Field.from_file('/path/to/file/file_name.out', file_format='lpjg_annual', source='lpjguess:agpp')
        """

        self.data = data
        self._grid: Grid = grid
        self._modified: bool = modified
        if source is None:
            self._metadata: dict[str, str | float | int] = {
                    'name': '[no name]',
                    'description': '[no description]',
                    'units': '[no units]',
                    }
        else:
            src, fld = source.split(':')
            source_data = get_source_data(src)
            self._metadata = {
                    'name': source_data['fields'][fld]['name'],
                    'description': source_data['fields'][fld]['description'],
                    'units': source_data['fields'][fld]['units'],
                    }
        self._history: list[str] = []
        self._timeop: str | None = None
        time_index = cast(pd.PeriodIndex, data.index.get_level_values('time'))
        self._time_freq: str = str(time_index.freqstr)

        # Order MultiIndex, necessary for slicing
        # Attribute _lexsort_depth is not to be used directly; but Pandas will raise an unsorted index error
        # after slicing, even if is_monotonic_increasing returns True, because _lexsort_depth is incorrectly set (I think)
        # Mypy doesn't register this attribute of pd.MultiIndex -> ignore
        if self._data.index._lexsort_depth < 3: # type: ignore
            self._data: pd.DataFrame = self._data.sort_index(level=0)


    def __getitem__(self, layers):
        """
        Invoke `self.sel_layers` with indexing notation
        """
        return self.sel_layers(layers)

    
    def __setitem__(self, layers: str | Sequence[str], value: Union[SupportsFloat, np.ndarray, pd.DataFrame, 'Field']) -> None:

        if isinstance(layers, str):
            layers = [layers]

        if isinstance(value, SupportsFloat):
            self.data[layers] = float(value)
            what = f'the scalar {value}'
        elif isinstance(value, Field):
            frameops.check_indices_match(self.data, value.data)
            self.data[layers] = value.data.copy()
            what = f'the following layers from another Field: {value.layers}'
        else:
            raise ValueError("Can only assign another Field or a scalar.")
        
        self._modified = True
        log_message = f'Layers {list(layers)} were assigned {what}.'
        self.log(log_message)


    @property
    def grid(self) -> Grid:
        """Grid: The grid associated with the data"""
        return self._grid


    @property
    def modified(self) -> bool:
        """bool: True if the Field has been modified after loading."""
        return self._modified


    @property
    def metadata(self) -> MappingProxyType[str, str | float | int]:
        """dict: Field's metadata (units, etc...)"""
        return MappingProxyType(self._metadata)


    @property
    def history(self) -> list[str]:
        """list: Keeps the history of modifications of the Field"""
        return self._history

    
    @property
    def timeop(self) -> str | None:
        """str: returns the reduction operation applied to the time dimension (if any)."""
        return self._timeop


    @property
    def time_freq(self) -> str:
        """str: returns the sampling frequency of the time axis."""
        return self._time_freq


    @property
    def layers(self) -> list[str]:
        """str: returns a list with the Field's layer names."""
        return list(self.data.columns)


    @classmethod
    def from_file(cls,
                  path: str,
                  file_format: str | None = None,
                  grid_type: str | None = None, 
                  grid: Grid | None = None,
                  source: str | None = None,
                  **kwargs) -> Self:
        """Construct a Field object from an LPJ-GUESS output file.

        Parameters
        ----------
        path : str
            Path to output file.
        file_format : str
            One of the registered formats (see file_readers.py). For LPJ-GUESS standard output:
                - 'lpjg_annual' (annual output)
                - 'lpjg_monthly' (monthly output)
        grid : Grid
            A Grid object describing the grid associated to the data. If no Grid is passed, it is inferred from the dataframe.
        grid_type : str
            The type of grid associated to the data. Accepted values are ['sites', 'lonlat']
        source : str
            The source to retrieve the file's metadata. The format for this argument is 'source:field'. For example, to read
            an LPJ-GUESS file and add metadata corresponding to Annual GPP:

            agpp = Field.from_file('/path/to/file/file_name.out', file_format='lpjg_annual', source='lpjguess:agpp')
        kwargs
            The kwargs are passed to the file reader.

        Returns
        -------
        A Field object.

        Notes
        -----
        - When a Grid object is provided (via the grid argument), the Field is always created
          with this grid, regardless of the value of 'grid_type', which is overriden. It is the
          responsibility of the caller to provide a consistent grid object.
        - Otherwise, a Grid object is constructed. If grid_type == 'sites', a default Grid (no grid information) is created.
          Otherwise, a grid is inferred from the data.
        """

        if grid_type is None:
            grid_type = "lonlat"

        if file_format is None:
            file_format = "lpjg_annual"

        # TODO: I shouldn't need to pass grid_type other than in the kwargs to a reader
        # A reader should be Callable[[str, **kwargs], pd.DataFrame]
        df = get_reader(file_format)(path, grid_type, **kwargs)
        format_desc = get_format_description(file_format)

        # If a grid is provided, it should be used:
        if grid is not None:
            pass
        # If it is not provided, it needs to be constructed
        else:
            grid = get_grid(grid_type).from_frame(df)

        field = cls(df, grid, source=source) 
        field.log(f"Data read from {path}")
        field.add_md('file format', format_desc)
        field.add_md('original file', path)

        return field


    def add_md(self, key: str, value: str | float | int) -> None:
        """Add an entry to the metadata dictionary.

        Parameters
        ----------
        key : str
            The key under which the value is stored.
        value : str | float | int
            The value of the metadata entry.

        Example
        -------
        # Load field
        anpp = Field.from_file("/path/to/file/anpp.out")
        # Add the GCM used to force the simulation to the metadata
        field.add_md('gcm', 'MPIESM2.1')

        Notes
        -----
        If the key already exists in the metadata dictionary, a KeyError will be raised. In
        order to overwrite an entry, use the set_md method.
        """
        if key in self._metadata:
            raise KeyError(f"Key {key} already exists (use set_md method to replace it)")
        else:
            self._metadata[key] = value


    def set_md(self, key: str, value: str | float | int) -> None:
        """Add or replace an entry in the metadata dictionary.

        Parameters
        ----------
        key : str
            The key under which the value is stored.
        value : str | float | int
            The value of the metadata entry.

        Example
        -------
        # Load field
        anpp = Field.from_file("/path/to/file/anpp.out")
        # Fails because 'name' is set in the constructor
        field.add_md('name', 'NPP') # KeyError
        field.set_md('name', 'NPP') # Okay
        """
        self._metadata[key] = value


    def copy_md(self, field: 'Field') -> None:
        """Replace the metadata with a copy of the passed Field's.

        Parameters
        ----------
        field : Field
            The field whose metadata is to be copied.
        """
        self._metadata = copy.deepcopy(field._metadata)


    def log(self, entries: str | list[str]) -> None:
        """File one or more entries in the Field's history log.

        The function files the passed entry in the history log and
        adds a timestamp.

        Parameters
        ----------
        entries : str | list[str]
            The entry or list of entries to log. If a list is provided,
            the same timestamp will be attached to all entries.
        """
        if isinstance(entries, str):
            entries = [entries]
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for entry in entries:
            self._history.append(f"[{len(self.history) + 1}] {dt}: {entry}")


    def copy_history(self, field: 'Field') -> None:
        """Replace history with a copy of the history of the passed Field.

        Parameters
        ----------
        field : Field
            The field whose history is to be copied.
        """
        self._history = copy.deepcopy(field.history)


    def sel_slice(self, lon_slice: Optional[tuple[float,float]] = None,
                        lat_slice: Optional[tuple[float,float]] = None,
                        time_slice: Optional[tuple[int,int]] = None,
                        inplace: bool = False) -> Union[None,'Field']:
        """Select a time or spatial slice from the Field.

        Parameters
        ----------
        lon_slice : Optional[tuple[float,float]] = None
            Tuple or list of floats specifying a slice in longitude.
        lat_slice : Optional[tuple[float,float]] = None
            Tuple or list of floats specifying a slice in latitude.
        time_slice : Optional[tuple[int,int]] = None
            Tuple or list of ints specifying a year range.
        inplace : bool = False
            If True, the slicing is performed in place.

        Returns
        -------
        If inplace is True, the slicing is performed in place and the method returns None.
        Otherwise the method returns a Field object containing the sliced data.
        """

        #TODO: The time slice should be based on datetime objects
        df, grid, log_message = frameops.sel_slice(self.data, self.grid, lon_slice, lat_slice, time_slice)

        if inplace:
            index: pd.MultiIndex = cast(pd.MultiIndex, df.index)
            # Attribute _lexsort_depth is not to be used directly; but Pandas will raise an unsorted index error
            # after slicing, even if is_monotonic_increasing returns True, because _lexsort_depth is incorrectly set (I think)
            # Mypy doesn't register this attribute of pd.MultiIndex -> ignore
            if index._lexsort_depth < 3: # type: ignore
                df = df.sort_index(level=0)
            self._data = df
            self._grid = grid
            self._modified = True
            self.log(log_message)
            return None
        else:
            field = Field(df, grid, modified = True)
            field.copy_history(self)
            field.copy_md(self)
            field.log(log_message)
            return field


    def sel_layers(self, layers: str | Sequence[str] | pd.Index, inplace: bool = False) -> Union[None,'Field']:
        """Select one or more layers from the Field.

        Parameters
        ----------
        layers: str | Sequence[str]
            Layer name or list of layer names.
        inplace : bool = False
            If True, the selection is performed in place.

        Returns
        -------
        If inplace is True, the selection is performed in place and the method returns None.
        Otherwise the method returns a Field object containing the selected data.
        """

        if isinstance(layers, str):
            layers = [layers]

        log_message=f"Selected layers {list(layers)}."
        if inplace:
            self._data = self._data[layers]
            self._modified = True
            self.log(log_message)
            return None
        else:
            df = self._data[layers].copy()
            grid = copy.deepcopy(self._grid)
            field = Field(df, grid, modified=True)
            field.copy_history(self)
            field.copy_md(self)
            field.log(log_message)
            return field


    def drop_layers(self, layers: str | Sequence[str] | pd.Index, inplace: bool = False) -> Union[None,'Field']:
        """Drop one or more layers from the Field.

        Parameters
        ----------
        layers : str | list
            Layer name or list of layer names.
        inplace : bool = False
            If True, the layers are dropped from the current object.

        Returns
        -------
        If inplace is True, the layers are dropped from the current Field and the method returns None.
        Otherwise the method returns a Field object with the selected data.
        """

        if isinstance(layers, str):
            layers = [layers]

        log_message=f"Dropped layers {list(layers)}."
        if inplace:
            self._data.drop(layers, axis=1, inplace=True)
            self._modified = True
            self.log(log_message)
            return None
        else:
            df = self._data.drop(layers, axis=1)
            grid = copy.deepcopy(self._grid)
            field = Field(df, grid, modified=True)
            field.copy_history(self)
            field.log(log_message)
            return field


    def red_layers(self, redop: str, layers: Optional[Sequence[str] | pd.Index] = None,
                   name: Optional[str] = None, drop: bool = False, inplace: bool = False) -> Union[None,'Field']:
        """Perform a reduction operation on the Field's layers.

        Parameters
        ----------
        redop : str
            The reduction operation. One of 'sum', 'av', 'maxLay', '/'.
        layers : None or a list of strings.
            List of names of layers to be reduced. If None, all layers are reduced.
        name : None or str.
            Name of the new layer to store the reduction. If None, the redop argument is used.
        drop : bool
            If True, the reduced layers are dropped from the data.
        inplace : bool
            If True, the layers are reduced in the current object.

        Returns
        -------
        If inplace is True, the layers are reduced in the current Field and the method returns None.
        Otherwise the method returns a Field object with the reduced data.
        """
        if layers is None:
            layers = self._data.columns

        # Copy avoids warning (error)
        df_red = self._data.copy()

        if name is None:
            name = f"{redop}"

        if redop == 'sum':
            df_red[name] = df_red[layers].sum(axis=1)
        if redop == 'av':
            df_red[name] = df_red[layers].mean(axis=1)
        if redop == 'maxLay':
            df_red[name] = df_red[layers].idxmax(axis=1)
        if redop == '/':
            if not len(layers) == 2:
                raise ValueError(f"Operation '{redop}' requires exactly two operands")
            df_red[name] = df_red[layers[0]] / df_red[layers[1]]
        if drop:
            layers_to_drop = [l for l in layers if l != name]
            df_red.drop(layers_to_drop, axis=1, inplace=True)

        log_message=f"Layer reduction operation '{redop}' applied to layers {list(layers)}, stored as layer '{name}'.{' Original layers were dropped.' if drop else ''}"
        if inplace:
            self._data = df_red
            self._modified = True
            self.log(log_message)
            return None
        else:
            grid = copy.deepcopy(self._grid)
            field = Field(df_red, grid, modified=True)
            field.copy_history(self)
            field.log(log_message)
            return field


    def filter(self, query: str, fill_nan: bool = False, inplace: bool = False) -> Union[None, 'Field']:
        '''Filter rows based on boolean query

        Parameters
        ----------
        query: str
            The string describing the boolean query in terms of the index or layers
        fill_nan: bool
            If False, rows where the query is False are removed (default behaviour).
            If True, the resulting field's data has NaNs where the query is false.
        inplace: bool
            Whether to perform the operation in place

        Returns
        -------
        If inplace is True, the filtering is performed on the current Field and the method returns None.
        Otherwise the method returns a Field object with the reduced data.

        Example
        --------
        # Load field
        aaet = Field.from_file("/path/to/file/aaet.out")
        print(aaet.layers) # [..., 'Total']
        # Filter rows for which layer 'Total' is greater than 100
        aaet1 = aaet.filter('Total > 100')
        # Filter rows for which layer 'Total' is greater than 100 and layer 'C3G' is lower than 10 (inplace)
        aaet.filter('Total > 100 and C3G < 10', inplace=True)

        Notes
        -----
        See pandas documentation for DataFrame.query() for more details on the query string.
        '''
        if fill_nan:
            index = self.data.query(f'not ({query})').index
            if inplace:
                self.data.loc[index,:] = np.nan
                df = self.data
                self._modified = True
            else:
                df = self.data.copy()
                df.loc[index,:] = np.nan
        else:
            if inplace:
                self.data.query(query, inplace=True)
                df = self.data
                self._modified = True
            else:
                df = self.data.query(query)

        log_message = f"Filter data: query = '{query}'{', fill with NaNs.' if fill_nan else '.'}"

        if df.empty and not fill_nan:
            grid: Grid = GridEmpty()
            log_message += ' Filter operation yielded empty field.'
        else:
            grid = get_grid(self.grid.grid_type).from_frame(df)
        
        if inplace:
            self._data = df
            self._grid = grid
            self._modified = True
            self.log(log_message)
            return None
        else:
            field = Field(df, grid, modified=True)
            field.copy_history(self)
            field.copy_md(self)
            field.log(log_message)
            return field
        

    def red_time(self, timeop: str, freq: str | None = None, inplace: bool = False) -> Union[None,'Field']:
        """Perform a reduction operation on the time axis.

        Parameters
        ----------
        timeop : str
            The time reduction operation: one of 'av', 'sum'.
        freq : str | None = None
            A string specifying the frequency of the reduction. This is formed by an integer number and
            one of 'M', 'Y'. For example, to perform an average every five years, specify timeop='av' and
            freq='5Y'. If freq=None the whole time series is reduced.
        inplace : bool = False
            If True, the reduction is performed on the current Field.
            
        Returns
        -------
        If inplace is True, the reduction is performed on the current Field and the method returns None.
        Otherwise the method returns a Field object with the reduced data.
        """
        df_red, log_message = frameops.red_time(self._data, timeop, freq)

        if inplace:
            self._data = df_red
            self._timeop = timeop
            self._modified = True
            self.log(log_message)
            return None
        else:
            field_red = Field(df_red, copy.deepcopy(self._grid), modified=True)
            field_red._timeop = timeop
            field_red.copy_history(self)
            field_red.log(log_message)
            return field_red


    def red_space(self, gridop: str, axis: Optional[str] = None, inplace: bool = False) -> Union[None,'Field']:
        """Perform a reduction operation on the spatial axes.

        Parameters
        ----------
        gridop : str
            The spatial reduction operation: one of 'av', 'sum'.
        axis : str | None = None
            One of 'lon', 'lat', or 'both'. If not specified, the reduction is performed on both axes.
        inplace : bool = False
            If True, the reduction is performed on the current Field.
            
        Returns
        -------
        If inplace is True, the reduction is performed on the current Field and the method returns None.
        Otherwise the method returns a Field object with the reduced data.
        """

        if axis is None:
            axis = 'both'

        df_red, grid_red, log_message = frameops.red_space(self.data, self.grid, gridop, axis)

        if inplace:
            self._data = df_red
            self._grid = grid_red
            self._modified = True
            self.log(log_message)
            return None
        else:
            field_red = Field(df_red, grid_red, modified=True)
            field_red.copy_history(self)
            field_red.log(log_message)
            return field_red


    def reduce(self, redspec: RedSpec, inplace: bool = False) -> Union[None,'Field']:
        """Perform the selection/slicing/reduction operations specified in te passed RedSpec object.

        Parameters
        ----------
        redspec : RedSpec
            A RedSpec object specifying how to slice and/or reduce the data.
        inplace : bool = False
            If True, the reduction is performed on the current Field.
            
        Returns
        -------
        If inplace is True, the reduction is performed on the current Field and the method returns None.
        Otherwise the method returns a Field object with the reduced data.
        """
        df_red, grid_red, log_message = frameops.apply_reduction(self._data, self._grid, redspec)

        time_index = cast(pd.PeriodIndex, df_red.index.get_level_values('time'))
        if inplace:
            self._data = df_red
            self._grid = grid_red
            self._modified = True
            self.log(log_message)
            if redspec.timeop is not None:
                self._timeop = redspec.timeop
                setattr(self, '_time_freq', str(time_index.freqstr))
            return None
        else:
            field_red = Field(df_red, grid_red, modified=True)
            field_red.copy_history(self)
            field_red.log(log_message)
            return field_red


    def convert_units(self, factor: SupportsFloat, units: str, inplace: bool = False) -> Union[None, 'Field']:
        """Convert the field's units by a multiplicative factor

        Parameters
        ----------
        factor : SupportsFloat
            Scalar by which all values in the field's data are multiplied
        units : str
            The new units to be set in the metadata 'units' entry.
        inplace : bool = False
            If True, the reduction is performed on the current Field.

        Notes
        -----
        This function does not perform any checks on whether the passed factor or
        units string make sense! It just trusts that the user knows what they are doing.
        """
        try:
            df = self._data*float(factor)
        except ValueError:
            raise TypeError("'factor' must be of numeric type, or convertible to 'float'.")

        log_message = f'Units changed to {units} (factor: {factor}).'

        if inplace:
            self._data = df
            self.set_md('units', units)
            self._modified = True
            self.log(log_message)
            return None
        else:
            grid = copy.deepcopy(self.grid)
            field = Field(df, grid, modified=True)
            field.copy_history(self)
            field.set_md('units', units)
            field.log(log_message)
            return field


    def rename_layers(self, new_names: dict[str, str]) -> None:
        """Rename the field's layers

        Parameters
        ----------
        new_names : dict
            A dictionary mapping existing layer names to their new names.
        """
        self.data.rename(columns=new_names, inplace=True)
        self.log(f"Layers renamed: {new_names}")


    def apply(self, op: str | Callable, operand: SupportsFloat | list[str] | None = None, layers: str | list[str] | None = None, how: Literal['left', 'right'] = 'left', inplace: bool = False) -> Union[None,'Field']:
        """Apply an operation/function to selected layers

        Parameters
        ----------
        op : str | Callable
            Operation to apply to layers. If a callable is passed, it must be numpy-vectorizable.
        operand : str | list[str] | None
            Operand to combine with layers through 'op'. Operand can be a constant number or the name of a layer. In the latter
            case, the operation will be performed element-wise. If 'op' is a Callable, this parameter is ignored.
        layers : str | list[str] | None
            A list of the names of the layers to apply the operation to. If None, the operation is applied to all layers.
        how : str = 'left'
            Position of the layers in the operation. This argument is relevant for non-commutative operations. For example, if
            how == 'left', a '-' operation will be layers - operand. If how = 'right', the operation will be operand - layers.
        inplace : bool
            Whether to perform the operation in place.

        Returns
        -------
        A field with the modified layers, or None if the operation is performed in place.
        """

        commutative_ops = {
            '+':   frameops.apply_sum,
            'sum': frameops.apply_sum,
            '*':   frameops.apply_mul,
            'mul': frameops.apply_mul,
        }

        non_commutative_ops = {
            '-':   frameops.apply_sub,
            'sub': frameops.apply_sub,
            '/':   frameops.apply_div,
            'div': frameops.apply_div,
        }

        if layers is None:
            layers = self.layers
        elif isinstance(layers, str):
            layers = [layers]

        if isinstance(operand, str):
            operand = [operand]

        if (op in commutative_ops or op in non_commutative_ops) and operand is None:
            raise ValueError(f"Operation {op} requires an operand")

        if inplace:
            df = self.data
        else:
            df = self.data.copy()

        if callable(op):
            frameops.apply_function(df, layers, op)
        elif op in commutative_ops:
            # Ignoring typing; at this point it's alredy known that operand is not None, but mypy's narrowing doesn't catch it
            commutative_ops[op](df, operand, layers) # type: ignore
        elif op in non_commutative_ops:
            # Ignoring typing; at this point it's alredy known that operand is not None, but mypy's narrowing doesn't catch it
            non_commutative_ops[op](df, operand, layers, how) # type: ignore
        else:
            raise ValueError(f"Operation must be a callable or one of {list(commutative_ops.keys()) + list(non_commutative_ops.keys())}.")

        log_message = f"Applied operation '{op}' to layers {layers}."

        if not inplace:
            grid = copy.deepcopy(self.grid)
            field = Field(df, grid, modified=True)
            field.copy_history(self)
            field.log(log_message)
            return field
        else:
            self._modified = True
            self.log(log_message)
            return None


    def __str__(self) -> str:

        history_str = '\n'.join(self.history)

        if self.data.empty:
            repr_str = [
                    f"Field is empty!",
                    "",
                    f"History",
                    f"-------",
                    history_str,
                    ]

            return '\n'.join(repr_str)

        metadata_str = '\n'.join([f"{k}: {v}" for k, v in self.metadata.items()])
        grid_type = get_grid_type(self._grid)

        time_index = self.data.index.get_level_values('time')
        time_start = time_index.min().start_time
        time_end = time_index.max().end_time
        time_str = [f"Span: {time_start} - {time_end}",
                    f"Frequency: {self.time_freq}",
                    ]
        if self._timeop is not None:
            time_str.append(f"Reduction: '{self._timeop}'")

        repr_str = [
                    f"Data",
                    f"----",
                    metadata_str,
                    "",
                    f"Grid",
                    f"----",
                    f"{self._grid}",
                    "\n"
                    f"Time series",
                    f"-----------",
                    '\n'.join(time_str),
                    "\n"
                    f"History",
                    f"-------",
                    history_str,
                    ]
        return "\n".join(repr_str)


    def __repr__(self) -> str:
        return self.__str__()


    def to_xarray(self):
        raise NotImplementedError
        #return self._data.to_xarray().sortby('lon').sortby('lat').sortby('time')


    def to_netcdf(self, fname: Optional[str] = None):
        raise NotImplementedError
        # TODO: This doesn't work w/ PeriodIndex!
        #data_xr = to_xarray(self._data)
        #data_xr.to_netcdf(fname)


    def to_csv(self, fname: str):
        raise NotImplementedError
        #self._data.to_csv(fname)

