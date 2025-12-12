# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 2020

(C) 2020, Florian Ramian
"""


def CreateWGNSignal( NoisePower=-40, RecordLength=4096, BandLimit=1.0 ):
    # function returns white Gaussian noise baseband signal
    #  (Gaussian on I and Gaussian on Q, Rayleigh distributed on magnitude)
    # NoisePower:   mean power in dBm
    # RecordLength: Record length in samples
    # BandLimit: limit noise power to BandLimit relative to sampling rate; .8 is a good choice when signal shall be replayed on a generator
    # returns the noise vector (scaled in Volts)

    import numpy
    import logging

    # dBm to Volts^2, 10^(np/10)/1000*50; divided by 2, because of I and Q
    std_dev = numpy.sqrt( numpy.power( 10, NoisePower/10)/40)
    data_real = numpy.random.normal( 0, std_dev, RecordLength)
    data_imag = numpy.random.normal( 0, std_dev, RecordLength)
    data = data_real + 1j * data_imag

    if BandLimit < 1:
        data = LowPassFilter( data, BandLimit)
    
    logging.info( "WGN vector length: "+str(RecordLength)+"; power: "+str(numpy.log10(numpy.mean(numpy.square(numpy.abs(data)))/50)*10+30)+" dBm")
    
    return data

def LowPassFilter( inData, RelativeBandwidth=.8, FilterTaps=100, KeepPower=False):
    # function applies a filter to inData with relative bandwidth
    # inData:               input data vector
    # RelativeBandwidth:    bandwidth of low pass ]0..1[
    # FilterTaps:           number of taps to be used for the filter
    # KeepPower:            if true, output signal is scaled so it has the same mean power as before
    # returns the filtered inData
    
    import numpy
    from scipy import signal
    import logging

    if( RelativeBandwidth<=0)&( RelativeBandwidth>=1):
        logging.error("Relative bandwidth must be >0 and <1!")
        return

    # filter noise, design filter first
    b = signal.firwin( FilterTaps, RelativeBandwidth)
    out = signal.filtfilt( b, 1, inData)

    if KeepPower:
        inpower = numpy.mean( numpy.power( numpy.abs(inData), 2))
        outpower = numpy.mean( numpy.power( numpy.abs(out), 2))
        out = out / outpower * inpower

    return out



if __name__ == "__main__":
    # execute only if run as a script
    pass