import pandas as pd
from canopy.core.field import Field
from canopy.grid.registry import get_grid
from canopy.grid.grid_abc import Grid
from canopy.grid.grid_empty import GridEmpty


def _select_overlap_exact(df1, df2):

    index_overlap = df1.index.intersection(df2.index)
    df1_overlap = df1.loc[index_overlap,:]
    df2_overlap = df2.loc[index_overlap,:]

    return df1_overlap, df2_overlap


def _select_overlap_with_spatial_tolerance(df1: pd.DataFrame, df2: pd.DataFrame, atol: float, use_coords: str | None = None):

    # Check use_coords before starting the calculations
    if use_coords not in [None, 'first', 'second']:
        raise ValueError("'use_coords' must either be 'first', 'second', or None (the default).")

    ax0, ax1 = df1.index.names[:2]
    coords_self = df1.reset_index().loc[:,[ax0, ax1, 'time']]
    coords_self['timestamp'] = coords_self.time.dt.to_timestamp().astype('datetime64[s]')
    coords_other = df2.reset_index().loc[:,[ax0, ax1, 'time']]
    coords_other['timestamp'] = coords_other.time.dt.to_timestamp().astype('datetime64[s]')

    cond1 = [(ax0, ax0, '>='), (ax1, ax1, '>='), ('timestamp', 'timestamp', '==')]
    cond2 = [(ax0, ax0, '>'), (ax1, ax1, '<'), ('timestamp', 'timestamp', '==')]
    cond3 = [(ax0, ax0, '<'), (ax1, ax1, '>'), ('timestamp', 'timestamp', '==')]
    cond4 = [(ax0, ax0, '<'), (ax1, ax1, '<'), ('timestamp', 'timestamp', '==')]

    # Have the next four lines ignore typing; the conditional_join method is not a Pandas standard method.
    # Instead, it is available through the pyjanitor library (https://pyjanitor-devs.github.io/pyjanitor/).
    # This seems to currently mess with mypy.
    dj1 = coords_self.conditional_join(coords_other, *cond1, use_numba=True) # type: ignore
    dj2 = coords_self.conditional_join(coords_other, *cond2, use_numba=True) # type: ignore
    dj3 = coords_self.conditional_join(coords_other, *cond3, use_numba=True) # type: ignore
    dj4 = coords_self.conditional_join(coords_other, *cond4, use_numba=True) # type: ignore

    mask = (dj1['left']
            .loc[:, [ax0, ax1]]
            .sub(dj1['right'].loc[:,[ax0, ax1]])
            .abs()
            .le(atol)
            .all(axis=1)
            )
    dj1 = dj1[mask]

    mask = (dj2['left']
            .loc[:, [ax0, ax1]]
            .sub(dj2['right'].loc[:,[ax0, ax1]])
            .abs()
            .le(atol)
            .all(axis=1)
            )
    dj2 = dj2[mask]

    mask = (dj3['left']
            .loc[:, [ax0, ax1]]
            .sub(dj3['right'].loc[:,[ax0, ax1]])
            .abs()
            .le(atol)
            .all(axis=1)
            )
    dj3 = dj3[mask]

    mask = (dj4['left']
            .loc[:, [ax0, ax1]]
            .sub(dj4['right'].loc[:,[ax0, ax1]])
            .abs()
            .le(atol)
            .all(axis=1)
            )
    dj4 = dj4[mask]

    dj = pd.concat([dj1, dj2, dj3, dj4], ignore_index=True, sort=False, copy=False)
    index1_overlap = dj['left'].set_index([ax0, ax1, 'time']).index
    df1_overlap = df1.loc[index1_overlap,:]
    index2_overlap = dj['right'].set_index([ax0, ax1, 'time']).index
    df2_overlap = df2.loc[index2_overlap,:]

    if use_coords == 'second':
        djj = dj.set_index([('left', ax0), ('left', ax1), ('left', 'time')])['right'].loc[:, [ax0, ax1, 'time']]
        djj.index.names=[ax0, ax1, 'time']
        df1_overlap = df1_overlap.join(djj).set_index([ax0, ax1, 'time'])
    elif use_coords == 'first':
        djj = dj.set_index([('right', ax0), ('right', ax1), ('right', 'time')])['left'].loc[:, [ax0, ax1, 'time']]
        djj.index.names=[ax0, ax1, 'time']
        df2_overlap = df2_overlap.join(djj).set_index([ax0, ax1, 'time'])

    return df1_overlap, df2_overlap


def overlap(field1: Field, field2: Field, atol: float | None = None, use_coords: str | None = None) -> tuple[Field, Field]:
    """Select overlapping field data rows

    This function takes two fields, and returns another two fields with the data corresponding to where the spatial and
    time coordinates of the original fields overlap. The overlap allows for a certain tolerance in the spatial coordinates.

    Parameters
    ----------
    field1 : Field
        The first field
    field2 : Field
        The second field
    atol : float | None
        If None (the default), the intersection of the indices is calculated exactly. Otherwise, it is done with the
        given absolute tolerance in the spatial coordinates separately (i.e; two coordinates are considered matching
        if the absolute difference between them is smaller or equal than the supplied 'atol')
    use_coords: str | None
        If None (the default), the returned fields have their original coordinates. If "first" ("second"), the returned
        fields will use the coordinates of the first (second field). See examples section.

    Returns
    -------
    Two fields holding the data from the original fields, but only where the original indices overlap.

    Notes
    -----
    Matching coordinates exactly is much faster than allowing for tolerance, so use atol=None, rather than atol=0, if you
    want an exact match!

    Example
    -------
    # This will match field entries with slightly offset spatial coordinates
    import canopy as cp

    # Load (dummy) data sources:
    my_source = cp.get_source("/path/to/some/data", "lpj_guess")
    my_other_source = cp.get_source("/path/to/some/other/data", "lpj_guess")

    # Load fields
    field1 = my_source.load_field('anpp')
    field2 = my_other_source.load_field('anpp')

    print(field1.data)
    #               TrBE  C4G
    # lon lat time           
    # 1.0 1.0 1989     0    0
    #         1990     1    2
    #     2.0 1989     2    4
    #         1990     3    6
    # 2.0 3.0 1989     4    8
    #         1990     5   10
    #         1991     6   12

    print(field2.data)
    #                TrBE  C4G
    # lon lat  time           
    # 1.1  2.1 1990     1    2
    # 2.1  3.1 1990     3    4
    #          1991     5    6
    #          1992     7    8
    # 3.1 -3.1 1984     9   10

    # Exact coordinate matching leads to empty fields:
    field1_overlap, field2_overlap = cp.overlap(field1, field2)
    print(field1)
    # 
    # Field is empty!
    # 
    # History
    # -------
    # [1] 2025-11-10 19:05:56: overlap: sliced with overlapping rows from another field (description: Pretend Annual NPP just for showcasing cp.overlap). The index intersection was calculated exactly. Field was sliced to empty.

    # Allowing some tolerance does the trick. Let's allow a tolerance of 0.2 degrees in the spatial coordinates
    field1_overlap, field2_overlap = cp.overlap(field1, field2, atol=0.2)

    print(field1_overlap.data)
    #               TrBE  C4G
    # lon lat time           
    # 1.0 2.0 1990     3    6
    # 2.0 3.0 1990     5   10
    #         1991     6   12
    
    print(field2_overlap.data)
    #               TrBE  C4G
    # lon lat time           
    # 1.1 2.1 1990     1    2
    # 2.1 3.1 1990     3    4
    #         1991     5    6

    # We can specify that the second field's coordinates should be used for both returned fields.
    # Having the same coordinates in both fields can help comparing them.

    field1_overlap, field2_overlap = cp.overlap(field1, field2, atol=0.2, use_coords="second")
    print(field1_overlap.data)
    #               TrBE  C4G
    # lon lat time           
    # 1.1 2.1 1990     3    6
    # 2.1 3.1 1990     5   10
    #         1991     6   12
    
    print(field2_overlap.data)
    #               TrBE  C4G
    # lon lat time           
    # 1.1 2.1 1990     1    2
    # 2.1 3.1 1990     3    4
    #         1991     5    6

    """

    if atol is not None and not field1.grid.is_compatible(field2.grid):
        raise ValueError("Exact overlap selection requires that the fields have compatible grids.")

    for ax1, ax2 in zip(field1.data.index.names[:2], field2.data.index.names[:2]):
        if ax1 != ax2:
            raise ValueError("Overlap selection requires that spatial axes have the same names for both fields.")

    if not (field1.time_freq == field2.time_freq):
        raise ValueError("Overlap selection requires that the time series of the fields have the same frequency.")

    if atol is None:
        df1, df2 = _select_overlap_exact(field1.data, field2.data)
        how = "exactly"
    else:
        df1, df2 = _select_overlap_with_spatial_tolerance(field1.data, field2.data, atol, use_coords)
        how = f"with tolerance {atol} in the spatial coordinates"

    log_message1 = f"overlap: sliced with overlapping rows from another field (description: {field2.metadata['description']}). The index intersection was calculated {how}."
    log_message2 = f"overlap: sliced with overlapping rows from another field (description: {field1.metadata['description']}). The index intersection was calculated {how}."
    if df1.empty:
        log_message1 += " Field was sliced to empty."
        log_message2 += " Field was sliced to empty."
        grid1: Grid = GridEmpty()
        grid2: Grid = GridEmpty()
    else:
        if use_coords is None:
            grid1 = get_grid(field1.grid.grid_type).from_frame(df1)
            grid2 = get_grid(field2.grid.grid_type).from_frame(df2)
        elif use_coords == 'first':
            grid1 = get_grid(field1.grid.grid_type).from_frame(df1)
            grid2 = get_grid(field1.grid.grid_type).from_frame(df1)
        elif use_coords == 'second':
            grid1 = get_grid(field2.grid.grid_type).from_frame(df2)
            grid2 = get_grid(field2.grid.grid_type).from_frame(df2)

    field1_overlap = Field(df1, grid1, modified=True)
    field1_overlap.copy_history(field1)
    field1_overlap.copy_md(field1)
    field1_overlap.log(log_message1)

    field2_overlap = Field(df2, grid2, modified=True)
    field2_overlap.copy_history(field2)
    field2_overlap.copy_md(field2)
    field2_overlap.log(log_message2)

    return field1_overlap, field2_overlap
