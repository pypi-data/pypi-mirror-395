"""Convenience backend for orca"""
from typing import Literal, Any
from collections.abc import Callable
import warnings

import numpy as np
import numpy.typing as npt


from pcss_qapi.utils.exceptions import MissingOptionalDependencyError
try:
    from ptseries.tbi.tbi_abstract import TBIDevice
    from ptseries.tbi.tbi_single_loop import TBISingleLoop
    from ptseries.tbi.tbi_multi_loop import TBIMultiLoop
    from ptseries.tbi.fixed_random_unitary import FixedRandomUnitary
    from ptseries.tbi import create_tbi
    from ptseries.algorithms.binary_solvers import BinaryBosonicSolver
    from ptseries.models import PTLayer

    from pcss_qapi.orca.ptseries_integration import PTAdapter  # pylint: disable=ungrouped-imports
    from pcss_qapi.base.connection_base import ApiConnection
except ImportError as ie:
    PACKAGE = str(ie.name)
    if 'ptseries' in PACKAGE:
        PACKAGE = 'ptseries (privately distributed - https://sdk.orcacomputing.com/)'
    raise MissingOptionalDependencyError(package_name=PACKAGE) from ie


class OrcaBackend:
    """Convenience class that provides different ptseries classes that use pcss_qapi"""

    _tbi_map = {
        'single_loop_simulator': 'single-loop',
        'multi_loop_simulator': 'multi-loop'
    }

    def __init__(self, connection: ApiConnection, name: str) -> None:
        self._connection = connection
        self.name = name

    def get_tbi(
        self,
        n_loops: int = 1,
        loop_lengths: list[int] | tuple[int, ...] | npt.NDArray[np.int_] | None = None,
        postselected: bool | None = None,
        postselection: bool = True,
        postselection_threshold: int | None = None,
        simulator_params: dict | None = None
    ) -> TBIDevice | TBISingleLoop | TBIMultiLoop | FixedRandomUnitary:
        """
        Get a PT instance connected to the api

        Args:
            n_loops (int):
                Number of loops in the TBI. Current PT devices support up to 2 loops. Defaults to 1.
            loop_lengths (list[int], tuple[int, ...], npt.NDArray[np.int_], optional):
                Lengths of the loops in the PT Series. If loop_lengths is specified then n_loops is not
                required, but if both are specified then they should be consistent. Defaults to None.
            postselected (bool):
                Deprecated: Whether postselection is enabled. Defaults to None.
            postselection (bool):
                Whether postselection is enabled. Defaults to False.
            postselection_threshold (int):
                The threshold for postselection. (1, number of input photons). Defaults to None. If None, and postselection is True, then
                the threshold is set to the number of input photons.
        """
        if simulator_params is None:
            simulator_params = {}

        if self.name in OrcaBackend._tbi_map:
            return create_tbi(
                tbi_type=OrcaBackend._tbi_map.get(self.name, None),
                n_loops=n_loops,
                loop_lengths=loop_lengths,
                postselected=postselected,
                postselection=postselection,
                postselection_threshold=postselection_threshold,
                **simulator_params
            )
        if len(simulator_params) > 0:
            warnings.warn('Simulator params have been passed into a real device TBI, they will be ignored.')

        return PTAdapter(
            connection=self._connection,
            n_loops=n_loops,
            loop_lengths=loop_lengths,
            postselected=postselected,
            postselection=postselection,
            postselection_threshold=postselection_threshold,
            machine=self.name
        )

    def get_ptlayer(
        self,
        in_features: int,
        input_state: list[int] | tuple[int, ...] | npt.NDArray[np.int_] | None = None,
        observable: Literal['mean', 'correlations', 'covariances', 'single-sample'] = "mean",
        gradient_mode: Literal['parameter-shift', 'finite-difference', 'spsa'] = 'parameter-shift',
        gradient_delta: float = np.pi / 10,
        n_samples: int = 100,
        tbi_params: dict | None = None,
        n_tiling: int = 1,
    ) -> PTLayer:
        """
        Get a PTLayer instance that communicates with the backend's assigned quantum computer.

        Args:
            input_state (list[int] | tuple[int, ...] | npt.NDArray[np.int_] | None, optional):
                Input state for the tbi. If None defaults to an alternating series of 0s and 1s. Defaults to None.
            in_features (int):
                Number fo layer input features.
            observable (Literal[&#39;avg, optional):
                Method of conversion from measurements to a tensor. Defaults to "avg-photons".
            gradient_mode (Literal[&#39;parameter, optional):
                Method to compute the gradient. Defaults to 'parameter-shift'.
            gradient_delta (float, optional):
                Delta to use with the parameter shift rule or for the finite difference. (0, 2*np.pi). Defaults to np.pi/10.
            n_samples (int, optional):
                Number of samples to draw. Current PT Devices support up to 5000 samples. Defaults to 100.
            tbi_params (dict | None, optional):
                Dictionary of optional parameters to instantiate the TBI. Defaults to None.
            n_tiling (int, optional):
                Uses n_tiling instances of PT Series and concatenates the results.
                Input features are distributed between tiles, which each have different trainable params.
                Defaults to 1.

        Returns:
            nn.Module: The parametrized PTLayer instance.
        """
        input_state = list(map(lambda x: x % 2, range(in_features + 1))) if input_state is None else input_state

        if tbi_params is None:
            tbi_params = {}

        if 'tbi_type' in tbi_params:
            warnings.warn('"tbi_type" is assigned automatically, ignoring set value.')
            tbi_params.pop('tbi_type')

        return PTLayer(
            input_state=input_state,
            in_features=in_features,
            observable=observable,
            gradient_mode=gradient_mode,
            gradient_delta=gradient_delta,
            n_samples=n_samples,
            n_tiling=n_tiling,
            tbi=self.get_tbi(**tbi_params)
        )

    def get_bbs(
        self,
        pb_dim: int,
        objective: np.ndarray | Callable[..., Any],
        input_state: list | None = None,
        tbi_params: dict | None = None,
        n_samples: int = 100,
        gradient_mode: Literal['parameter-shift', 'finite-difference', 'spsa'] = 'parameter-shift',
        gradient_delta: float = np.pi / 6,
        device: str = "cpu",
        sampling_factor: int = 2,
    ) -> BinaryBosonicSolver:
        """
        Get a BinaryBosonicSolver instance connected to the api

        Args:
            pb_dim (int):
                Dimension of the binary problem.
            objective (np.ndarray | Callable[..., Any]):
                The function to minimize.
            input_state (list | None, optional):
                The input state for the underlying PTLayer. Defaults to None.
            tbi_params (dict | None, optional):
                Optional params for the tbi. Defaults to None.
            n_samples (int, optional):
                Number of samples used for calculating expectation values. Current PT Devices support up to 5000 samples. Defaults to 100.
            gradient_mode (Literal, optional):
                Gradient algorithm to use. Defaults to 'parameter-shift'.
            gradient_delta (float, optional):
                Delta value for parameter shift of finite difference algorithms. (0, 2*np.pi). Defaults to np.pi/6.
            spsa_params (dict | None, optional):
                Optional parameters for the SPSA gradient method. Defaults to None.
            device (str, optional):
                PTLayer device. Defaults to "cpu".
            sampling_factor (int, optional):
                Number of times quantum samples are passed through the classical flipping layer. Positive integer. Defaults to 2.
            entropy_penalty (float, optional):
                Defaults to 0.1.

        Returns:
            BinaryBosonicSolver: BinaryBosonicSolver instance
        """

        if tbi_params is None:
            tbi_params = {}

        if 'tbi_type' in tbi_params:
            warnings.warn('"tbi_type" is assigned automatically, ignoring set value.')
            tbi_params.pop('tbi_type')

        bbs = BinaryBosonicSolver(
            pb_dim=pb_dim,
            objective=objective,
            input_state=input_state,
            n_samples=n_samples,
            gradient_mode=gradient_mode,
            gradient_delta=gradient_delta,
            sampling_factor=sampling_factor,
            tbi=self.get_tbi(*tbi_params)
        )

        bbs.pt_layer = bbs.pt_layer.to(device)
        return bbs

    def __repr__(self) -> str:
        return f"OrcaBackend[{self.name}] on connection {self._connection}"
