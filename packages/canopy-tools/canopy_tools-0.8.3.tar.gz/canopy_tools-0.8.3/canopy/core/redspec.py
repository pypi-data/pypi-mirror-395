from typing import Optional
from dataclasses import dataclass

@dataclass
class RedSpec:
    layers: Optional[list[str] | str] = None
    time_slice: Optional[tuple[int,int]] = None
    lat_slice: Optional[tuple[float,float]] = None
    lon_slice: Optional[tuple[float,float]] = None
    gridop: str | None = None
    axis: str = 'both'
    timeop: str | None = None
    freq: str | None = None

    def __post_init__(self):
        if isinstance(self.layers, str):
            self.layers = [self.layers]

