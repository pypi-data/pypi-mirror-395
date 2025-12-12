# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 08:13:26 2019

@author: RAMIAN
"""

from instrumentRS import instrumentRS
from instrumentRSExceptions import FileLoadError


class instrumentRS_VSE(instrumentRS):      
    """Python class implementing functionality for Rohde & Schwarz VSE Vector Signal Explorer software.
    It is based on the instrumentRS class for socket connectivity of R&S instruments."""
    #Store all measurement objects in this dictionary
    __MeasurementList = {}
    __PersistentChannels = None
    __OverWriteChannels = None
    __CurrentChannel = "Spectrum"
    
    def __init__(self, IpAddress,Port=5025, timeout=2, PersistentChannels = True, OverWriteChannels = True):
        super(instrumentRS_VSE,self).__init__( IpAddress, Port, timeout)
        self.__PersistentChannels = PersistentChannels
        self.__OverWriteChannels = OverWriteChannels
        
    def ChannelSelect( self, channelname):
        if self.__CurrentChannel != channelname:
            self.__CurrentChannel = channelname
            self.Write( "INST:SEL '"+ self.__CurrentChannel+"'")

    def LoadFile( self, filename, channelname=""):
        if channelname != "":
            self.ChannelSelect( channelname)
        self.Write("INST:BLOC:CHAN:SOUR FILE")
        if ".iq.tar" in filename.lower():
            self.Write("INST:BLOC:CHAN:FILE:IQT \""+filename+"\",1")
        else:
            raise FileLoadError( "File format not supported")
    
    
def main():
    #for testing only, commented out are some things you can test!
    #pass

    #import time
    vse=instrumentRS_VSE("127.0.0.1",PersistentChannels =False)
    #vse.StartLogging("test.txt")
    vse.Connect()
    print(vse.GetID())
    
    vse.GetSystErr()
    vse.Close()
    
    
if __name__ == "__main__":
    # execute only if run as a script
    main()    
