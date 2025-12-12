from pytest_httpserver.httpserver import HTTPServer
from pcss_qapi.base.connection_base import ApiConnection


def get_test_connection(httpserver: HTTPServer) -> ApiConnection:
    test_connection = ApiConnection(
        oauth_client_id='test',
        oauth_issuer=httpserver.url_for(''),
        oauth_min_ttl_seconds=60,
        api_health_url=httpserver.url_for('/health'),
        task_endpoints_url=httpserver.url_for('/tasks'),
        machine_endpoints_url=httpserver.url_for('/machines'),
    )
    return test_connection
