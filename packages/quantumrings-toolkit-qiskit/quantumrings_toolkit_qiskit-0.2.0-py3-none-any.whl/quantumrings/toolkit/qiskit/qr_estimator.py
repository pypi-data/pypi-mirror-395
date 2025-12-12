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
# This code is a derivative work of the qiskit provided EstimatorV2 class
# See: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/estimator-v2
# https://github.com/Qiskit/qiskit-ibm-runtime/blob/stable/0.42/qiskit_ibm_runtime/estimator.py
#

# pylint: disable=wrong-import-position,wrong-import-order

import os
import platform

import numpy as np
from collections.abc import Sequence
from typing import List, Union, Iterable, Optional

from qiskit.circuit import QuantumCircuit
from qiskit.providers import Options

from qiskit.primitives import BackendEstimatorV2
from qiskit.primitives.containers.estimator_pub import EstimatorPub
from qiskit.primitives.containers import EstimatorPubLike
from qiskit import transpile


if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from qiskit.primitives import DataBin
from qiskit.primitives import PubResult
from qiskit.primitives import PrimitiveResult
from qiskit.primitives import PrimitiveJob

from dataclasses import dataclass

from .qr_translator import QrTranslator
from .qr_backend_for_qiskit import QrBackendV2
from .qr_session import QrSession

from qiskit.quantum_info.operators.base_operator import BaseOperator
from qiskit.quantum_info.operators.symplectic.sparse_pauli_op import SparsePauliOp as SparsePauliOp
from qiskit.quantum_info import PauliList
from qiskit.quantum_info.operators.symplectic.base_pauli import BasePauli


class QrEstimatorV2(BackendEstimatorV2):
    """
    Given an observable of the type
    :math:`O=\\sum_{i=1}^Na_iP_i`, where :math:`a_i` is a complex number and :math:`P_i` is a
    Pauli operator, the estimator calculates the expectation :math:`\\mathbb{E}(P_i)` of each
    :math:`P_i` and finally calculates the expectation value of :math:`O` as
    :math:`\\mathbb{E}(O)=\\sum_{i=1}^Na_i\\mathbb{E}(P_i)`. The reported ``std`` is calculated
    as

    .. math::

        \\frac{\\sum_{i=1}^{n}|a_i|\\sqrt{\\textrm{Var}\\big(P_i\\big)}}{\\sqrt{N}}\\:,

    where :math:`\\textrm{Var}(P_i)` is the variance of :math:`P_i`, :math:`N=O(\\epsilon^{-2})` is
    the number of shots, and :math:`\\epsilon` is the target precision [1].

    Each tuple of ``(circuit, observables, <optional> parameter values, <optional> precision)``,
    called an estimator primitive unified bloc (PUB), produces its own array-based result. The
    :meth:`~.QrEstimatorV2.run` method can be given a sequence of pubs to run in one call.

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
        Constructor for the QrEstimatorV2 class.

        Args:
            | backend: The Quantum Rings backend to run the primitive on.
            | options: The options to control the defaults shots (``default_shots``)
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
        if ((backend is None) and (mode is None)):
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
        
        #
        # if we get here, we have a proper backend to work with
        #

        self._qr_provider = self._backend._qr_provider
        self._qr_backend = self._backend._qr_backend
        self._precision = self._backend._precision
        self._num_circuits = 1
        self._default_options = Options()
        
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
                if isinstance( run_options["shots"], (int, np.int64)):
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

        super().__init__(backend = self._backend)
     
    @property
    def options(self) -> Options:
        """
        Returns the default options
        """
        return self._default_options
        
    def job_call_back(self, job_id, state, job) -> None:
        """
        Call back for the job
        """
        pass


    def init_observable(self, observable: BaseOperator | str) -> SparsePauliOp:
        """
        Restructures the observable.
        """
        if isinstance(observable, SparsePauliOp):
            return observable
        elif isinstance(observable, BaseOperator) and not isinstance(observable, BasePauli):
            raise Exception(f"observable type not supported: {type(observable)}")
        else:
            if isinstance(observable, PauliList):
                raise Exception(f"observable type not supported: {type(observable)}")
            elif isinstance(observable, tuple):
                return observable
            elif isinstance(observable, np.ndarray):
                observable_array = []
                for obs in observable:
                    for ob in obs:
                        observable_array.append(ob)
                return observable_array
            return SparsePauliOp(observable)
        

    def validate_observables(
            self,
            observables: Sequence[BaseOperator | str] | BaseOperator | str,
            ) -> tuple[SparsePauliOp, ...]:
        """
        Validates the integrity of the observables
        """
        if isinstance(observables, str) or not isinstance(observables, Sequence):
            observables = (observables,)
        if len(observables) == 0:
            raise ValueError("No observables were provided.")
        
        observable_tuple = tuple(self.init_observable(obs) for obs in observables)
        if isinstance(observable_tuple[0], list):
            reworked_tuple = ()
            for obs in observable_tuple[0]:
               reworked_tuple += (obs, )
            return reworked_tuple 
        else:
            return  observable_tuple

      
    def run_estimator(self, circuit, observables,  params, **run_options) -> float:
        """
        The actual executor of the estimator object

        Args:
            | circuit: The qiskit version of QuantumCircuit to excute.
            | observables: List of Pauli observables
            | params: List of floating point parameters, if the circuit is parametrized.
            | run_options: specific parameters for the run method. Overrides the default values.

        Returns:
            | The sum of the Pauli expectation value for the observables for the given circuit.
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

        if isinstance(params, list):
            if (len(params) > 0):
                if isinstance(params[0], np.ndarray):
                    params = params[0]

        # Confirm we have the right number of params
        if (isinstance(params, np.ndarray)) or (isinstance(params, list)):
            if (circuit.num_parameters != len(params)):
                raise Exception (f"The given number of parameters {len(params)} does not equal the count of parameters {circuit.num_parameters} in the circuit.")
        elif (isinstance(params, np.float64)) or (isinstance(params, float)):
            if (circuit.num_parameters != 1):
                raise Exception (f"The given number of parameters 1 does not equal the count of parameters {circuit.num_parameters} in the circuit.")

        #Assign parameters
        if (circuit.num_parameters):
            if (isinstance(params, np.float64)) or (isinstance(params, float)):
                subs_params = []
                subs_params.append(params)
                run_input = circuit.assign_parameters(subs_params)
            else:
                run_input = circuit.assign_parameters(params)
        else:
            run_input = circuit

        # Flatten the circuit and clean all debris
        qr_basis_gates = self._qr_backend._basis_gates
        qc_transpiled = transpile(run_input, basis_gates=qr_basis_gates, optimization_level=3)

        self._max_qubits = qc_transpiled.num_qubits
        self._max_clbits = qc_transpiled.num_clbits

        if ( self._max_qubits <= 0 ):
            raise Exception( "Submitted quantum circuit does not use any qubits")
        
        observables = self.validate_observables(observables)

        # check whether the Pauli operator sizes match  max_qubit
        pauli_list =  observables[0].paulis
        pauli_string =  pauli_list[0]

        if (self._max_qubits != len(pauli_string)):
            raise Exception( "The Pauli operator length is not matching number of qubits")
        
        qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
        if ( self._max_clbits > 0):
            creg = QuantumRingsLib.ClassicalRegister(self._max_clbits, "meas")
            qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)
        else:
            creg = QuantumRingsLib.ClassicalRegister(self._max_qubits, "meas")
            qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)

       
        qt = QrTranslator()
        # export the measurements to QuantumRings Structure
        qt.translate_quantum_circuit(qc_transpiled, qc, True)
        
        # first execute the circuit
        job = self._qr_backend.run(qc, shots = 1, mode = self._mode, **runtime_parameters)
        job.wait_for_final_state(0.0, 5.0, self.job_call_back)
        self._job_id = job.job_id   # Store the last used job ID as the reference job id.
        results = job.result()
    
        # We must setup the Pauli operator now.
        # for each Pauli operator
        avg = 0.0
        qubit_list = [i for i in range(0, self._max_qubits)]

        for obs in observables:
            pauli_list = obs.paulis
            coeffs_list = obs.coeffs

            for p in range(len(pauli_list)):
                weight = coeffs_list[p].real
                pauli  = pauli_list[p].to_label()

                expectation_value = results.get_pauliexpectationvalue( pauli,qubit_list,0,0).real * weight

                avg = avg + expectation_value
        
       
        return avg
        
   
    def _process_pub_two(self, circuit, observable, param_) -> List[float]:
        """
        Executes one instance of the circuit and iterates over the param_ list

        Args:
            | circuit: The qiskit version of QuantumCircuit to excute.
            | observables: List of Pauli observables
            | params_: List of floating point parameters, if the circuit is parametrized.

        Returns:
            | pub_data is updated with the list of expectation values.
        """

        pub_data = []
        if (isinstance(param_, np.ndarray)):
            if param_.ndim == 1:
                pub_data.append(self.run_estimator(circuit, observable, param_))
            else:
                for param_row in param_:
                    pub_data.append(self.run_estimator(circuit, observable, param_row))
        elif (isinstance(param_, list)):
            if len(param_) == 0:
                pub_data.append(self.run_estimator(circuit, observable, param_))
            elif (isinstance(param_[0], list)):
                avg_exp = []
                for param_row in param_:
                    avg_exp.append(self.run_estimator(circuit, observable, param_row))
                pub_data.append(avg_exp)
            else:
                 pub_data.append(self.run_estimator(circuit, observable, param_))
        else:
            pub_data.append(self.run_estimator(circuit, observable, param_))
        
        return pub_data
      
        
    def _run(self, pubs: list[EstimatorPub]) -> PrimitiveResult[PubResult]:
        """
        Dispatcher for the PUBs

        Args:
            | pubs: List of PUBs.

        Returns:
            | A Primitive Result Object.
        """
        return PrimitiveResult([self._run_pub(pub) for pub in pubs], metadata={"version": 2})
    

    def _run_pub(self, pub: EstimatorPub) -> PubResult:
        """
        This internal method executes the PUBs.
        Iterates over the observables for the given circuit.

        Args:
            | pubs: List of PUBs.

        Returns:
            | PubResult object.

        """
        # pre-process the estimator inputs to fit the required format

        circuit = None
        observables = None
        parameter_values = None
    
        if (isinstance(pub, tuple)):
    
            if len(pub) < 2:
                raise Exception("Unsupported pub. The pub for the Estimator must have atleast a QuantumCiruit and SparsePauliOp Observables")
    
            if (len(pub) == 2):
                circuit = pub[0]
                observables = pub[1]
                parameter_values = None
            elif (len(pub) == 3):
               circuit = pub[0]
               observables = pub[1]
               parameter_values = pub[2]
        else:
            circuit = pub.circuit
            observables = pub.observables
            parameter_values = pub.parameter_values

        pub_data = []

        if (isinstance(observables, list)):
            for observable_list in observables:
                if (isinstance(observable_list, list)):
                    for observable_item in observable_list:
                        # check what's up with pub[2]
                        res = self._process_pub_two(circuit,observable_item, parameter_values)
                        pub_data.extend(res)
                elif (isinstance(observable_list, SparsePauliOp)):
                    observable_item = observable_list
                    res = self._process_pub_two(circuit, observable_item, parameter_values)
                    pub_data.extend(res)
                else:
                    raise Exception(f"observable type not supported: {type(observables)}")
        elif (isinstance(observables, SparsePauliOp)):
            # QAOA type sample
            observable_item = observables
            res = self._process_pub_two(circuit, observable_item, parameter_values)
            pub_data.extend(res)
        elif (isinstance(observables, np.ndarray)):
            for observable_item in observables:
                res = self._process_pub_two(circuit,observable_item, parameter_values)
                pub_data.extend(res)
        else:
            raise Exception(f"observable type not supported: {type(observables)}")
        
        evs = np.array(pub_data, dtype = np.float64)
        stds = np.zeros(evs.shape)

        # return results wrapped in PubResult
        data = DataBin(evs=evs, stds = stds, shape=evs.shape )

        if (self._precision == "single"):
            precision_value = 0.001
        else:
            precision_value = 0.0001
        return PubResult(
            data, metadata={"target_precision": precision_value, "shots":1, "circuit_metadata": circuit.metadata}
        )

    def run(
        self, pubs: Iterable[EstimatorPubLike], *, precision: float | None = None
        ) -> PrimitiveJob[PrimitiveResult[PubResult]]:
        """
        Executes the pubs and estimates all associated observables.

        Args:
            | pubs: The pub to preprocess.
            | precision: None

        Returns:
            The job associated with the pub
        """
        my_estimator_job = PrimitiveJob(self._run, pubs)
        my_estimator_job._submit()
        return  my_estimator_job

