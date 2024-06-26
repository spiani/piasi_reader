"""
Piasi-reader: a library to read and convert the native IASI L1C files
Copyright (C) 2015  Stefano Piani

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

from __future__ import division

from struct import unpack
from numpy import (fromstring, dtype, int8, uint8, int32, uint32, zeros, array,
                   meshgrid, argmax, max)

dui = dtype(uint8)
dui = dui.newbyteorder('>')

def where_greater(a, b):
    """
    Given two array, a and b, return a new array c with the same
    length as b such that c[i] is the index of the first element
    of a to be greater (or equal) than b[i] (if there is not such
    an element, it returns -1 on that entry)
    """

    M = meshgrid(a,b)
    comparisons = (a >= M[1])
    output = argmax(comparisons, axis=1)
    # Now, when every element in a is smaller than the elements in b,
    # we have 0 as entry. Now we will put that entries to -1
    fix_empty_entries = max(comparisons, axis=1) - 1
    output += fix_empty_entries
    return output

def read_vint(raw_data):
    n_elements = len(raw_data) // 5
    as_uint_data = fromstring(raw_data, dtype=dui).reshape(n_elements, 5)
    mantissa = zeros((n_elements,), dtype = uint32)
    for i in range(4):
        mantissa += as_uint_data[:,i+1]*(256**(3-i))
    return int32(mantissa) / 10.0**int8(as_uint_data[:,0])

def read_short_date(raw_data):
    n_elements = len(raw_data) // 6
    format_string = ">"
    for i in range(n_elements):
        format_string += "HI"
    unpacked_data = unpack(format_string, raw_data)
    return array(unpacked_data, dtype=int32).reshape(n_elements,2)
