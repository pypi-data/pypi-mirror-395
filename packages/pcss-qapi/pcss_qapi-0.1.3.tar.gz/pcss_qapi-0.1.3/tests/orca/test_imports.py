import sys
import importlib
from unittest import mock
import pytest
from pytest import skip

try:
    import pcss_qapi.orca.backend
except ImportError:
    skip(allow_module_level=True)

from pcss_qapi.utils.exceptions import MissingOptionalDependencyError


def test_import_errors():
    with pytest.raises(MissingOptionalDependencyError) as e:
        with mock.patch.dict(sys.modules, {'ptseries': None, 'ptseries.tbi': None}):
            delset = set()
            for mod in sys.modules.keys():
                if 'pcss_qapi.orca' in mod:
                    delset.add(mod)
            for d in delset:
                sys.modules.pop(d)
            importlib.import_module('pcss_qapi.orca.backend')

    assert e.match(r'.*sdk\.orcacomputing.*')


def test_orca_task_can_be_imported_without_ptseries():
    with mock.patch.dict(sys.modules, {'ptseries': None, 'ptseries.tbi': None}):
        delset = set()
        for mod in sys.modules.keys():
            if 'pcss_qapi.orca' in mod:
                delset.add(mod)
        for d in delset:
            sys.modules.pop(d)
        from pcss_qapi.orca.orca_task import OrcaTask
