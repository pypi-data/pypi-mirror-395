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
# This code is a derivative work of the qiskit provided JobV1 class
# See: https://github.com/Qiskit/qiskit/blob/stable/1.3/qiskit/providers/job.py#L42-L147
# https://docs.quantum.ibm.com/api/qiskit/qiskit.providers.JobV1#jobv1
#

# pylint: disable=wrong-import-position,wrong-import-order

import os
import platform

from qiskit.providers import JobV1, JobStatus
from qiskit.result import Result

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from .qr_translator import QrTranslator

class QrJobV1(JobV1):
    """
    Implements a derivative of the qiskit JobV1 object class.
    """
    def __init__(self, backend, job) -> None:
        """Initializes the asynchronous job.

        Args:
            backend: the QrBackendV2 used to run the job.
            job: the job instance returned by the :meth:`QuantumRings.BackendV2.run` method.
        """
        self._qr_job = job
        self._job_id = job.job_id
        self._num_circuits = 1
        self._job_result = [{}]
        self._job_result = [
            {
                "data": {},
                "shots": 1024,
                "header": {},
                "success": True,
            }
            for i in range(self._num_circuits)
        ]
        super().__init__(backend, job.job_id)
               

    def cancel(self) -> None:
        """Cancel this job."""
        if ( self._job_id is None ):
            raise Exception( "Can't cancel a non existing job.")
        self._qr_job.cancel_job(self._job_id)
        
    def submit(self) -> None:
        """submit a new job. This method is not supported."""
        # Implementation of job submission logic
        raise Exception( "Not supported")
        
    def get_counts(self, ) -> dict:
        """Returns the number of counts"""
        return self.result().get_counts()

    def get_probabilities(self):
        """Returns the probabilities."""
        return self.result().get_probabilities()

    def result(self) -> Result:
        """Returns the Result object"""
        # wait for the job to complete
        self.wait_for_final_state(None, 5, None)
        
        # Check for job status and return accordingly 
        self._result = self._qr_job.result()

               
        # if we get here, the job is executed and done successfully

        try:
            counts = self._qr_job.result().get_counts()
        except Exception as ex:
            counts = {}
        
        try:
            unitary = self._qr_job.result().get_unitary()
        except Exception as ex:
            unitary = [[]]

        try:
            memory = self._qr_job.result().get_memory()
        except Exception as ex:
            memory  = {}
            
        try:
            state_vector = self._qr_job.result().get_statevector()
        except Exception as ex:
            state_vector = []

        self._job_result[0]["data"] = {
            "counts": counts,
            "unitary" : unitary,
            "memory" : memory,
            "statevector" : state_vector,
            "metadata": {},
        }
        result_dict = {
            "results": self._job_result,
            "job_id": self._job_id,
            "backend_name": self._qr_job.backend().name,
            "backend_version": self._qr_job.backend().backend_version,
            "qobj_id": self._qr_job.job_id,
            "success": self._qr_job.done(),
        }
        
        return Result.from_dict( result_dict )

    
    def translate_job_status(self, qr_status) -> JobStatus:
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
        
    def status(self) -> JobStatus:
        """Returns the current status of the job"""
        # Return the current status of the job
        qr_status = self._qr_job.status()
        return QrTranslator.translate_job_status (qr_status)
