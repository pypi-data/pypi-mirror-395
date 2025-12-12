"""
irradpy2 - Multi-source solar radiation dataset downloader and forecasting toolkit.

This package provides unified high-level APIs for:
- BSRN (Baseline Surface Radiation Network)
- MIDC (NREL)
- SRML (UOregon)
- SAURAN (South Africa)
- SURFRAD (NOAA)
- SOLRAD (NOAA)
- Forecasting tools (RNN / LSTM / Informer)

Users can either:
    from irradpy2 import midc
    midc.download_midc(...)

Or:
    from irradpy2.midc import download_midc
"""

__version__ = "0.2.5"

# Export module-level namespaces
from . import bsrn
from . import midc
from . import srml
from . import sauran
from . import solrad
from . import surfrad
from . import prediction

__all__ = [
    "bsrn",
    "midc",
    "srml",
    "sauran",
    "solrad",
    "surfrad",
    "prediction",
]
