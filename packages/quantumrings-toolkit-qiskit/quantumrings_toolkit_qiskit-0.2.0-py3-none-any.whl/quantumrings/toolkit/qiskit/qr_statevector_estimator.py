# This code is part of Quantum Rings toolkit for qiskit.
#
# (C) Copyright IBM 2022, 2024.
# (C) Copyright Quantum Rings Inc, 2024-2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

#
# This code is a derivative work of the qiskit provided StatevectorEstimator class
# See: https://github.com/Qiskit/qiskit/blob/stable/2.2/qiskit/primitives/statevector_estimator.py
# https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorEstimator
#

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from qiskit.quantum_info import SparsePauliOp

from qiskit.primitives.containers import DataBin, EstimatorPubLike, PrimitiveResult, PubResult
from qiskit.primitives.containers.estimator_pub import EstimatorPub
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit.primitives import StatevectorEstimator


import os
import platform

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from .qr_statevector import QrStatevector
from .qr_backend_for_qiskit import QrBackendV2
from .qr_estimator import QrEstimatorV2 as Estimator

class QrStatevectorEstimator(StatevectorEstimator):
    """
    An implementation of the StatevectorEstimator for the Quantum Rings backend
    """
    def __init__(
        self, *, default_precision: float = 0.0, seed: np.random.Generator | int | None = None, **kwargs
    ):
        """
        Constructor of the QrStatevectorEstimator class.

        Args:
            | default_precision (float): The default precision for the estimator if not specified during run.
            | seed (int): The seed or Generator object for random number generation.
            |             If None, a random seeded default RNG will be used.
        """
        self._default_precision = default_precision
        self._seed = seed

        token = None
        name = None
        backend_str = None
        gpu_id = 0

        self._qr_provider = None
        precision_ = "single"
        self._backend = None
        mode_ = "sync"

        if ( kwargs is not None):
            if ("token" in kwargs ):
                if isinstance( kwargs["token"], str):
                    token = kwargs["token"]
            if ("name" in kwargs ):
                if isinstance( kwargs["name"], str):
                    name = kwargs["name"]
            if ("backend" in kwargs ):
                if isinstance( kwargs["backend"], str):
                    backend_str = kwargs["backend"]
                elif isinstance( kwargs["backend"], QrBackendV2):
                    self._backend = kwargs["backend"]
            if ("precision" in kwargs ):
                if isinstance( kwargs["precision"], str):
                    precision = kwargs["precision"]
            if ("gpu" in kwargs ):
                if isinstance( kwargs["gpu"], int):
                    gpu_id = kwargs["gpu"] 
   
        if None == self._backend:
            if ( token != None ) and ( name != None ):
                self._qr_provider = QuantumRingsLib.QuantumRingsProvider(name = name, token = token)
            else:
                self._qr_provider = QuantumRingsLib.QuantumRingsProvider()

            if None == backend_str:
                self._backend = QrBackendV2(self._qr_provider, precision = precision, gpu = gpu_id)
            else:
                self._backend = QrBackendV2(self._qr_provider, backend=backend_str, precision = precision, gpu = gpu_id)

        if ( self._backend is None ):
            raise Exception ("Unable to obtain backend. Please check the arguments")
        
        shots_ = 1
        mode_ = "sync"
        performance_ = "HIGHESTEFFICIENCY"
        threshold_ = None
        transfer_to_cpu_ = True

        #
        # Check for configuration parameters through the options dictionary
        #

        if ( kwargs is not None):
            if ("shots" in kwargs ):
                if isinstance( kwargs["shots"], (int, np.int64)):
                    shots_ = kwargs["shots"]
                else:
                    raise Exception( "Invalid argument for shots")
                
            if ("mode" in kwargs ):
                if isinstance( kwargs["mode"], str):
                    mode_= kwargs["mode"].lower()
                    if (  mode_ not in ["sync", "async"]):
                        raise Exception( "Invalid argument for mode")
                else:
                    raise Exception( "Invalid argument for mode")
                
            if ("performance" in kwargs ):
                if isinstance(kwargs["performance"], str):
                    p = kwargs["performance"].upper()
                    if (p not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "CUSTOM"]):
                        raise Exception( "Invalid argument for performance")
                    performance_ = p
                else:
                    raise Exception( "Invalid argument for performance")

            if ("threshold" in kwargs ):
                if isinstance( kwargs["threshold"], int):
                    threshold_= kwargs["threshold"]
                else:
                    raise Exception( "Invalid argument for performance")

            if ("precision" in kwargs ):
                if isinstance( kwargs["precision"], str):
                    p = kwargs["precision"].lower()
                    if (p not in ["single", "double"]):
                        raise Exception( "Invalid argument for precision")
                    precision_ = p
                else:
                    raise Exception( "Invalid argument for precision_")

            if ("transfer_to_cpu" in kwargs ):
                if isinstance( kwargs["transfer_to_cpu"], bool):
                    transfer_to_cpu_  = kwargs["transfer_to_cpu"]
                else:
                    raise Exception( "Invalid argument for transfer_to_cpu")

        self._shots = shots_
        self._mode = mode_
        self._performance = performance_
        self._threshold = threshold_
        self._precision = precision_
        self._transfer_to_cpu =  transfer_to_cpu_
        self._qr_backend = self._backend._qr_backend 

        self._runtime_parameters = {}
        self._runtime_parameters["performance"]        = self._performance
        if ("CUSTOM" == self._performance):
            self._runtime_parameters["threshold"]      = self._threshold
        self._runtime_parameters["precision"]          = self._precision
        self._runtime_parameters["quiet"]              = True 
        self._runtime_parameters["defaults"]           = True
        self._runtime_parameters["transfer_to_cpu"]    = self._transfer_to_cpu
        self._runtime_parameters["backend"] = self._qr_backend
        self._runtime_parameters["mode"] = self._mode
        self._runtime_parameters["shots"] =self._shots

        super().__init__(
            default_precision = default_precision, 
            seed = seed, 
            )
        return

    @property
    def default_precision(self) -> float:
        """Return the default precision"""
        return self._default_precision

    @property
    def seed(self) -> np.random.Generator | int | None:
        """Return the seed or Generator object for random number generation."""
        return self._seed

    def run(
        self, pubs: Iterable[EstimatorPubLike], *, precision: float | None = None
    ) -> PrimitiveJob[PrimitiveResult[PubResult]]:
        """
        Executes the list of pubs.

        Args:
            | pubs (Iterable[EstimatorPubLike]): List of pubs to be estimated.
            | precision (float): Optional: The precsion with which the circuit is to be executed.

        Returns:
            PrimitiveJob object composed from the PrimitiveResult.

        """
        if precision is None:
            precision = self._default_precision
        coerced_pubs = [EstimatorPub.coerce(pub, precision) for pub in pubs]

        job = PrimitiveJob(self._run, coerced_pubs)
        job._submit()
        return job

    def _run(self, pubs: list[EstimatorPub]) -> PrimitiveResult[PubResult]:
        """
        Dispatcher for the pub.
        
        Args:
            | pubs ( list[EstimatorPub])): List of pubs to be estimated.

        Returns:
            PrimitiveResult object from the PubResult
        """
        return PrimitiveResult([self._run_pub(pub) for pub in pubs], metadata={"version": 2})

    def _run_pub(self, pub: EstimatorPub) -> PubResult:
        """
        Executes one pub instance.
        
        Args:
            | pub (EstimatorPub): The pub to be executed.

        Returns:
            The PubResult object.
        """
        
        circuit = pub.circuit
        observables = pub.observables
        parameter_values = pub.parameter_values
        precision = pub.precision
        
        bound_circuits = parameter_values.bind_all(circuit)
        
        bc_circuits, bc_obs = np.broadcast_arrays(bound_circuits, observables)
        
        evs = np.zeros_like(bc_circuits, dtype=np.float64)
        stds = np.zeros_like(bc_circuits, dtype=np.float64)
        
        for index in np.ndindex(*bc_circuits.shape):
            bound_circuit = bc_circuits[index]
            observable = bc_obs[index]
           
            estimator = Estimator(backend = self._backend)
            
            paulis, coeffs = zip(*observable.items())
            obs = SparsePauliOp(paulis, coeffs)  

            job = estimator.run([(bound_circuit, obs)])
            
            # Get results for the first (and only) PUB
            pub_result = job.result()[0]

            expectation_value = pub_result.data.evs
            
            evs[index] = expectation_value

        data = DataBin(evs=evs, stds=stds, shape=evs.shape)
        return PubResult(
            data, metadata={"target_precision": precision, "circuit_metadata": pub.circuit.metadata}
        )
