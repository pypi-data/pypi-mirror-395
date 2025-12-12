# This code is part of Quantum Rings SDK.
#
# (C) Copyright Quantum Rings Inc, 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=wrong-import-position,wrong-import-order

import os
import platform

from qiskit.circuit import QuantumCircuit
from qiskit.providers import JobStatus

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

class QrTranslator:
    """
    A helper class that translates qiskit components into equivalent QuantumRingsLib's components.
    """
    def __init__(self):
        """
        Class initializer.
        """
        self._qregs = []
        self._cregs = []

        pass

    def check_add_if_condition (
            gate, 
            operation
            ) -> None:
        """
        Checks if an IF condition is to be added to a quantum gate created using QuantumRingsLib's circuit building functions.

        Args:
            | gate: Quantum gate created using a QuantumRingsLib's circuit building function.
            | operation: qiskit operation that was used to generate the gate.

        Returns:
            None
        """
        if ( True == hasattr(operation, "condition")):
            if (None != operation.condition):
                creg_bit = operation.condition[0]._index
                creg_condition = operation.condition[1]
                gate.c_if(creg_bit, creg_condition)
        return
    

    def translate_qiskit_instruction(
        self,
        instruction,
        qc: QuantumRingsLib.QuantumCircuit,
        qubit_lookup_vector,
        ignore_meas,
        ) -> None:
        """
        Translates a given qiskit instruction into a QuantumRingsLib.QuantumCircuit quantum gate.

        Args:
            | instruction : qiskit instruction to be translated from
            | qc : QuantumRingsLib.QuantumCircuit to be constructed.
            | qubit_lookup_vector: The mapping of the qubits
            | ignore_meas (bool): Whether to ignore the measurement instructo=ions at the end.
            
        Returns:
            Nothing. See qc.
        """
        name = instruction.operation.name
        opn = instruction.operation
        
        remapped_qubit_list = []

        if (True == instruction.is_controlled_gate()):
            number_of_controls_in_this_gate_ = instruction.operation.num_ctrl_qubits
        else:
            number_of_controls_in_this_gate_ = 0

        for i in range (len(instruction.qubits)):
            reg_name = instruction.qubits[i]._register.name
            reg_index = instruction.qubits[i]._index

            absolute_index = self.find_qubit_absolute_index(reg_name, reg_index)
            if (-1 != absolute_index):
                    remapped_qubit_list.append(absolute_index)
            elif ( reg_name == "q"):
                if reg_index < len(qubit_lookup_vector):
                    relative_index = qubit_lookup_vector[reg_index]
                    remapped_qubit_list.append(relative_index)
                else:
                    raise Exception ("Unable to map the instructions qubits")
            elif (reg_name == "control"):
                if reg_index < len(qubit_lookup_vector):
                    relative_index = qubit_lookup_vector[reg_index]
                    remapped_qubit_list.append(relative_index)
                else:
                    raise Exception ("Unable to map the instructions control qubits")
            elif (reg_name == "target"):
                if ( reg_index +  number_of_controls_in_this_gate_ ) < len(qubit_lookup_vector):
                    relative_index = qubit_lookup_vector[(reg_index+ number_of_controls_in_this_gate_)]  
                    remapped_qubit_list.append(relative_index)
                else:
                    raise Exception ("Unable to map the instructions control qubits")
            
        #
        # Instructions dispatcher
        #
    
        if (name == "h"):
            gate = qc.h(remapped_qubit_list[0])
        elif (name == "x"):
            gate = qc.x(remapped_qubit_list[0])
        elif (name == "id"):
            gate = qc.id(remapped_qubit_list[0])
        elif (name == "t"):
            gate = qc.t(remapped_qubit_list[0]) 
        elif (name == "s"):
            gate = qc.s(remapped_qubit_list[0]) 
        elif (name == "tdg"):
            gate = qc.tdg(remapped_qubit_list[0])
        elif (name == "sdg"):
            gate = qc.sdg(remapped_qubit_list[0])
        elif (name == "sx"):
            gate = qc.sx(remapped_qubit_list[0])
        elif (name == "sxdg"):
            gate = qc.sxdg(remapped_qubit_list[0])                  
        elif (name == "p"):
            gate = qc.p(instruction.params[0], remapped_qubit_list[0])   
        elif (name == "r"):
            gate = qc.r(instruction.params[0], instruction.params[1], remapped_qubit_list[0])   
        elif (name == "rx"):
            gate = qc.rx(instruction.params[0], remapped_qubit_list[0])   
        elif (name == "ry"):
            gate = qc.ry(instruction.params[0], remapped_qubit_list[0]) 
        elif (name == "rz"):
            gate = qc.rz(instruction.params[0], remapped_qubit_list[0]) 
        elif (name == "u") or (name == "u3"):
            gate = qc.u(instruction.params[0], instruction.params[1], instruction.params[2], remapped_qubit_list[0])   
        elif (name == "y"):
            gate = qc.y(remapped_qubit_list[0])  
        elif (name == "z"):
            gate = qc.z(remapped_qubit_list[0])  
        elif (name == "delay"):
            gate = qc.delay(instruction.params[0], remapped_qubit_list[0]) 
        elif (name == "cx"):
            gate = qc.cx(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "cy"):
            gate = qc.cy(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "cz"):
            gate = qc.cz(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "ch"):
            gate = qc.ch(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "cp"):
            gate = qc.cp(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "crx"):
            gate = qc.crx(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])            
        elif (name == "cry"):
            gate = qc.cry(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])        
        elif (name == "crz"):
            gate = qc.crz(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "cs"):
            gate = qc.cs(remapped_qubit_list[0], remapped_qubit_list[1])
        elif (name == "csdg"):
            gate = qc.csdg(remapped_qubit_list[0], remapped_qubit_list[1])           
        elif (name == "csx"):
            gate = qc.csx(remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "cu"):
            gate = qc.cu(instruction.params[0], instruction.params[1], instruction.params[2], instruction.params[3], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "dcx"):
            gate = qc.dcx(remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "ecr"):
            gate = qc.ecr(remapped_qubit_list[0], remapped_qubit_list[1])                
        elif (name == "iswap"):
            gate = qc.iswap(remapped_qubit_list[0], remapped_qubit_list[1])   
        elif (name == "rxx"):
            gate = qc.rxx(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "ryy"):
            gate = qc.ryy(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1])  
        elif (name == "rzx"):
            gate = qc.rzx(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "rzz"):
            gate = qc.rzz(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "swap"):
            gate = qc.swap(remapped_qubit_list[0], remapped_qubit_list[1])   
        elif (name == "measure"):
            if ( False == ignore_meas):
                gate = qc.measure(remapped_qubit_list[0], instruction.clbits[0]._index)
            else:
                gate = qc.id(remapped_qubit_list[0])
        elif (name == "reset"):
            gate = qc.reset(remapped_qubit_list[0])   
        elif (name == "cu1"):
            gate = qc.cu1(instruction.params[0], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "cu3"):
            gate = qc.cu3(instruction.params[0], instruction.params[1], instruction.params[2], remapped_qubit_list[0], remapped_qubit_list[1]) 
        elif (name == "u1"):
            gate = qc.u1(instruction.params[0], remapped_qubit_list[0])
        elif (name == "u2"):
            gate = qc.u2(instruction.params[0], instruction.params[1], remapped_qubit_list[0])                
        elif (name == "barrier"):
            gate = qc.barrier(remapped_qubit_list)
        elif (name == "ms"):
            gate = qc.ms(instruction.params[0], remapped_qubit_list)
        elif (name == "rv"):
            gate = qc.rv(instruction.params[0], instruction.params[1], instruction.params[2], remapped_qubit_list[0])
        elif (name == "mcp"):
            gate = qc.mcp(instruction.params[0], remapped_qubit_list[:-1], remapped_qubit_list[-1])
        elif (name == "rccx"):
            gate = qc.rccx(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "rcccx"):
            gate = qc.rcccx(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2], remapped_qubit_list[3])
        elif (name == "cswap"):
            gate = qc.cswap(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "ccx"):
            gate = qc.ccx(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "ccz"):
            gate = qc.ccz(remapped_qubit_list[0], remapped_qubit_list[1], remapped_qubit_list[2])
        elif (name == "mcx"):
            gate = qc.mcx(remapped_qubit_list[:-1], remapped_qubit_list[-1])
        elif (name == "unitary"):
            unitary_matrix = instruction.operation.params[0]
            gate = qc.unitary(unitary_matrix[0][0], unitary_matrix[0][1], unitary_matrix[1][0], unitary_matrix[1][1], remapped_qubit_list[0])
        else:
            return False
                
        QrTranslator.check_add_if_condition(gate, opn)
        return True

    def find_qubit_absolute_index(
            self,
            name,
            index
        ):
        """
        Returns the qubit's absolute index in the mapping.

        Args:
            | name (str): The name of the quantum register
            | index (int): The qubits index in the register

        Returns
            The absolute index of the qubit.

        """
        start = 0

        for register_name, register_size in self._qregs:
            if (name == register_name):
                if index < register_size:
                    return start + index
                else:
                    raise Exception ("Register size is less than the requested value")
            else:
                start += register_size
        
        return -1
        
 
    def translate_quantum_circuit(
            self,
            run_input : QuantumCircuit, 
            qc: QuantumRingsLib.QuantumCircuit,
            ignore_meas = False,
            ) -> None:
        """
        Translates a qiskit quantum circuit object to a Quantum Rings quantum circuit object.

        Args:
            run_input (QuantumCircuit): Input qiskit QuantumCircuit
            qc (QuantumRingsLib.QuantumCircuit): Output Quantum Rings QuantumCircuit
            ignore_meas (bool): Optional: Whether to ignore measurement instructions. By default it is False.
        """
        
        for qr in run_input.qregs:
            self._qregs.append((qr.name, qr.size))

        for cr in run_input.cregs:
            self._cregs.append((cr.name, cr.size))

        qubit_lookup_vector = [i for i in range(0, run_input.num_qubits)]

        for instruction in run_input:

            if ( True == self.translate_qiskit_instruction( instruction, qc, qubit_lookup_vector, ignore_meas ) ):
                continue

            raise Exception ("Error in transpiled circuit. Unsupported gate. Can not be translated in current form.")
        
    
    def translate_job_status(
            qr_status : QuantumRingsLib.JobStatus
            ) -> JobStatus:
        """
        Translates a QuantumRingsLib defined JobStatus to a qiskit defined JobStatus.

        Args:
            | qr_status : QuantumRingsLib.JobStatus

        Returns:
            Equivalent qiskit JobStatus
        """
        if (qr_status == QuantumRingsLib.JobStatus.INITIALIZING):
            return JobStatus.INITIALIZING
        elif (qr_status == QuantumRingsLib.JobStatus.QUEUED):
            return JobStatus.QUEUED
        elif (qr_status == QuantumRingsLib.JobStatus.VALIDATING):
            return JobStatus.VALIDATING
        elif (qr_status == QuantumRingsLib.JobStatus.RUNNING):
            return JobStatus.RUNNING
        elif (qr_status == QuantumRingsLib.JobStatus.CANCELLED):
            return JobStatus.CANCELLED
        elif (qr_status == QuantumRingsLib.JobStatus.DONE):
            return JobStatus.DONE
        elif (qr_status == QuantumRingsLib.JobStatus.ERROR):
            return JobStatus.ERROR
        else:
            return qr_status

    def print_instruction(instruction, 
                          lookup_vector=[],
                          remap_vector=[]
                          ) -> None:
        """
        Prints a qiskit instruction
        """
        name = "\t" + instruction.operation.name
        name += '('
        for i in range (len(instruction.params)):
            name +=  str(instruction.params[i]) + ","
        name += ') '
        
        for i in range (len(instruction.qubits)):
            name += instruction.qubits[i]._register.name + '[' + str(instruction.qubits[i]._index) + '],'

        name = name[:-1]
        
        if ( len(instruction.clbits)):
            name += " -> "

            for i in range (len(instruction.clbits)):
                name += instruction.clbits[i]._register.name + '[' + str(instruction.clbits[i]._index) + '],'

            name = name[:-1]

        print(f"Instruction: {name} Remap Vector: {remap_vector}")
    
    def analyze_instructions(run_input) -> None:
        """
        Prints a given qiskit QuantumCircuit
        """
        for instruction in run_input:
            QrTranslator.print_instruction(instruction) 