""" PT tbi Adapter """
from __future__ import annotations

import os

import numpy as np
import numpy.typing as npt

from ptseries.tbi.pt import PT
from ptseries.tbi.tbi_abstract import TBIDevice
from pcss_qapi.orca.orca_task import OrcaTask

from pcss_qapi.base.connection_base import ApiConnection


class PTAdapter(PT):
    """ Adapter for PT tbi

    Args:
        connection (ApiConnection):
            Connection object.
        n_loops (int):
            The number of loops in the TBI system. Defaults to 1
        loop_lengths (list[int], tuple[int, ...], npt.NDArray[np.int_], optional):
            The lengths of the loops in the TBI setup. Defaults to None.
        postselection (bool):
            Whether to use postselection or not during sampling. Defaults to True.
        postselection_threshold: (int, optional):
            The threshold for postselection. (1, number of input photons). Defaults to None. If None, and postselection is True then
            the threshold is set to the number of input photons.
        ip_address (str, optional):
            The IP address of the device. Defaults to None.
        machine (str, optional):
            The machine name. Defaults to None.
    """
    # pylint:disable=too-few-public-methods

    def __init__(  # pylint: disable=super-init-not-called
        self,
        connection: ApiConnection,
        n_loops: int = 1,
        loop_lengths: list[int] | tuple[int, ...] | npt.NDArray[np.int_] | None = None,
        postselected: bool | None = None,
        postselection: bool = True,
        postselection_threshold: int | None = None,
        ip_address: str | None = None,
        machine: str | None = None,
        **kwargs,
    ):
        TBIDevice.__init__(  # pylint: disable=non-parent-init-called
            self,
            n_loops=n_loops,
            loop_lengths=loop_lengths,
            postselected=postselected,
            postselection=postselection,
            postselection_threshold=postselection_threshold,  # pylint: disable=duplicate-code
            ip_address=ip_address,
            url=connection.task_endpoints_url,
            machine=machine,
        )

        self.pt_kwargs = kwargs
        self.connection = connection
        self.sample_async_flag = False

    def _submit_job_async(
        self,
        input_state: list[int] | tuple[int, ...],
        bs_angles: list[float] | tuple[float, ...],
        n_samples: int,
    ) -> str:
        """Prepares and sends sample request to PT.

        Args:
            input_state: description of input modes. The left-most entry corresponds to the first mode entering the loop.
            bs_angles: list of beam splitter angles
            n_samples: number of samples to draw. Current PT Devices support up to 5000 samples Defaults to 1.
        """
        task = OrcaTask(
            input_state=input_state,
            bs_angles=bs_angles,
            loop_lengths=self.loop_lengths,
            machine=self.machine,
            connection=self.connection,
            n_samples=n_samples,
            postselection=self.postselection,
            postselection_threshold=self.postselection_threshold,
            **self.pt_kwargs
        )
        task.submit()
        return task.uid

    def _request_samples(
        self,
        input_state: list[int] | tuple[int, ...],
        bs_angles: list[float] | tuple[float, ...],
        n_samples: int,
        # TODO: figure out if we should do anything with this arg
        save_dir: str | os.PathLike | None = None,  # pylint:disable=unused-argument
    ) -> npt.NDArray[np.int_]:
        """Prepares and sends sample request to PT.

        Args:
            input_state: description of input modes.
                The left-most entry corresponds to the first mode entering the loop.
            bs_angles: list of beam splitter angles
            n_samples: number of samples to draw. Defaults to 1.
            save_dir: Path to the directory in which to save results. If set to None the results are not saved. Defaults
                to None.
        """
        task = OrcaTask(
            input_state=input_state,
            bs_angles=bs_angles,
            loop_lengths=self.loop_lengths,
            machine=self.machine,
            connection=self.connection,
            n_samples=n_samples,
            postselection=self.postselection,
            postselection_threshold=self.postselection_threshold,
            **self.pt_kwargs
        )
        task.submit()
        result_json = task.results()
        samples = result_json
        samples = self._reformat_samples(samples)
        return samples
