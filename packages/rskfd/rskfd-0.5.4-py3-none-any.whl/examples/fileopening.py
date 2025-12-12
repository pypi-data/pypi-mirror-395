# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 2021

(C) 2021, Rohde&Schwarz, ramian
"""

import rskfd

def ConvertIiQq2Wv():
    '''
    Test
    '''
    # there is no sampling rate in an iqw file
    fs = 320e6
    data = rskfd.ReadIqw( r'\\myserver\signal\higher_qams.iiqq', iqiq=False)
    rskfd.WriteWv( data, fs, r'\\myserver\signal\higher_qams.wv')
    rskfd.WriteBin( data, fs, r'\\myserver\signal\higher_qams.bin')
    rskfd.WriteIqTar( data, fs, r'\\myserver\signal\higher_qams.iq.tar')



def ReadFile( filename):
    '''
    Test
    '''
    data,fs = rskfd.ReadWv( filename)
    print( f'RMS power in file: {rskfd.MeanPower( data)} dBm, peak power: {rskfd.MeanPower( data)} dBm.\n')
    rskfd.WriteWv( data, fs, 'myfilename.wv')



def ReadWvTest():
    '''
    Test the wv reading routine (tags!!)
    '''
    iq, fs = rskfd.ReadWv(r'\\myserver\signal\higher_qams.wv')


def ReadIqTar64bitTest():
    '''
    Test the wv reading routine (tags!!)
    '''
    # iq,fs = rskfd.ReadIqTar(r'C:\Users\ramian\Documents\k18\testing\AmptoolsMeas.iq.tar')
    # iq = rskfd.ReadIqw(r'C:\Users\ramian\Downloads\iq_data.complex.float64', 'float64')
    iq1, fs = rskfd.ReadIqTar(r'C:\Users\ramian\Documents\wideband_vna\KeysightApproach\Testsignal\FileMay.iq.tar')

    rskfd.WriteIqTar(iq1, fs, 'float32test.iq.tar', DataType='float32')
    rskfd.WriteIqTar(iq1, fs, 'float64test.iq.tar', DataType='float64')
    rskfd.WriteIqTar(iq1, fs, 'int8.iq.tar', DataType='int8')
    rskfd.WriteIqTar(iq1, fs, 'int16.iq.tar', DataType='int16')
    rskfd.WriteIqTar(iq1, fs, 'int32.iq.tar', DataType='int32')
    iq2, fs2 = rskfd.ReadIqTar('float32test.iq.tar')
    iq3, fs3 = rskfd.ReadIqTar('float64test.iq.tar')
    iq4, fs4 = rskfd.ReadIqTar('int8.iq.tar')
    iq5, fs4 = rskfd.ReadIqTar('int16.iq.tar')
    iq6, fs4 = rskfd.ReadIqTar('int32.iq.tar')

    error1 = 0
    error2 = 0
    error3 = 0
    error4 = 0
    error5 = 0
    iqvectorlength = len(iq1)
    for n in range(iqvectorlength):
        error1 = error1 + abs(iq1[n] - iq2[n])
        error2 = error2 + abs(iq1[n] - iq3[n])
        error3 = error3 + abs(iq1[n] - iq4[n])
        error4 = error4 + abs(iq1[n] - iq5[n])
        error5 = error5 + abs(iq1[n] - iq6[n])

    error1 = error1 / iqvectorlength
    error2 = error2 / iqvectorlength
    error3 = error3 / iqvectorlength
    error4 = error4 / iqvectorlength
    error5 = error5 / iqvectorlength

    if error1 > 1e-20:
        print(f'float32 not ok (error {error1})!')

    if error2 > 1e-40:
        print(f'float64 not ok (error {error2})!')

    if error3 > 2/2**8:
        print(f'int8 not ok (error {error3})!')

    if error4 > 2/2**16:
        print(f'int16 not ok (error {error4})!')

    if error5 > 2/2**32:
        print(f'int32 not ok (error {error5})!')

    rskfd.ShowLogFFT(iq1)
    pass


if __name__ == "__main__":
	#pass
    #ReadWvTest()
    ReadIqTar64bitTest()
