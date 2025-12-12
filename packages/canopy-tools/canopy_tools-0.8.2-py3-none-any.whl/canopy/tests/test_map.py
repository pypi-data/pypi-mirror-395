# -----------------------------------------
# | Tests for map generation using canopy |
# -----------------------------------------

import pytest
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend before pyplot import
from canopy import Field
import canopy.visualization as cv

DATA_DIR = Path("tests/test_data")

@pytest.mark.filterwarnings("ignore:FigureCanvasAgg is non-interactive, and thus cannot be shown:UserWarning")
def test_make_simple_map():
    """Test make_simple_map on example field without error"""

    field = Field.from_file(DATA_DIR / "anpp_spain_1990_2010.out.gz")

    cv.make_simple_map(
        field=field,
        layer="Total",
        timeop="sum",
        cb_label="Carbon Pool",
        unit="kgC m-2",
        title="Carbon Pool in Spain from 1990 to 2010 (summed over time)",
        n_classes=3,
        classification=[0, 10, 20, 40],
        palette="YlOrRd",
        custom_palette=None,
        extend="both",
        proj="EuroPP",
        force_zero=True,
        dark_mode=True,
        transparent=True,
        x_fig=10,
        y_fig=8
    )

@pytest.mark.filterwarnings("ignore:FigureCanvasAgg is non-interactive, and thus cannot be shown:UserWarning")
def test_make_diff_map():
    """Test make_simple_map on example field without error"""

    field_a = Field.from_file(DATA_DIR / "anpp_spain_1990_2010.out.gz")
    field_b = Field.from_file(DATA_DIR / "anpp_spain_1990_2010_mod.out.gz")

    cv.make_diff_map(
        field_a=field_a,
        field_b=field_b,
        layer="Total",
        timeop="sum",
        cb_label="Carbon Pool",
        unit="kgC m-2",
        title="Carbon Pool in Spain from 1990 to 2010 (summed over time)",
        n_classes=6,
        classification="linear",
        palette="YlOrRd",
        custom_palette=None,
        extend="both",
        proj="EuroPP",
        force_zero=True,
        dark_mode=True,
        transparent=True,
        x_fig=10,
        y_fig=8
    )