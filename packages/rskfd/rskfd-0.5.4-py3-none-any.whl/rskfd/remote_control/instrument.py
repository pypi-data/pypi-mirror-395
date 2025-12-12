# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 15:02:17 2019

@authors: RAMIAN, TIPTON
"""

from enum import Enum
import math
import socket
import logging
import struct
import timeit
import time
import numpy as np

logger = logging.getLogger('rskfd.instrument')
logger.addHandler(logging.NullHandler())


class instrument(object):
    '''
    Python class implementing a raw socket connection client,
    mainly designed around instrument control
    '''

    __ipaddress = ""
    __port = 5025
    __sendcls = True
    __msocket = None
    __timeout = 2
    __LogReadings = True
    __TimeStamp = False
    # It's recommended to use a power of 2 for BufferSize
    _InBufferSize = 4 * 2**10   # 4kByte
    __IDString = ""
    __Options = None

    class SyncMethod(Enum):
        '''
        enum class supporting different sync methods
        '''
        OpcQuery = 0
        Blocking = 1
        StbPoll = 2

    @staticmethod
    def GetNumberOfDigits(number):
        '''
        count number of digits
        '''

        if number < 0:
            number *= -1
        if number == 0:
            return 1

        return math.ceil(math.log10( number))

    def __init__(self, IpAddress, port=5025, timeout=2, sendcls=True):
        '''
        init method;
            IP Address is required
            port            : port to communicate with
            timeout         : timeout value
            sendcls         : clear error queue before communicating to instrument
        '''
        self.__ipaddress = IpAddress
        self.__port = port
        self.__timeout = timeout
        self.__sendcls = sendcls

    def __del__(self):
        if self.__msocket:
            self.__msocket.close()

    def __QueryID(self):
        self.Write("*IDN?")
        self.__IDString = self.Read()

    def GetID(self):
        '''
        return the instrument's ID string
        '''
        if self.__IDString == '':
            self.__QueryID()
        return self.__IDString

    def __QueryOpt(self):
        self.Write("*OPT?")
        self.__Options = self.Read().split(",")
        self.__Options.remove("")

    def GetOpt(self):
        '''
        return the instrument's option string
        '''
        if self.__Options is None:
            self.__QueryOpt()
        return self.__Options

    def IsLocalHost(self):
        '''
        Return boolean true when instrument runs on localhost (e.g. VSE)
        '''
        if self.__ipaddress.lower().find('localhost') >= 0 | self.__ipaddress.lower().find('127.0.0.1'):
            # missing check for same IP address
            return True
        else:
            return False

    def SetTimeout(self, timeout):
        '''
        Set the timeout for the connection (non blocking socket).
        For a blocking socket, use 'None'
        '''
        self.__timeout = timeout
        try:
            self.__msocket.settimeout( self.__timeout)
        except:
            pass

    def SetBufferSize(self, buffersize):
        '''
        Set the input buffer size for the connection.
        Returns rounded or clipped buffersize.
        '''
        if buffersize < 1:
            buffersize = 1
        if buffersize > 10e6:
            buffersize = 10e6
        buffersize = round(buffersize)
        self._InBufferSize = buffersize

        return buffersize

    def GetTimeout(self):
        '''
        Returns the specified timeout, 'None' meaning blocking socket
        '''
        return self.__msocket.gettimeout()

    def Synchronize(self, method=SyncMethod.StbPoll, timeout=None):
        '''Function to synchronize with instruments.
        Input:
        SyncMethod:
            SyncMethod.OpcQUery:    Use *OPC? to synchronize, i.e. a blocking query
            SyncMethod.Blocking:    Use *WAI to synchronize, i.e. block execution of next command until finished, no query
            SyncMethod.StbPoll:     Poll *ESR? until bit 0 is set, i.e. non blocking query
        timeout:    Timeout value, before function returns with timeout error

        Output:
        SyncOk: returns 1 when sync was successful, or 0 on timeout
        '''

        SyncOk = 0

        # Save current timeout and set user timeout
        if timeout is None:
            timeoutstorage = self.__timeout
            self.SetTimeout(timeout)
        else:
            timeout = self.GetTimeout()

        # OPC Query Sync mode
        if method == self.SyncMethod.OpcQuery:
            self.Write('*OPC?')
            try:
                value = int(self.Read())
                if value == 1:
                    SyncOk = 1
            except socket.timeout:
                pass

        # *WAI blocking mode
        if method == self.SyncMethod.Blocking:
            self.Write('*WAI')

        # *ESR? polling mode
        if method == self.SyncMethod.StbPoll:
            self.Write('*OPC')
            start = timeit.default_timer()
            while (not SyncOk and ((timeit.default_timer()-start) <= self.__timeout) ):
                SyncOk = int(self.Query('*ESR?')) & 1
                # sleep for 2 ms, so we don't poll too often
                time.sleep(.002)

        # Restore timeout
        if timeout != self.__timeout:
            self.SetTimeout(timeoutstorage)

        return SyncOk

    def Connect(self, getID=True, getOptions=False, Preset=False):
        '''
        Connects to the specified instrument and opens the connection
        '''

        try:
            self.__msocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
            self.__msocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.__msocket.connect( (self.__ipaddress, self.__port))
            self.__msocket.settimeout(self.__timeout)
            if Preset:
                self.Query('*RST;*OPC?')
            # Clear Error Queue
            if self.__sendcls:
                self.Write('*CLS')
            if getID:
                self.__QueryID()
            if getOptions:
                self.__QueryOpt()
        except ConnectionRefusedError:
            return -1
        except TimeoutError:
            return -1

        return 0

    def Close(self):
        '''
        Closes the connection
        '''

        self.CloseSocket()
        return

    def StartLogging(self, LogReadings=True):
        '''
        Start logging into FileName
        ClearFile deletes file, if set to True
        '''
        self.__LogReadings = LogReadings

    def UserCommentToLogFile(self, comment):
        '''
        Write a user comment to the log file
        '''
        comment = 'USERCOMMENT: ' + comment
        logger.info(comment)

    def ___LogToFile(self, Command):
        logger.info(Command)

    def Write(self, Command, Binary=False, AddTermination=True):
        '''
        Write a command; termination character (\n) automatically added
        '''

        if self.__msocket is None:
            raise Exception('Connection is closed, use connect first!')

        self.___LogToFile(Command)
        if AddTermination:
            if Command.endswith("\n") is False:
                Command = Command + "\n"
        if Binary:
            self.__msocket.sendall(Command)
        else:
            self.__msocket.sendall(Command.encode('ASCII'))

    def Read(self, decode=True, NumberOfBytes=-1, TerminationCharacter='\n'):
        '''
        Read back from the connected instrument
        '''

        if self.__msocket is None:
            raise Exception('Connection is closed, use connect first!')

        if NumberOfBytes == -1:
            NumberOfBytes = self._InBufferSize

        try:
            BytesRead = 0
            TerminationRead = False
            while BytesRead < NumberOfBytes and not TerminationRead:
                data = self.__msocket.recv(NumberOfBytes)
                BytesRead = len(data)
                if data.endswith(bytes(TerminationCharacter, 'utf-8')):
                    TerminationRead = True
        except:
            message = "Timeout while reading data!"
            if self.__LogReadings:
                self.___LogToFile(message)
            else:
                logging.warn(message)
            return None

        if decode:
            try:
                data = data.decode("ASCII")
                if TerminationRead:
                    data = data[:-1]
            except:
                message = "Binary data received!"
                if self.__LogReadings:
                    self.___LogToFile(message)
                else:
                    logging.warn(message)
                data = str(len(data)) + " binary bytes"

            if self.__LogReadings:
                self.___LogToFile(data)
        else:
            if self.__LogReadings:
                self.___LogToFile("{} bytes of binary data read".format(len(data))) 

        return data

    def Query(self, Command):
        """Write command and read result from connected instrument"""

        self.Write(Command)
        data = self.Read()

        return data

    def CloseSocket(self):
        """Close the connection"""
        self.__msocket.close()
        self.__IDString = ""
        self.__Options = []

    def OpenSocket( self):
        """Open the connection"""
        try:
            self.__msocket.connect((instrument.__ipaddress, instrument.__port))
            self.__msocket.settimeout(self.__timeout)
        except ConnectionRefusedError:
            pass

    def GetSystErr(self):
        """Return system error as (integer,string)"""
        self.Write("SYST:ERR?")
        result = self.Read()
        retlist = result.split(",")

        return int(retlist[0]), retlist[1]

    def UseNaN(self, vfcData):
        """Replace the SCPI representation of NaN (9.91*10^37) by NaN"""

        return [np.nan if x > 9.909e37 else x for x in vfcData]

    def ReadBinary(self, BytesPerValue=4, IqRead=False, NaNCheck=False, ReturnSamples=True):
        """Binary read of multiple values from the instrument, e.g. trace or I/Q data
        Input Values:
            BytesPerValue:  specifies the number of bytes that form a float; in format REAL,32 this is 4
            IqRead:         if set to true, complex I/Q pairs are returned; works only if instrument returns samples in iqiq order
            NaNCheck:       if set to true, the SCPI representation of NaN is replaced by Python's NaN
            ReturnSamples:  only set to false for interface tests; if set to false, function will only read back bytes and dump them

        Output Values:
            data vector when ReturnSamples is true
            byte counter when ReturnSamples is false
            """

        digits = self.Read(NumberOfBytes=2)

        if digits[1] == "(":
            # in this case we have more than 10 digits for the number of bytes enclosed by "(" and ")"
            digits += self.Read(NumberOfBytes=11)
            while digits[-1] != ")":
                digits += self.Read(NumberOfBytes=1)
            NumberOfBytesToRead = int(digits[2:-1])
        else:
            digits = int(digits[1])
            NumberOfBytesToRead = int(self.Read(NumberOfBytes=digits))

        if ReturnSamples:
            # This is the real code to read out samples
            NumericData = []
            oldData = b""

            ReadCounter = 0
            while ReadCounter <= NumberOfBytesToRead:   # we need to also read the closing character
                RawData = self.Read(decode=False)
                ReadCounter += len(RawData)
                RawData = oldData + RawData
                ReadSamples = len(RawData) // BytesPerValue
                if BytesPerValue == 4:
                    NumericData.extend(list(struct.unpack("f"*ReadSamples, RawData[0:ReadSamples*BytesPerValue])))
                elif BytesPerValue == 8:
                    NumericData.extend(list(struct.unpack("d"*ReadSamples, RawData[0:ReadSamples*BytesPerValue])))
                else:
                    logging.error("Format currently not supported!")
                oldData = RawData[ReadSamples*BytesPerValue:]

            if NaNCheck:
                NumericData = self.UseNaN( NumericData)

            if IqRead:
                from rskfd import Iqiq2Complex
                NumericData = Iqiq2Complex( NumericData)

            return NumericData
        else:
            # Binary Read and Dump results section; only a byte counter is returned; transfer speed check only
            ReadCounter = 0
            while ReadCounter <= NumberOfBytesToRead:   #we need to also read the closing character
                RawData = self.Read( decode=False)
                ReadCounter += len(RawData)

            return ReadCounter

    def ReadBinaryToFile(self, FileName):
        """Binary read of multiple values from the instrument directly into an iqw file.
        This function assumes 4 byte floating point format, usually commanded by
        FORM REAL,32"""

        digits = self.Read(NumberOfBytes=2)

        if digits[1] == "(":
            # in this case we have more than 10 digits for the number of bytes enclosed by "(" and ")"
            digits += self.Read(NumberOfBytes=11)
            while digits[-1] != ")":
                digits += self.Read(NumberOfBytes=1)
            NumberOfBytesToRead = int(digits[2:-1])
        else:
            digits = int(digits[1])
            NumberOfBytesToRead = int(self.Read(NumberOfBytes=digits))

        file = open(FileName, "wb")

        ReadCounter = 0
        while ReadCounter <= NumberOfBytesToRead:   # we need to also read the closing character
            RawData = self.Read(decode=False)
            ReadCounter += len(RawData)
            if ReadCounter <= NumberOfBytesToRead:
                file.write(RawData)
            else:
                file.write(RawData[:(NumberOfBytesToRead-ReadCounter)])

        file.close()

    def Reset(self):
        """Reset on the connection, includes sending an ABORt, a *CLS
        Close and Reconnect."""
        self.Write("ABORt;*CLS")
        self.CloseSocket()
        self.Connect()

    def EmptyBuffer(self):
        """Empty raw socket buffer. Work around needed if program terminated during raw socket transfer."""

        actualtimeout = self.GetTimeout()
        self.SetTimeout(.1)
        try:
            while self.Read(decode=False, NumberOfBytes=1000):
                pass
        except:
            pass
        self.SetTimeout(actualtimeout)


if __name__ == "__main__":
    # execute only if run as a script
    fsw = instrument('localhost', port=5026, sendcls=False)
    fsw.Connect()
    fsw.Query('*IDN?')
    fsw.Close()
    # pass   
