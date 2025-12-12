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
# This code is a derivative work of the qiskit provided Sampler V1 class
# See: https://github.com/Qiskit/qiskit/blob/stable/1.3/qiskit/primitives/sampler.py#L39-L162
# https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.Sampler
#


# pylint: disable=wrong-import-position,wrong-import-order

import os
import platform


from typing import List, Union, Iterable, Tuple
from collections.abc import Iterable, Sequence

from qiskit import QuantumCircuit
from qiskit.circuit import Instruction
from qiskit.providers import Options, JobV1, JobStatus
from qiskit.providers.backend import BackendV2
from qiskit.primitives import BackendSampler
from qiskit.result import Result
from qiskit.primitives.containers import SamplerPubLike,  SamplerPubResult
from qiskit.primitives.containers.sampler_pub import SamplerPub
from qiskit.result import QuasiDistribution
from qiskit.transpiler.passmanager import PassManager

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from qiskit.primitives import DataBin
from qiskit.primitives import PubResult
from qiskit.primitives import PrimitiveResult, SamplerResult
from qiskit.primitives import PrimitiveJob
from qiskit import transpile


from .qr_meas import meas
from .qr_translator import QrTranslator
from .qr_backend_for_qiskit import QrBackendV2


import numpy
        
class QrSamplerV1(BackendSampler):
    """
    Creates a QrSamplerV1 object that calculates quasi-probabilities of bitstrings from quantum circuits.
    Derives from the qiskit SamplerV1 class.

    When the quantum circuit is executed using the method :meth:`quantumrings.toolkit.qiskit.QrSamplerV1.run()`, this class returns a
    :class:`quantumrings.toolkit.qiskit.QrJobV1` object. 
   
    This method is called with the following parameters

    * quantum circuits (:math:`\\psi_i(\\theta)`): list of (parameterized) quantum circuits.
      (a list of :class:`~qiskit.circuit.QuantumCircuit` objects)

    * parameter values (:math:`\\theta_k`): list of sets of parameter values
      to be bound to the parameters of the quantum circuits.
      (list of list of float)

    Calling the method :meth:`quantumrings.toolkit.qiskit.QrJobV1.result()` yields a :class:`~qiskit.primitives.SamplerResult`
    object, which contains probabilities or quasi-probabilities of bitstrings.

    Example:
    
    .. code-block:: python

        from  quantumrings.toolkit.qiskit import QrSamplerV1 as Sampler
        from qiskit import QuantumCircuit
        from qiskit.circuit.library import RealAmplitudes

        # a Bell circuit
        bell = QuantumCircuit(2)
        bell.h(0)
        bell.cx(0, 1)
        bell.measure_all()

        # two parameterized circuits
        pqc = RealAmplitudes(num_qubits=2, reps=2)
        pqc.measure_all()
        pqc2 = RealAmplitudes(num_qubits=2, reps=3)
        pqc2.measure_all()

        theta1 = [0, 1, 1, 2, 3, 5]
        theta2 = [0, 1, 2, 3, 4, 5, 6, 7]

        # initialization of the sampler
        sampler = Sampler()

        # Sampler runs a job on the Bell circuit
        job = sampler.run(circuits=[bell], parameter_values=[[]], parameters=[[]])
        job_result = job.result()
        print([q.binary_probabilities() for q in job_result.quasi_dists])

        # Sampler runs a job on the parameterized circuits
        job2 = sampler.run(
            circuits=[pqc, pqc2],
            parameter_values=[theta1, theta2],
            parameters=[pqc.parameters, pqc2.parameters])
        job_result = job2.result()
        print([q.binary_probabilities() for q in job_result.quasi_dists])

    """
    def __init__(self, 
        backend: QrBackendV2 = None,
        options: dict | None = None,
        run_options: dict | None = None,
        bound_pass_manager: PassManager | None = None,
        skip_transpilation: bool = False,
        ):
        """
        Args:
            backend: The QrBackendV2 backend.
            options: The options to control the default shots(``shots``)
            run_options: See options above.
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

        if backend is None:
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
        
        else:
            if (False == isinstance(backend, QrBackendV2)):
                raise Exception ("The backend for this class should be a Quantum Rings Backend.")
            else:
                self._backend = backend

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
                if isinstance( run_options["shots"], (int, numpy.int64)):
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
        self._default_options.skip_transplile = skip_transpilation

        super().__init__(backend = self._backend)

    @property
    def options(self) -> Options:
        """Return the options"""
        return self._default_options
        
       
    def job_call_back(self, job_id, state, job) -> None:
        pass

    def run_sampler(self, circuits, **run_options):
        results = []

        # Validate the circuits parameter.
        if not isinstance(circuits, QuantumCircuit):
            raise Exception( "Invalid argument passed for Quantum Circuit.")

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

        #
        # Transpile the circuit now
        #

        qr_basis_gates = self._qr_backend._basis_gates
        qc_transpiled = transpile(circuits, basis_gates=qr_basis_gates, optimization_level=3)

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

        # export the measurements to QuantumRings Structure
        qt = QrTranslator()
        qt.translate_quantum_circuit(qc_transpiled , qc, False)
        
        job = self._qr_backend.run(qc, shots = self._shots, mode = self._mode, **runtime_parameters)
        job.wait_for_final_state(0.0, 5.0, self.job_call_back)
        results = job.result()
        counts = results.get_counts()
        self._job_id = job.job_id
        
        return counts


    def run_pub(
        self,
        circuit,
        parameter,
        **run_options,
        ):

        results = []
        metadata = []

        if (circuit.num_parameters):
            if (parameter is not None):
                run_input = circuit.assign_parameters(parameter)
            else:
                raise Exception ("None object is passed for parameter, whereas circuit is parametrized")
        else:
            run_input = circuit
            

        if "shots" in run_options:
            shots = run_options["shots"]
        else:
            shots = self._default_options.shots

        counts_org = self.run_sampler(run_input, shots = shots)

        counts = {}
        cbits_to_retain = 0

        for j in range (len(circuit.cregs)):
            cbits_to_retain += circuit.cregs[j].size

        for key, value in counts_org.items():
            counts[key[-cbits_to_retain:]]=value

        quasi_dist = QuasiDistribution({outcome: freq / shots for outcome, freq in counts.items()})

        results.append(quasi_dist)
        metadata.append({"shots": shots})
        
        return SamplerResult(results, metadata=metadata )

    def _run(self,
        circuits: tuple[QuantumCircuit, ...],
        parameter_values: tuple[tuple[float, ...], ...] | None,
        **run_options,):
        results = []
        metadata = []

        index = 0

        if not ( isinstance(parameter_values, tuple) or parameter_values is None):
            raise TypeError("Parameter must be a tuple of tuples or None")

        if isinstance(parameter_values, tuple):
            for i, row in enumerate(parameter_values):
                if not isinstance(row, tuple):
                    raise TypeError(f"Row {i} is not a tuple in Parameter")
                for j, val in enumerate(row):
                    if not isinstance(val, (int, float)):
                        raise TypeError(f"Value at ({i},{j}) is not a float: {val}")

            if len(parameter_values) !=  len(circuits):
                raise ValueError("The number of circuits does not match the number of parameter tuples")

        for circuit_l in circuits:
            #
            # Check if it is a parametrized circuit. If so, assign parameters
            #
            if isinstance(circuit_l, tuple):
                
                for circuit in circuit_l:
                    if ( None == parameter_values):
                        res = self.run_pub(circuit, parameter_values, **run_options)
                    else:
                        res = self.run_pub(circuit, parameter_values[index], **run_options)
                        index += 1
                results.append(res)
            else:
                circuit = circuit_l

                res = self.run_pub(circuit, parameter_values, **run_options)
   
                return res
        return results

    def run(
        self,
        circuits: QuantumCircuit | Sequence[QuantumCircuit],
        parameter_values: Sequence[float] | Sequence[Sequence[float]] | None = None,
        **run_options,
        ):
        """
        Run the sampling job.

        Args:
            circuits: One of more circuit objects.
            parameter_values: Parameters to be bound to the circuit.
            run_options: Backend runtime options used for circuit execution.

        Returns:
            The job object of the result of the sampler. The i-th result corresponds to
            ``circuits[i]`` evaluated with parameters bound as ``parameter_values[i]``.

        Raises:
            ValueError: Invalid arguments are given.
        """
        run_input = []     
        if(isinstance(circuits, QuantumCircuit)):
            run_input.append(circuits)
        else:
            run_input = circuits
        my_sampler_job = PrimitiveJob(self._run, run_input, parameter_values, **run_options)
        my_sampler_job._submit()
        return  my_sampler_job
    