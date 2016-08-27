import struct
import spcxbutcher.spc

class SPCXParser:
    def __init__( self, filename ):
        self._file = open( filename, 'rb' )
        self._done = False
        self._spcs = []
        self._parse()

    def _parse( self ):
        while not self._done:
            spcUnitCount, = struct.unpack( '<L', self._file.read( spcxbutcher.spc.UNIT_SIZE ) )
            self._parseSPC( spcUnitCount )

        self._verifySPCNumber( spcUnitCount )

    def _parseSPC( self, spcUnitCount ):
        spc = spcxbutcher.spc.fromFile( spcUnitCount, self._file )
        if spc is None:
            self._done = True
            return
        self._spcs.append( spc )

    def _verifySPCNumber( self, lastUnitRead ):
        expectedSPCNumber = lastUnitRead
        if expectedSPCNumber != len( self._spcs ):
            raise Exception( "expected {} SPCs but found {}".format( expectedSPCNumber, len( self._spcs ) ) )

    def __len__( self ):
        return len( self._spcs )


    def __iter__( self ):
        return iter( self._spcs )
