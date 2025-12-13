try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

def version():
    return __version__

from canopy.core.field import Field
from canopy.core.raster import Raster
from canopy.core.redspec import RedSpec
from canopy.core.constants import *
from canopy.sources import get_source
from canopy.util.fieldops import make_raster, make_lines, concat2, merge_fields, filter_region
from canopy.util.compare_ts import compare_ts
from canopy.util.overlap import overlap
from canopy.json.run_json import run_json
from canopy.tests.test_data.registry import get_test_data
