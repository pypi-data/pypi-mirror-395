"""Job ABCs"""
import os
import json
from typing import Any
from abc import ABC, abstractmethod
from pcss_qapi.utils import FSManager


class BaseRemoteJob(ABC):
    """Blueprint for an api remote job (non qiskit)"""

    def __init__(self, job_type: str) -> None:
        super().__init__()
        self.uid = None
        self.type = job_type  # Provider type

    @abstractmethod
    def _is_remote_available(self) -> bool:
        """Check if remote api is up"""
    @abstractmethod
    def _submit(self):
        """Submit job to remote"""

    @abstractmethod
    def _get_job_metadata(self) -> dict:
        """Additional metadata to save"""

    def _save_job(self):
        save_path = FSManager.get_task_directory(self.type)
        os.makedirs(save_path, exist_ok=True)
        with open(os.path.join(save_path, f'{self.uid}.json'), 'w+', encoding='UTF-8') as f:
            f.write(json.dumps(self._get_job_metadata()))

    def submit(self) -> None:
        """Submit job to remote"""
        if not self._is_remote_available():
            raise ValueError('Remote server is unreachable')
        self._submit()
        self._save_job()

    @property
    @abstractmethod
    def status(self) -> Any:
        """Task status"""

    @abstractmethod
    def results(self) -> Any:
        """Get task results"""

    @abstractmethod
    def cancel(self) -> bool:
        """Attempt to cancel task if it is queued, return True if successful"""
