# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 08:13:26 2019

@author: RAMIAN
"""

from rskfd import instrumentRS


class instrumentRS_FSW(instrumentRS):      
    """Python class implementing functionality for Rohde & Schwarz FSW class Signal- And Spectrum Analyzer instruments.
    It is based on the instrumentRS class for socket connectivity of R&S instruments."""
    #Store all measurement objects in this dictionary
    __MeasurementList = {}
    __PersistentChannels = None
    __OverWriteChannels = None
    __CurrentChannel = "Spectrum"
    
    def __init__(self, IpAddress,Port=5025, timeout=2, PersistentChannels = True, OverWriteChannels = True):
        super(instrumentRS_FSW,self).__init__( IpAddress, Port, timeout)
        self.__PersistentChannels = PersistentChannels
        self.__OverWriteChannels = OverWriteChannels
        
    def ChannelSelect( self, channelname):
        if self.__CurrentChannel != channelname:
            self.__CurrentChannel = channelname
            self.Write( "INST:SEL '"+ self.__CurrentChannel+"'")
    
        
    def SetCenterFrequency( self, CenterFrequency):
        self.Write("FREQ:CENT "+str(CenterFrequency))
        
    def SetReferenceLevel( self, ReferenceLevel):
        self.Write("DISP:WIND:TRAC:Y:RLEV "+str(ReferenceLevel))
        
    def SetRfAttenuation( self, RfAttenuation):
        self.Write("INP:ATT:AUTO OFF")
        self.Write("INP:ATT "+str(RfAttenuation))
        
    def CoupleCenterFrequency( self):
        self.Write("INST:COUP:CENT ALL")
        
    def CoupleRefLevel( self):
        self.Write("INST:COUP:RLEV ALL")
        
    def CoupleRfAttenuation( self):
        self.Write("INST:COUP:ATTEN ALL")
        
        
    def SetupAclr( self, ChannelBandwidth = 98.28e6, AdjacentChannelBandwidth = 98.28e6, AdjacentChannelSpacing = 100e6, NumberOfAdjacentChannels = 1, Rbw = 100e3, CenterFrequency = 1e9, SweepTime = 10e-3):
        """Function that configures an ACLR measurement"""
    
        from AclrMeasurement import AclrMeasurement
        
        MeasName = "ACLR"
        #Need to remove existing object from MeasurementList expliticly, because of destructor
        self.__MeasurementList.pop(MeasName,None)
        self.__MeasurementList.update( {MeasName:AclrMeasurement( self, ChannelBandwidth = ChannelBandwidth, AdjacentChannelBandwidth = AdjacentChannelBandwidth,
                                                       AdjacentChannelSpacing = AdjacentChannelSpacing, NumberOfAdjacentChannels = NumberOfAdjacentChannels,
                                                       Rbw = Rbw, CenterFrequency = CenterFrequency, SweepTime = SweepTime, Overwrite = self.__OverWriteChannels, ChannelName = MeasName, Persistence = self.__PersistentChannels)})
    
    def MeasureAclr( self):
        """Function running the previously configured meausrement. Returns all measured values!"""
        
        MeasName = "ACLR"
        return self.__MeasurementList.get(MeasName).MeasureAclr()
    
    def DeleteAclr( self):
        MeasName = "ACLR"
        self.__MeasurementList.pop(MeasName)
    
    
    
    def SetupAmplifier(self, CenterFrequency):
        from AmplifierMeasurement import AmplifierMeasurement
        
        MeasName = "Amplifier"
        self.__MeasurementList.update( {MeasName:AmplifierMeasurement( self, CenterFrequency = CenterFrequency, Overwrite = self.__OverWriteChannels, Persistence = self.__PersistentChannels)})
        
    def GetAmplifier( self):
        MeasName = "Amplifier"
        return self.__MeasurementList.get(MeasName)

    def MeasureAmplifier(self):
        MeasName = "Amplifier"
        return self.__MeasurementList.get(MeasName).MeasureAmplifier()
    
    def DeleteAmplifier( self):
        MeasName = "Amplifier"
        self.__MeasurementList.pop(MeasName)

        
        
    def TakeScreenshot( self, localfile):
        """
        Function takes a screenshot from the instrument and transfers it to the local machine.
        
        Input arguments:
            localfile:  file name on local machine; file extension automatically sets file type

        Supported file types:
            png, jpg, wmf, bmp
        """
        import os

        remotefile = r"C:\temp\temp"
        # store current display update mode
        dispupdate = self.Query("SYST:DISP:UPD?")
        # display update on
        self.Write("SYST:DISP:UPD ON")
        # softkeys off
        self.Write("DISP:SKEY:STAT OFF")
        # logo off
        self.Write("DISP:LOGO OFF")
        # screencolor, no color change
        self.Write("HCOP:CMAP:DEF4")
        # No timestamp
        self.Write("HCOP:TDST:STAT OFF")
        # destination mass memory MMEM
        self.Write("HCOP:DEST 'MMEM'")
        # format
        _, fileextension = os.path.splitext( localfile)
        if fileextension.lower() == ".bmp":
            fileformat = "BMP"
        elif fileextension.lower() == ".wmf":
            fileformat = "WMF"
        elif fileextension.lower() == ".jpg":
            fileformat = "JPEG"
        elif fileextension.lower() == ".jpeg":
            fileformat = "JPEG"
        else:
            fileformat = "PNG"   

        self.Write("HCOP:DEV:LANG "+ fileformat)
        #self.Write("HCOP:CONT HCOP")
        self.Write("MMEM:NAME '"+remotefile+"'")
        self.Write("HCOP:IMM;*WAI")
        self.FileDownload( remotefile+"."+fileformat, localfile)
        self.Write("DISP:SKEY:STAT ON")
        self.Write( "SYST:DISP:UPD "+dispupdate)
        
        
    def SetupG5NR( self, CenterFrequency = 1e9, Downlink = True, Bandwidth = 100e6, NumberOfSubFrames = 10, CaptureTime = 20.1e-3):
        """Function that configures an ACLR measurement"""
    
        from G5NRMeasurement import G5NRMeasurement
        
        MeasName = "5GNR"
        #Need to remove existing object from MeasurementList expliticly, because of destructor
        self.__MeasurementList.pop(MeasName,None)
        self.__MeasurementList.update( {MeasName:G5NRMeasurement( self, Overwrite = self.__OverWriteChannels, ChannelName = MeasName, Persistence = self.__PersistentChannels,
                                                                 CenterFrequency = CenterFrequency,
                                                                 Downlink = Downlink, Bandwidth = Bandwidth, NumberOfSubFrames = NumberOfSubFrames, CaptureTime = CaptureTime)})
    
    def MeasureG5NR( self):
        """Function running the previously configured meausrement. Returns all measured values!"""
        
        MeasName = "5GNR"
        return self.__MeasurementList.get(MeasName).MeasureG5NR()
    
    def DeleteG5NR( self):
        MeasName = "5GNR"
        self.__MeasurementList.pop(MeasName)
        
        
    
    
def main():
    #for testing only, commented out are some things you can test!
    #pass

    #import time
    vse=instrumentRS_FSW("10.99.2.11",PersistentChannels =False)
    #vse.StartLogging("test.txt")
    vse.Connect()
    print(vse.GetID())
    vse.TakeScreenshot( "myscnshot.png")
    vse.TakeScreenshot( "myscnshot.bmp")
    vse.TakeScreenshot( "myscnshot.wmf")
    vse.TakeScreenshot( "myscnshot.jpg")
    
    
#ACLR Example
#    vse.SetupAclr(CenterFrequency = 3.3e9,NumberOfAdjacentChannels=3)
#    data=vse.MeasureAclr()
#    vse.DeleteAclr()
#    for x in data:
#        print(str(x))
#    vse.SetupAmplifier(3e9)


#mMplifier Example
    # vse.SetupAmplifier( 3e9)
    # ampli = vse.GetAmplifier()
    # ampli.ConnectGenerator( "169.254.138.159")
    # vse.MeasureAmplifier()
    
    #vse.FileDownload(r"C:\temp\FSW_Screenshot_2019-03-15_14-32-38.PNG",r"screenshot.png")
    #vse.FileUpload(r"screenshot.png", r"C:\temp\test.PNG")
    #print(vse.GetOpt())
    #vse.StartLogging("test.txt", True)
    #vse.Write("TRAC:IQ:DATA:FORM IQP")
    #vse.Write("FORM REAL,32;:TRAC:IQ:DATA:MEM?")
    #start = time.time_ns() only from 3.7 on
    #start = time.time()
    #floatdata=vse.ReadBinaryToFile("test1.iqw")
    #floatdata=vse.ReadBinary()
    #duration = time.time() - start
    #print("Total: {} samples in {:2.2f} ms. Speed: {:3.0f} MBit/s".format(len(floatdata),duration*1e3,len(floatdata)*4*8/duration/1e6))
    vse.GetSystErr()
    vse.Close()
    
    
if __name__ == "__main__":
    # execute only if run as a script
    pass
    #main()    
