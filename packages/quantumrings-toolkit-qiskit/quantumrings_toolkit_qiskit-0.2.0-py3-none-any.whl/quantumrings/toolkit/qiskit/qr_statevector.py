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
# This code is a derivative work of the qiskit provided Statevector class
# See: https://github.com/Qiskit/qiskit/blob/stable/1.3/qiskit/quantum_info/states/statevector.py
# https://docs.quantum.ibm.com/api/qiskit/qiskit.quantum_info.Statevector#statevector
#


# pylint: disable=wrong-import-position,wrong-import-order

import os
import platform

from qiskit import QuantumCircuit
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

from qiskit.circuit.instruction import Instruction

import numpy as np

class QrStatevector():
    """ Implements the Quantum Rings Statevector class"""

    def __init__(
        self,
        data: np.ndarray | list | QuantumCircuit | Instruction,
        dims: int | tuple | list | None = None,
        *args, 
        **kwargs
    ):
        """
        Initialize a Quantum Rings statevector object.

        Args:
            | data: Data from which the statevector can be constructed. This can be either a complex
            |    vector, another statevector, a ``Operator`` with only one column or a
            |    ``QuantumCircuit`` or ``Instruction``.  If the data is a circuit or instruction,
            |    the statevector is constructed by assuming that all qubits are initialized to the
            |    zero state.
            | dims: The subsystem dimension of the state (usually 2).

        """

        token = None
        name = None
        backend_str = None
        gpu_id = 0

        self._qr_provider = None
        precision_ = "single"
        self._backend = None
        mode_ = "sync"

        if isinstance(data, (list, np.ndarray)):
            self._data = np.asarray(data, dtype=complex)
        elif isinstance(data, (QuantumCircuit, Instruction)):
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
                        precision_ = kwargs["precision"]
                if ("gpu" in kwargs ):
                    if isinstance( kwargs["gpu"], int):
                        gpu_id = kwargs["gpu"] 
   
            if None == self._backend:
                if ( token != None ) and ( name != None ):
                    self._qr_provider = QuantumRingsLib.QuantumRingsProvider(name = name, token = token)
                else:
                    self._qr_provider = QuantumRingsLib.QuantumRingsProvider()

                if None == backend_str:
                    self._backend = QrBackendV2(self._qr_provider, precision = precision_, gpu = gpu_id)
                else:
                    self._backend = QrBackendV2(self._qr_provider, backend=backend_str, precision = precision_, gpu = gpu_id)

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
            
            if isinstance(data, Instruction):
                data = data.definition

            #
            # Transpile the circuit
            #
            qr_basis_gates = self._qr_backend._basis_gates
            qc_transpiled = transpile(data, basis_gates=qr_basis_gates, optimization_level=3)

            self._max_qubits = qc_transpiled.num_qubits #max_qubits
            self._max_clbits = qc_transpiled.num_clbits #max_clbits

            if ( self._max_qubits <= 0 ):
                raise Exception( "Submitted quantum circuit does not use any qubits")
            
            if 0 == self._max_clbits:
                self._max_clbits = self._max_qubits 
     
            #TODO: Check control loops
            qreg = QuantumRingsLib.QuantumRegister(self._max_qubits, "q")
            creg = QuantumRingsLib.ClassicalRegister(self._max_clbits, "meas")
            qc   = QuantumRingsLib.QuantumCircuit(qreg, creg, name = qc_transpiled.name,  global_phase = qc_transpiled.global_phase)
  
        
            # export the measurements to QuantumRings Structure
            qt = QrTranslator()
            qt.translate_quantum_circuit(qc_transpiled, 
                                                   qc,
                                                   False
                                                   ) 
        
            runtime_parameters = {}
            runtime_parameters["performance"]        = self._performance
            if ("CUSTOM" == self._performance):
                runtime_parameters["threshold"]      = self._threshold
            runtime_parameters["precision"]          = self._precision
            runtime_parameters["quiet"]              = True 
            runtime_parameters["defaults"]           = True
            runtime_parameters["transfer_to_cpu"]    = self._transfer_to_cpu
            
            job = self._qr_backend.run(qc, shots = 1, mode = self._mode, **runtime_parameters)
            job.wait_for_final_state(0.0, 5.0, self.job_call_back)
            self._results = job.result()
            self._data = np.array(self._results.get_statevector())
        
        else:
            raise Exception ("Invalid input data format for QrStatevector")
        
        ndim = self._data.ndim
        shape = self._data.shape
        if ndim != 1:
            if ndim == 2 and shape[1] == 1:
                self._data = np.reshape(self._data, shape[0])
                shape = self._data.shape
            elif ndim != 2 or shape[1] != 1:
                raise Exception("Invalid input: not a vector or column-vector.")
        
        return

    def release_resources(self):
        """ Releases the associated resources """
        print("Object destroyed.")
        del self._data
        del self._results
        self._data = None
        self._results = None


    def job_call_back(self, job_id, state, job) -> None:
        pass
        
    @property
    def data(self) -> np.ndarray:
        """Returns data."""
        return self._data

    def sample_memory(self, shots: int, qargs: None | list = None) -> np.ndarray:
        """
        Sample a list of qubit measurement outcomes in the computational basis.

        Args:
            | shots (int): number of samples to generate.
            | qargs (None or list): subsystems to sample measurements for,
            |                    if None sample measurement of all
            |                    subsystems (Default: None).

        Returns:
            np.array: list of sampled counts if the order sampled.

        Additional Information:

            This function *samples* measurement outcomes using the measure
            :meth:`probabilities` for the current state and `qargs`. It does
            not actually implement the measurement so the current state is
            not modified.

            The seed for random number generator used for sampling can be
            set to a fixed value by using the stats :meth:`seed` method.
        """

        # Get measurement probabilities for measured qubits
        probs = self._results.get_probabilities(0, 0, qargs)

        # Generate list of possible outcome string labels
        labels = self._index_to_ket_array(
            np.arange(len(probs)), self.dims(qargs), string_labels=True
        )

        #
        # Normalize the probs so that they sum upto 1.0 exactly.
        #

        probs_np = np.array(probs, dtype=np.float64)
        probs_normalized = probs_np / probs_np.sum()


        return np.random.default_rng().choice(labels, p=probs_normalized, size=shots)
    

    @staticmethod
    def _index_to_ket_array(
        inds: np.ndarray, dims: tuple, string_labels: bool = False
    ) -> np.ndarray:
        """
        Convert an index array into a ket array.

        Args:
            inds (np.array): an integer index array.
            dims (tuple): a list of subsystem dimensions.
            string_labels (bool): return ket as string if True, otherwise
                                  return as index array (Default: False).

        Returns:
            np.array: an array of ket strings if string_label=True, otherwise
                      an array of ket lists.
        """
        shifts = [1]
        for dim in dims[:-1]:
            shifts.append(shifts[-1] * dim)
        kets = np.array([(inds // shift) % dim for dim, shift in zip(dims, shifts)])

        if string_labels:
            max_dim = max(dims)
            char_kets = np.asarray(kets, dtype=np.str_)
            str_kets = char_kets[0]
            for row in char_kets[1:]:
                if max_dim > 10:
                    str_kets = np.char.add(",", str_kets)
                str_kets = np.char.add(row, str_kets)
            return str_kets.T

        return kets.T
    
    def dims(self, qargs=None):
        """Return tuple of input dimension for specified subsystems."""
        return (2,) * len(qargs)
    