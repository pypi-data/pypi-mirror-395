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
# This code is a derivative work of the qiskit provided StatevectorSampler class
# See: https://github.com/Qiskit/qiskit/blob/stable/1.3/qiskit/primitives/statevector_sampler.py
# https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.StatevectorSampler
#


# pylint: disable=wrong-import-position,wrong-import-order
from __future__ import annotations

import os
import platform

import warnings
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import NDArray

from qiskit import QuantumCircuit

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from .qr_backend_for_qiskit import QrBackendV2

from qiskit.primitives.containers import (
    BitArray,
    DataBin,
    PrimitiveResult,
    SamplerPubResult,
    SamplerPubLike,
)
from qiskit.primitives.containers.sampler_pub import SamplerPub
from qiskit.primitives.containers.bit_array import _min_num_bytes
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit.primitives import StatevectorSampler
from qiskit.primitives.statevector_sampler import _final_measurement_mapping


@dataclass
class _MeasureInfo:
    creg_name: str
    num_bits: int
    num_bytes: int
    qreg_indices: list[int]


class QrStatevectorSampler(StatevectorSampler):
    """
    The QrStatevectorSampler class.
    """
    def __init__(self, *, default_shots: int = 1024, seed: np.random.Generator | int | None = None, **kwargs):
        """
        Constructor of the QrStatevectorSampler class.
        Args:
            | default_shots (int):  The default shots for the sampler if not specified during run. By default it is 1024.
            | seed (int): Optional: The seed or Generator object for random number generation.
            |                       If None, a random seeded default RNG will be used.
        """

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
        
        shots_ = default_shots
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
            default_shots = default_shots, 
            seed = seed, 
            )
        return

    def run(
        self, pubs: Iterable[SamplerPubLike], *, shots: int | None = None
    ) -> PrimitiveJob[PrimitiveResult[SamplerPubResult]]:
        """
        Executes the list of pubs.
        
        Args:
            | pubs ( Iterable[SamplerPubLike])): List of pubs to be sampled.
            | shots (int): Number of samples for each of the pubs

        Returns:
            PrimitiveJob object from the PrimitiveResult
        """
        if shots is None:
            shots = self._default_shots
        coerced_pubs = [SamplerPub.coerce(pub, shots) for pub in pubs]
        if any(len(pub.circuit.cregs) == 0 for pub in coerced_pubs):
            warnings.warn(
                "One of your circuits has no output classical registers and so the result "
                "will be empty. Did you mean to add measurement instructions?",
                UserWarning,
            )

        job = PrimitiveJob(self._run, coerced_pubs)
        job._submit()
        return job

    def _run(self, pubs: Iterable[SamplerPub]) -> PrimitiveResult[SamplerPubResult]:
        """
        Dispatcher for the pub.
        
        Args:
            | pubs ( list[SamplerPub])): List of pubs to be estimated.

        Returns:
            PrimitiveResult object from the SamplerPubResult
        """
        
        results = [self._run_pub(pub) for pub in pubs]

        return PrimitiveResult(results, metadata={"version": 2})
    
    
    def qr_preprocess_circuit(self, circuit: QuantumCircuit):
        """
        Derives the _MeasurementInfo from the circuit and preconditions the same.

        Args:
            | circuit (QuantumCircuit ): The circuit to be preconditioned.

        Returns:
            | The preconditioned circuit, qargs for the final measurements, and the list of _MeasureInfo corresponding to the cregs.
        """
        num_bits_dict = {creg.name: creg.size for creg in circuit.cregs}
        mapping = _final_measurement_mapping(circuit)
        qargs = sorted(set(mapping.values()))
        qargs_index = {v: k for k, v in enumerate(qargs)}

        # num_qubits is used as sentinel to fill 0 in _samples_to_packed_array
        sentinel = len(qargs)
        indices = {key: [sentinel] * val for key, val in num_bits_dict.items()}
        
        for key, qreg in mapping.items():
            creg, ind = key
            indices[creg.name][ind] = qargs_index[qreg]
        
        meas_info = [
            _MeasureInfo(
                creg_name=name,
                num_bits=num_bits,
                num_bytes=_min_num_bytes(num_bits),
                qreg_indices=indices[name],
            )
            for name, num_bits in num_bits_dict.items()
        ]
        return circuit, qargs, meas_info

    def _run_pub(self, pub: SamplerPub) -> SamplerPubResult:
        """
        Executes one pub instance.
        
        Args:
            | pub (SamplerPub): The pub to be executed.

        Returns:
            The SamplerPubResult object.
        """

        circuit, qargs, meas_info = self.qr_preprocess_circuit(pub.circuit)

        bound_circuits = pub.parameter_values.bind_all(circuit)

        arrays = {
            item.creg_name: np.zeros(
                bound_circuits.shape + (pub.shots, item.num_bytes), dtype=np.uint8
            )
            for item in meas_info
        }

        for index, bound_circuit in np.ndenumerate(bound_circuits):
            self._runtime_parameters["shots"] = pub.shots
            
            my_dict = self._runtime_parameters
            my_dict.pop('shots', None)

            job = self._backend.run(bound_circuit, shots = pub.shots, **my_dict)
            result = job.result()
            samples = result.get_memory()
            
            samples_array = np.array([np.fromiter(sample, dtype=np.uint8) for sample in samples])

            del samples

            for item in meas_info:
                ary = self._samples_to_packed_array(samples_array, item.num_bits, item.qreg_indices)
                arrays[item.creg_name][index] = ary

            del samples_array

        meas = {
            item.creg_name: BitArray(arrays[item.creg_name], item.num_bits) for item in meas_info
        }

        return SamplerPubResult(
            DataBin(**meas, shape=pub.shape),
            metadata={"shots": pub.shots, "circuit_metadata": pub.circuit.metadata},
        )

    def _samples_to_packed_array(
        self,
        samples: NDArray[np.uint8], num_bits: int, indices: list[int]
    ) -> NDArray[np.uint8]:
        """
        A helper routine that packs the samples into an uint8 array.
        """
        # samples of `Statevector.sample_memory` will be in the order of
        # qubit_last, ..., qubit_1, qubit_0.
        # reverse the sample order into qubit_0, qubit_1, ..., qubit_last and
        # pad 0 in the rightmost to be used for the sentinel introduced by _preprocess_circuit.
        ary = np.pad(samples[:, ::-1], ((0, 0), (0, 1)), constant_values=0)
        # place samples in the order of clbit_last, ..., clbit_1, clbit_0
        ary = ary[:, indices[::-1]]
        # pad 0 in the left to align the number to be mod 8
        # since np.packbits(bitorder='big') pads 0 to the right.
        pad_size = -num_bits % 8
        ary = np.pad(ary, ((0, 0), (pad_size, 0)), constant_values=0)
        # pack bits in big endian order
        ary = np.packbits(ary, axis=-1)
        return ary