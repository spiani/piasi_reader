from struct import unpack
from numpy import fromstring, dtype, int8, int16, int32, uint8, uint16, uint32, bool_, arange, newaxis, zeros, float64
from utilities import read_vint, read_short_date, where_greater

from grh import GRH
from parameters import AMCO, AMLI, CCD, IMLI, IMCO, NBK, NCL, PN, SB, SGI, SNOT, SS

class MDR(object):

    @staticmethod
    def read(raw_data, grh, giadr_sf):
        mdr = MDR()

        dt = dtype(int32)
        dt = dt.newbyteorder('>')
        di = dtype(int8)
        di = di.newbyteorder('>')
        ds = dtype(int16)
        ds = ds.newbyteorder('>')
        dui = dtype(uint8)
        dui = dui.newbyteorder('>')
        dus = dtype(uint16)
        dus = dus.newbyteorder('>')
        dut = dtype(uint32)
        dut = dut.newbyteorder('>')

        offset = 0
        increase = 0

        increase = 1
        mdr.degraded_inst_mdr = unpack('>?', raw_data[offset : offset + increase])[0]
        offset += increase

        increase = 1
        mdr.degraded_proc_mdr = unpack('>?', raw_data[offset : offset + increase])[0]
        offset += increase
         
        increase = 4 * 1
        mdr.GEPSIasiMode = fromstring(raw_data[offset : offset + increase], dtype=di)
        offset += increase

        increase = 4 * 1
        mdr.GEPSOPSPROCMode = fromstring(raw_data[offset : offset + increase], dtype=di)
        offset += increase

        increase = 32 * 1
        mdr.GEPSIdConf = fromstring(raw_data[offset : offset + increase], dtype=di)
        offset += increase

        increase = 2 * PN * SNOT * 5
        mdr.GEPSLocIasiAvhrr_IASI = read_vint(raw_data[offset : offset + increase]).reshape(2, PN, SNOT)
        offset+= increase

        increase = 2 * SGI * SNOT * 5
        mdr.GEPSLocIasiAvhrr_IIS = read_vint(raw_data[offset : offset + increase]).reshape(2, SGI, SNOT)
        offset+= increase

        increase = 6 * SNOT * 1
        mdr.OBT = fromstring(raw_data[offset : offset + increase], dtype=di).reshape(6, SNOT)
        offset += increase
        
        increase = SNOT * 6
        mdr.ONBoardUTC = read_short_date(raw_data[offset : offset + increase])
        offset += increase

        increase = SNOT * 6
        mdr.GEPSDatIasi = read_short_date(raw_data[offset : offset + increase])        
        offset += increase

        increase = CCD * 4
        mdr.GIsfLinOrigin = fromstring(raw_data[offset : offset + increase], dtype=dt)
        offset += increase

        increase = CCD * 4
        mdr.GIsfColOrigin = fromstring(raw_data[offset : offset + increase], dtype=dt)
        offset += increase

        increase = CCD * 4
        mdr.GIsfPds1 = fromstring(raw_data[offset : offset + increase], dtype=dt) / float(10**6) 
        offset += increase

        increase = CCD * 4
        mdr.GIsfPds2 = fromstring(raw_data[offset : offset + increase], dtype=dt) / float(10**6) 
        offset += increase

        increase = CCD * 4
        mdr.GIsfPds3 = fromstring(raw_data[offset : offset + increase], dtype=dt) / float(10**6) 
        offset += increase

        increase = CCD * 4
        mdr.GIsfPds4 = fromstring(raw_data[offset : offset + increase], dtype=dt) / float(10**6) 
        offset += increase

        increase = SNOT * 1
        mdr.GEPS_CCD = fromstring(raw_data[offset : offset + increase], dtype=bool_) 
        offset += increase

        increase = SNOT * 4
        mdr.GEPS_SP = fromstring(raw_data[offset : offset + increase], dtype=dt) 
        offset += increase

        increase = IMCO * IMLI * SNOT * 2
        mdr.GIrcImage = fromstring(raw_data[offset : offset + increase], dtype=dus).reshape(IMCO, IMLI, SNOT) 
        offset += increase

        if grh.record_subclass_version == 4:
            increase = PN * SNOT * 1
            mdr.GQisFlagQual = fromstring(raw_data[offset : offset + increase], dtype=bool_).reshape(PN, SNOT)
            offset += increase
        elif grh.record_subclass_version == 5:
            increase = SB * PN * SNOT * 1
            mdr.GQisFlagQual_SCV5 = fromstring(raw_data[offset : offset + increase], dtype=bool_).reshape(SB, PN, SNOT)
            offset += increase

            increase = PN * SNOT * 2
            mdr.GQisFlagQualDetailed = fromstring(raw_data[offset : offset + increase], dtype=ds).reshape(PN, SNOT)
            offset += increase

        increase = 5
        mdr.GQisQualIndex = read_vint(raw_data[offset : offset + increase])[0] 
        offset += increase

        increase = 5
        mdr.GQisQualIndexIIS = read_vint(raw_data[offset : offset + increase])[0] 
        offset += increase

        increase = 5
        mdr.GQisQualIndexLoc = read_vint(raw_data[offset : offset + increase])[0] 
        offset += increase

        increase = 5
        mdr.GQisQualIndexRad = read_vint(raw_data[offset : offset + increase])[0] 
        offset += increase

        increase = 5
        mdr.GQisQualIndexSpect = read_vint(raw_data[offset : offset + increase])[0] 
        offset += increase

        increase = 4
        mdr.GQisSysTecIISQual = fromstring(raw_data[offset : offset + increase], dtype=dut)[0]
        offset += increase

        increase = 4
        mdr.GQisSysTecSondQual = fromstring(raw_data[offset : offset + increase], dtype=dut)[0]
        offset += increase

        increase = 2 * PN * SNOT * 4
        mdr.GGeoSondLoc = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(2, PN, SNOT) / 1e06 
        offset += increase

        increase = 2 * PN * SNOT * 4
        mdr.GGeoSondAnglesMETOP = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(2, PN, SNOT) / 1e06 
        offset += increase

        increase = 2 * SGI * SNOT * 4
        mdr.GGeoIISAnglesMETOP = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(2, SGI, SNOT) / 1e06 
        offset += increase

        increase = 2 * PN * SNOT * 4
        mdr.GGeoSondAnglesSUN = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(2, PN, SNOT) / 1e06 
        offset += increase

        increase = 2 * SGI * SNOT * 4
        mdr.GGeoIISAnglesSUN = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(2, SGI, SNOT) / 1e06 
        offset += increase

        increase = 2 * SGI * SNOT * 4
        mdr.GGeoIISLoc = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(2, SGI, SNOT) / 1e06 
        offset += increase

        increase = 4
        mdr.earth_satellite_distance = fromstring(raw_data[offset : offset + increase], dtype=dut)[0]
        offset += increase

        increase = 5
        mdr.IDefSpectDWn1b = read_vint(raw_data[offset : offset + increase])[0]
        offset += increase

        increase = 4
        mdr.IDefNsFirst1b = fromstring(raw_data[offset : offset + increase], dtype=dt)[0]
        offset += increase

        increase = 4
        mdr.IDefNsLast1b = fromstring(raw_data[offset : offset + increase], dtype=dt)[0]
        offset += increase

        num_ch = mdr.IDefNsLast1b - mdr.IDefNsFirst1b + 1
        
        pos = where_greater(giadr_sf.IDefScaleSondNslast, arange(num_ch) + mdr.IDefNsFirst1b - 1)
        rad_sfs = giadr_sf.IDefScaleSondScaleFactor[pos]

        mdr.GS1cSpect = zeros((SS, PN, SNOT), dtype=float64)
        increase = SS * PN * SNOT * 2
        GS1cSpect = fromstring(raw_data[offset : offset + increase], dtype=ds).reshape(SS, PN, SNOT)
        offset += increase
        mdr.GS1cSpect[0:num_ch,:,:] = GS1cSpect[0:num_ch,:,:] / 10.**rad_sfs[:, newaxis, newaxis]

        increase = CCD * 100 * 5
        mdr.IDefCovarMatEigenVal1c = read_vint(raw_data[offset : offset + increase]).reshape(CCD, 100)
        offset+= increase

        increase = NBK * 4
        mdr.IDefCcsChannelId = fromstring(raw_data[offset : offset + increase], dtype=dt) 
        offset += increase

        increase = PN * SNOT * 4
        mdr.GCcsRadAnalNbClass = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(PN, SNOT) 
        offset += increase
        
        increase = NCL * PN * SNOT * 5
        mdr.GCcsRadAnalWgt = read_vint(raw_data[offset : offset + increase]).reshape(NCL, PN, SNOT)
        offset+= increase

        increase = NCL * PN * SNOT * 4
        mdr.GCcsRadAnalY = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(NCL, PN, SNOT)/ 1e06 
        offset+= increase

        increase = NCL * PN * SNOT * 4
        mdr.GCcsRadAnalZ = fromstring(raw_data[offset : offset + increase], dtype=dt).reshape(NCL, PN, SNOT)/ 1e06 
        offset+= increase

        increase = NBK * NCL * PN * SNOT * 5
        mdr.GCcsRadAnalMean = read_vint(raw_data[offset : offset + increase]).reshape(NBK, NCL, PN, SNOT)
        offset+= increase

        increase = NBK * NCL * PN * SNOT * 5
        mdr.GCcsRadAnalStd = read_vint(raw_data[offset : offset + increase]).reshape(NBK, NCL, PN, SNOT)
        offset+= increase

        increase = AMCO * AMLI * SNOT * 1
        mdr.GCcsImageClassified = fromstring(raw_data[offset : offset + increase], dtype=dui).reshape(AMCO, AMLI, SNOT) 
        offset+= increase

        increase = 4
        mdr.IDefCcsMode = fromstring(raw_data[offset : offset + increase], dtype=dt)[0] 
        offset+= increase

        increase = SNOT * 2
        mdr.GCcsImageClassifiedNbLin = fromstring(raw_data[offset : offset + increase], dtype=ds) 
        offset+= increase

        increase = SNOT * 2
        mdr.GCcsImageClassifiedNbCol = fromstring(raw_data[offset : offset + increase], dtype=ds) 
        offset+= increase

        increase = SNOT * 5
        mdr.GCcsImageClassifiedFirstLin = read_vint(raw_data[offset : offset + increase])
        offset+= increase

        increase = SNOT * 5
        mdr.GCcsImageClassifiedFirstCol = read_vint(raw_data[offset : offset + increase])
        offset+= increase

        increase = NCL * SNOT * 1
        mdr.GCcsRadAnalType = fromstring(raw_data[offset : offset + increase], dtype=bool_).reshape(NCL, SNOT) 
        offset+= increase

        if grh.record_subclass_version == 5:
            increase = SNOT * 5
            mdr.GIacVarImagIIS = read_vint(raw_data[offset : offset + increase])
            offset+= increase

            increase = SNOT * 5
            mdr.GIacAvgImagIIS = read_vint(raw_data[offset : offset + increase])
            offset+= increase

            increase = PN * SNOT * 1
            mdr.GEUMAvhrr1BCldFrac = fromstring(raw_data[offset : offset + increase], dtype=dui) 
            offset+= increase

            increase = PN * SNOT * 1
            mdr.GEUMAvhrr1BLandFrac = fromstring(raw_data[offset : offset + increase], dtype=dui) 
            offset+= increase

            increase = PN * SNOT * 1
            mdr.GEUMAvhrr1BQual = fromstring(raw_data[offset : offset + increase], dtype=di) 
            offset+= increase

        assert grh.record_size == offset + GRH.size 

        return mdr



    def __str__(self):
        output  = "============ IASI MDR 1C ============\n"
        output += "Degraded inst mdr = " + str(self.degraded_inst_mdr) + "\n"
        output += "Degraded proc mdr = " + str(self.degraded_proc_mdr) + "\n"
        output += "GEPS Iasi mode = " + str(self.GEPSIasiMode) + "\n"
        output += "GEPSOPSPROC Mode = " + str(self.GEPSOPSPROCMode) + "\n"
        output += "GEPS id conf =\n" + str(self.GEPSIdConf) + "\n"
        output += "GEPS LocIasiAvhrr IASI =\n" + str(self.GEPSLocIasiAvhrr_IASI) + "\n"
        output += "GEPS LocIasiAvhrr IIS =\n" + str(self.GEPSLocIasiAvhrr_IIS) + "\n"
        output += "OBT =\n" + str(self.OBT) + "\n"
        output += "ONBoard UTC =\n" + str(self.ONBoardUTC) + "\n"
        output += "GEPS Dat Iasi =\n" + str(self.GEPSDatIasi) + "\n"
        output += "GIsfLinOrigin = " + str(self.GIsfLinOrigin) + "\n"
        output += "GIsfColOrigin = " + str(self.GIsfColOrigin) + "\n"
        output += "GIsfPds1 = " + str(self.GIsfPds1) + "\n"
        output += "GIsfPds2 = " + str(self.GIsfPds2) + "\n"
        output += "GIsfPds3 = " + str(self.GIsfPds3) + "\n"
        output += "GIsfPds4 = " + str(self.GIsfPds4) + "\n"
        output += "GEPS CCD =\n" + str(self.GEPS_CCD) + "\n"
        output += "GEPS SP =\n" + str(self.GEPS_SP) + "\n"
        output += "GIrcImage =\n" + str(self.GIrcImage) + "\n"
        try:
            output += "GQisFlagQual =\n" + str(self.GQisFlagQual) + "\n"
        except AttributeError:
            pass
        try:
            output += "GQisFlagQual_SCV5 =\n" + str(self.GQisFlagQual_SCV5) + "\n"
            output += "GQisFlagQualDetailed =\n" + str(self.GQisFlagQualDetailed) + "\n"
        except AttributeError:
            pass
        output += "GQisQualIndex = " + str(self.GQisQualIndex) + "\n"
        output += "GQisQualIndexIIS = " + str(self.GQisQualIndexIIS) + "\n"
        output += "GQisQualIndexLoc = " + str(self.GQisQualIndexLoc) + "\n"
        output += "GQisQualIndexRas = " + str(self.GQisQualIndexRad) + "\n"
        output += "GQisQualIndexSpect = " + str(self.GQisQualIndexSpect) + "\n"
        output += "GQisSysTecIISQual = " + str(self.GQisSysTecIISQual) + "\n"
        output += "GQisSysTecSondQual = " + str(self.GQisSysTecSondQual) + "\n"
        output += "GGeoSondLoc =\n" + str(self.GGeoSondLoc) + "\n"
        output += "GGeoSondAnglesMETOP =\n" + str(self.GGeoSondAnglesMETOP) + "\n"
        output += "GGeoIISAnglesMETOP =\n" + str(self.GGeoIISAnglesMETOP) + "\n"
        output += "GGeoSondAnglesSUN =\n" + str(self.GGeoSondAnglesSUN) + "\n"
        output += "GGeoIISAnglesSUN =\n" + str(self.GGeoIISAnglesSUN) + "\n"
        output += "GGeoIISLoc =\n" + str(self.GGeoIISLoc) + "\n"
        output += "earth_satellite_distance = " + str(self.earth_satellite_distance) + "\n"
        output += "IDefSpectDWn1b = " + str(self.IDefSpectDWn1b) + "\n"
        output += "IDefNsfirst1b = " + str(self.IDefNsFirst1b) + "\n"
        output += "IDefNsLAST1b = " + str(self.IDefNsLast1b) + "\n"
        output += "GS1cSpect =\n" + str(self.GS1cSpect) + "\n"
        output += "IDefCovarMatEigenVal1c =\n" + str(self.IDefCovarMatEigenVal1c) + "\n"
        output += "IDefCcsChannelId = " + str(self.IDefCcsChannelId) + "\n"
        output += "GCcsRadAnalNbClass =\n" + str(self.GCcsRadAnalNbClass) + "\n"
        output += "GCcsRadAnalWgt =\n" + str(self.GCcsRadAnalWgt) + "\n"
        output += "GCcsRadAnalY =\n" + str(self.GCcsRadAnalY) + "\n"
        output += "GCcsRadAnalZ =\n" + str(self.GCcsRadAnalZ) + "\n"
        output += "GCcsRadAnalMean =\n" + str(self.GCcsRadAnalMean) + "\n"
        output += "GCcsRadAnalStd =\n" + str(self.GCcsRadAnalStd) + "\n"
        output += "GCcsImageClassified =\n" + str(self.GCcsImageClassified) + "\n"
        output += "IDefCcsMode = " + str(self.IDefCcsMode) + "\n"
        output += "GCcsImageClassifiedNbLin =\n" + str(self.GCcsImageClassifiedNbLin) + "\n"
        output += "GCcsImageClassifiedNbCol =\n" + str(self.GCcsImageClassifiedNbCol) + "\n"
        output += "GCcsImageClassifiedFirstLin =\n" + str(self.GCcsImageClassifiedFirstLin) + "\n"
        output += "GCcsImageClassifiedFirstCol =\n" + str(self.GCcsImageClassifiedFirstCol) + "\n"
        output += "GCcsRadAnalType =\n" + str(self.GCcsRadAnalType) + "\n"
        try:
            output += "GIacVarImagIIS =\n" + str(self.GIacVarImagIIS) + "\n"
            output += "GEUMAvhrr1BCldFrac =\n" + str(self.GEUMAvhrr1BCldFrac) + "\n"
            output += "GEUMAvhrr1BLandFrac =\n" + str(self.GEUMAvhrr1BLandFrac) + "\n"
            output += "GEUMAvhrr1BQual =\n" + str(self.GEUMAvhrr1BQual) + "\n"
        except AttributeError:
            pass
        
        return output

