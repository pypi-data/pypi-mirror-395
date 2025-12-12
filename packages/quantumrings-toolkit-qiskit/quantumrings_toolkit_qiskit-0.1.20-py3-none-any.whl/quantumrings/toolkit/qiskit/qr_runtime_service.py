# This code is part of Quantum Rings toolkit for qiskit.
#
# (C) Copyright IBM 2022, 2024.
# (C) Copyright Quantum Rings Inc, 2024, 2025
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

#
# This code is a derivative work of the qiskit provided QiskitRuntimeService class
# See: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/qiskit-runtime-service
# https://github.com/Qiskit/qiskit-ibm-runtime/blob/stable/0.42/qiskit_ibm_runtime/qiskit_runtime_service.py
#


# pylint: disable=wrong-import-position,wrong-import-order

import configparser
import os
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, Callable, Optional, Union, List, Any, Type, Sequence, Tuple

if platform.system() == "Windows":
    cuda_path = os.getenv("CUDA_PATH", "")
    if "" != cuda_path:
        #create from the environment
        cuda_path += "\\bin"
        os.add_dll_directory(cuda_path)

import QuantumRingsLib

from .qr_backend_for_qiskit import QrBackendV2

class QrRuntimeService:
    """
    A class for creating the Quantum Rings runtime.
    """
    def __new__(cls, *args, **kwargs):
        """
        Creates the actual object
        """
        instance = super().__new__(cls)  # actually creates the object
        return instance
    
    def __init__(
            self,
            token:      Optional[str] = None,
            url:        Optional[str] = None,
            filename:   Optional[str] = None,
            name:       Optional[str] = None,
            **kwargs
        ) -> None:
        """
        Class constructor.

        Args:
            token       (str): Quantum Rings provided API token for the user's account
            url         (str): An alternate URL, if provided by Quantum Rings
            filename    (str): An alternate file from which the user's details are to be loaded.
            name        (str): Quantum Rings provided user account name. Usually the email ID of the user.

        Returns:
            The class object.
        """
        self.configuration = {}
        self.configuration["token"] = token
        if None != url:
            self.configuration["url"] = url
        self.configuration["name"] = name
        self._qr_provider = None

        if None != filename and os.path.exists(filename):
            config = configparser.ConfigParser()
            config.read(filename)

            if "default" not in config:
                raise ValueError("Missing [default] section in config file")

            self.configuration = dict(config["default"])

        if ("token" not in self.configuration) or ("name" not in self.configuration):
            self._qr_provider = QuantumRingsLib.QuantumRingsProvider()
        else:
            if "url" in self.configuration:
                self._qr_provider = QuantumRingsLib.QuantumRingsProvider(
                                    name = self.configuration["name"],
                                    token = self.configuration["token"],
                                    url = self.configuration["url"]
                                    )
            else:
                self._qr_provider = QuantumRingsLib.QuantumRingsProvider(
                    name = self.configuration["name"],
                    token = self.configuration["token"]
                    )

        if ( self._qr_provider == None ):
            raise Exception ("Unable to obtain Quantum Rings Provider. Please check the arguments")
        
        return
    

    def backends(
        self,
        **kwargs: Any,    
        ) -> list[str] :
        """
        Returns the list of available backends

        Args:
            None

        Returns:
            A list of available backends.
        """
        return self._qr_provider.backends()
    

    def active_account(self) -> dict :
        """
        Returns the currently active account

        Args:
            None

        Returns:
            The details of the currently active account in the form of a dict.
        """
        return self._qr_provider.active_account()

    def backend(
        self,
        name: str,
        **kwargs,    
        ) -> QrBackendV2 :
        """
        Obtains the handle to the requested backend

        Args:
            name       (str): Name of the backend to be acquired.
            precision  (str): An optional precision parameter - "single" or "double"
            gpu        (int): An optional GPU ID to use.
            num_qubits (int): An optional number of qubits the backend will use.

        Returns:
            A handle to the required backend.
        """

        self._precision = "single"
        self._gpu_id = 0
        self._backend = name.lower()
        self._num_qubits = None
        self._qr_backend = None

        backend_parameters = {}

        if ( isinstance(kwargs.get('precision'), str ) ):
            self._precision= kwargs.get('precision')
            self._precision = self._precision.lower()
            backend_parameters['precision'] = self._precision

        if ( isinstance(kwargs.get('gpu'), int ) ):
            self._gpu_id = kwargs.get('gpu')
            backend_parameters['gpu'] = self._gpu_id

        if ( isinstance(kwargs.get('num_qubits'), int ) ):
            self._num_qubits = kwargs.get('num_qubits')
            backend_parameters['num_qubits'] = self._num_qubits

        backend_parameters["provider"] = self._qr_provider
        backend_parameters["name"] = self._backend

        self._qr_backend = QrBackendV2( **backend_parameters )

        if (None == self._num_qubits):
            self._num_qubits = self._qr_backend._num_qubits
        
        return self._qr_backend
    

    def delete_account(
        self,
        filename: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs: Any,
        ) -> bool:

        """
        Deletes a saved account from the file if provided or from the system configuration file

        Args:
            filename: Name of file from which the account is to be deleted.
            name: Name of the saved account to be deleted.

        Returns:
            True if the account was deleted.
            False if no account was found or if the operation could not be performed.
        """
        if None != filename and os.path.exists(filename):
            config = configparser.ConfigParser()
            config.read(filename)

            sections_to_remove = [section for section in config.sections() if name in config[section]]
    
            for section in sections_to_remove:
                config.remove_section(section)

            with open(filename, "w") as f:
                config.write(f)

        else:
            self._qr_provider.delte_account(name)

        return True
    
    
    def active_instance(self):
        raise NotImplementedError("This method is currently not supported.")

    def instances(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")

    def active_instance(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")  

    def check_pending_jobs(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")

    def delete_job(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")
    
    def job(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")

    def jobs(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")
    
    def usage(self, **kwarge):
        raise NotImplementedError("This method is currently not supported.")

    def least_busy(self, **kwargs) -> QuantumRingsLib.BackendV2:
        """
        Return the "scarlet_quantum_rings" backend.
        This backend can be used everywhere, whether there is a GPU or not.
        Though it may not be performing quite well when comparted with a GPU based implementaiton
        with certain kinds of circuits.

        Args:
            min_num_qubits  (int): An optional number of qubits the backend will use..
            precision  (str): An optional precision parameter - "single" or "double"

        Returns:
            The backend "scarlet_quantum_rings".

        Raises:
            None
        """

        backend_parameters = {}

        if ( isinstance(kwargs.get('precision'), str ) ):
            self._precision= kwargs.get('precision')
            self._precision = self._backend.lower()
            backend_parameters['precision'] = self._precision

        if ( isinstance(kwargs.get('num_qubits'), int ) ):
            self._num_qubits = kwargs.get('num_qubits')
            backend_parameters['num_qubits'] = self._num_qubits


        return QrBackendV2(provider = self._qr_provider, name = "scarlet_quantum_rings", **backend_parameters)
    
    def save_account(
        self,
        token: Optional[str] = None,
        url: Optional[str] = None,
        filename: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs
        ) -> None:
        """
        Saves the account in the provided filename or in the system confifutation file.

        Args:
            token: Quantum Rings Provided access key.
            url: Validation server's URL. 
            filename: Full name of the file where the details are saved.
            name: Name of the Quantum Rings account.

        Returns:
            None

        Raises:
            None
        """
        if (name == None) or (token == None):
            raise ValueError("Missing data. Provide \"name\" and \"token\"")
        backend = None
        if isinstance(kwargs.get('backend'), str ):
            backend = kwargs.get('provider')

        if None != filename:
            config = configparser.ConfigParser()

            # Add a section called "default"

            if None == url and backend != None:
                config["default"] = {
                    "email": name,
                    "key": token,
                    "backend": "mybackend",
                }
            elif None == url and backend == None:
                config["default"] = {
                    "email": name,
                    "key": token,
                }
            elif None != url and backend == None:
                config["default"] = {
                    "email": name,
                    "key": token,
                    "url": url,
                }
            else:
                config["default"] = {
                    "email": name,
                    "key": token,
                    "backend": backend,
                    "url": url,
                }

            with open(filename, "w") as configfile:
                config.write(configfile)

        else:
            if url == None and backend == None:
                self._qr_provider.save_account(name = name, token = token)
            elif url != None and backend == None:
                self._qr_provider.save_account(name = name, token = token, url = url)
            elif url == None and backend != None:
                self._qr_provider.save_account(name = name, token = token, backend = backend)
            else:
                self._qr_provider.save_account(name = name, token = token, url = url, backend = backend)

        
        return
    
    def saved_accounts(
        self,
        filename: Optional[str] = None,
        **kwargs,
        ) -> dict:
        """
        Provides the details of the account saved in the provided file or in the
        system configuration file.

        Args:
            filename: Name of file whose accounts are returned.

        Returns:
            A dictionary with information about the accounts saved on disk.

        Raises:
            None
        """
        if filename != None and os.path.exists(filename):
            config = configparser.ConfigParser()
            config.read(filename)

            if "default" not in config:
                raise ValueError("Missing [default] section in config file")

            return dict(config["default"])
        else:
            return  self.qr_provider.saved_accounts()
        
             
        


    



