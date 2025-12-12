"""Provider ABCs"""
from abc import ABC, abstractmethod
from typing import Any

from pcss_qapi.base.connection_base import ApiConnection
from pcss_qapi.auth.connections import PcssQapiConnection


class BaseProvider(ABC):
    """Backend provider ABC"""

    def __init__(
        self,
        connection: ApiConnection = PcssQapiConnection
    ) -> None:
        self.connection = connection

    @abstractmethod
    def get_backend(self, backend_name) -> Any:
        """Get backend with the name of backend_name"""

    @abstractmethod
    def available_backends(self, simulators: bool = False) -> list[str]:
        """
        Return names of available backends for the authed user.

        Returns:
            list[str]: Backend names.
        """

    @abstractmethod
    def least_busy(self) -> Any:
        """
        Return least busy backend from the pool of **real** backends.

        Returns:
            object: Least busy backend.
        """
