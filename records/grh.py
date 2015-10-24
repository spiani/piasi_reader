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

from struct import unpack, pack

grh_type_dict = { 1 : 'MPHR',
                  2 : 'SPHR',
                  3 : 'IPR',
                  4 : 'GEADR',
                  5 : 'GIADR',
                  6 : 'VEADR',
                  7 : 'VIADR',
                  8 : 'MDR'}

class GRH(object):

    size = 20 # This is the dimension (in bytes) of the grh

    def __init__(self):
        self.__record_class = None
        self.instrument_group = None
        self.record_subclass = None
        self.record_subclass_version = None
        self.record_size = None
        self.record_start_time_day = None
        self.record_start_time_msec = None
        self.record_stop_time_day = None
        self.record_stop_time_msec = None
    
    @staticmethod
    def read_grh(f):
        raw_data = f.read(GRH.size)
        grh_data = unpack('>BBBBIHIHI',raw_data)
        grh = GRH()
        grh.__record_class = grh_data[0]
        grh.instrument_group = grh_data[1]
        grh.record_subclass = grh_data[2]
        grh.record_subclass_version = grh_data[3]
        grh.record_size = grh_data[4]
        grh.record_start_time_day = grh_data[5]
        grh.record_start_time_msec = grh_data[6]
        grh.record_stop_time_day = grh_data[7]
        grh.record_stop_time_msec = grh_data[8]
        return grh

    @property
    def record_class(self):
        return grh_type_dict[self.__record_class]

    def __str__(self):
        output  = 'Record class:             ' + str(self.record_class) + '\n'
        output += 'Instrument group:         ' + str(self.instrument_group) + '\n'
        output += 'Record subclass:          ' + str(self.record_subclass) + '\n'
        output += 'Record subclass version:  ' + str(self.record_subclass_version) + '\n'
        output += 'Record size:              ' + str(self.record_size) + '\n'
        output += 'Record start time (day):  ' + str(self.record_start_time_day) + '\n'
        output += 'Record start time (msec): ' + str(self.record_start_time_msec) + '\n'
        output += 'Record stop time (day):   ' + str(self.record_start_time_day) + '\n'
        output += 'Record stop time (msec):  ' + str(self.record_start_time_msec)
        return output

    @property
    def raw(self):
        return pack('>BBBBIHIHI', self.__record_class,
                                  self.instrument_group,
                                  self.record_subclass,
                                  self.record_subclass_version,
                                  self.record_size,
                                  self.record_start_time_day,
                                  self.record_start_time_msec,
                                  self.record_stop_time_day,
                                  self.record_stop_time_msec
                                 )
