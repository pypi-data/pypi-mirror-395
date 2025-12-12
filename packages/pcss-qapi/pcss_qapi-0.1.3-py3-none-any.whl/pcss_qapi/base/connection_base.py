"""Connection base"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiConnection:
    """Base class for defining a new api connection"""

    oauth_client_id: str
    oauth_issuer: str
    oauth_min_ttl_seconds: int
    api_health_url: str
    task_endpoints_url: str
    machine_endpoints_url: str

    def __str__(self) -> str:
        return f"<{self.task_endpoints_url.replace('https://', '').replace('http://', '').split('/', maxsplit=1)[0]}>"

    def __repr__(self) -> str:
        return str(self)
