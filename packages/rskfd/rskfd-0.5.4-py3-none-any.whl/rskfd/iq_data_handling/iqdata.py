# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 22:01:25 2019

@author: RAMIAN
"""

#TODO: errorhandling

import numpy as np


def __DataTypeStr2Int(DataType):
    """
    Converts a string data type to int, defaults to float 32
    float32 ==> 1, float64 ==> 2, int8 ==> 3, int16 ==> 4, int32 ==> 5
    """
    RetType = 1
    if DataType.lower().strip() == "float32":
        RetType = 1
    elif DataType.lower().strip() == "float64":
        RetType = 2
    elif DataType.lower().strip() == "int8":
        RetType = 3
    elif DataType.lower().strip() == "int16":
        RetType = 4
    elif DataType.lower().strip() == "int32":
        RetType = 5

    return RetType


def __DataTypeInt2Str(DataType):
    """
    Converts a string data type to int, defaults to float 32
    float32 ==> 1, float64 ==> 2, int8 ==> 3, int16 ==> 4, int32 ==> 5
    """
    RetType = "float32"
    if DataType == 1:
        RetType = "float32"
    elif DataType == 2:
        RetType = "float64"
    elif DataType == 3:
        RetType = "int8"
    elif DataType == 4:
        RetType = "int16"
    elif DataType == 5:
        RetType = "int32"

    return RetType


def __NumberOfBytes(DataType):
    """
    Returns number of bytes per value
    float32 ==> 4, float64 ==> 8, int8 ==> 1, int16 ==> 2, int32 ==> 4
    """
    RetVal = 4
    if not isinstance(DataType, int):
        DataType = __DataTypeStr2Int(DataType)
    if DataType == 1:
        RetVal = 4
    elif DataType == 2:
        RetVal = 8
    elif DataType == 3:
        RetVal = 1
    elif DataType == 4:
        RetVal = 2
    elif DataType == 5:
        RetVal = 4

    return RetVal


def Iqiq2Complex( iqData):
    """Returns a complex list of I/Q samples from a single list containing IQIQIQ values
    complexList = Iqiq2Complex(iqiqiqList)"""

    import logging

    if len(iqData) % 2 > 0:
        logging.warn("Expecting IQIQIQ order, input vector has odd number of samples!")

    NumberOfSamples = len(iqData) // 2

    complexList = [complex(iqData[2*n], iqData[2*n+1]) for n in range(NumberOfSamples)]    
    return complexList



def Iiqq2Complex(iqData):
    """Returns a complex list of I/Q samples from a single list containing IIIQQQ values
    complexList = Iiqq2Complex(iiiqqqList)"""

    import logging

    if len(iqData) % 2 > 0:
        logging.warn("Expecting IIIQQQ order, input vector has odd number of samples!")

    NumberOfSamples = len(iqData) // 2

    complexList = [complex(iqData[n], iqData[n+NumberOfSamples]) for n in range(NumberOfSamples)]    
    return complexList



def Complex2Iqiq(complexList):
    """Returns a list of I/Q samples from a complex list.
    iqiqiqList = Complex2Iqiq(complexList)"""

    f = lambda iq, i: iq.real if i == 0 else iq.imag
    iqiqiqList = [f(iq, i) for iq in complexList for i in range(2)]

    return iqiqiqList



def Complex2Iiqq( complexList):
    """Returns a list of I/Q samples from a complex list.
    iiiqqqList = Complex2Iiqq(complexList)"""

    iqiqiqList = [iq.real for iq in complexList]
    iqiqiqList.append([iq.imag for iq in complexList])

    return iqiqiqList



def WriteIqw( iqData, FileName, AppendExisting=False, DataType="float32"):
    """Writes an IQW file (file of binary floats).
    iqData can be a list of complex or list of floats. List of floats will
    be written directly into iqw - regardles of order iiqq or iqiq.
    Note: IIIQQQ is a deprecated format, don't use it for new files.
    writtenSamples = WriteIqw( iqList, "MyFile.iqiq.iqw").
    DataType (supported): float32, float64
    """

    import struct
    import logging

    # check if iqData is complex
    if isinstance(iqData[0], complex):
        iqData = Complex2Iqiq(iqData)

    NumberOfSamples = len(iqData) // 2
    ScalingFactor = 1

    try:
        if AppendExisting:
            file = open(FileName, "ab")
        else:
            file = open(FileName, "wb")
        if __DataTypeStr2Int(DataType) == 1:
            # float 32
            file.write(struct.pack("f"*len(iqData), *iqData))
        elif __DataTypeStr2Int(DataType) == 2:
            # float64
            file.write(struct.pack("d"*len(iqData), *iqData))
        elif __DataTypeStr2Int(DataType) == 3:
            # int16
            ScalingFactor = max(map(abs, iqData))/(2**(__NumberOfBytes(DataType)*8-1)-1)
            iqData = [round(item / ScalingFactor) for item in iqData]
            file.write(struct.pack("b"*len(iqData), *iqData))
        elif __DataTypeStr2Int(DataType) == 4:
            # int16
            ScalingFactor = max(map(abs, iqData))/(2**(__NumberOfBytes(DataType)*8-1)-1)
            iqData = [round(item / ScalingFactor) for item in iqData]
            file.write(struct.pack("h"*len(iqData), *iqData))
        elif __DataTypeStr2Int(DataType) == 5:
            # int16
            ScalingFactor = max(map(abs, iqData))/(2**(__NumberOfBytes(DataType)*8-1)-1)
            iqData = [round(item / ScalingFactor) for item in iqData]
            file.write(struct.pack("i"*len(iqData), *iqData))

        file.close
    except:
        logging.error("File (" + FileName + ") write error!")

    return NumberOfSamples, ScalingFactor



def ReadIqw( FileName, iqiq=True, DataType="float32", bComplex=True):
    """Reads an IQW (can be iiqq or iqiq) file. Returns complex samples.
    If iqiq is True, samples are read pairwise (IQIQIQ),
    otherwise in blocks, i first then q (IIIQQQ)
    Note: IIIQQQ is a deprecated format, don't use it for new files.
    iqList = ReadIqw("MyFile.iqw", iqiq = True)
    DataType (supported): float32, float64
    bComplex: if set to False, function will read real-valued data
    """

    import struct
    import logging

    BytesPerValue = __NumberOfBytes(__DataTypeStr2Int(DataType))

    try:
        file = open(FileName, "rb")
        data = file.read()
        file.close
        ReadSamples = len(data) // BytesPerValue
    except:
        logging.error("File open error (" + FileName+")!")

    if __DataTypeStr2Int(DataType) == 1:
        # float 32
        data = list(struct.unpack("f"*ReadSamples, data))
    elif __DataTypeStr2Int(DataType) == 2:
        # float64
        data = list(struct.unpack("d"*ReadSamples, data))
    elif __DataTypeStr2Int(DataType) == 3:
        # int8
        data = list(struct.unpack("b"*ReadSamples, data))
    elif __DataTypeStr2Int(DataType) == 4:
        # int16
        data = list(struct.unpack("h"*ReadSamples, data))
    elif __DataTypeStr2Int(DataType) == 5:
        # int32
        data = list(struct.unpack("i"*ReadSamples, data))

    if bComplex:
        if iqiq:
            data = Iqiq2Complex(data)
        else:
            data = Iiqq2Complex(data)

    return data



def WriteBin( iqData, fSamplingRate, FileName):
    """Writes a bin file, e.g. for use on KS generators
    iqData can be a list of complex or list of floats (iqiqiq format mandatory).
    writtenSamples = WriteBin("MyFile.bin",complexList, fs)
    Note: Max power is "1", i.e. I^2+Q^2<=1
    """

    import struct
    from datetime import date
    import math
    import logging

    # check if iqData is complex
    if isinstance(iqData[0], complex):
        iqData = Complex2Iqiq( iqData)

    NumberOfSamples = len(iqData) // 2

    # Find maximum magnitude and scale for max to be FullScale (1.0)
    power = []
    for n in range(NumberOfSamples):
        power.append(abs(iqData[2*n]**2 + iqData[2*n+1]**2))
    scaling = math.sqrt( max(power))

    # normalize to magnitude 1
    iqData = [ iq / scaling for iq in iqData]

    # calculate rms in dB (below full scale)
    rms = math.sqrt(sum(power)/NumberOfSamples)/scaling
    rms = abs(20*math.log10( rms))
    # Convert to int16, use floor function, otherwise distribution is not correct
    iqData = [ math.floor(iq * 32767 + .5) for iq in iqData]

    try:
        file = open( FileName, "wb")

        # binary block, big endian
        for nIdx in range(len(iqData)):
            file.write( struct.pack(">h", iqData[nIdx]))

        file.close()
    except:
        logging.error("File (" + FileName + ") write error!" )

    return NumberOfSamples



def WriteWv( iqData, fSamplingRate, FileName):
    """Writes a WV file.
    iqData can be a list of complex or list of floats (iqiqiq format mandatory).
    writtenSamples = WriteWv("MyFile.wv",complexList, fs)"""

    import struct
    from datetime import date
    import math
    import logging

    # check if iqData is complex
    if isinstance( iqData[0], complex):
        iqData = Complex2Iqiq( iqData)

    NumberOfSamples = len(iqData) // 2

    # Find maximum magnitude and scale for max to be FullScale (1.0)
    power = []
    for n in range(NumberOfSamples):
        power.append(abs(iqData[2*n]**2 + iqData[2*n+1]**2))
    scaling = math.sqrt(max(power))

    # normalize to magnitude 1
    iqData = [iq / scaling for iq in iqData]

    # calculate rms in dB (below full scale)
    rms = math.sqrt(sum(power)/NumberOfSamples)/scaling
    rms = abs(20*math.log10( rms))
    # Convert to int16, use floor function, otherwise distribution is not correct
    iqData = [ math.floor(iq * 32767 +.5) for iq in iqData]
        
    try:
        file = open( FileName, "wb")

        file.write( "{TYPE: SMU-WV,0}".encode("ASCII"))
        file.write( "{COMMENT: R&S WaveForm, TheAE-RA}".encode("ASCII"))
        file.write( ("{DATE: " + str(date.today())+ "}").encode("ASCII"))
        file.write( ("{CLOCK:" +str(fSamplingRate) + "}").encode("ASCII"))
        file.write( ("{LEVEL OFFS:" +  "{:2.4f}".format(rms) + ",0}").encode("ASCII"))
        file.write( ("{SAMPLES:" + str(NumberOfSamples) + "}").encode("ASCII"))
    #TODO: markers
    #     if( m1start > 0 && m1stop > 0)
    #        %Control Length only needed for markers
    #        fprintf(file_id,'%s',['{CONTROL LENGTH:' num2str(data_length) '}']);
    #        fprintf(file_id,'%s',['{CLOCK MARKER:' num2str(fSamplingRate) '}']);
    #        fprintf(file_id,'%s',['{MARKER LIST 1: ' num2str(m1start) ':1;' num2str(m1stop) ':0}']);
    #    end
        file.write( ("{WAVEFORM-" +  str(4*NumberOfSamples+1) + ": #").encode("ASCII"))

        # binary block
        file.write( struct.pack("h"*len(iqData),*iqData))
        
        file.write( "}".encode("ASCII"))

        file.close()
    except:
        logging.error("File (" + FileName +") write error!" )
        
    return NumberOfSamples



def ReadWv( FileName, ReadData=True, ConvertData=True):
    """Reads a WV file. Returns a list with complex numbers (I/Q) and the sampling rate
    iqiqiqList,fs = ReadWv("MyFile.wv")
    ReadData:       if set to False, we'll only return the parameters from the header
    ConvertData:    convert to complex floating point, otherwise keep original format"""

    import re
    import struct
    import logging

    try:
        file = open(FileName, "rb")
        if(ReadData):
            data = file.read()
        else:
            data = file.read( 30000)     # for the header, 30 kB should be sufficient
        file.close()
    except:
        logging.error( "File open error ("+ FileName+")!")
        return

    binaryStart = 0
    tags = ""
    Counter = 0
    ConverterSize = 20
    while (binaryStart == 0) & (Counter < len(data)):
        tags += data[Counter:Counter+ConverterSize].decode("ASCII", "ignore")
        Counter += ConverterSize
        #{WAVEFORM-20001: #
        res = re.search("WAVEFORM.{0,20}:.{0,3}#", tags)
        if res is not None:
            binaryStart = res.span()[1]

    if (Counter > len(data)) & (binaryStart == 0):
        logging.warning("Required tags not found, potentially incompatible file format!")

    res = re.search("SAMPLES[ ]*:[ ]*(?P<NumberOfSamples>[0-9]*)[ ]*}", tags)
    if res:
        NumberOfSamples = int(res.group("NumberOfSamples"))
    else:
        NumberOfSamples = np.nan
    # res = re.search("CLOCK[ ]*:[ ]*(?P<SamplingRate>[0-9]*.[0-9]*[eE]?[+\-]?[0-9]*)",tags)
    res = re.search("CLOCK[ ]*:[ ]*(?P<SamplingRate>[0-9]*.[0-9]*[eE]?[+\-]?[0-9]*)[ ]*}", tags)
    if res:
        SamplingRate = float(res.group("SamplingRate"))
    else:
        SamplingRate = np.nan
    res = re.search("LEVEL OFFS[ ]*:[ ]*(?P<RMSLevelOffset>[0-9]*.?[0-9]*),", tags)
    if res:
        RmsLevelOffset = float(res.group("RMSLevelOffset"))
    else:
        RmsLevelOffset = np.nan
    res = re.search("Signal generated for SMx RMS level[ ]*:[ ]*(?P<RfRmsLevel>-?[0-9]*.?[0-9]*)[ ]*", tags)
    if res:
        RfRmsLevel = float(res.group("RfRmsLevel"))
    else:
        RfRmsLevel = np.nan

    if ReadData and ConvertData:
        data = list(struct.unpack("h"*NumberOfSamples*2, data[binaryStart:binaryStart+NumberOfSamples*4]))
        data = list(map( lambda x: x/32767.0, data))
        data = Iqiq2Complex(data)
    else:
        data = data[binaryStart:]

    if ReadData:
        return data, SamplingRate
    else:
        return SamplingRate, NumberOfSamples, RmsLevelOffset, RfRmsLevel


def __WriteXml(fs, NumberOfSamples, filenameiqw, filenamexml, fCenterFrequency=0, DataType="float32", ScalingFactor=1):
    """Function to write the xml part of the iq.tar
    __WriteXml( samplingrate, numberofsamples, filenameiqw, filenamexml)
    DataType (supported): float32, float64
    ScalingFactor: scaling factor in Volts
    """

    from datetime import datetime

    xmlfile = open(filenamexml, "w")

    xmlfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    xmlfile.write("<?xml-stylesheet type=\"text/xsl\" href=\"open_IqTar_xml_file_in_web_browser.xslt\"?>\n")
    xmlfile.write("<RS_IQ_TAR_FileFormat fileFormatVersion=\"2\" xsi:noNamespaceSchemaLocation=\"http://www.rohde-schwarz.com/file/RsIqTar.xsd\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n")
    # Optional
    xmlfile.write("<Name>Python iq.tar Writer (iqdata.py)</Name>\n")
    # Optional
    xmlfile.write("<Comment>RS WaveForm, TheAE-RA</Comment>\n")
    xmlfile.write("<DateTime>"+ datetime.now(None).isoformat() + "</DateTime>\n")
    xmlfile.write("<Samples>" + str(NumberOfSamples) + "</Samples>\n")
    xmlfile.write("<Clock unit=\"Hz\">" + str(fs) + "</Clock>\n")
    xmlfile.write("<Format>complex</Format>\n")
    xmlfile.write(f"<DataType>{__DataTypeInt2Str(__DataTypeStr2Int(DataType))}</DataType>\n")
    # Optional
    xmlfile.write(f"<ScalingFactor unit=\"V\">{ScalingFactor}</ScalingFactor>\n")
    # Optional
    # xmlfile.write("<NumberOfChannels>1</NumberOfChannels>\n")
    xmlfile.write("<DataFilename>" + filenameiqw + "</DataFilename>\n")
    # Optional
    if fCenterFrequency != 0:
        xmlfile.write( f'<UserData><RohdeSchwarz><SpectrumAnalyzer><CenterFrequency unit="Hz">{fCenterFrequency}</CenterFrequency></SpectrumAnalyzer></RohdeSchwarz></UserData>\n')

    xmlfile.write("</RS_IQ_TAR_FileFormat>\n")
    xmlfile.close()

    return



def WriteIqTar(iqData, fs, FileName, fCenterFrequency=0, DataType="float32"):
    """Writes an iq.tar file. Complex iqData values are interpreted as Volts.
    iqData can be a list of complex or list of floats (iqiqiq format).
    writtenSamples = WriteIqTar(iqList,fs,"MyFile.iq.tar")
    DataType (supported): float32, float64
    """

    import tarfile
    import os
    import re
    import logging

    ScalingFactor = 1
    path, filename = os.path.split(FileName)
    # Create binary file
    binaryfile = re.sub("iq.tar", f"complex.1ch.{__DataTypeInt2Str(__DataTypeStr2Int(DataType))}", filename, flags=re.IGNORECASE)
    NumberOfSamples, ScalingFactor = WriteIqw(iqData, os.path.join(path, binaryfile), DataType=DataType)
    if NumberOfSamples == 0:
        return 0

    # xsltfilename = "open_IqTar_xml_file_in_web_browser.xslt"
    xmlfilename = re.sub("iq.tar", "xml", filename, flags=re.IGNORECASE)
    __WriteXml(fs, NumberOfSamples, binaryfile, os.path.join(path, xmlfilename), fCenterFrequency=fCenterFrequency, DataType=DataType, ScalingFactor=ScalingFactor)

    try:
        tar = tarfile.open(FileName, "w")
        tar.add(os.path.join(path, binaryfile), arcname=binaryfile)
        # xslt is optional
        # tar.add( os.path.join(path, xsltfilename), arcname=xsltfilename)
        tar.add(os.path.join(path, xmlfilename), arcname=xmlfilename)
        tar.close()
        os.remove(os.path.join(path, binaryfile))
        os.remove(os.path.join(path, xmlfilename))
    except:
        logging.error("IqTar (" + FileName +") write error!" )

    return NumberOfSamples



def ReadIqTar(FileName, ChannelToRead=1):
    """Reads an iq.tar file. 
    data,fs = ReadIqTar("MyFile.iq.tar", ChannelToRead = 1)
    ChannelToRead specifies the channel to be read. "0" reads all channels and returns a matrix.
    """

    import tarfile
    import os
    import xml.etree.ElementTree as ET
    import logging

    data = []
    fs = 0

    try:
        tar = tarfile.open(FileName, "r:")
        a = tar.getnames()
        xmlfile = [filename for filename in a if ".xml" in filename.lower()]
        xmlfile = xmlfile[0]
        tar.extract(xmlfile)
        tree = ET.parse(xmlfile)
        root = tree.getroot()
        binaryfilename = root.find("DataFilename").text
        fs = float(root.find("Clock").text)
        logging.debug(f'Using clock rate: {fs} Hz')

        helper = root.find("DataType")
        DataType = __DataTypeInt2Str(__DataTypeStr2Int(helper.text))
        logging.debug(f'Using data type: {DataType}')

        helper = root.find("Samples")
        NumberOfSamples = 1
        if helper.text:
            NumberOfSamples = int(root.find("Samples").text)
        logging.debug(f'Using number of samples: {NumberOfSamples}')

        helper = root.find("Format")
        bComplex = 1
        if helper.text:
            if helper.text.lower().find('real') >= 0:
                bComplex = 0
        logging.debug(f'Using complex: {bComplex}')

        helper = root.find("ScalingFactor")
        ScalingFactor = 1
        if helper.text:
            if helper.get("unit") != "V":
                logging.warn("Only (V)olts scaling factor supported - assuming 1V!")
            else:
                ScalingFactor = float(root.find("ScalingFactor").text)
        logging.debug(f'Using scaling factor: {ScalingFactor} V')

        helper = root.find("NumberOfChannels")
        NumberOfChannels = 1
        if helper is not None:
            if helper.text:
                NumberOfChannels = int(root.find("NumberOfChannels").text)
        logging.debug(f'Using Number of channels: {NumberOfChannelss}')

        os.remove(xmlfile)
        del root
        tar.extract(binaryfilename)
        tar.close()
        data = ReadIqw(binaryfilename, DataType=DataType, bComplex=bComplex)
        os.remove(binaryfilename)

    except:
        logging.error("IqTar (" + FileName + ") read error!")

    # Apply scaling factor
    if ScalingFactor != 1:
        data = [sample * ScalingFactor for sample in data]

    # separate channels
    if NumberOfChannels > 1:

        if (ChannelToRead > NumberOfChannels):
            logging.warn("File " + FileName + " only contains " + str(NumberOfChannels) + " channels, using channel 1!")
            ChannelToRead = 1
        if ChannelToRead > 0:
            data1 = []
            # for n in range(NumberOfSamples):
            # data1.append( data[n*NumberOfChannels+ChannelToRead-1])
            data1 = data[ChannelToRead-1::NumberOfChannels]
        else:
            import numpy
            data1 = numpy.empty((NumberOfSamples, NumberOfChannels), dtype=complex)
            for n in range(NumberOfSamples):
                for m in range(NumberOfChannels):
                    if m==0:
                        data1[n][m] = data[n*NumberOfChannels+m]
        data = data1

    return data, fs



def Iqw2Iqtar(FileName, fs, keepIqw=False, fCenterFrequency=0, DataType="float32"):
    """Converts an iqw file into iq.tar. Suggested to use after directly reading
    binary data from instrument into file (iqw).
    Note: iqw must be in iqiqiq format
    iqtarFilename = WriteIqTar(iqList,fs,"MyFile.iq.tar")"""

    import os
    import tarfile
    import re
    import logging

    NumberOfSamples = 0

    if os.path.isfile( FileName):
        NumberOfSamples = os.stat( FileName).st_size // 8
    else:
        logging.error("File " + FileName+" does not exist!")

    path, filename = os.path.split(FileName)
    iqtarfile = re.sub("iqw", "iq.tar", filename, flags=re.IGNORECASE)
    xmlfile = re.sub("iqw", "xml", filename, flags=re.IGNORECASE)
    binaryfile = re.sub("iqw", f"complex.1ch.{__DataTypeInt2Str(__DataTypeStr2Int(DataType))}", filename, flags=re.IGNORECASE)
    os.rename(FileName, os.path.join(path, binaryfile))

    __WriteXml(fs, NumberOfSamples, binaryfile, os.path.join(path, xmlfile), fCenterFrequency=fCenterFrequency, DataType=DataType)

    try:
        tar = tarfile.open( os.path.join(path, iqtarfile), "w")
        tar.add(os.path.join(path, binaryfile), arcname=binaryfile)
        # xslt is optional
        # tar.add( os.path.join(path, xsltfilename), arcname=xsltfilename)
        tar.add(os.path.join(path, xmlfile), arcname=xmlfile)
        tar.close()
        if not keepIqw:
            os.remove(os.path.join(path, binaryfile))
        else:
            os.rename(os.path.join(path, binaryfile), FileName)
        os.remove(os.path.join(path, xmlfile))
    except:
        logging.error("IqTar (" + FileName + ") write error!")

    return os.path.join(path, iqtarfile)



def Iqw2Wv(FileName, fs, keepIqw=False):
    """Converts an iqw file into wv. Suggested to use after directly reading
    binary data from instrument into file (iqw).
    Note: iqw must be in iqiqiq format
    writtenSamples = WriteIqTar(iqList,fs,"MyFile.iq.tar")"""

    import os
    import re
    import logging
    import numpy
    import math
    import struct
    from datetime import date

    NumberOfSamples = 0
    BytesPerValue = 4
    BlockSize = 10000

    if os.path.isfile(FileName):
        NumberOfSamples = os.stat(FileName).st_size // (BytesPerValue * 2)
    else:
        logging.error("File " + FileName+" does not exist!")

    #path,filename = os.path.split(FileName)
    wvfile = re.sub("iqw", "wv", FileName, flags=re.IGNORECASE)

    rmsvalue = 0
    maxvalue = 0

    # first run throug iqw to determine rms and peak level  
    try:
        file = open( FileName, "rb")
        ReadCounter = 0
        while ReadCounter < NumberOfSamples:
            data = file.read(2*BytesPerValue*BlockSize)
            ReadSamples = len(data) // BytesPerValue
            ReadCounter += ReadSamples / 2
            data = list(struct.unpack("f"*ReadSamples, data))
            data = Iqiq2Complex(data)
            data = numpy.abs(data)
            rmsvalue += numpy.sum(numpy.power(numpy.abs(data), 2))
            maxofvector = numpy.amax(data)
            maxvalue = max(maxofvector, maxvalue)
        file.close
        rmsvalue = numpy.sqrt(rmsvalue/NumberOfSamples)
    except:
        logging.error( "File open error (" + FileName+")!")

    scaling = maxvalue
    maxvalue = 20*numpy.log10(maxvalue/scaling)
    rmsvalue = 20*numpy.log10(rmsvalue/scaling)

    # now we convert the data
    try:
        fileout = open(wvfile, "wb")     
        file = open(FileName, "rb")

        # header
        fileout.write("{TYPE: SMU-WV,0}".encode("ASCII"))
        fileout.write("{COMMENT: R&S WaveForm, TheAE-RA}".encode("ASCII"))
        fileout.write(("{DATE: " + str(date.today())+ "}").encode("ASCII"))
        fileout.write(("{CLOCK:" + str(fs) + "}").encode("ASCII"))
        fileout.write(("{LEVEL OFFS:" + "{:2.4f}".format(-1*rmsvalue) + "," + "{:2.4f}".format(maxvalue) + "}").encode("ASCII"))
        fileout.write(("{SAMPLES:" + str(NumberOfSamples) + "}").encode("ASCII"))
        fileout.write(("{WAVEFORM-" + str(4*NumberOfSamples+1) + ": #").encode("ASCII"))

        # now copy data from iqw to wv
        ReadCounter = 0
        while ReadCounter < NumberOfSamples:
            data = file.read(2*BytesPerValue*BlockSize)
            ReadSamples = len(data) // BytesPerValue
            ReadCounter += ReadSamples / 2
            data = list(struct.unpack("f"*ReadSamples, data))
            data = data / scaling
            # Convert to int16, use floor function, otherwise distribution is not correct
            data = [math.floor(iq * 32767 + .5) for iq in data]
            fileout.write(struct.pack("h"*len(data),*data))

        fileout.write("}".encode("ASCII"))
        fileout.close()
        file.close()

        # remove iqw
        os.remove(FileName)
    except:
        logging.error("File (" + FileName + ") write error!")    



if __name__ == "__main__":
    # execute only if run as a script
    pass
