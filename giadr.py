from struct import unpack
from numpy import fromstring, float64, int8, uint8, int16, int32, uint32, bool_, dtype, zeros

from grh import GRH
from parameters import PN, IMLI, IMCO

class GIADR_quality(object):

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
        giadr.IDefPsfSondY = (fromstring(raw_data[offset : offset + increase], dtype=dt)/1e6).reshape(100,PN)
        offset += increase

        increase = 100 * PN * 4 
        giadr.IDefPsfSondZ = (fromstring(raw_data[offset : offset + increase], dtype=dt)/1e6).reshape(100,PN)
        offset += increase

        increase = 100 * 100 * PN * 5
        PsfSond_raw = fromstring(raw_data[offset : offset + increase], dtype=dui).reshape(100, 100, PN, 5)
        offset+= increase
        IDefPsfSondWgt_int = zeros((100, 100, PN), dtype = uint32)
        for i in range(4):
            IDefPsfSondWgt_int += PsfSond_raw[:,:,:,i+1]*(256**(3-i))
        giadr.IDefPsfSondWgt = int32(IDefPsfSondWgt_int) / 10.0**int8(PsfSond_raw[:,:,:,0])

        increase = 4
        giadr.IDefllSSrfNsfirst = unpack('>i',raw_data[offset : offset + increase])[0]
        offset += increase
        giadr.IDefllSSrfNslast  = unpack('>i',raw_data[offset : offset + increase])[0]
        offset += increase
        
        increase = 100 * 5
        IDefllSSrf_raw = fromstring(raw_data[offset : offset + increase], dtype=dui).reshape(100, 5)
        offset += increase
        IDefllSSrf_int = zeros((100,), dtype = uint32)
        for i in range(4):
            IDefllSSrf_int += IDefllSSrf_raw[:,i+1]*(256**(3-i))
        giadr.IDefllSSrf = int32(IDefllSSrf_int) / 10.0**int8(IDefllSSrf_raw[:,0])

        increase = 5
        IDefllSSrfDWn_elements = unpack('>bi', raw_data[offset : offset + increase])
        offset += increase
        giadr.IDefllSSrfDWn = IDefllSSrfDWn_elements[1] / 10.0**IDefllSSrfDWn_elements[0]

        increase = IMCO * IMLI * 5
        IDefIISNeDT_raw = fromstring(raw_data[offset : offset + increase], dtype=dui).reshape(IMCO, IMLI, 5)
        offset+= increase
        IDefIISNeDT_int = zeros((IMCO,IMLI), dtype = uint32)
        for i in range(4):
            IDefIISNeDT_int += IDefIISNeDT_raw[:,:,i+1]*(256**(3-i))
        giadr.IDefIISNeDT = int32(IDefIISNeDT_int) / 10.0**int8(IDefIISNeDT_raw[:,:,0])

        increase = IMCO * IMLI * 1
        giadr.IDefDptIISDeadPix = fromstring(raw_data[offset : offset + increase], dtype=bool_).reshape(IMCO, IMLI)
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
        

class GIADR_scale_factors(object):

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
