# -*- coding: utf-8 -*-
'''
Created on Thu Mar 21 15:04:00 2019

@author: RAMIAN
'''


import os
from functools import partial
from rskfd import instrument


class instrumentRS(instrument):
    '''
    Python class implementing functionality for Rohde & Schwarz instruments.
    It is based on the instrument class for socket connectivity.
    '''


    def FileDownload( self, remoteFile, localFile):
        '''
        Download file from the instrument to the local file
        '''
        self.Write(f'MMEM:DATA? "{remoteFile}"' )
        self.ReadBinaryToFile(localFile)


    def FileUpload( self, localFile, remoteFile):
        '''
        Upload a file to the instrument
        '''

        if os.path.isfile( localFile) == 0:
            raise Exception('File '+localFile+' does not exist')

        statinfo = os.stat(localFile)
        self.Write('MMEM:DATA "' + remoteFile + '",#' + str(instrument.GetNumberOfDigits(statinfo.st_size)) + str(statinfo.st_size), AddTermination = False )

        file = open( localFile, 'rb')
        for chunk in iter(partial(file.read, self._InBufferSize), b''):
            self.Write( chunk, Binary = True, AddTermination = False)
        file.close()
        self.Write('\n')


if __name__ == '__main__':
    # execute only if run as a script
    pass
