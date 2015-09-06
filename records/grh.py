from struct import unpack

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

