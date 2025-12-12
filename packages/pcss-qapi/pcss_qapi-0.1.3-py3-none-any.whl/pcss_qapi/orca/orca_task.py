"""Methods for communicating with psnc quantum api"""
import time
import requests

from pcss_qapi.base.job_base import BaseRemoteJob
from pcss_qapi.base.connection_base import ApiConnection

from pcss_qapi.auth import AuthorizationService
from pcss_qapi.utils.requests import raise_for_common


class OrcaTask(BaseRemoteJob):
    """
    Represents a single task for orca on psnc quantum api.

    Args:
        input_state (list[int], tuple[int]):
            Description of input modes. The left-most entry corresponds to the first mode entering the loop.
        bs_angles (list[float], tuple[float]):
            List of beam splitter angles for the ORCA.
        loop_lengths (list[int] | tuple[int, ...] | npt.NDArray[np.int_]):
            Lengths of the loops in the PT Series.
        machine (str):
            Name of the device.
        connection (ApiConnection):
            Connection object.
        n_samples (int):
            Number of samples to draw. Current PT Devices support up to 5000 samples. Defaults to 200.
        postselection (bool):
            Whether postselection is enabled. Defaults to False.
        postselection_threshold (int):
            The threshold for postselection. (1, number of input photons). Defaults to None. If None, and postselection is True, then
            the threshold is set to the number of input photons.
    """

    def __init__(
            self,
            input_state,
            bs_angles,
            loop_lengths,
            machine,
            connection: ApiConnection,
            n_samples=200,
            postselection=False,
            postselection_threshold=None,
            **kwargs) -> None:

        self.machine = machine
        self.task_payload = {
            'input_state': input_state,
            'bs_angles': bs_angles,
            'n_samples': n_samples,
            'loop_lengths': loop_lengths,
            'postselection': postselection,
            'postselection_threshold': postselection_threshold,
            'machine': machine,
            'extra_options': kwargs
        }
        self.connection = connection
        self.uid: str
        self._job_ids = []
        self._results = []

        self._created_time = None

        self._submitted = False

        super().__init__('orca')

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-API-Key': f'{AuthorizationService.get_api_key(self.connection)}'
        }

    def _get_job_metadata(self) -> dict:
        return self.task_payload | {'url': self.connection.task_endpoints_url}

    def _is_remote_available(self) -> bool:
        return True
        # try:
        #     response = requests.get(self.connection.api_health_url, timeout=5)
        #     return response.ok
        # except Exception:  # pylint:disable = broad-exception-caught
        #     return False

    def _submit(self):
        """Submit task for execution on remote"""
        response = requests.post(
            self.connection.task_endpoints_url,
            headers=self._get_headers(),
            json={
                'machine': self.machine,
                'payload': self.task_payload
            },
            timeout=5
        )

        raise_for_common(response)

        response_data = response.json()

        self.uid = response_data.get('uid', None)
        self._created_time = response_data.get('created', None)

        if self.uid is None:
            raise ValueError('API did not return task UID')

    def _try_get_results(self):
        try:
            response = requests.get(
                f'{self.connection.task_endpoints_url}/{self.uid}/results',
                headers=self._get_headers(),
                timeout=1
            )

            if not raise_for_common(response, default_raises_generic=False):
                return {}
        # Sometimes the api times out on result collection, quirky... TODO: check if this can be removed in the future.
        except requests.ReadTimeout:
            return {}

        response_data = response.json()

        return response_data

    def results(self) -> list[str]:
        """
        Get task results. Blocks the thread until results are available.

        Returns:
            list[str]: List of bitstrings obtained from runs.
        """
        if self._results != []:
            return self._results

        while not self.status == "Completed":
            time.sleep(0.5)

        res = self._try_get_results()
        if res == {}:
            raise ValueError("Task results have been deleted from remote.")

        if not isinstance(res, list):
            raise ValueError(f'Invalid result type: {type(res)}, {res}')

        self._results = res
        return res

    @property
    def status(self):
        """Task status"""
        response = requests.get(
            f'{self.connection.task_endpoints_url}/{self.uid}/status',
            headers=self._get_headers(),
            timeout=5
        )

        raise_for_common(response)

        response_data = response.json()

        return response_data.get('status', 'Unknown')

    def cancel(self) -> bool:
        response = requests.post(
            f'{self.connection.task_endpoints_url}/{self.uid}/cancel',
            headers=self._get_headers(),
            timeout=5
        )

        return response.ok
