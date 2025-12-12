"""Backend provider for ORCA devices"""
import json
import os

import requests

from pcss_qapi.base.provider_base import BaseProvider
from pcss_qapi.orca.backend import OrcaBackend
from pcss_qapi.orca.orca_task import OrcaTask
from pcss_qapi.utils import FSManager
from pcss_qapi.utils.requests import raise_for_common

from pcss_qapi.auth.auth_service import AuthorizationService


class OrcaProvider(BaseProvider):
    """Backend provider for ORCA devices"""

    _task_type = 'orca'
    _always_available_backends = ['single_loop_simulator', 'multi_loop_simulator']

    def get_backend(self, backend_name: str) -> OrcaBackend:
        return OrcaBackend(self.connection, backend_name)

    def available_backends(self, simulators: bool = False):
        if simulators:
            return OrcaProvider._always_available_backends
        response = requests.get(self.connection.machine_endpoints_url, timeout=10)

        raise_for_common(response)
        return response.json().get('names', [])

    def least_busy(self) -> OrcaBackend:
        response = requests.get(
            f'{self.connection.machine_endpoints_url}/queue-count',
            headers={'X-API-Key': f'{AuthorizationService.get_api_key(self.connection)}'},
            timeout=10)

        raise_for_common(response)
        queue_counts = response.json()
        return self.get_backend(min(self.available_backends(False), key=lambda x: queue_counts.get(x, 0)))

    @staticmethod
    def get_task_ids() -> list[str]:
        """Get ids of all submitted tasks linked to this provider"""
        save_dir = FSManager.get_task_directory(OrcaProvider._task_type)
        if not os.path.exists(save_dir):
            return []
        return [x.split('.')[0] for x in os.listdir(save_dir)]

    def get_task(self, task_id: str) -> OrcaTask:
        """Get OrcaTask by task id"""
        with open(
            os.path.join(
                FSManager.get_task_directory(OrcaProvider._task_type),
                f'{task_id}.json'
            ),
            'r',
                encoding='utf-8') as f:
            meta = json.loads(f.read())

            task = OrcaTask(**meta, connection=self.connection)
            task._submitted = True  # pylint:disable = protected-access
            task.uid = task_id
            return task
