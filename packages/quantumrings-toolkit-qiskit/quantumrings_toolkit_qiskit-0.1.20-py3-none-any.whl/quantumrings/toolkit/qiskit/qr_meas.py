# This code is part of Quantum Rings SDK.
#
# (C) Copyright Quantum Rings Inc, 2024, 2025.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# pylint: disable=wrong-import-position,wrong-import-order

from typing import List, Union, Iterable, Tuple


#
# a helper class for the sampler to hold the measurement data
#

class meas:
    """
    A helper class for the QrSamplerV2 to store the measurement data.
    """
    def __init__(self, bitstrings: list[str], shots: int = 0, shape: tuple[int, ...] | None = None):
        """
        Class initializer
        Args:
        results: The Results dictionary from the execution of a Quantum Circuit
        """
        if shots == 0:
            self.num_shots = len(bitstrings)
        else:
            self.num_shots =  shots

        self.array = bitstrings
        self.num_bits = len(bitstrings[0])
        self.shape = shape
  
    
    def get_int_counts(self, loc: int | tuple[int, ...] | None = None) -> dict[int, int]:
        """
        Returns the integer counts of the Results
        """
        creg_counts = {}
        if (loc == None):
            for bitstring in  self.array:
                creg_counts[bitstring] = creg_counts.get(bitstring, 0) + 1
        elif (isinstance(loc, int)):
            indx = loc
            start = indx * self.num_shots
            end = self.num_shots
            for bitstring in  self.array[start : start + end]:
                creg_counts[bitstring] = creg_counts.get(bitstring, 0) + 1
        elif (isinstance(loc, tuple)):
            for i in range (len(loc)):
                indx = loc[i]
                start = indx * self.num_shots
                end = self.num_shots
                for bitstring in  self.array[start : start + end]:
                    creg_counts[bitstring] = creg_counts.get(bitstring, 0) + 1

        int_counts_dict = {}
        for key, value in creg_counts.items():
            int_counts_dict[int(key,2)] = value
        return int_counts_dict
        
    def get_counts(self, loc: int | tuple[int, ...] | None = None) -> dict[str, int]:
        """
        Returns the binary counts of the Results.
        """
        creg_counts = {}
        if (loc == None):
            for bitstring in  self.array:
                creg_counts[bitstring] = creg_counts.get(bitstring, 0) + 1
        elif (isinstance(loc, int)):
            indx = loc
            start = indx * self.num_shots
            end = self.num_shots
            for bitstring in  self.array[start : start + end]:
                creg_counts[bitstring] = creg_counts.get(bitstring, 0) + 1
        elif (isinstance(loc, tuple)):
            for i in range (len(loc)):
                indx = loc[i]
                start = indx * self.num_shots
                end = self.num_shots
                for bitstring in  self.array[start : start + end]:
                    creg_counts[bitstring] = creg_counts.get(bitstring, 0) + 1
        return creg_counts
    
    def get_bitstrings(self, loc: int | tuple[int, ...] | None = None) -> list[str]:

        if self.array == None:
            return []
        if (loc == None):
            return self.array
        if (isinstance(loc, int)):
            indx = loc
            if (indx > (len(self.array) - 1)):
                return []
            else:
                result = []
                indx = loc
                start = indx * self.num_shots
                end = self.num_shots
                for bitstring in  self.array[start : start + end]:
                    result.append(bitstring)
                return result 
        if (isinstance(loc, tuple)):
            result = []
            for i in range (len(loc)):
                indx = loc[i]
                start = indx * self.num_shots
                end = self.num_shots
                for bitstring in  self.array[start : start + end]:
                    result.append(bitstring)
            return result
        return []
        
        