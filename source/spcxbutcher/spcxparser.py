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

    def _parseSPC( self, spcUnitCount ):
        try:
            spc = spcxbutcher.spc.SPC( spcUnitCount, self._file )
            self._spcs.append( spc )
        except spcxbutcher.spc.NoMoreSPCs:
            self._done = True

    def __len__( self ):
        return len( self._spcs )


    def __iter__( self ):
        return iter( self._spcs )
