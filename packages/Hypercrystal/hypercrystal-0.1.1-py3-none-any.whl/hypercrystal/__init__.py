from . import misc
from . import h2_math
from . import shapes
from . import tessellations
from . import projections
from . import notation

from .misc import *
from .h2_math import *
from .shapes import *
from .tessellations import *
from .projections import *

from .misc import __all__ as _misc_all
from .h2_math import __all__ as _math_all
from .shapes import __all__ as _shapes_all
from .tessellations import __all__ as _tessellation_all
from .projections import __all__ as _projections_all

__all__ = [
    "misc",
    "h2_math",
    "shapes",
    "tessellations",
    "projections",
    *_math_all,
    *_misc_all,
    *_shapes_all,
    *_tessellation_all,
    *_projections_all,
    "notation"
]

# suggestion shape functions -> (intersections, collisions, distances, generation)
# suggestion infinite lines
