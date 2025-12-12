"""ORCA Computing providers, backends, etc."""
import warnings

from pcss_qapi.utils.exceptions import MissingOptionalDependencyError
from .orca_task import OrcaTask

__all__ = ['OrcaTask']

# We want OrcaTask to be available even without ptseries
try:
    from .backend import OrcaBackend
    from .provider import OrcaProvider
    __all__ += ['OrcaProvider', 'OrcaBackend']
except MissingOptionalDependencyError as e:
    warnings.warn(e.msg)
