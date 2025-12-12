"""Connection definitions"""

from pcss_qapi.base.connection_base import ApiConnection

PcssQapiConnection = ApiConnection(
    oauth_client_id='jupyter.quantum.psnc.pl-notebooks',
    oauth_issuer='https://sso.classroom.pionier.net.pl/auth/realms/Classroom',
    oauth_min_ttl_seconds=60,
    api_health_url='https://api.quantum.psnc.pl/api/health/test-connection',
    task_endpoints_url='https://api.quantum.psnc.pl/api/open/tasks',
    machine_endpoints_url='https://api.quantum.psnc.pl/api/open/machines',
)


__all__ = ['PcssQapiConnection']
