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

from __future__ import print_function, division

import numpy as np
from os.path import getsize, join

from records.record_content import uninterpreted_content
from records.grh import GRH
from records.mdr import MDR
from records.mphr import MPHR
from records.giadr import GIADR_quality, GIADR_scale_factors

from parameters import PN, SNOT


class MphrNotFoundException(Exception):
    """A error that happens if the file do not has a MPHR"""
    pass

class GiadrQualityNotFoundException(Exception):
    """A error that happens if the file do not has a GIADR quality"""
    pass

class GiadrScalefactorsNotFoundException(Exception):
    """A error that happens if the file do not has a GIADR scalefactor"""
    pass

class NotSoManyRecordsException(ValueError):
    """
    This error is raised if something tries to access to a record whose
    number is greater than the total number of records
    """
    pass

class Record(object):
    """
    The Record is the unit of information of the IASI files. Every file is composed
    by one or more records. Every record is made of two elements:
      - a grh which contains some metadata about the record
      - a content, i.e. the real data

    While in principle it is possible to create a record calling the __init__ method
    and passing a gdr object and the content, usually a record is created buy the read
    method starting from a file

    Args:
        - *grh*: a GRH object
        - *content*: a record_content object
    """
    def __init__(self, grh, content):
        self.__grh = grh
        self.__content = content

    @property
    def type(self):
        """
        The type of the record as string. It could be one of the following:
          - MPHR
          - SPHR
          - IPR
          - GEADR
          - GIADR
          - VEADR
          - VIADR
          - MDR
        """
        return self.__grh.record_class
    
    @property
    def size(self):
        """
        The dimension in bytes of the record. It also includes the dimension
        of the grh
        """
        return self.__grh.record_size

    @property
    def grh(self):
        """
        The grh of the record
        """
        return self.__grh

    @property
    def content(self):
        """
        The content of the record. If the record is interpreted, it is
        an object that store all the information read; if not, it is just
        a sequence of bytes.
        """
        return self.__content

    @property
    def interpreted(self):
        """
        A boolean value that is True if the record is interpreted.
        """
        return self.content.interpreted
    
    @staticmethod
    def read(f):
        """
        Create a Record object starting from a file descriptor. If the
        record do not requires other informations, it will also be
        interpreted (for example for the mphr record). Otherwise, it
        will be returned as not interpreted (this is expecially true for
        the mdr records which require a GIADR scalefactor record)

        Args:
            -*f*: A file descriptor

        Returns:
            A Record object
        """
        grh = GRH.read_grh(f)
        if grh.record_class == 'MPHR':
            content = MPHR.read_mphr(f, grh)
        elif grh.record_class == 'GIADR':
            if grh.record_subclass == 0:
                content = GIADR_quality.read(f, grh)
            elif grh.record_subclass == 1:
                content = GIADR_scale_factors.read(f, grh)
            else:
                data = f.read(grh.record_size - GRH.size)
                content = uninterpreted_content(data)
        else:
            data = f.read(grh.record_size - GRH.size)
            content = uninterpreted_content(data)
        return Record(grh, content)


class IasiL1cNativeFile(object):
    def __init__(self, filename):
        self.__record_list = []
        self.__size = getsize(filename)

        # Read content from the file
        bytes_read = 0
        with open(filename, 'rb') as iasi_file:
            while bytes_read < self.__size:
                rcd = Record.read(iasi_file)
                self.__record_list.append(rcd)
                bytes_read += rcd.size
        self.__read_mdrs()

    @property
    def size(self):
        """
        An integer which is the size of the file in bytes
        """
        return self.__size

    @property
    def n_of_records(self):
        """
        An integer which is the number of the records saved in the file
        """
        return len(self.__record_list)

    def get_record(self, i):
        """
        Return the i-th record saved inside the file

        Args:
            - *i*: an integer between 0 and n_of_records

        Returns:
            An object of the Record class
        """

        if i>= self.n_of_records:
            raise NotSoManyRecordsException
        return self.__record_list[i]

    def get_mphr(self):
        """
        Return the record with the mphr of the file.

        Returns:
            An object of the Record class
        """

        mphr_records = [rcd for rcd in self.__record_list if rcd.type == 'MPHR']
        if len(mphr_records) == 0:
            raise MphrNotFoundException
        return mphr_records[0].content

    def get_giadr_quality(self):
        """
        Return the record with the GIADR quality of the file.

        Returns:
            An object of the Record class
        """

        giadr_records = [rcd for rcd in self.__record_list 
                         if rcd.type == 'GIADR' and rcd.grh.record_subclass == 0]
        if len(giadr_records) == 0:
            raise GiadrQualityNotFoundException
        return giadr_records[0].content

    def get_giadr_scalefactors(self):
        """
        Return the record with the GIADR scalefactors of the file.

        Returns:
            An object of the Record class
        """

        giadr_records = [rcd for rcd in self.__record_list 
                         if rcd.type == 'GIADR' and rcd.grh.record_subclass == 1]
        if len(giadr_records) == 0:
            raise GiadrScalefactorsNotFoundException
        return giadr_records[0].content
    
    def get_mdrs(self):
        """
        Return a list of all the records of mdr type

        Returns:
            A list of record objects
        """
        return [r.content for r in self.__record_list if r.type == "MDR"]

    def __read_mdrs(self):
        mdr_record_positions = [i for i in range(self.n_of_records) 
                                  if self.__record_list[i].type == 'MDR']
        giadr = self.get_giadr_scalefactors()
        for i in mdr_record_positions:
            mdr_record = self.__record_list[i]
            new_content = MDR.read(mdr_record.content, mdr_record.grh, giadr)
            self.__record_list[i] = Record(mdr_record.grh, new_content)

    def get_latitudes(self):
        """
        Return a numpy array with all the latitudes read from all the records
        of the file.
        """
        mdrs = self.get_mdrs()
        latitudes_list = [mdr.GGeoSondLoc[1,:].T for mdr in mdrs]
        return np.concatenate(latitudes_list)

    def get_longitudes(self):
        """
        Return a numpy array with all the longitudes read from all the records
        of the file.
        """
        mdrs = self.get_mdrs()
        longitudes_list = [mdr.GGeoSondLoc[0,:].T for mdr in mdrs]
        return np.concatenate(longitudes_list)

    def get_radiances(self):
        """
        Return a numpy array with all the radiances read from all the records
        of the file.
        """

        mdrs = self.get_mdrs()
        radiances_list = [mdr.GS1cSpect for mdr in mdrs]
        return np.concatenate(radiances_list).T
        
    def get_zenith_angles(self):
        """
        Return an array with all the zenith angles read from all the records
        of the file.
        """
        mdrs = self.get_mdrs()
        zenith_angles_list = [mdr.GGeoSondAnglesMETOP[0,:].T for mdr in mdrs]
        return np.concatenate(zenith_angles_list)

    def get_solar_zenith_angles(self):
        """
        Return an array with all the solar zenith angles read from all the records
        of the file.
        """
        mdrs = self.get_mdrs()
        solar_zenith_angles_list = [mdr.GGeoSondAnglesSUN[0,:].T for mdr in mdrs]
        return np.concatenate(solar_zenith_angles_list)

    def get_solar_azimuth_angles(self):
        """
        Return an array with all the solar azimuth angles read from all the records
        of the file.
        """
        mdrs = self.get_mdrs()
        solar_azimuth_angles_list = [mdr.GGeoSondAnglesSUN[1,:].T for mdr in mdrs]
        return np.concatenate(solar_azimuth_angles_list)

    def get_avhrr_cloud_fractions(self):
        """
        Return an array with all the avhrr cloud fractions read from all the records
        of the file.
        """

        mdrs = self.get_mdrs()
        avhrr_cloud_fraction_list = [mdr.GEUMAvhrr1BCldFrac.T for mdr in mdrs]
        return np.concatenate(avhrr_cloud_fraction_list)

    def get_land_fractions(self):
        """
        Return an array with all the land fractions read from all the records
        of the file.
        """

        mdrs = self.get_mdrs()
        avhrr_cloud_fraction_list = [mdr.GEUMAvhrr1BLandFrac.T for mdr in mdrs]
        return np.concatenate(avhrr_cloud_fraction_list)
        
    def get_date_day(self):
        mdrs = self.get_mdrs()
        date_day_list = [mdr.GEPSDatIasi[:,0] for mdr in mdrs]
        return np.concatenate(date_day_list)

    def get_date_msec(self):
        mdrs = self.get_mdrs()
        date_msec_list = [mdr.GEPSDatIasi[:,1] for mdr in mdrs]
        return np.concatenate(date_msec_list)


    def __save_data(self, array_data, output_dir, file_name, data_type, shape):

        if data_type is None:
            to_save = array_data
            data_type = to_save.dtype
        else:
            to_save = array_data.astype(data_type)
        
        n_of_elements = to_save.size

        if shape is not None:
            assert np.prod(shape) == n_of_elements

        data_size = str(data_type.itemsize)
        i = 0
        while not data_type.name[i:].isdigit():
            i+=1
        data_name = data_type.name[:i].replace('float', 'real')
        
        complete_file_name = file_name + '.' + data_name + data_size
 
        if shape is not None and len(shape)>1:
            for i in range(1,len(shape)):
                complete_file_name += '.' + str(i)

        file_path = join(output_dir, complete_file_name)
        with open(file_path, 'wb') as fbf_file:
            to_save.tofile(fbf_file) 

        return True


    def save_latitudes(self,
                       output_dir = '.',
                       file_name = 'iasi_latitude',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_latitudes(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_longitudes(self,
                       output_dir = '.',
                       file_name = 'iasi_longitude',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_longitudes(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_radiances(self,
                       output_dir = '.',
                       file_name = 'iasi_radiance',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_radiances(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_zenith_angles(self,
                       output_dir = '.',
                       file_name = 'iasi_zenith',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_zenith_angles(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_solar_zenith_angles(self,
                       output_dir = '.',
                       file_name = 'solar_zenith',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_solar_zenith_angles(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_solar_azimuth_angles(self,
                       output_dir = '.',
                       file_name = 'solar_azimuth',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_solar_azimuth_angles(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_avhrr_cloud_fractions(self,
                       output_dir = '.',
                       file_name = 'avhrr_cloud_fraction',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_avhrr_cloud_fractions(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_land_fractions(self,
                       output_dir = '.',
                       file_name = 'land_fraction',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_land_fractions(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_date_day(self,
                       output_dir = '.',
                       file_name = 'observation_date_day',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_date_day(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_date_msec(self,
                       output_dir = '.',
                       file_name = 'observation_date_msec',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_date_msec(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)
