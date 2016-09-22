import struct
import spcxbutcher.spc
import logging

class SPCXParser:
    def __init__( self, filename ):
        self._file = open( filename, 'rb' )
        self._done = False
        self._count = 0

    def _parse( self ):
        while not self._done:
            unit = self._file.read( spcxbutcher.spc.UNIT_SIZE )
            spcUnitCount, = struct.unpack( '<L', unit )
            spc = self._parseSPC( spcUnitCount )
            if spc is None:
                continue
            yield spc

        self._verifySPCNumber( spcUnitCount )

    def _parseSPC( self, spcUnitCount ):
        spc = spcxbutcher.spc.fromFile( spcUnitCount, self._file )
        if spc is None:
            self._done = True
            return
        self._count += 1
        return spc

    def _verifySPCNumber( self, lastUnitRead ):
        expectedSPCNumber = lastUnitRead
        if expectedSPCNumber != self._count:
            raise Exception( "expected {} SPCs but found {}".format( expectedSPCNumber, self._count ) )

    def __iter__( self ):
        return self._parse()
