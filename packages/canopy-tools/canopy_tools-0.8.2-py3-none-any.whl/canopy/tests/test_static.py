# ------------------------------------------
# | Tests for static plotting using canopy |
# ------------------------------------------

import pytest
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend before pyplot import
from canopy import Field
import canopy.visualization as cv

DATA_DIR = Path("tests/test_data")

@pytest.mark.filterwarnings("ignore:FigureCanvasAgg is non-interactive, and thus cannot be shown:UserWarning")
def test_make_static_plot():
    """Test that make_static_plot works on two test fields."""

    field_a = Field.from_file(DATA_DIR / "anpp_spain_1990_2010.out.gz")
    field_b = Field.from_file(DATA_DIR / "anpp_spain_1990_2010_mod.out.gz")

    cv.make_static_plot(
        field_a=field_a,
        field_b=field_b,
        layers=["Abi_alb","Bet_pen","Bet_pub","Que_rob","C3_gr"],
        field_a_label="no mod",
        field_b_label="mod",
        unit_a="kgC m-2",
        unit_b="kgC m-2",
        title="Actual NPP in Spain (1990-2010)", 
        palette="tab10",
        move_legend = True,
        dark_mode=True, 
        transparent=False,
        x_fig=10,
        y_fig=10
        )