import pandas as pd
from typing_extensions import Self
from canopy.grid.grid_abc import Grid
from canopy.grid.registry import register_grid

grid_type = 'empty'

@register_grid(grid_type)
class GridEmpty(Grid):
    """Grid associated to an empty DataFrame."""

    def __init__(self):
        super().__init__(grid_type, axis0='axis0', axis1='axis1')

    @classmethod
    def from_frame(cls, df: pd.DataFrame) -> Self:
        return cls()

    def get_sliced_grid(self, axis0_slice: tuple[float,float] | None, axis1_slice: tuple[float,float] | None) -> Grid:
        return GridEmpty()

    def get_reduced_grid(self, gridop: str, axis: str) -> Grid:
        return GridEmpty()

    def is_compatible(self, other) -> bool:
        return self.grid_type == other.grid_type

    def to_txt(self, fname: str, sep: str = ' ', randomize: bool = False) -> None:
        raise ValueError("Empty grid cannot be written to a text file.")

    def __add__(self, other):
        if not self.is_compatible(other):
            raise ValueError("Grids are not compatible")
        return GridEmpty()

