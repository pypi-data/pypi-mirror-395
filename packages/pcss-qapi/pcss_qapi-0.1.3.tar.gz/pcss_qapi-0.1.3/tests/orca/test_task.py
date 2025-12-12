from pytest_httpserver import HTTPServer

from pytest import skip

try:
    from pcss_qapi.orca.orca_task import OrcaTask
except ImportError:
    skip(allow_module_level=True)
from tests.utils.conf import inject_conf

from tests.utils.orca import UID, REAL_QC, RESULTS, setup_server_orca_endpoints
from tests.utils.auth import setup_server_auth_endpoints
from tests.utils.connection import get_test_connection

from pcss_qapi import AuthorizationService


@inject_conf
def test_send(httpserver: HTTPServer):
    httpserver = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)

    AuthorizationService.login(conn, key="test")

    task = OrcaTask([1, 0, 1], [0.7853981633974483, 0.25], [1], "ORCA1", get_test_connection(httpserver))

    task.submit()

    assert task.uid == UID


@inject_conf
def test_response(httpserver: HTTPServer):
    httpserver = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)

    AuthorizationService.login(conn, key="test")

    task = OrcaTask([1, 0, 1], [0.7853981633974483, 0.25], [1], "ORCA1", get_test_connection(httpserver))

    task.submit()

    assert task.results() == RESULTS
    assert REAL_QC.num_reqs >= 1
