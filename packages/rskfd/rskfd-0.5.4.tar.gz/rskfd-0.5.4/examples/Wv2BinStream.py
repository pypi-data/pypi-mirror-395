# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 2021

(C) 2021, Rohde&Schwarz, ramian
"""

import struct
import re
import math


def ConvertWv2BinStream( FileName, bScale = False):
    '''
    Convert large wv files to bin (KS file format), i.e. do not read full iq vector
    Note: bin file must not have a higher power than "1", use rescale option to make sure
    '''
    SampleSize = 4 # 2 x 2 bytes
    BlockSize = 50000

    try:
        file = open(FileName, "rb")
        data = file.read( 30000)     # for the header, 30 kB should be sufficient
    except:
        print( "File open error ("+ FileName+")!")

    binaryStart = 0
    tags = ""
    Counter = 0
    ConverterSize = 20
    while (binaryStart == 0) & (Counter < len(data)):
        tags += data[Counter:Counter+ConverterSize].decode("ASCII","ignore")
        Counter += ConverterSize
        #{WAVEFORM-20001: #
        res = re.search("WAVEFORM.{0,20}:.{0,3}#",tags)
        if res is not None:
            binaryStart = res.span()[1]

    if binaryStart == 0:
        print("Binary start not found!\n")

    if (Counter > len(data)) & (binaryStart == 0):
        print( "Required tags not found, potentially incompatible file format!")

    res = re.search("SAMPLES[ ]*:[ ]*(?P<NumberOfSamples>[0-9]*)[ ]*}",tags)
    if res:
        NumberOfSamples = int( res.group("NumberOfSamples"))
    else:
        NumberOfSamples = -1
    
    outFileName = FileName.lower().replace( '.wv', '.bin')
    outfile = open( outFileName, "wb")

    # data = data[binaryStart:]
    # data = data + file.read( SampleSize-(len(data) % SampleSize))
    # NumberOfInt16s = len(data)//2
    # SampleCount = NumberOfInt16s // 2
    # data = list(struct.unpack("h"*NumberOfInt16s, data))
    # for nIdx in range(NumberOfInt16s):
    #     if bScale:
    #         outfile.write( struct.pack(">h",data[nIdx]))
    fScaler = 1
    if bScale:
        # first loop only to find max
        SampleCount = 0
        file.seek(binaryStart)
        fMaxPower = 0
        while SampleCount < NumberOfSamples:
            SamplesToRead = NumberOfSamples-SampleCount
            if SamplesToRead > BlockSize:
                SamplesToRead = BlockSize
            data = file.read( SamplesToRead * SampleSize)
            NumberOfInt16s = len(data)//2
            data = list(struct.unpack("h"*NumberOfInt16s, data))
            fData = list(map( lambda x: x/32767.0, data ))
            for nIdx in range(0,len(fData)//2):
                fMaxPower = max( [fMaxPower, fData[nIdx*2]**2 + fData[1+nIdx*2]**2])
            SampleCount = SampleCount + SamplesToRead
        fScaler = math.sqrt( fMaxPower)
    
    SampleCount = 0
    file.seek(binaryStart)
    fMaxPower = 0
    while SampleCount < NumberOfSamples:
        SamplesToRead = NumberOfSamples-SampleCount
        if SamplesToRead > BlockSize:
            SamplesToRead = BlockSize
        data = file.read( SamplesToRead * SampleSize)
        NumberOfInt16s = len(data)//2
        data = list(struct.unpack("h"*NumberOfInt16s, data))
        for nIdx in range(NumberOfInt16s):
            if bScale:
                data[nIdx] = round( data[nIdx] / fScaler)
            outfile.write( struct.pack(">h",data[nIdx]))
        SampleCount = SampleCount + SamplesToRead

    file.close()
    outfile.close()



if __name__ == "__main__":
    # pass
    # Testcode
    filename = r'C:\Users\ramian\Downloads\EVM_Eval_11be_320MHz_MCS13'
    ConvertWv2BinStream( filename+'.wv', bScale=True)
    # import rskfd
    # iq,fs = rskfd.ReadWv(filename + '.wv')
    # rskfd.WriteBin( iq,fs, filename +'.bin')
