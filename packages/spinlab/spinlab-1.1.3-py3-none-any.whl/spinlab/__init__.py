"""SpinLab - Bringing the Power of Python to Spin-NMR Spectroscopy"""

from .core.data import SpinData
from .core.ufunc import *
from .core.util import *

from .constants import *
from .fitting import *
from .math import *

from .io import *
from .io.save import save
from .io.load import load

from .analysis.relaxation_fit import *
from .analysis.simulate_enhancement_profiles import *
from .analysis.peaks import *

from .processing import *
from .widgets import *
from .plotting import *
from .reporting import *
from .version import __version__

# config
from .config.config import SpinLAB_CONFIG
