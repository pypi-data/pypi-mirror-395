# \"\"\"Expose most of Python math module functions under aimath.math_ext namespace.\"\"\"

import math

from math import *

# re-export as names from this module; also provide __all__
__all__ = [name for name in dir(math) if not name.startswith("__")]
# convenience: alias common names
pi = math.pi
e = math.e
inf = math.inf
nan = math.nan
