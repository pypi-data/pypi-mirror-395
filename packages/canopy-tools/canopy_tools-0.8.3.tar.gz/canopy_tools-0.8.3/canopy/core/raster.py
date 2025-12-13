import numpy as np
from dataclasses import dataclass

@dataclass
class Raster:
    xx: np.ndarray | None = None
    yy: np.ndarray | None = None
    vmap: np.ndarray | None = None
    labels: dict | None = None

