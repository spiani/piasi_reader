from __future__ import print_function, division

from os.path import getsize

from grh import GRH
from mdr import MDR
from mphr import MPHR
from giadr import GIADR_quality, GIADR_scale_factors


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

    def read_mdrs(self):
        mdr_record_positions = [i for i in range(self.n_of_records) 
                                  if self.__record_list[i].type == 'MDR']
        giadr = self.get_giadr_scalefactors()
        for i in mdr_record_positions:
            mdr_record = self.__record_list[i]
            new_content = MDR.read(mdr_record.content, mdr_record.grh, giadr)
            self.__record_list[i] = Record(mdr_record.grh, new_content)

if __name__ == '__main__':
    iasi_file = IasiL1cNativeFile(IASI_FILENAME)
    iasi_file.read_mdrs()
    print(iasi_file.get_record(8).content)

