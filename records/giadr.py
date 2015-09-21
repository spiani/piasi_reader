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

from struct import unpack
from numpy import fromstring, float64, int8, uint8, int16, int32, uint32, bool_, dtype, zeros

from piasi_reader.utilities import read_vint
from piasi_reader.records.record_content import interpreted_content
from piasi_reader.records.grh import GRH
from piasi_reader.parameters import PN, IMLI, IMCO

class GIADR_quality(interpreted_content):

    @staticmethod
    def read(f, grh):
        giadr = GIADR_quality()
        raw_data = f.read(grh.record_size - GRH.size)

        dt = dtype(int32)
        dt = dt.newbyteorder('>')
        dui = dtype(uint8)
        dui = dui.newbyteorder('>')

        offset = 0
        increase = 0

        increase = PN * 4
        giadr.IDefPsfSondNbLin = fromstring(raw_data[offset : offset + increase], dtype=dt)
        offset += increase

        increase = PN * 4
        giadr.IDefPsfSondNbCol = fromstring(raw_data[offset : offset + increase], dtype=dt)
        offset += increase

        increase = 5
        SampFactor_elements = unpack('>bi', raw_data[offset : offset + increase])
        offset += increase
        giadr.IDefPsfSondOverSampFactor = SampFactor_elements[1] / (10.0**SampFactor_elements[0])

        increase = 100 * PN * 4 
        giadr.IDefPsfSondY = (fromstring(raw_data[offset : offset + increase], dtype=dt)/1e6).reshape(PN, 100).T
        offset += increase

        increase = 100 * PN * 4 
        giadr.IDefPsfSondZ = (fromstring(raw_data[offset : offset + increase], dtype=dt)/1e6).reshape(PN,100).T
        offset += increase

        increase = 100 * 100 * PN * 5
        giadr.IDefPsfSondWgt = read_vint(raw_data[offset : offset + increase]).reshape(PN, 100, 100).T
        offset+= increase

        increase = 4
        giadr.IDefllSSrfNsfirst = unpack('>i',raw_data[offset : offset + increase])[0]
        offset += increase
        giadr.IDefllSSrfNslast  = unpack('>i',raw_data[offset : offset + increase])[0]
        offset += increase
        
        increase = 100 * 5
        giadr.IDefllSSrf = read_vint(raw_data[offset : offset + increase])
        offset += increase

        increase = 5
        giadr.IDefllSSrfDWn = read_vint(raw_data[offset : offset + increase])[0]
        offset += increase

        increase = IMCO * IMLI * 5
        giadr.IDefIISNeDT = read_vint(raw_data[offset : offset + increase]).reshape(IMLI, IMCO).T
        offset+= increase

        increase = IMCO * IMLI * 1
        giadr.IDefDptIISDeadPix = fromstring(raw_data[offset : offset + increase], dtype=bool_).reshape(IMLI, IMCO)
        offset+= increase        
                
        assert grh.record_size == offset + GRH.size 
        return giadr


    def __str__(self):
        output  = "========== IASI GIADR QUALITY ==========\n"
        output += "IDefPsfSondNbLin = " + str(self.IDefPsfSondNbLin) + "\n"
        output += "IDefPsfSondNbCol = " + str(self.IDefPsfSondNbCol) + "\n"
        output += "IDefPsfSondOverSampFactor = " + str(self.IDefPsfSondOverSampFactor) + "\n"
        output += "IDefPsfSondY =\n" + str(self.IDefPsfSondY) + "\n" 
        output += "IDefPsfSondZ =\n" + str(self.IDefPsfSondZ) + "\n" 
        output += "IDefPsfSondWgt =\n" + str(self.IDefPsfSondWgt) + "\n" 
        output += "IDefllSSrfNsfirst = " + str(self.IDefllSSrfNsfirst) + "\n" 
        output += "IDefllSSrfNslast = " + str(self.IDefllSSrfNslast) + "\n" 
        output += "IDefllSSrf =\n" + str(self.IDefllSSrf) + "\n" 
        output += "IDefllSSrfDWn = " + str(self.IDefllSSrfDWn) + "\n" 
        output += "IDefIISNeDT =\n" + str(self.IDefIISNeDT) + "\n" 
        output += "IDefDptIISDeadPix =\n" + str(self.IDefDptIISDeadPix)
        return output 
        

class GIADR_scale_factors(interpreted_content):

    @staticmethod
    def read(f, grh):
        giadr = GIADR_scale_factors()
        raw_data = f.read(grh.record_size - GRH.size)

        ds = dtype(int16)
        ds = ds.newbyteorder('>')

        int_data = fromstring(raw_data, dtype=ds, count = 32)
        
        giadr.IDefScaleSondNbScale = int_data[0]
        giadr.IDefScaleSondNsfirst = int_data[1:11]
        giadr.IDefScaleSondNslast  = int_data[11:21]
        giadr.IDefScaleSondScaleFactor = int_data[21:31]
        giadr.IDefScaleIISScaleFactor = int_data[31]

        return giadr
        
    def __str__(self):
        output  = "========== IASI GIADR SCALEFACTOR ==========\n"
        output += "IDefScaleSondNbScale =      " + str(self.IDefScaleSondNbScale) + "\n"
        output += "IDefScaleSondNsfirst =     "  + str(self.IDefScaleSondNsfirst) + "\n"
        output += "IDefScaleSondNslast =      "  + str(self.IDefScaleSondNslast) + "\n"
        output += "IDefScaleSondScaleFactor = "  + str(self.IDefScaleSondScaleFactor) + "\n"
        output += "IDefScaleIISScaleFactor =   " + str(self.IDefScaleIISScaleFactor)
        return output
