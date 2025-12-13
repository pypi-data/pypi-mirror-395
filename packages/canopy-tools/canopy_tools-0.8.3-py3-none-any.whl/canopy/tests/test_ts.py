# -----------------------------------------------
# | Tests for time series plotting using canopy |
# -----------------------------------------------

import pytest
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Set non-GUI backend before pyplot import
from canopy import Field
import canopy.visualization as cv

DATA_DIR = Path("tests/test_data")

@pytest.mark.filterwarnings("ignore:FigureCanvasAgg is non-interactive, and thus cannot be shown:UserWarning")
def test_make_time_series():
    """Test that make_time_series works on a test field."""

    field = Field.from_file(DATA_DIR / "anpp_spain_1990_2010.out.gz")

    cv.make_time_series(
        fields=field,
        layers=["Abi_alb","Bet_pen","Bet_pub","Que_rob","C3_gr"],
        gridop="sum",
        make_diff=False,
        yaxis_label="Carbon Pool (kgC m-2)",
        title="Carbon Pool in Spain from 1990 to 2010",
        unit="%",
        palette="Greens",
        move_legend=True,
        legend_style="default",
        max_labels_per_col=3,
        baseline=True,
        stacked=False,
        relative=True,
        dark_mode=True,
        x_fig=10,
        y_fig=5,
        linewidth=2.5,
        alpha=0.7,
        linestyle='--'
        )