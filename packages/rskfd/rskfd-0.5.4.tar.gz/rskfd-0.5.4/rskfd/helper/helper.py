# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 2020

(C) 2020, Florian Ramian
"""

from enum import Enum 
class unit(Enum):
    volt    = 1
    dBm     = 2
    watt    = 3



def ShowLogFFT( data, fs = 1, MaxFftLength = 10000, bPlotRelative = True):
    """Helper function showing the magnitude of the FFT on a logarithmic scale.
    Signal length is limited to MaxFftLength to speed up FFT calculation.
    Input data is interpreted as Volts and converted to dBm."""

    # currently disabled
    # pass

    import matplotlib.pyplot as plt
    import numpy
    limiterlen = min(MaxFftLength,len(data))

    plt.ion()
    plt.show()

    if bPlotRelative:
        mag = 20*numpy.log10(numpy.abs(numpy.fft.fftshift(numpy.fft.fft(data[:limiterlen]))))
        # normalize to mean
        meanmag = 10*numpy.log10( numpy.mean( numpy.power( 10, mag/10)))
        mag = mag - meanmag
    else:
        mag = 10*numpy.log10(numpy.power( numpy.abs( numpy.fft.fftshift( numpy.fft.fft( data[:limiterlen]))), 2)/50/limiterlen)+30

    freq = numpy.multiply(range(-(limiterlen//2), (limiterlen+1)//2), fs/limiterlen)
    plt.plot(freq,mag)
    plt.grid( True)
    plt.xlabel( 'freq / Hz')
    if bPlotRelative:
        plt.ylabel( 'relative power / dB')
    else:
        plt.ylabel( 'power / dBm')
    plt.draw()
    plt.pause(.001)



def ConvertUnit( data, inUnit=unit.volt, outUnit=unit.dBm, impedance = 50):
    """
    ConverUnit converts a vector or scalar from an input unit to an output unit using the given impedance.
    data:       input vector or scalar; values can be complex for volts
    inUnit:     input unit, default Volts
    outUnit:    output unit, default dBm
    impedance:  impedance for conversion from power to amplitude, default 50 Ohms
    """
    
    # Not the fastest implementation, but easiest:
    # convert all input to volts, then to target unit
    import numpy
    
    if( inUnit == unit.watt):
        data = numpy.sqrt(data*impedance)
    elif( inUnit == unit.dBm):
        data = numpy.sqrt( numpy.power( 10, data/10) / 1000 * impedance)

    # here we have volts

    if( outUnit == unit.dBm):
        data = 10 * numpy.log10( numpy.power( numpy.abs( data), 2) / impedance) + 30
    elif( outUnit == unit.watt):
        data = numpy.power( numpy.abs( data), 2) / impedance

    return data



def Scale2dBm( vfcIqData, fTargetRMSPower):
    '''
    Scales an input data vector to a target mean power
    vfcIqData:          input vector, any unit
    fTargetRMSPower:    target RMS power
    
    Output vector will be in Volts over 50 Ohms
    '''
    import numpy
        
    fInputPower = MeanPower( vfcIqData)
    vfcIqData = numpy.multiply( vfcIqData, 10**((fTargetRMSPower-fInputPower)/20))

    return vfcIqData



def MeanPower( data, inUnit=unit.volt, outUnit=unit.dBm, impedance = 50):
    """
    MeanPower calculates the mean power of an input vector
    data:       input vector
    inUnit:     input unit, default Volts
    outUnit:    output unit, default dBm
    impedance:  impedance for conversion from power to amplitude, default 50 Ohms
    """

    import numpy

    data = ConvertUnit( data, inUnit=inUnit, outUnit=unit.volt, impedance=impedance)

    # formula calculates mean power from volts to dBm
    power = numpy.log10( numpy.mean( numpy.power( numpy.abs(data), 2) / impedance)) * 10 +30

    power = ConvertUnit( power, inUnit=inUnit.dBm, outUnit=outUnit, impedance=impedance)
    
    return power



def MaxPower( data, inUnit=unit.volt, outUnit=unit.dBm, impedance = 50):
    """
    MaxPower returns the max power of an input vector
    data:       input vector
    inUnit:     input unit, default Volts
    outUnit:    output unit, default dBm
    impedance:  impedance for conversion from power to amplitude, default 50 Ohms
    """

    import numpy

    data = ConvertUnit( data, inUnit=inUnit, outUnit=unit.volt, impedance=impedance)

    # formula calculates mean power from volts to dBm
    power = numpy.log10( numpy.power( max( numpy.abs( data)), 2) / impedance) * 10 +30

    power = ConvertUnit( power, inUnit=inUnit.dBm, outUnit=outUnit, impedance=impedance)
    
    return power



if __name__ == "__main__":
    # execute only if run as a script
    pass
