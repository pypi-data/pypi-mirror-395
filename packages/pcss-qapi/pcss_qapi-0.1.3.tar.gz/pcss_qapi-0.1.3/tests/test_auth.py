import time
import pytest
from pytest_httpserver.httpserver import HTTPServer

from pcss_qapi.auth.auth_service import AuthorizationService
from pcss_qapi.auth.oauth_flow import OAuthManager

from tests.utils.auth import setup_server_auth_endpoints
from tests.utils.conf import inject_conf
from tests.utils.connection import get_test_connection
from tests.utils.orca import setup_server_orca_endpoints


def test_oauth_manager(httpserver):
    httpserver: HTTPServer = setup_server_auth_endpoints(httpserver)

    oauth_man = OAuthManager('banana', httpserver.url_for(''), 60)

    assert oauth_man.client_id == 'banana'
    assert oauth_man.issuer == httpserver.url_for('')
    assert oauth_man.min_ttl == 60

    assert oauth_man.device_endpoint == f'{httpserver.url_for("")}/device'
    assert oauth_man.token_endpoint == f'{httpserver.url_for("")}/token'

    acc, ref = oauth_man.get_device_flow_tokens()

    assert acc is not None
    assert ref is not None

    time.sleep(1)

    acc_refreshed, ref_refreshed = oauth_man.get_refreshed_tokens(ref)

    assert acc is not None
    assert ref_refreshed is not None
    assert acc_refreshed != acc
    assert ref != ref_refreshed


@inject_conf
@pytest.mark.skip("Secret auth for now")
def test_refresh(httpserver: HTTPServer):
    httpserver = setup_server_auth_endpoints(setup_server_orca_endpoints(httpserver))
    conn = get_test_connection(httpserver)

    AuthorizationService.login(conn, key="test")

    key = AuthorizationService.get_api_key(conn)

    time.sleep(2)

    key2 = AuthorizationService.get_api_key(conn)
    assert key != key2
