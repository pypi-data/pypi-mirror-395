# This code is part of Quantum Rings toolkit for qiskit-machine-learning.
#
# (C) Copyright IBM 2022, 2024.
# (C) Copyright Quantum Rings Inc, 2024, 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

#
# This code is a derivative work of the qiskit provided TrainableFidelityQuantumKernel class
# See: https://qiskit-community.github.io/qiskit-machine-learning/_modules/qiskit_machine_learning/kernels/trainable_fidelity_quantum_kernel.html#TrainableFidelityQuantumKernel
# https://qiskit-community.github.io/qiskit-machine-learning/stubs/qiskit_machine_learning.kernels.TrainableFidelityQuantumKernel.html
#

# pylint: disable=wrong-import-position,wrong-import-order

from __future__ import annotations

from typing import Sequence

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter, ParameterVector
from qiskit_machine_learning.state_fidelities import BaseStateFidelity

from qiskit_machine_learning.kernels.fidelity_quantum_kernel import FidelityQuantumKernel, KernelIndices
from qiskit_machine_learning.kernels.trainable_kernel import TrainableKernel

from .qr_fidelity_quantum_kernel import QrFidelityQuantumKernel
from quantumrings.toolkit.qiskit import QrBackendV2

class QrTrainableFidelityQuantumKernel(TrainableKernel, QrFidelityQuantumKernel):
    def __init__(
        self,
        *,
        feature_map: QuantumCircuit | None = None,
        fidelity: BaseStateFidelity | None = None,
        training_parameters: ParameterVector | Sequence[Parameter] | None = None,
        enforce_psd: bool = True,
        evaluate_duplicates: str = "off_diagonal",
         ** kwargs,
        ) -> None:
        
        if ( isinstance(kwargs.get('backend'), QrBackendV2 ) ):
            self._backend = kwargs.get('backend')
        else:
            self._backend = None

        run_options = { }

        if (None != self._backend):
            run_options["backend"] = self._backend

        super().__init__(
            feature_map = feature_map,
            fidelity   = fidelity,
            training_parameters = training_parameters,
            enforce_psd = enforce_psd,
            evaluate_duplicates = evaluate_duplicates,
            **run_options,
            )
        
        # override the num of features defined in the base class
        self._num_features = feature_map.num_parameters - self._num_training_parameters
        self._feature_parameters = [
        parameter
        for parameter in feature_map.parameters
        if parameter not in self._training_parameters
        ]
        self._parameter_dict = {parameter: None for parameter in feature_map.parameters}

    def _get_parameterization(
        self, x_vec: np.ndarray, y_vec: np.ndarray
        ) -> tuple[np.ndarray, np.ndarray, KernelIndices]:
        new_x_vec = self._parameter_array(x_vec)
        new_y_vec = self._parameter_array(y_vec)
    
        return super()._get_parameterization(new_x_vec, new_y_vec)

    def _get_symmetric_parameterization(
        self, x_vec: np.ndarray
        ) -> tuple[np.ndarray, np.ndarray, KernelIndices]:
        new_x_vec = self._parameter_array(x_vec)

        return super()._get_symmetric_parameterization(new_x_vec)