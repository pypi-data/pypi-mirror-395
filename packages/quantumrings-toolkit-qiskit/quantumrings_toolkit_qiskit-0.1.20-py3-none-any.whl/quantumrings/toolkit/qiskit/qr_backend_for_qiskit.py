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
# This code is a derivative work of the qiskit provided BackendV2 class
# See: https://github.com/Qiskit/qiskit/blob/stable/1.3/qiskit/providers/backend.py
# https://docs.quantum.ibm.com/api/qiskit/qiskit.providers.BackendV2
#


# pylint: disable=wrong-import-position,wrong-import-order
import os
import platform

from qiskit.circuit import QuantumCircuit, Instruction
from qiskit.circuit.library.standard_gates import get_standard_gate_name_mapping
from qiskit.transpiler import CouplingMap, Target, InstructionProperties, QubitProperties
from qiskit.providers import Options, JobV1, JobStatus
from qiskit.providers.backend import BackendV2
from qiskit.result import Result
from qiskit.circuit.controlflow import (
    IfElseOp,
    WhileLoopOp,
    ForLoopOp,
    SwitchCaseOp,
    BreakLoopOp,
    ContinueLoopOp,
    )

from qiskit import transpile

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)


import QuantumRingsLib

from .qr_translator import QrTranslator
from .qr_job_for_qiskit import QrJobV1


class QrBackendV2(BackendV2):

    """
    Supporter class for a qiskit V2 compatible backend object for Quantum Rings, meant to be used along with qiskit packages.

    """
    
    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a BackendV2 based backend for Quantum Rings. 

        Usage:
            If the user already has obtained the reference to the QuantumRingsLib.QuantumRingsProvider object, 
            the reference can be provided using the 'provider' argument.
            Otherwise, the user can provide the account's 'name' and 'token' as parameters.
            If the user has saved the account details locally using the QuantumRingsLib.QuantumRingsProvider.save_account api,
            this method can be called without any arguments.

        Examples:
            >>> backend = QrBackendV2()        # Uses the account information that is locally stored.
            >>> backend = QrBackendV2(num_qubits = 5)        # Uses the account information that is locally stored, sets the number of qubits to 5.

            >>> provider = QuantumRingsLib.QuantumRingsProvider(token = <YOUR_TOKEN>, name = <YOUR_ACCOUNT>)
            >>> backend  = QrBackendV2(provider)

            >>> backend = QrBackendV2(token = <YOUR_TOKEN>, name = <YOUR_ACCOUNT>)

        Args:
            provider   (QuantumRingsLib.QuantumRingsProvider): An optional backwards reference to the QuantumRingsLib.QuantumRingsProvider object.
            token      (str): An optional access key to the QuantumRingsLib.QuantumRingsProvider. 
            name       (str): An optional account name to be used to autenticate the user.
            num_qubits (int): The number of qubits the backend will use.
            backend    (str): An optional name of the backend to be used
            precision  (str): An optional precision parameter - "single" or "double"
            gpu        (int): GPU ID to use.

        Raises:
            Exception: If not able to obtain the Quantum Rings Provider or the backend.

        """

        if ( isinstance(kwargs.get('token'), str ) ) and ( isinstance(kwargs.get('name'), str ) ):
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider(token = kwargs.get('token'), name = kwargs.get('name'))
        elif isinstance(kwargs.get('provider'), QuantumRingsLib.QuantumRingsProvider ):
            self._qr_provider = kwargs.get('provider')
        elif (len(args) > 1 ) and ( isinstance(args[0], str ) ) and ( isinstance(args[1], str ) ):
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider(token = args[0], name = args[1])
        elif (len(args) > 0 ) and ( isinstance(args[0], QuantumRingsLib.QuantumRingsProvider ) ):
            self._qr_provider = args[0]
        else:
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider()

        if ( self._qr_provider is None ):
            raise Exception ("Unable to obtain Quantum Rings Provider. Please check the arguments")
        
        # Some default backend parameters
        self._backend = "scarlet_quantum_rings"
        self._precision = "single"
        self._gpu_id = 0

        if ( isinstance(kwargs.get('backend'), str ) ):
            self._backend = kwargs.get('backend')
            self._backend = self._backend.lower()

        if ( isinstance(kwargs.get('precision'), str ) ):
            self._precision = kwargs.get('precision')
            self._precision = self._precision.lower()

        if ( isinstance(kwargs.get('gpu'), int ) ):
            self._gpu_id = kwargs.get('gpu')
          
        self._qr_backend = self._qr_provider.get_backend(
                                                name = self._backend,
                                                precision = self._precision,
                                                gpu = self._gpu_id
                                                )
        
        if ( self._qr_backend is None ):
            raise Exception ("Unable to obtain backend. Please check the arguments")
            return
            
        super().__init__(
            provider = "Quantum Rings Provider",
            name= self._qr_backend.name,
            description = self._qr_backend.description,
            online_date = self._qr_backend.online_date,
            backend_version = self._qr_backend.backend_version,
            )

        if ( isinstance(kwargs.get('num_qubits'), int ) ):
            n = kwargs.get('num_qubits')
            if ( self._qr_backend.num_qubits >= n ):
                self._num_qubits = n
                self._coupling_map = self._qr_backend.get_coupling_map(self._num_qubits)
            else:
                raise Exception( f"Requested number of qubits {n} is more than the provisioned {self._qr_backend.num_qubits}." )
                return
        else:
             self._num_qubits = self._qr_backend.num_qubits
             self._coupling_map = self._qr_backend.coupling_map

        self._dt = self._qr_backend.dt
        self._dtm = self._qr_backend.dtm
       
        self._supported_gates = get_standard_gate_name_mapping()
        self._basis_gates = self._qr_backend._basis_gates
        
        self._build_target(self)
        return

    @staticmethod
    def _build_target(self) -> None:
        """
        Builds the Quantum Rings target associated with the backend. 

        Args:
            None

        Returns:
            None

        Raises:
            None

        """

        qubitproperties = []
        for i in range(self._num_qubits):
            qp = QubitProperties()
            target_qp = self._qr_backend.qubit_properties(i)
            qp.frequency = target_qp.frequency
            qp.t1 = target_qp.t1
            qp.t2 = target_qp.t2

            qubitproperties.append(qp)
           
        self._target = Target(
            description = f"{self._qr_backend.description} with {self._num_qubits} qubits",
            num_qubits = self._num_qubits,
            dt = self._qr_backend.dt,
            qubit_properties = qubitproperties,
            concurrent_measurements = [list(range(self._num_qubits))],
            )

        for gate_name in self._basis_gates:
            if gate_name not in self._supported_gates:
                raise Exception(f"Provided basis gate {gate_name} is not valid.")
            gate = self._supported_gates[gate_name]
            if self._num_qubits < gate.num_qubits:
                raise Exception(f"Gate {gate_name} needs more qubits than the total qubits {self.num_qubits} enabled by the backend.")

            if gate.num_qubits > 1:
                qarg_set = self._coupling_map 
            else:
                qarg_set = range(self._num_qubits)
            

            props = {}
            for qarg in qarg_set:
                if isinstance(qarg, int):
                    key = (qarg,)  
                else:
                    key = (qarg[0], qarg[1])
                
                ip = InstructionProperties(duration = 1, error = 0.001)
                props[key] = ip

            self._target.add_instruction(gate, properties = props, name = gate_name)

        self._target.add_instruction(IfElseOp, name="if_else")
        self._target.add_instruction(WhileLoopOp, name="while_loop")
        self._target.add_instruction(ForLoopOp, name="for_loop")
        self._target.add_instruction(SwitchCaseOp, name="switch_case")
        self._target.add_instruction(BreakLoopOp, name="break")
        self._target.add_instruction(ContinueLoopOp, name="continue")
                  
        return

                    
    @property
    def target(self) -> Target:
        """
        Returns the Quantum Rings target associated with the backend. 
        """
        return self._target

    @classmethod
    def _default_options(cls) -> Options:
        """
        Returns the default configuration options. 

        Args:
            None

        Returns:
            Options

        Raises:
            None

        """
        op = Options(
            shots = 1024,
        	mode = "sync",
        	performance = "HIGHESTEFFICIENCY",
        	quiet = True,
        	defaults = True,
        	generate_amplitude = False
        )
        return op


    #@classmethod
    def run(self, run_input, **run_options) -> QrJobV1:
        """
        Executes a qiskit quantum circuit using the Quantum Rings backend 

        Example:
            >>> from qiskit.circuit import QuantumCircuit
            >>> from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister, AncillaRegister
            >>> from qiskit.visualization import plot_histogram
            >>> from matplotlib import pyplot as plt
            >>> 
            >>> import QuantumRingsLib
            >>> from QuantumRingsLib import QuantumRingsProvider
            >>> from quantumrings.toolkit.qiskit import QrBackendV2
            >>> from quantumrings.toolkit.qiskit import QrJobV1
            >>> 
            >>> from matplotlib import pyplot as plt
            >>> 
            >>> qr_provider = QuantumRingsProvider(token =<YOUR_TOKEN>, name=<YOUR_ACCOUNT>)
            >>> 
            >>> shots = 1000
            >>> numberofqubits =  int(qr_provider.active_account()["max_qubits"])
            >>> q = QuantumRegister(numberofqubits , 'q')
            >>> c = ClassicalRegister(numberofqubits , 'c')
            >>> qc = QuantumCircuit(q, c)
            >>> 
            >>> 
            >>> # Create the GHZ state (Greenberger-Horne-Zeilinger)
            >>> qc.h(0);
            >>> for i in range (qc.num_qubits - 1):
            >>>     qc.cx(i, i + 1);
            >>> 
            >>> # Measure all qubits
            >>> qc.measure_all();
            >>> 
            >>> # Execute the quantum code
            >>> mybackend = QrBackendV2(qr_provider, num_qubits = qc.num_qubits)
            >>> job = mybackend.run(qc, shots = shots)
            >>> 
            >>> result = job.result()
            >>> counts = result.get_counts()
            >>> plot_histogram(counts)

        Args:
            run_input (QuantumCircuit): 
                A qiskit QuantumCircuit object.

            shots      (int):
                The number of times the circuit needs to be executed in repetition. The measurement counts are maintained only for the first 10,000 shots. If more execution cycles
                are required, a file name can be provided where the measurements are logged.

            mode   (str):
                | default - "sync"  - The quantum circuit is executed synchronously.
                | "async" - The quantum circuit is executed asynchronously.

            performance (str):
                | One of the following strings that define the quality of the circuit execution.
                | default - "HighestEfficiency"
                | "BalancedAccuracy"
                | "HighestAccuracy"
                | "Automatic"
                 | "custom"

            quiet (bool):
                | default - True - Does not print any message
                | False - Prints some messages, such as which instruction is executed, which may be of help in tracking large circuits

            defaults (bool):
                | default - True  - Uses standard internal settings.
                | False - Uses compact internal settings.
                
            generate_amplitude (bool):
                | True  - Generate amplitudes corresponding to the measurements and print them in the logging file for measurements.
                | (default)  False - Amplitudes are not printed in the logging file.

            file (str):
                An optional file name for logging the measurements.

            max_threads (int):
                An optional number of threads to use for parallel measurements

            threshold (int):
                An optional threshold to use when the performance is set to "custom". If not set, when the performance = "custom"
                the system will set performance = "HighestEfficiency"

            transfer_to_cpu (bool):
                | default - True - If a GPU is used, automatically transfer to CPU for final measurement 
                | False - Stays in the GPU mode itself for final measurements

            precision (str):
                | "single" (the Default, if not overwritten earlier) - single precision arithmetic
                | "double" - sets double precision arithmetic


        Returns:
            QrJobV1

        Raises:
            Exception: If not able to obtain the Quantum Rings Provider or the backend.

        """

        if not isinstance(run_input, QuantumCircuit):
            raise Exception( "Invalid argument passed for Quantum Circuit.")
            return
        
        #
        # Transpile the circuit and flatten it.
        #

        qr_basis_gates = self._qr_backend._basis_gates
        qc_transpiled = transpile(run_input, basis_gates=qr_basis_gates, optimization_level=3)

        self._max_qubits = qc_transpiled.num_qubits #max_qubits
        self._max_clbits = qc_transpiled.num_clbits #max_clbits

        if ( self._max_qubits <= 0 ):
            raise Exception( "Submitted quantum circuit does not use any qubits")

        #TODO: Check control loops
        qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
        creg = QuantumRingsLib.ClassicalRegister(self._max_clbits, "meas")
        qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)

        #
        # We expect the transpiler to do a decent jobs of using required qubits and classical bits
        # for each instruction properly.
        # So they are not value checked
        #
        
        qt = QrTranslator()
        qt.translate_quantum_circuit(qc_transpiled , qc, False)

       

        #
        # parse the arguments and build the run parameters
        #
        
        run_parameters = {}

        if "shots" in run_options:
            shots = run_options.get("shots")
            if not isinstance(shots, int):
                raise Exception( "Invalid argument for shots")

            if ( shots <= 0 ):
                raise Exception( "Invalid argument for shots")

        else:
            shots = self._default_options().shots
            
        if ("mode" in run_options ):
            if isinstance( run_options["mode"], str):
                mode = run_options["mode"].lower()
                if (  mode not in ["sync", "async"]):
                    raise Exception( "Invalid argument for mode")
            else:
                raise Exception( "Invalid argument for mode")
        else:
            mode = self._default_options().mode

        run_parameters["mode"] = mode

        if "performance" in run_options:
            performance = run_options.get("performance")
            performance = performance.upper()
            if (performance not in ["HIGHESTEFFICIENCY", "BALANCEDACCURACY", "HIGHESTACCURACY", "AUTOMATIC", "CUSTOM"] ):
                raise Exception( "Invalid argument for performance")

        else:
            performance = self._default_options().performance


        if "threshold" in run_options:
            threshold = run_options.get("threshold")
            if not isinstance(threshold, int):
                raise Exception( "Invalid argument for threshold")
 
        else:
            threshold = None

        if performance == "CUSTOM":
            if None == threshold:
                raise Exception( "Threshold is not set for custom precision")
  
            else:
                run_parameters["threshold"] = threshold

        run_parameters["performance"] = performance
        

        if "quiet" in run_options:
            quiet = run_options.get("quiet")
            if not isinstance(quiet, bool):
                raise Exception( "Invalid argument for quiet")
   
        else:
            quiet = self._default_options().quiet

        run_parameters["quiet"] = quiet

        if "generate_amplitude" in run_options:
            generate_amplitude = run_options.get("generate_amplitude")
            if not isinstance(generate_amplitude, bool):
                raise Exception( "Invalid argument for generate_amplitude")

        else:
            generate_amplitude = self._default_options().generate_amplitude

        log_file = ""
        if "file" in run_options:
            log_file = run_options.get("file")
            if isinstance(log_file, str):
                run_parameters["file"] = log_file
            else:
                raise Exception( "Invalid argument for file")
   
            
        if ("" == log_file):
            generate_amplitude = False
            run_parameters["generate_amplitude"] = False
        else:
            if True == generate_amplitude:
                run_parameters["generate_amplitude"] = True

        if "max_threads" in run_options:
            max_threads = run_options.get("max_threads")
            if isinstance(max_threads, int):
                run_parameters["max_threads"] = max_threads
            else:
                raise Exception( "Invalid argument for max_threads")


        if "transfer_to_cpu" in run_options:
            transfer_to_cpu = run_options.get("transfer_to_cpu")
            if isinstance(transfer_to_cpu , bool):
                run_parameters["transfer_to_cpu"] = transfer_to_cpu
            else:
                raise Exception( "Invalid argument for transfer_to_cpu")

            
        if "precision" in run_options:
            precision = run_options.get("precision")
            if isinstance(precision, str):
                precision = precision.lower()
                if precision in ["single", "double"]:
                    run_parameters["precision"] = precision
                else:
                    raise Exception( "Invalid argument for precision")

            else:
                raise Exception( "Invalid argument for precisiopn")


        job = self._qr_backend.run(qc, shots = shots, **run_parameters)
        job.wait_for_final_state(0.0, 5.0, self.job_call_back)
        my_job = QrJobV1(self._qr_backend, job)
        return my_job

    def job_call_back(self, job_id, state, job) -> None:
        pass

    @property
    def max_circuits(self) -> int:
        """
        Returns the maximum number of circuits the backend can run at a time. 
        """
        return self._qr_backend.max_circuits
    
    @property
    def num_qubits(self) -> int:
        """
        Returns the number of qubits the backend supports. 
        """
        return self._num_qubits


