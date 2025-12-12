# This code is part of Quantum Rings toolkit for qiskit.
#
# (C) Copyright IBM 2022, 2024.
# (C) Copyright Quantum Rings Inc, 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

#
# This code is a derivative work of the qiskit provided EstimatorV1 class
# See: https://github.com/Qiskit/qiskit/blob/stable/1.3/qiskit/primitives/estimator.py#L38-L172
# https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.Estimator
#

# pylint: disable=wrong-import-position,wrong-import-order

import os
import platform

from typing import List, Union, Tuple, Optional
from collections.abc import Iterable, Sequence

from qiskit.circuit import QuantumCircuit, Instruction
from qiskit.providers import Options, JobV1, JobStatus
from qiskit.providers.backend import BackendV2

from qiskit.primitives import BackendEstimator
from qiskit.result import Result
from qiskit.primitives.containers.estimator_pub import EstimatorPub
from qiskit.primitives.containers import EstimatorPubLike

from qiskit.primitives import DataBin
from qiskit.primitives import PubResult
from qiskit.primitives import PrimitiveResult, EstimatorResult
from qiskit.primitives import PrimitiveJob

from qiskit.quantum_info import Pauli
from qiskit.quantum_info.operators.symplectic.sparse_pauli_op import SparsePauliOp as SparsePauliOp
from qiskit.quantum_info.operators.base_operator import BaseOperator
from qiskit import transpile

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from .qr_translator import QrTranslator
from .qr_backend_for_qiskit import QrBackendV2
from .qr_session import QrSession

from dataclasses import dataclass
import numpy

import threading
import time

class QrEstimatorV1(BackendEstimator):
    """
    A derivative of the BackendEstimatorV1 class, to estimates expectation values of quantum circuits and observables using the Quantum Rings backend.

    An estimator is initialized with an empty parameter set. The estimator is used to
    create a :class:`~qiskit.providers.JobV1`, via the
    :meth:`qiskit.primitives.Estimator.run()` method. This method is called
    with the following parameters

    * quantum circuits (:math:`\\psi_i(\\theta)`): list of (parameterized) quantum circuits
      (a list of :class:`~qiskit.circuit.QuantumCircuit` objects).

    * observables (:math:`H_j`): a list of :class:`~qiskit.quantum_info.SparsePauliOp`
      objects.

    * parameter values (:math:`\\theta_k`): list of sets of values
      to be bound to the parameters of the quantum circuits
      (list of list of float).

    The method returns a :class:`~qiskit.providers.JobV1` object, calling
    :meth:`qiskit.providers.JobV1.result()` yields the
    a list of expectation values plus optional metadata like confidence intervals for
    the estimation.

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
            | backend: The Quantum Rings backend to run the primitive on.
            | options: The options to control the defaults
            | run_options: See options.
        """

        token = None
        name = None
        backend_str = None
        precision = "single"
        gpu_id = 0

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

        # Step 1: Get the backend to use
        if (backend is None) and ( mode is None):
            # if the user has not provided the backend,
            # first check if the user has provided the token and the name
            
            if ( token != None ) and ( name != None ):
                qr_provider = QuantumRingsLib.QuantumRingsProvider(name = name, token = token)
            else:
                qr_provider = QuantumRingsLib.QuantumRingsProvider()

            if None != backend_str:    
                self._backend = QrBackendV2(qr_provider, precision = precision, gpu = gpu_id)
            else:
                self._backend = QrBackendV2(qr_provider, backend=backend_str, precision = precision, gpu = gpu_id)

            if (self._backend._qr_backend.num_qubits == 0):
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

        self.lock = threading.Lock()
        
        # Dynamical decoupling options
        self._default_options.dynamical_decoupling = Options()
        self._default_options.dynamical_decoupling.enable = False
        self._default_options.dynamical_decoupling.sequence_type = "XY4"
        
        # Twirling options
        self._default_options.twirling = Options()
        self._default_options.twirling.enable_gates = False
        self._default_options.twirling.num_randomizations = 1
        
        shots_ = 1
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
                if isinstance( options["shots"], (int, numpy.int64)):
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
                    raise Exception( "Invalid argument for precision")
                
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
                if isinstance( run_options["shots"], (int, numpy.int64)):
                    shots_ = run_options["shots"]
                else:
                    raise Exception( "Invalid argument for shots")
                
            if ("mode" in run_options ):
                if isinstance( run_options["mode"], str):
                    mode_ = run_options["mode"].lower()
                    if ( mode_ not in ["sync", "async"]):
                        raise Exception( "Invalid argument for mode")
                else:
                    raise Exception( "Invalid argument for mode")
                
            if ("performance" in run_options ):
                if isinstance( run_options["performance"], str):
                    p = run_options["performance"].upper()
                    if (p not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "CUSTOM"]):
                        raise Exception( "Invalid argument for performance")
                    else:
                        performance_ = p
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


        self._default_options.shots = shots_
        self._default_options.mode = mode_
        self._default_options.performance = performance_
        self._default_options.precision = precision_
        self._default_options.threshold = threshold_
        self._default_options.quiet = True
        self._default_options.defaults = True
        self._default_options.generate_amplitude = False
        self._default_options.transfer_to_cpu = transfer_to_cpu_

        super().__init__(backend = backend)
     
    @property
    def options(self) -> Options:
        """Returns the options"""
        return self._default_options
        
    def job_call_back(self, job_id, state, job) -> None:
        pass

    def run_estimator(self, circuits, observables,  params, **run_options):
        results = []
        
        with self.lock:
            # Fetch run time options
            if "shots" in run_options:
                self._shots = run_options.get("shots")
                if not isinstance(self._shots, (int, numpy.int64)):
                    raise Exception( "Invalid argument for shots")
                if ( self._shots <= 0 ):
                    raise Exception( "Invalid argument for shots")
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
                    self._performance = self._performance.upper()
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
            if (isinstance(params, numpy.float64)):
                if (circuits.num_parameters != 1 ):
                    raise Exception ("The given number of parameters is less than the parameters in the circuit.")

            else:
                if params is not None: 
                    if (circuits.num_parameters > len(params)):
                        raise Exception ("The given number of parameters is less than the parameters in the circuit.")


            #Assign parameters
            if (circuits.num_parameters):
                if (isinstance(params, numpy.float64)):
                    subs_params = []
                    subs_params.append(params)
                    run_input = circuits.assign_parameters(subs_params)
                else:
                    if params is not None:
                        run_input = circuits.assign_parameters(params)
                    else:
                        raise Exception ("Invalid parameters passed.")

            else:
                run_input = circuits

            # Flatten the circuit and clean all debris
            qr_basis_gates = self._qr_backend._basis_gates
            qc_transpiled = transpile(run_input, basis_gates=qr_basis_gates, optimization_level=3)


            self._max_qubits = qc_transpiled.num_qubits
            self._max_clbits = qc_transpiled.num_clbits
            
            # check whether the Pauli operator sizes match  max_qubit

            if (isinstance(observables, Pauli)):
                pauli_string = observables.to_label()
                if (self._max_qubits != len(pauli_string)):
                    raise Exception( "The Pauli operator length is not matching number of qubits")
            elif (isinstance(observables, SparsePauliOp)):
                if (self._max_qubits != len(observables.paulis[0])):
                    raise Exception( "The Pauli operator length is not matching number of qubits")
            else:
                observable = observables[0]
                if (isinstance(observable, SparsePauliOp)):
                    if (self._max_qubits != len(observable.paulis[0])):
                        raise Exception( "The Pauli operator length is not matching number of qubits")
                elif (isinstance(observable, Pauli)):
                    pauli_string = observable.to_label()
                    if (self._max_qubits != len(pauli_string)):
                        raise Exception( "The Pauli operator length is not matching number of qubits")
                else:
                    raise Exception( "Unsupported observable format")
                
                        
         
            qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
            if ( self._max_clbits > 0):
                creg = QuantumRingsLib.ClassicalRegister(self._max_clbits, "meas")
                qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)
            else:
                creg = QuantumRingsLib.ClassicalRegister(self._max_qubits, "meas")
                qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)

            
            # Export the qiskit QuantumCircuit to QuantumRings Structure
            qt = QrTranslator()
            qt.translate_quantum_circuit(qc_transpiled, qc, True)
            
            # We must setup the Pauli operator now.
            # for each Pauli operator
            avg = 0.0

            if (isinstance(observables, Pauli)):
                sp = SparsePauliOp([observables.to_label()],coeffs=[1])
                pauli_list = sp.to_list()
            elif (isinstance(observables, SparsePauliOp)):
                pauli_list = observables.to_list()
            else:
                observable = observables[0]
                if (isinstance(observable, SparsePauliOp)):
                    pauli_list = observable.to_list()
                elif (isinstance(observable, Pauli)):
                    sp = SparsePauliOp([observable.to_label()],coeffs=[1])
                    pauli_list = sp.to_list()
                else:
                    raise Exception( "Unsupported observable format")


            # first execute the circuit
            job = self._qr_backend.run(qc, shots = 1, mode = self._mode, performance = self._performance, quiet = True)
            job.wait_for_final_state(0, 5, self.job_call_back)
            self._job_id = job.job_id   # Store the last used job ID as the reference job id.
            results = job.result()
            qubit_list = [i for i in range(0, self._max_qubits)]

            for p in range(len(pauli_list)):
                weight = pauli_list[p][1].real
                pauli  = pauli_list[p][0]

                expectation_value = results.get_pauliexpectationvalue( pauli,qubit_list,0,0).real * weight
                            
                avg = avg + expectation_value

            return avg
        
    
    def _run(
        self,
        circuits: tuple[QuantumCircuit, ...],
        observables: tuple[BaseOperator, ...],
        parameter_values: tuple[tuple[float, ...], ...],
        **run_options,):

        loop_index = 0
        results_data = numpy.array([])
        metadata = []

        if "shots" in run_options:
            shots = run_options["shots"]
        else:
            shots = self._default_options.shots
            run_options["shots"] = shots

        if (len(circuits) == 1):
            results_by_observables = []
            circuit = circuits[0]
            for observable_ in observables:
                if parameter_values is None:
                    param_ = None
                    results_by_parameter_values = self.run_estimator(circuit, observable_, param_, **run_options)
                else:
                    results_by_parameter_values = []
                    for param_ in  parameter_values:
                        results_by_parameter_values.append(self.run_estimator(circuit, observable_, param_, **run_options))
            
                results_by_observables.append(results_by_parameter_values)
                loop_index += 1
                metadata.append({"shots": shots})
            
            results_data = numpy.array(results_by_observables)
      
        else:
            for circuit in circuits:
                observable_ = observables[loop_index]
                if parameter_values is not None:
                    param_ = parameter_values[loop_index]
                else:
                    param_ = None

                results_data = numpy.append(results_data, self.run_estimator(circuit, observable_, param_, **run_options))

                loop_index += 1
                metadata.append({"shots": shots})

        return EstimatorResult(results_data, metadata=metadata )
    
    

    def run(
        self,
        circuits: Sequence[QuantumCircuit] | QuantumCircuit,
        observables: Sequence[BaseOperator | str] | BaseOperator | str,
        parameter_values: Sequence[Sequence[float]] | Sequence[float] | float | None = None,
        **run_options,
        ) -> PrimitiveJob[PrimitiveResult[PubResult]]:
        """
        Executes the pubs and estimates all associated observables.

        Args:
            | pubs: The pub to preprocess.
            | precision: None

        Returns:
            The job associated with the pub
        """
        circuit_list = []
        observable_list = []
        parameter_list = []

        if(isinstance(circuits, QuantumCircuit)):
            circuit_list.append(circuits)
        else:
            circuit_list = circuits

        if((isinstance(observables, str)) or (isinstance(observables, BaseOperator))):
            observable_list.append(observables)
        else:
            observable_list = observables

        if(isinstance(parameter_values, float)):
            parameter_list.append(parameter_values)
        else:
            parameter_list = parameter_values

        num_circuits_ = len(circuit_list)
        
       
        # We have preprocessed the arguments and arranged them in right order

        my_estimator_job = PrimitiveJob(self._run, circuit_list, observable_list, parameter_list, **run_options)
        my_estimator_job._submit()
        return  my_estimator_job

