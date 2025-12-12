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
# This code is a derivative work of the qiskit provided SamplerQNN class
# See: https://qiskit-community.github.io/qiskit-machine-learning/_modules/qiskit_machine_learning/neural_networks/sampler_qnn.html#SamplerQNN
# https://qiskit-community.github.io/qiskit-machine-learning/stubs/qiskit_machine_learning.neural_networks.SamplerQNN.html
#


# pylint: disable=wrong-import-position,wrong-import-order

from quantumrings.toolkit.qiskit import QrSamplerV2
from quantumrings.toolkit.qiskit import QrBackendV2

from qiskit.primitives import BaseSamplerV1
from qiskit.primitives.base import BaseSamplerV2
from typing import Callable, cast, Iterable, Sequence

from qiskit.circuit import Parameter
from qiskit.primitives import BaseSampler, SamplerResult, Sampler
from qiskit.transpiler.passmanager import BasePassManager

from qiskit_machine_learning.neural_networks import SamplerQNN
from qiskit_machine_learning.gradients import (
    BaseSamplerGradient,
    ParamShiftSamplerGradient,
    SamplerGradientResult,
)

from qiskit.circuit import Parameter, QuantumCircuit

class QrSamplerQNN(SamplerQNN):
    def __init__(
        self,
        *,
        circuit: QuantumCircuit,
        sampler: BaseSampler | None = None,
        input_params: Sequence[Parameter] | None = None,
        weight_params: Sequence[Parameter] | None = None,
        sparse: bool = False,
        interpret: Callable[[int], int | tuple[int, ...]] | None = None,
        output_shape: int | tuple[int, ...] | None = None,
        gradient: BaseSamplerGradient | None = None,
        input_gradients: bool = False,
        pass_manager: BasePassManager | None = None,
        **kwargs,
        ):

        if ( isinstance(kwargs.get('backend'), QrBackendV2 ) ):
            self._backend = kwargs.get('backend')
        else:
            self._backend = None

        if isinstance( kwargs.get("precision"), str):
            self._precision = kwargs.get("precision")
        else:
            self._precision = None
        
        if isinstance( kwargs.get("gpu"), int):
            self._gpu_id = kwargs.get("gpu")
        else:
            self._gpu_id = None

        run_options = {}

        if None !=  self._gpu_id:
            run_options["gpu"] = self._gpu_id

        if None !=  self._precision:
            run_options["precision"] = self._precision

        if ( None == self._backend):
            qr_sampler = QrSamplerV2(**run_options)
        else:
            qr_sampler = QrSamplerV2(backend = self._backend, **run_options)
        
        super().__init__(
            circuit = circuit, 
            sampler = qr_sampler, 
            input_params = input_params, 
            weight_params = weight_params, 
            sparse = sparse, 
            interpret = interpret, 
            output_shape = output_shape, 
            gradient = gradient, 
            input_gradients = input_gradients,
            pass_manager = pass_manager,
            )
        return
    