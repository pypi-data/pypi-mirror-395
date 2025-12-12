# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 2020

(C) 2020, Florian Ramian
"""

# This is example code on how to use the instrument.py and derived classes

def exampleTestConnection( ipaddress):
    # use only the raw instrument.py interface and give all (SCPI) commands explicitly
    # this should work for all instruments supporting a raw socket interface
    # import instrument.py class
    import rskfd

    # now open connection, default port is 5025
    myinstrument = rskfd.instrument( ipaddress)
    myinstrument.Connect()

    # Write something "*IDN?"
    myinstrument.Write( "*IDN?")
    # Print whatever we read back
    print( myinstrument.Read())

    #Close connection
    myinstrument.CloseSocket()



def exampleFileDownload( ipaddress):
    # now we'll use instrumentRS class
    #import class

    import rskfd

    # now open connection, default port is 5025, same as above, but called now through instrumentRS
    myinstrument = rskfd.instrumentRS( ipaddress)
    myinstrument.Connect()

    # Write something "*IDN?", as above in example 1
    myinstrument.Write( "*IDN?")
    # Print whatever we read back
    print( myinstrument.Read())

    # by using instrumentRS - we get more functionality, e.g. FileDownload
    # uses raw string to avoid escaping, transfers a remote (win.ini) to a local file mytest.txt
    myinstrument.FileDownload( r"C:\Windows\win.ini", "mytest.txt")

    #Close connection
    myinstrument.CloseSocket()



def exampleCaptureIqData( ipaddress, CaptureLength=200000):
    # now we'll use instrumentRS.py
    #import class

    import rskfd

    # now open connection, default port is 5025, same as above, but called now through instrumentRS
    myinstrument = rskfd.instrumentRS( ipaddress)
    myinstrument.Connect()

    # Identify instrument
    print( myinstrument.Query( '*IDN?'))

    # now we'll set up a fill I/Q capture
    # Example would work on R&S signal and spectrum analyzers

    # Preset
    myinstrument.Write( '*RST')
    # open I/Q analyzer app
    myinstrument.Write( 'INST:SEL IQ')
    # single sweep mode
    myinstrument.Write( 'INIT:CONT OFF')
    # set frequency and reference level
    myinstrument.Write( 'FREQ:CENT 1.2e9')
    myinstrument.Write( 'DISP:WIND:TRAC:Y:RLEV 0')
    # set sampling rate and capture length
    fs = 10e6
    myinstrument.Write( 'TRAC:IQ:SRAT ' + str(fs))
    myinstrument.Write( 'TRAC:IQ:RLEN ' + str(CaptureLength))
    # now sweep and synchronize to end of sweep
    myinstrument.Write( 'INIT:IMM')
    myinstrument.Synchronize()
    # Read back iq vector, use binary transfer, IQ pairwise
    myinstrument.Write( 'FORM REAL,32;:TRAC:IQ:DATA:FORM IQP')
    myinstrument.Write( 'TRAC:IQ:DATA:MEM?')
    iq = myinstrument.ReadBinary()

    #Close connection
    myinstrument.CloseSocket()

    # iq vector is now 2xrecord length with I and Q pairwise
    # now we use iqdata module and convert it to a complex vector

    iq_complex = rskfd.Iqiq2Complex( iq)
    iq_complex.clear()

    # or we could write the data to an iq..pytar file (R&S analysis file format)
    rskfd.WriteIqTar( iq, fs, 'mytest.iq.tar' )



def exampleIqFileReadWrite():
    # this example generates a noise signal and saves/rereads it
    import rskfd
    import re
    from scipy import signal
    import numpy

    # create WGN signal with a mean power of -50 dBm
    noise = rskfd.CreateWGNSignal( -50)
    out = rskfd.LowPassFilter( noise, RelativeBandwidth=.8, FilterTaps=100, KeepPower=True)

    # create wv file, set sampling rate 125 MHz
    fs = 125e6
    filename = 'wgn_'+str(fs*.8/1e6)+'mhz'
    rskfd.WriteIqTar( out, fs, filename+'.iq.tar')

    # Read back wv and save it as iq.tar
    rereadnoise,rereadfs = rskfd.ReadIqTar( filename+'.iq.tar')
    # note that wv files are normalized to peak power, whereas iq.tar files are saved in Volts (typically)
    rskfd.WriteWv( rereadnoise, rereadfs, filename+'.wv')
    
    # plot noise
    rskfd.ShowLogFFT( noise, fs, bPlotRelative=False)
    rskfd.ShowLogFFT( out, fs, bPlotRelative=False)
    input( "Press return to finish!")


def exampleSpeedTest( ipaddress):
    # example that shows performance of I/Q data transfer
    
    import time
    import rskfd

    # use example3 to configure I/Q analyzer
    exampleCaptureIqData( ipaddress, CaptureLength=10e6)

    # now reopen connectio0
    myinstrument = rskfd.instrumentRS( ipaddress)
    myinstrument.Connect()

    # do a first measurement
    myinstrument.Write( 'TRAC:IQ:DATA?')
    iq = myinstrument.ReadBinary()

    meas_start = time.perf_counter()
    myinstrument.Write( 'TRAC:IQ:DATA?')
    iq = myinstrument.ReadBinary(IqRead=True)
    meastime = time.perf_counter() - meas_start
    print( "Single Meas & Read command (TRAC:IQ:DATA?)")
    print("Total: {} samples in {:2.2f} ms. Rate: {:2.2f} Mbit/s".format(len(iq),meastime*1e3,8*8*len(iq)/1e6/meastime))

    meas_start = time.perf_counter()
    myinstrument.Write( 'INIT:IMM;*WAI;:TRAC:IQ:DATA:MEM?')
    iq = myinstrument.ReadBinary(IqRead=True)
    meastime = time.perf_counter() - meas_start
    print( "Separate Meas & Read Commands (INIT:IMM;*WAI;:TRAC:IQ:DATA:MEM?)")
    print("Total: {} samples in {:2.2f} ms. Rate: {:2.2f} Mbit/s".format(len(iq),meastime*1e3,8*8*len(iq)/1e6/meastime))

    meas_start = time.perf_counter()
    myinstrument.Write( 'TRAC:IQ:DATA:MEM?')
    iq = myinstrument.ReadBinary(IqRead=True)
    meastime = time.perf_counter() - meas_start
    print( "Read only (TRAC:IQ:DATA:MEM?)")
    print("Total: {} samples in {:2.2f} ms. Rate: {:2.2f} Mbit/s".format(len(iq),meastime*1e3,8*8*len(iq)/1e6/meastime))

    # This code only transfers the bytes from instrument to PC - no conversion so it measures the interface speed
    meas_start = time.perf_counter()
    myinstrument.Write( 'TRAC:IQ:DATA:MEM?')
    samples = myinstrument.ReadBinary(ReturnSamples=False)
    meastime = time.perf_counter() - meas_start
    print( "Read only (TRAC:IQ:DATA:MEM?)")
    print("Total: {} bytes in {:2.2f} ms. Rate: {:2.2f} Mbit/s".format(samples,meastime*1e3,8*samples/1e6/meastime))

    myinstrument.CloseSocket()
   


def main():
    # Adapt ip address and uncomment the examples you want to run
    ipaddress = "10.99.2.11"
    # exampleTestConnection( ipaddress)
    # exampleFileDownload( ipaddress)
    # exampleCaptureIqData( ipaddress)
    # exampleIqFileReadWrite()
    exampleSpeedTest( ipaddress)


if __name__ == "__main__":
    main()