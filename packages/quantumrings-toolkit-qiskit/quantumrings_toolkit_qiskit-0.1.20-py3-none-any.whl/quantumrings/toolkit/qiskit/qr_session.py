# This code is part of Quantum Rings toolkit for qiskit.
#
# (C) Copyright IBM 2022
# (C) Copyright Quantum Rings Inc, 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

#
# This code is a derivative work of the qiskit provided Session class
# See: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/session
# https://github.com/Qiskit/qiskit-ibm-runtime/blob/stable/0.42/qiskit_ibm_runtime/session.py
#


# pylint: disable=wrong-import-position,wrong-import-order
import re
import time

from typing import Union, Dict, Optional, Type, Any
from types import TracebackType

from .qr_backend_for_qiskit import QrBackendV2
from .qr_runtime_service import QrRuntimeService


class QrSession:
    """
    A template class to run a sequence or a batch of jobs on the Quantum Rings backend.

    """

    def __init__(
        self,
        backend: QrBackendV2,
        max_time: Optional[Union[int, str]] = None,
        *,
        create_new: Optional[bool] = True,
        ):  
        """
        Session constructor.

        Args:
            | backend (QrBackendV2): Instance of ``QrBackend`` class.

            | max_time (Union[int, str]): Optional: Maximum allowed time for the session before it is closed. It can be specified
                                                    in seconds or as a string like "2h 30m 10s".
                
            | create_new (bool): Optional: If True, A new session is created

        Raises:
            Exception: If an input value is invalid.
        """

        if (False == isinstance(backend, QrBackendV2)):
            raise Exception ("The backend for this class should be a Quantum Rings Backend.")
        else:
            self._backend = backend
        
        if (True == isinstance(max_time, int)):
            self._max_time = max_time
        elif (True == isinstance(max_time, str)):
            parsed_time = re.findall(r"(\d+[dhms])", max_time)
            total_seconds = 0
            if parsed_time:
                for time_unit in parsed_time:
                    unit = time_unit[-1]
                    value = int(time_unit[:-1])
                    if unit == "d":
                        total_seconds += value * 86400
                    elif unit == "h":
                        total_seconds += value * 3600
                    elif unit == "m":
                        total_seconds += value * 60
                    elif unit == "s":
                        total_seconds += value
                    else:
                        raise Exception(f"Invalid input: for max_time: {max_time}")
            else:
                 raise Exception(f"Invalid input: for max_time: {max_time}")
            
            self._max_time = total_seconds
        
        self._active = True
        self._status = "In Progress"
        self._session_id = None
        self._service = None
        self._start_time = time.time()

        #
        # Further processing of the session. that is, creation of the session object, timersc
        #

        return
    

    def backend(self) -> QrBackendV2:
        """Return backend for this session.

        Returns:
            Backend for this session. None if unknown.
        """

        return self._backend
    
    
    def cancel(self) -> None:
        """
        Cancels the associted session
        """

        self._active = False
        self._status = "Inactive"
    
        #
        # TODO:
        # End the active session
        #

        return
    
    def close(self) -> None:
        """
        Closes the current session.
        No new jobs will be accepted.
        However, existing jobs in the queue will be completed, if there is still time to complete them.

        """
        
        self._active = False
        self._status = "Inactive"

        #
        # TODO:
        # Close the active session
        #

        return
    
    def status(self) -> str:
        """
        Returns the current session status.

        Returns:
            A string describing the current status of the session.
        """

        return self._status
    
    def details(self) -> Optional[Dict[str, Any]]:
        """
        Return session details.

        """

        #
        # TODO:
        # Add more details of jobs and timings
        # For now, this is all we care of
        #

        return {
            "backend_name": self._backend._qr_backend.name,
            "state": self._status,
            "max_time": self._max_time
            }


    @property
    def session_id(self) -> Optional[str]:
        """
        Returns the session ID.

        Returns:
            Returns the session ID
        """
        return self._session_id

    @property
    def service(self) -> QrRuntimeService:
        """
        Returns the service associated with this session.

        Returns:
            An object of the class QrRuntimeService
            
        """
        return self._service

    @classmethod
    def from_id(cls, session_id: str, service: QrRuntimeService) -> "QrSession":
        """
        Construct a Session object with a given session_id

        Args:
            session_id: the id of the session to be created. T
            service: instance of the ``QrRuntimeService`` class.

         Raises:
            Exception, should an error occur

        Returns:
            A new Session with the given ``session_id``

        """
        new_session = QrSession(backend = service._qr_backend, create_new = True)
        new_session.session_id = session_id

        #
        # TODO
        # Manage any session related tasks here
        #

        return new_session
    
    def usage(self) -> Optional[float]:
        """
        Returns the time elapsed since the start of the session in seconds.
        """
        return (time.time() - self._start_time)

    def __enter__(self) -> "QrSession":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()