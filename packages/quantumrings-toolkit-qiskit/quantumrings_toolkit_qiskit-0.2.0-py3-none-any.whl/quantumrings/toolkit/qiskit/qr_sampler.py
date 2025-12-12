# This code is part of Quantum Rings toolkit for qiskit.
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
# This code is a derivative work of the qiskit provided Sampler V2 class
# See: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/sampler-v2
# https://github.com/Qiskit/qiskit-ibm-runtime/blob/stable/0.42/qiskit_ibm_runtime/sampler.py
#


# pylint: disable=wrong-import-position,wrong-import-order
import os
import platform

import warnings
from collections import defaultdict
from dataclasses import dataclass
from typing import Union, Iterable, Optional, Any

from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2
from qiskit.primitives.containers.sampler_pub import SamplerPub
from qiskit import transpile
from qiskit.primitives.containers.bit_array import _min_num_bytes
from qiskit.primitives.primitive_job import PrimitiveJob


if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from qiskit.primitives.containers import (
    BitArray,
    DataBin,
    PrimitiveResult,
    SamplerPubLike,
    SamplerPubResult,
)

from .qr_meas import meas
from .qr_translator import QrTranslator
from .qr_backend_for_qiskit import QrBackendV2
from .qr_session import QrSession


import numpy as np


@dataclass
class Options:
    """Options for :class:`~.QrSamplerV2`"""

    default_shots: int = 1024
    """The default shots to use if none are specified in :meth:`~.run`.
    Default: 1024.
    """

    seed_simulator: int | None = None
    """The seed to use in the simulator. If None, a random seed will be used.
    Default: None.
    """

    run_options: dict[str, Any] | None = None
    """A dictionary of options to pass to the backend's ``run()`` method.
    Default: None (no option passed to backend's ``run`` method)
    """


@dataclass
class _MeasureInfo:
    creg_name: str
    num_bits: int
    num_bytes: int
    start: int
    
class QrSamplerV2(BackendSamplerV2):
    """
    Implements a BackendSamplerV2 derived class for the QrBackendV2. 
    
    A tuple of ``(circuit, <optional> parameter values, <optional> shots)``, called a sampler
    primitive unified bloc (PUB) can be submitted to this class for execution.

    """
    def __init__(
        self,
        *, 
        backend: QrBackendV2 = None,
        mode: Optional[Union[QrBackendV2, QrSession]] = None,
        options: dict | None = None,
        run_options: dict | None = None
        ):
        """
        Args:
            | backend   (QrBackendV2): QrBackendV2 backend. Can be None.
            | mode      (Optional[Union[QrBackendV2, QrSession]]): Optional. Either QrBackendV2 or QrSession object or None.
            | options  : The options to control the defaults such as shots (``default_shots``)
            | run_options: See options.
        """

        token = None
        name = None
        backend_str = None
        precision = "single"
        gpu_id = 0
        qr_provider = None

        if ( options is not None):
            if ("token" in options ):
                if isinstance( options["token"], str):
                    token = options["token"]
            if ("name" in options ):
                if isinstance( options["name"], str):
                    name = options["name"]
            if ("backend" in options ):
                if isinstance( options["backend"], str):
                    backend_str = options["backend"]
            if ("precision" in options ):
                if isinstance( options["precision"], str):
                    precision = options["precision"]
            if ("gpu" in options ):
                if isinstance( options["gpu"], int):
                    gpu_id = options["gpu"]  

        if ( run_options is not None):
            if ("token" in run_options ):
                if isinstance( run_options["token"], str):
                    token = run_options["token"]
            if ("name" in run_options ):
                if isinstance( run_options["name"], str):
                    name = run_options["name"]
            if ("backend" in run_options ):
                if isinstance( run_options["backend"], str):
                    backend_str = run_options["backend"]
            if ("precision" in run_options ):
                if isinstance( run_options["precision"], str):
                    precision = run_options["precision"]
            if ("gpu" in run_options ):
                if isinstance( run_options["gpu"], int):
                    gpu_id = run_options["gpu"] 

        if ((backend is None) and (mode is None)):
            # if the user has not provided the backend,
            # first check if the user has provided the token and the name
            
            if ( token != None ) and ( name != None ):
                qr_provider = QuantumRingsLib.QuantumRingsProvider(name = name, token = token)
            else:
                qr_provider = QuantumRingsLib.QuantumRingsProvider()

            if None == backend_str:
                self._backend = QrBackendV2(qr_provider, precision = precision, gpu = gpu_id)
            else:
                self._backend = QrBackendV2(qr_provider, backend=backend_str, precision = precision, gpu = gpu_id)

            if (0 == self._backend._qr_backend.num_qubits):
                raise Exception("Either provide a valid QrBackendV2 object as a parameter or save your account credentials using QuantumRingsLib.QuantumRingsProvider.save_account method")
        
        elif None != backend:
            if (False == isinstance(backend, QrBackendV2)):
                raise Exception ("The backend for this class should be a Quantum Rings Backend.")
            else:
                self._backend = backend

        elif None != mode:
            if (True == isinstance(mode, QrBackendV2)):
                self._backend = mode
            elif (True == isinstance(mode, QrSession)):
                self._backend = mode.backend()
                

        self._qr_provider = self._backend._qr_provider
        self._qr_backend = self._backend._qr_backend
        self._precision = self._backend._precision        
        self._num_circuits = 1
        self._default_options = Options()
        
        
        shots_ = 1024
        mode_ = "sync"
        performance_ = "HIGHESTEFFICIENCY"
        threshold_ = None
        precision_ = "single"
        transfer_to_cpu_ = True

        #
        # Check for configuration parameters through the options dictionary
        #

        if ( options is not None):
            if ("shots" in options ):
                if isinstance( options["shots"], (int, np.int64)):
                    shots_ = options["shots"]
                else:
                    raise Exception( "Invalid argument for shots")
                
            if ("mode" in options ):
                if isinstance( options["mode"], str):
                    mode_= options["mode"].lower()
                    if (  mode_ not in ["sync", "async"]):
                        raise Exception( "Invalid argument for mode")
                else:
                    raise Exception( "Invalid argument for mode")
                
            if ("performance" in options ):
                if isinstance( options["performance"], str):
                    p = options["performance"].upper()
                    if (p not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "CUSTOM"]):
                        raise Exception( "Invalid argument for performance")
                    performance_ = p
                else:
                    raise Exception( "Invalid argument for performance")

            if ("threshold" in options ):
                if isinstance( options["threshold"], int):
                    threshold_= options["threshold"]
                else:
                    raise Exception( "Invalid argument for performance")

            if ("precision" in options ):
                if isinstance( options["precision"], str):
                    p = options["precision"].lower()
                    if (p not in ["single", "double"]):
                        raise Exception( "Invalid argument for precision")
                    precision_ = p
                else:
                    raise Exception( "Invalid argument for precision_")
 

            if ("transfer_to_cpu" in options ):
                if isinstance( options["transfer_to_cpu"], bool):
                    transfer_to_cpu_  = options["transfer_to_cpu"]
                else:
                    raise Exception( "Invalid argument for transfer_to_cpu")
        #
        # Check for configuration parameters through the run_options dictionary
        #
                    
        if ( run_options is not None):
            if ("shots" in run_options ):
                if isinstance( run_options["shots"], (int, np.int64)):
                    shots_ = run_options["shots"]
                else:
                    raise Exception( "Invalid argument for shots")
                
            if ("mode" in run_options ):
                if isinstance( run_options["mode"], str):
                    mode_ = run_options["mode"].lower()
                    if (mode_ not in ["sync", "async"]):
                        raise Exception( "Invalid argument for mode")
                    else:
                        mode_ = run_options["mode"]
                else:
                    raise Exception( "Invalid argument for mode")
                
            if ("performance" in run_options ):
                if isinstance( run_options["performance"], str):
                    p = run_options["performance"].upper()
                    if (p not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "CUSTOM"]):
                        raise Exception( "Invalid argument for performance")
                    else:
                        performance_ = run_options["performance"]
                else:
                    raise Exception( "Invalid argument for performance")
                
            if ("threshold" in run_options ):
                if isinstance( run_options["threshold"], int):
                    threshold_= run_options["threshold"]
                else:
                    raise Exception( "Invalid argument for performance")

            if ("precision" in run_options ):
                if isinstance( run_options["precision"], str):
                    p = run_options["precision"].lower()
                    if (p not in ["single", "double"]):
                        raise Exception( "Invalid argument for precision")
                    precision_ = p
                else:
                    raise Exception( "Invalid argument for precision_")
                
            if ("transfer_to_cpu" in run_options ):
                if isinstance( run_options["transfer_to_cpu"], bool):
                    transfer_to_cpu_  = run_options["transfer_to_cpu"]
                else:
                    raise Exception( "Invalid argument for transfer_to_cpu")            
                
        if "CUSTOM" == performance_ and None == threshold_:
            raise Exception( "Threshold must be provided for custom performance")

        # Dynamical decoupling options
        self._default_options.dynamical_decoupling = Options()
        self._default_options.dynamical_decoupling.enable = False
        self._default_options.dynamical_decoupling.sequence_type = "XY4"
        
        # Twirling options
        self._default_options.twirling = Options()
        self._default_options.twirling.enable_gates = False
        self._default_options.twirling.num_randomizations = 1
        
        self._default_options.shots = shots_
        self._default_options.mode = mode_
        self._default_options.performance = performance_
        self._default_options.precision = precision_
        self._default_options.threshold = threshold_
        self._default_options.quiet = True
        self._default_options.defaults = True
        self._default_options.generate_amplitude = False
        self._default_options.transfer_to_cpu = transfer_to_cpu_        

        self.default_shots = shots_

        super().__init__(backend = self._backend)

    @property
    def options(self) -> Options:
        """Returns the options"""
        return self._default_options
        
       
    def job_call_back(self, job_id, state, job) -> None:
        """
        Call back routine for the sampler
        """
        pass

    def run_sampler(self, circuit, parameter_values, shots, **run_options):
        """
        Executes one instance of the circuit.
        Args:
            | circuit (QuantumCircuit) : The qiskit quantum circuit to be exectuted
            | parameter_Values (NDArray or float) : optional parameter array, if the circuit is parametried.
            | shots (int) : Number of shots the circuit is to be sampled.
            | run_options (dict) : A dictionary of configuration parameters for the circuit execution.

        Returns:
            The Result object.

        """
        results = []

        # Validate the circuits parameter.
        if not isinstance(circuit, QuantumCircuit):
            raise Exception( "Invalid argument passed for Quantum Circuit.")

        # Fetch run time options
        if "shots" in run_options:
            self._shots = run_options.get("shots")
            if not isinstance(self._shots, (int, np.int64)):
                raise Exception( "Invalid argument for shots")
            if ( self._shots <= 0 ):
                raise Exception( "Invalid argument for shots")
        else:
            if shots != None:
                self._shots = shots
            else:
                self._shots = self._default_options.shots
            
        if "mode" in run_options:
            self._mode = run_options.get("mode")
            if not isinstance(self._mode, str):
                raise Exception( "Invalid argument for mode")
            else:
                self._mode = self._mode.lower()
                if (self._mode not in ["sync", "async"]):
                    raise Exception( "Invalid argument for mode")
        else:
            self._mode = self._default_options.mode

        if "performance" in run_options:
            self._performance = run_options.get("performance")
            if not isinstance(self._performance, str):
                raise Exception( "Invalid argument for performance")
            else:
                self._performance = self._mode.upper()
                if (self._performance not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "CUSTOM"]):
                    raise Exception( "Invalid argument for performance")
        else:
            self._performance = self._default_options.performance

        if ("threshold" in run_options ):
            if isinstance( run_options["threshold"], int):
                self._threshold_= run_options["threshold"]
            else:
                raise Exception( "Invalid argument for performance")
        else:
            self._threshold = self._default_options.threshold

        if ("precision" in run_options ):
            if isinstance( run_options["precision"], str):
                p = run_options["precision"].lower()
                if (p not in ["single", "double"]):
                    raise Exception( "Invalid argument for precision")
                self._precision = p
            else:
                raise Exception( "Invalid argument for precision_")
        else:
            self._precision = self._default_options.precision

        if ("transfer_to_cpu" in run_options ):
            if isinstance( run_options["transfer_to_cpu"], bool):
                self._transfer_to_cpu  = run_options["transfer_to_cpu"]
            else:
                raise Exception( "Invalid argument for transfer_to_cpu")
        else:
            self._transfer_to_cpu = self._default_options.transfer_to_cpu
                
        if "CUSTOM" == self._performance and None == self._threshold:
            raise Exception( "Threshold must be provided for custom performance")
    

        runtime_parameters = {}
        runtime_parameters["performance"]        = self._performance
        if ("CUSTOM" == self._performance):
            runtime_parameters["threshold"]      = self._threshold
        runtime_parameters["precision"]          = self._precision
        runtime_parameters["quiet"]              = self._default_options.quiet 
        runtime_parameters["defaults"]           = self._default_options.defaults
        runtime_parameters["generate_amplitude"] = self._default_options.generate_amplitude
        runtime_parameters["transfer_to_cpu"]    = self._default_options.transfer_to_cpu


        # Confirm we have the right number of params
   
        if (isinstance(parameter_values, np.ndarray)) or (isinstance(parameter_values, list)):
            if (circuit.num_parameters != len(parameter_values)):
                raise Exception (f"The given number of parameters {len(parameter_values)} does not equal the count of parameters {circuit.num_parameters} in the circuit.")
        elif (isinstance(parameter_values, np.float64)) or (isinstance(parameter_values, float)):
            if (circuit.num_parameters != 1):
                raise Exception (f"The given number of parameters 1 does not equal the count of parameters {circuit.num_parameters} in the circuit.")


        #Assign parameters
        if (circuit.num_parameters):
            if (isinstance(parameter_values, np.float64)):
                subs_params = []
                subs_params.append(parameter_values)
                run_input = circuit.assign_parameters(subs_params)
            else:
                run_input = circuit.assign_parameters(parameter_values)
        else:
            run_input = circuit


        #
        # Transpile the circuit now
        #

        qr_basis_gates = self._qr_backend._basis_gates
        qc_transpiled = transpile(run_input, basis_gates=qr_basis_gates, optimization_level=3)

        self._max_qubits = qc_transpiled.num_qubits #max_qubits
        self._max_clbits = qc_transpiled.num_clbits #max_clbits

        if ( self._max_qubits <= 0 ):
            raise Exception( "Submitted quantum circuit does not use any qubits")
        

        # if we get here, the measurement instructions, if any, are at the end of the circuit
        # create the quantum circuit now
        
        #TODO: Check control loops
        qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
        creg = QuantumRingsLib.ClassicalRegister(self._max_clbits, "meas")
        qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)

        qt = QrTranslator()
        qt.translate_quantum_circuit(qc_transpiled , qc, False)

        job = self._qr_backend.run(qc, shots = self._shots, mode = self._mode, **runtime_parameters)
        job.wait_for_final_state(0.0, 5.0, self.job_call_back)
        self._job_id = job.job_id

        results = job.result()

        return results


    def qr_analyze_circuit(self, circuit: QuantumCircuit) -> tuple[list[_MeasureInfo], int]:
        """
        Analyzes the information for each creg in a circuit and builds the _MeasureInfo
        Args:
            | circuit (QuantumCircuit) : The qiskit Quantum Circuit object to be analyzed

        Returns:
            | A list of _MeasureInfo, corresponding to each CREG n the system.
        
        """
        meas_info = []
        max_num_bits = 0
        for creg in circuit.cregs:
            name = creg.name
            num_bits = creg.size
            if num_bits != 0:
                start = circuit.find_bit(creg[0]).index
            else:
                start = 0
            meas_info.append(
                _MeasureInfo(
                    creg_name=name,
                    num_bits=num_bits,
                    num_bytes=_min_num_bytes(num_bits),
                    start=start,
                )
            )

            max_num_bits = max(max_num_bits, start + num_bits)
            
        return meas_info, _min_num_bytes(max_num_bits)

        
    def qr_postprocess_pub(
        self,
        result_memory: list[str],
        shots: int,
        shape: tuple[int, ...],
        meas_info: list[_MeasureInfo],
        max_num_bytes: int,
        circuit_metadata: dict,
    ) -> SamplerPubResult:
        """
        A routine to post process the pub and construct the SamplerPubResult
        Args:
            | result_memory (list[str]): An array of the measured bitstrings for a given clasical register, for the pub
            | shots (int): Number of shots
            | shape (tuple[int, ...]): Expected shape of the result data
            | meas_info (list[_MeasureInfo]): Corresponding _MeasureInfo list
            | max_num_bytes (int): Number of bytes required ot store each measured bitstring as a uint8 array
            | circuit_metadata (dict): Metadata of the circuit

        Returns:
            The SamplerPubResult object

        """

        if len(shape) == 0:
            num_blocks = 1
        else:
            num_blocks = shape[0]

        arrays = {}
        meas = {}
        
        for item in meas_info:
            arrays_list = []

            for block_idx in range(num_blocks):
                start = block_idx * shots
                end = min(start + shots, len(result_memory))
                block = result_memory[start:end]

                for b in block:
                    value = int(b, 2)
                    byte_data = value.to_bytes(item.num_bytes, byteorder='big')
                    np_row = np.frombuffer(byte_data, dtype=np.uint8)
                    arrays_list.append(np_row)

                arr = np.array(arrays_list, dtype=np.uint8)

                arrays[item.creg_name] = arr

        for item in meas_info:
            reshaped = arrays[item.creg_name].reshape(num_blocks, shots, arrays[item.creg_name].shape[1])
            meas[item.creg_name] = BitArray(reshaped, item.num_bits)
        
        return SamplerPubResult(
            DataBin(**meas, shape=shape),
            metadata={"shots": shots, "circuit_metadata": circuit_metadata},
        )


    def _run_pubs(self, pubs: list[SamplerPub], shots: int) -> list[SamplerPubResult]:
        """
        Compute results for pubs that all require the same value of ``shots``.
        
        Args:
            | pubs (list[SamplerPub]): The list of SamplerPubs to be processed
            | shots (int): Number of shots

        Returns:
            A list of SamplerPubResult objects corresponding to each pub

        """
        # prepare circuits
        bound_circuits = [pub.parameter_values.bind_all(pub.circuit) for pub in pubs]
    
        flatten_circuits = []
        for circuits in bound_circuits:
            flatten_circuits.extend(np.ravel(circuits).tolist())

        # Execite the circuits and collect the results in a 2d list
        result_memory = []
        for i in range(len(flatten_circuits)):
            result = self.run_sampler(flatten_circuits[i], None, shots = shots)
            bitstrings = result.get_memory()
            result_memory.append(bitstrings)
        
        results = []
        start = 0

        loop_index = 0
        for pub, bound in zip(pubs, bound_circuits):
            meas_info, max_num_bytes  = self.qr_analyze_circuit(pub.circuit)
            end = start + bound.size
            flat = [x for sublist in result_memory[start:end] for x in sublist]

            #print(f"Index: {loop_index} shots: {shots} shape: {bound.shape} start: {start} end: {end}")

            results.append(
                self.qr_postprocess_pub(
                    flat,
                    shots,
                    bound.shape,
                    meas_info,
                    max_num_bytes,
                    pub.circuit.metadata,
                )
            )
            start = end
            loop_index += 1

        return results
        
    

    def _run(self, pubs: Iterable[SamplerPub], *, shots: int | None = None) -> PrimitiveResult[SamplerPubResult]:
        """
        Dispatches the input pubs for execution.

        Args:
            | pubs (Iterable[SamplerPub]): List of SamplerPub objects for exection
            | shots (int): Number of shots

        Returns:
            The PrimitiveResult object composed from an array of SamplerPubResult objects. 

        """
        pub_dict = defaultdict(list)
        # consolidate pubs with the same number of shots
        for i, pub in enumerate(pubs):
            pub_dict[pub.shots].append(i)

        results = [None] * len(pubs)
        for shots, lst in pub_dict.items():
            # run pubs with the same number of shots at once
            pub_results = self._run_pubs([pubs[i] for i in lst], shots)
            # reconstruct the result of pubs
            for i, pub_result in zip(lst, pub_results):
                results[i] = pub_result
      
        # return results wrapped in PrimitiveResult
        return PrimitiveResult(results, metadata={"version": 2})


    def run(
        self, pubs: Iterable[SamplerPubLike], *, shots: int | None = None
        ) -> PrimitiveJob[PrimitiveResult[SamplerPubResult]]:
        """
        Executes the pubs and estimates all associated observables.

        Args:
            | pubs: The pub to preprocess.
            | shots: Number of times the circuit needs to be executed.

        Returns:
            The job associated with the pub
        """
        if None == shots:
            shots = self._default_options.shots

        coerced_pubs = [SamplerPub.coerce(pub, shots) for pub in pubs]

        my_sampler_job = PrimitiveJob(self._run, coerced_pubs, shots=shots)
        my_sampler_job._submit()
        return  my_sampler_job
    