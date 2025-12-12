"""Uaaronium: Aaron's mathematics engine (v1.2)."""

from . import arithmetic
from . import number_systems
from . import roots
from . import logs_phi
from . import logs_phi_bridge
from . import taylor_engine
from . import differentiation
from . import partial_diff
from . import golden
from . import series_tools
from . import iterative
from . import physics

from .roots import nth_root, root_of_ten
from .logs_phi import ln, log10, log_base, phi_region_triplet
from .logs_phi_bridge import golden_region_constants, is_golden_region
from .golden import golden_sample, golden_mistake

__all__ = [
    'arithmetic', 'number_systems', 'roots', 'logs_phi', 'logs_phi_bridge',
    'taylor_engine', 'differentiation', 'partial_diff', 'golden',
    'series_tools', 'iterative', 'physics',
    'nth_root', 'root_of_ten', 'ln', 'log10', 'log_base',
    'phi_region_triplet', 'golden_region_constants', 'is_golden_region',
    'golden_sample', 'golden_mistake'
]
