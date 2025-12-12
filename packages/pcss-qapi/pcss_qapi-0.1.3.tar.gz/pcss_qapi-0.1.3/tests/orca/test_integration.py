from pytest_httpserver import HTTPServer
from pytest import skip

try:
    from ptseries.tbi.tbi_abstract import TBIDevice
    from ptseries.tbi.tbi_single_loop import TBISingleLoop
    from ptseries.tbi.tbi_multi_loop import TBIMultiLoop
    from ptseries.tbi.fixed_random_unitary import FixedRandomUnitary
    from ptseries.algorithms.binary_solvers import BinaryBosonicSolver
    from ptseries.models import PTLayer
    import torch
    from pcss_qapi import AuthorizationService
    from pcss_qapi.orca.backend import OrcaBackend
    from pcss_qapi.orca.provider import OrcaProvider
    from pcss_qapi.orca.ptseries_integration import PTAdapter

    from tests.utils.conf import inject_conf
    from tests.utils.connection import get_test_connection
    from tests.utils.orca import setup_server_orca_endpoints, REAL_QC
    from tests.utils.auth import setup_server_auth_endpoints


except ImportError:
    skip(allow_module_level=True)


def _check_backend_tbi(backend: OrcaBackend, tbi_type: type[TBIDevice] |
                       type[TBISingleLoop] | type[TBIMultiLoop] | type[FixedRandomUnitary]):
    assert isinstance(backend.get_tbi(), tbi_type)
    assert isinstance(backend.get_ptlayer(in_features=1).tbi, tbi_type)
    assert isinstance(backend.get_bbs(5, lambda x: 100).pt_layer.tbi, tbi_type)


def test_simulators():
    provider = OrcaProvider()
    sims = [provider.get_backend(i) for i in provider.available_backends(simulators=True)]
    for sim, tbi_type in zip(sims, [TBISingleLoop, TBIMultiLoop]):
        _check_backend_tbi(sim, tbi_type)


@inject_conf
def test_backend(httpserver):
    be = OrcaBackend(get_test_connection(httpserver), 'ORCA1')
    assert isinstance(be.get_tbi(), PTAdapter)
    assert isinstance(be.get_ptlayer(in_features=1), PTLayer)
    assert isinstance(be.get_bbs(5, lambda x: 100), BinaryBosonicSolver)


@inject_conf
def test_tbi(httpserver):
    httpserver: HTTPServer = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)
    AuthorizationService.login(conn, key="test")
    be = OrcaBackend(conn, 'ORCA1')
    tbi = be.get_tbi()
    tbi.sample([0, 1, 0], [2, 3], n_samples=100, n_tiling=1)
    assert REAL_QC.num_reqs >= 1


@inject_conf
def test_pt_layer(httpserver):
    httpserver: HTTPServer = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)
    AuthorizationService.login(conn, key="test")
    be = OrcaBackend(conn, 'ORCA1')
    layer = be.get_ptlayer(in_features=2)

    layer(torch.tensor([[1.0, 0.0]]))
    assert REAL_QC.num_reqs >= 1


@inject_conf
def test_bbs(httpserver):
    httpserver: HTTPServer = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)
    AuthorizationService.login(conn, key="test")
    be = OrcaBackend(conn, 'ORCA1')
    bbs = be.get_bbs(5, lambda x: 100)
    bbs.train(updates=1)
    assert REAL_QC.num_reqs >= 1


@inject_conf
def test_provider(httpserver):
    httpserver: HTTPServer = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)
    AuthorizationService.login(conn, key="test")
    prov = OrcaProvider(conn)

    assert len(prov.get_task_ids()) == 0

    backend_least_busy = prov.least_busy()

    assert isinstance(backend_least_busy, OrcaBackend)

    assert backend_least_busy.name == 'ORCA-PT-1-B'

    backend_connect = prov.get_backend('ORCA-PT-1-A')

    assert isinstance(backend_connect, OrcaBackend)

    backend_connect.get_ptlayer(in_features=2)(torch.tensor([[1.0, 0.0]]))

    task_id = prov.get_task_ids()[0]

    # task = prov.get_task(task_id)

    # assert isinstance(task, OrcaTask)
