from __future__ import print_function, division

import numpy as np
from os.path import getsize, join

from records.grh import GRH
from records.mdr import MDR
from records.mphr import MPHR
from records.giadr import GIADR_quality, GIADR_scale_factors

from parameters import PN, SNOT


IASI_FILENAME = '/media/step/Volume/l2vdp/my_tests/bin/IASI_xxx_1C_M02_20120323201748Z_20120323202228Z_N_O_20120330080026Z.nat'

class MphrNotFoundException(Exception):
    pass

class GiadrQualityNotFoundException(Exception):
    pass

class GiadrScalefactorsNotFoundException(Exception):
    pass

class NotSoManyRecordsException(ValueError):
    pass

class Record(object):
    def __init__(self, grh, content):
        self.__grh = grh
        self.__content = content

    @property
    def type(self):
        return self.__grh.record_class
    
    @property
    def size(self):
        return self.__grh.record_size

    @property
    def grh(self):
        return self.__grh

    @property
    def content(self):
        return self.__content
    
    @staticmethod
    def read(f):
        grh = GRH.read_grh(f)
        if grh.record_class == 'MPHR':
            content = MPHR.read_mphr(f)
        elif grh.record_class == 'GIADR':
            if grh.record_subclass == 0:
                content = GIADR_quality.read(f, grh)
            elif grh.record_subclass == 1:
                content = GIADR_scale_factors.read(f, grh)
            else:
                content = f.read(grh.record_size - GRH.size)
        else:
            content = f.read(grh.record_size - GRH.size)
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
        return self.__size

    @property
    def n_of_records(self):
        return len(self.__record_list)
    
    def get_record(self, i):
        if i>= self.n_of_records:
            raise NotSoManyRecordsException
        return self.__record_list[i]
    
    def get_mphr(self):
        mphr_records = [rcd for rcd in self.__record_list if rcd.type == 'MPHR']
        if len(mphr_records) == 0:
            raise MphrNotFoundException
        return mphr_records[0].content

    def get_giadr_quality(self):
        giadr_records = [rcd for rcd in self.__record_list 
                         if rcd.type == 'GIADR' and rcd.grh.record_subclass == 0]
        if len(giadr_records) == 0:
            raise GiadrQualityNotFoundException
        return giadr_records[0].content

    def get_giadr_scalefactors(self):
        giadr_records = [rcd for rcd in self.__record_list 
                         if rcd.type == 'GIADR' and rcd.grh.record_subclass == 1]
        if len(giadr_records) == 0:
            raise GiadrScalefactorsNotFoundException
        return giadr_records[0].content
    
    def get_mdrs(self):
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
        mdrs = self.get_mdrs()
        latitudes_list = [mdr.GGeoSondLoc[1,:].T for mdr in mdrs]
        return np.concatenate(latitudes_list)

    def get_longitudes(self):
        mdrs = self.get_mdrs()
        longitudes_list = [mdr.GGeoSondLoc[0,:].T for mdr in mdrs]
        return np.concatenate(longitudes_list)

    def get_radiances(self):
        mdrs = self.get_mdrs()
        radiances_list = [mdr.GS1cSpect for mdr in mdrs]
        return np.concatenate(radiances_list).T
        
    def get_zenith_angles(self):
        mdrs = self.get_mdrs()
        zenith_angles_list = [mdr.GGeoSondAnglesMETOP[0,:].T for mdr in mdrs]
        return np.concatenate(zenith_angles_list)

    def get_solar_zenith_angles(self):
        mdrs = self.get_mdrs()
        solar_zenith_angles_list = [mdr.GGeoSondAnglesSUN[0,:].T for mdr in mdrs]
        return np.concatenate(solar_zenith_angles_list)

    def get_solar_azimuth_angles(self):
        mdrs = self.get_mdrs()
        solar_azimuth_angles_list = [mdr.GGeoSondAnglesSUN[1,:].T for mdr in mdrs]
        return np.concatenate(solar_azimuth_angles_list)

    def get_avhrr_cloud_fraction(self):
        mdrs = self.get_mdrs()
        avhrr_cloud_fraction_list = [mdr.GEUMAvhrr1BCldFrac.T for mdr in mdrs]
        return np.concatenate(avhrr_cloud_fraction_list)

    def get_land_fraction(self):
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

    def save_avhrr_cloud_fraction(self,
                       output_dir = '.',
                       file_name = 'avhrr_cloud_fraction',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_avhrr_cloud_fraction(),
                                output_dir,
                                file_name,
                                data_type,
                                shape)

    def save_land_fraction(self,
                       output_dir = '.',
                       file_name = 'land_fraction',
                       data_type = None,
                       shape = None):
        return self.__save_data(self.get_land_fraction(),
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




if __name__ == '__main__':
    iasi_file = IasiL1cNativeFile(IASI_FILENAME)
