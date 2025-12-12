# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 2021

(C) 2021, Rohde&Schwarz, ramian
"""

def ConvertSparams( s, inputformat = "ri", outputformat = "ri"):
### Helper function to convert s parameters from one format into another. Supported formats for inputformat and outputformat are:
    #           dbmag:  magnitude in dB/phase in degrees
    #           ri:     real / imaginary
    #           mag:    linear magnitude / degrees
###
    import numpy
    import logging

    if inputformat.lower().find( "ri")>=0:
        informat = 1
    elif inputformat.lower().find( "dbmag")>=0:
        informat = 2
    elif inputformat.lower().find( "mag")>=0:
        informat = 3
    else:
        logging.error( "Input format not supported!")
        return

    if outputformat.lower().find( "ri")>=0:
        outformat = 1
    elif outputformat.lower().find( "dbmag")>=0:
        outformat = 2
    elif outputformat.lower().find( "mag")>=0:
        outformat = 3
    else:
        logging.error( "Output format not supported!")
        return

    outvector = []
    try:
        vectorlength = len( s)
    except:
        vectorlength = 1
    for m in range( vectorlength):
        if numpy.isscalar( s):
            allsparams = s
        else:
            allsparams = s[m]

        outvectorentry = []
        try:
            numparamstowrite = len( s[0])
        except:
            numparamstowrite = 1

        for n in range( numparamstowrite):
            if numpy.isscalar( allsparams):
                sparam = allsparams
            else:
                sparam = allsparams[n]

            # Convert to RI first
            if informat == 1:
                helper = sparam
            elif informat == 2:
                helper = numpy.power( 10, numpy.real( sparam)/20) * numpy.exp( 1j * numpy.imag(sparam)/180*numpy.pi)
            else:
                helper = numpy.real( sparam) * numpy.exp( 1j * numpy.imag(sparam)/180*numpy.pi)

            # Convert to RI first
            if outformat == 1:
                sparam = helper
            elif outformat == 2:
                sparam = complex( 20 * numpy.log10( numpy.abs( helper)), numpy.angle( helper, deg=True))
            else:
                sparam = complex( numpy.abs( helper), numpy.angle( helper, deg=True))
            

            # make sure we always return a list of lists
            # if numpy.isscalar( sparam) and numparamstowrite == 1:
            #     outvectorentry = sparam       
            # else:
            outvectorentry.append( sparam)      

        if vectorlength > 1:
            outvector.append( outvectorentry)
        else:
            outvector = outvectorentry


    return outvector


def ReadSnP( filename, outputformat = "ri"):
    ### Read in a Touchstone file and return a S-parameter matrix (over frequency) as well as a frequency vector.
    #       outputformat:    format of output list <s>
    #           dbmag:  magnitude in dB/phase in degrees
    #           ri:     real / imaginary
    #           mag:    linear magnitude / degrees
    ###
    import logging
    import re
    import numpy

    s =  []
    f = []

    numparamstoread = 0
    if filename.lower().find(".s1p") >=0 or filename.lower().find(".fres") >=0:
        numparamstoread = 1
    elif filename.lower().find(".s2p") >=0:
        numparamstoread = 4
    elif filename.lower().find(".s3p") >=0:
        numparamstoread = 9
    elif filename.lower().find(".s4p") >=0:
        numparamstoread = 16
    else:
        logging.error( "Format not supported!")
        return

    searchstring = r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"

    file = open( filename)

    importstyle = "ri"
    freqscaling = 1

    while True:
        inline = file.readline()
        if not inline:
            break
        
        if inline[0] == "!" or inline[0] == "#":
            if re.search( '[ ,\t]+RI[ ,\t]+', inline):
                importstyle = "ri"
            elif re.search( '[ ,\t]+DB[ ,\t]+', inline):
                importstyle = "dbmag"
            elif re.search( '[ ,\t]+MA[ ,\t]+', inline):
                importstyle = "mag"
            elif re.search( '[ ,\t]+HZ[ ,\t]+', inline):
                freqscaling = 1
            elif re.search( '[ ,\t]+KHZ[ ,\t]+', inline):
                freqscaling = 1e3
            elif re.search( '[ ,\t]+MHZ[ ,\t]+', inline):
                freqscaling = 1e6
            continue
        else:
            myvalues = [float(numbers) for numbers in re.findall(searchstring, inline)]

            if len(myvalues) != numparamstoread*2+1:
                #error
                logging.error( "Read error!")
                break
            else:
                f.append( myvalues[0] * freqscaling)
                # 1 sparameter ==> list of complex floats, otherwise list of lists
                if numparamstoread == 1:
                    helper = ConvertSparams( complex( myvalues[1], myvalues[2]), inputformat=importstyle)
                    if numpy.isscalar( helper) == False:
                        helper = helper[0]
                    s.append( helper)
                else:
                    sparamtupel = []
                    for n in range(numparamstoread):
                        helper = ConvertSparams( complex( myvalues[2*n+1], myvalues[2*n+2]), inputformat=importstyle)
                        if numpy.isscalar( helper) == False:
                            helper = helper[0]
                        sparamtupel.append( helper)
                    s.append( sparamtupel)
    

    file.close()

    return s,f


def WriteSnP( s, f, filename, inputformat = "ri", outputformat = "ri"):
    ### Write a Tocuhstone file, which contains frequency points of input vector f, and s-parameters contained in s:
    #       s:  list of n-tupels, where n is 1 for s1p or fres formats, and 4 for s2p
    #       f:  list of frequencies
    #       filename:   full filename
    #       inputformat:    format of input list <s>
    #       outputformat:   format in SnP file
    #           dbmag:  magnitude in dB/phase in degrees
    #           ri:     real / imaginary
    #           mag:    magnitude linear / degrees
    ###

    import logging
    import datetime
    import numpy
    import re

    #outputformat = "ri

    s = ConvertSparams( s, inputformat=inputformat, outputformat=outputformat) 

    file = open( filename, "w")

    if outputformat.lower().find("ri") >=0:
        file.write( "#  HZ   S   RI   R     50.00\n")
    elif outputformat.lower().find("dbmag") >=0:
        file.write( "#  HZ   S   DB   R     50.00\n")
    else:
        file.write( "#  HZ   S   MA   R     50.00\n")

    now = datetime.datetime.now()

    file.write( "! rskfd SnP writer tool\n")
    file.write( "! Date: " +  now.strftime("%Y-%m-%d %H:%M:%S") + "\n")

    try:
        numparamstowrite = len( s[0])
    except:
        numparamstowrite = 1


    #fileformats
    #   1: s2p
    #   2: fres
    #   0: s1p

    if filename.lower().find( ".s2p") >=0:
        fileformat = 1
    elif filename.lower().find( ".fres") >=0:
        fileformat = 2
    elif filename.lower().find( ".s1p") >=0:
        fileformat = 0
    else:
        logging.error( "File type not supported!")
        return

    if fileformat == 1:
        if numparamstowrite == 1:
            file.write( "! Measurements: (S11)    S21     (S12)   (S22)\n")
        else:
            file.write( "! Measurements:  S11     S21     S12     S22\n")

    elif fileformat == 2:
        file.write( "! Measurements: S21\n")
    else:
        file.write( "! Measurements: S11\n")
    file.write( "!\n")

    for x in range( len( f)):
        if fileformat == 1:
            if numparamstowrite == 1:
                file.write( "{:f}   0   0   {:f}    {:f}    0   0   0   0\n".format( f[x], numpy.real(s[x][0]), numpy.imag(s[x][0])))
            else:
                file.write( "{:f}   {:f}    {:f}    {:f}    {:f}    {:f}    {:f}    {:f}    {:f}\n".format( f[x], numpy.real(s[x][0]), numpy.imag(s[x][0]), numpy.real(s[x][1]), numpy.imag(s[x][1]), numpy.real(s[x][2]), numpy.imag(s[x][2]), numpy.real(s[x][3]), numpy.imag(s[x][3])))
        else:
            file.write( "{:f}   {:f}    {:f}\n".format( f[x], numpy.real(s[x][0]), numpy.imag(s[x][0])))

    file.close()



if __name__ == "__main__":
	# pass

    # Test Section
    import numpy
    import rskfd

    filename = "myfile"
    extension = ".fres"

    # Create test file
    n= 101
    if extension.lower().find( ".s2p")>=0:
        numparams = 4
    else:
        numparams = 1
    f = numpy.linspace( 1e7, 1e10, num = n)
    #s = numpy.random.rand( n) +1j* numpy.random.rand( n)
    s = 2* ((numpy.random.rand( n, numparams)-.5) + 1j*2*( numpy.random.rand( n, numparams)-.5))
    rskfd.WriteSnP( s, f, filename + "-ri-backup" + extension, inputformat="ri")
    
    # Test conversion
    s,f = rskfd.ReadSnP( filename + "-ri-backup" + extension)
    rskfd.WriteSnP( s, f, filename + "-dbmag" + extension, inputformat="ri", outputformat="dbmag")
    s,f = rskfd.ReadSnP( filename + "-dbmag" + extension)
    rskfd.WriteSnP( s, f, filename + "-mag" + extension, inputformat="ri", outputformat="mag")
    s,f = rskfd.ReadSnP( filename + "-mag" + extension)
    rskfd.WriteSnP( s, f, filename + extension, inputformat="ri")
