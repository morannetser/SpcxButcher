import struct

UNIT_SIZE = 4
UNIT_FORMAT = '<L'
assert struct.calcsize( UNIT_FORMAT ) == UNIT_SIZE

class _FileOver( Exception ): pass

class SPC:
    def __init__( self, unitCount, file ):
        content = file.read( UNIT_SIZE * unitCount )
        self._iterator = struct.iter_unpack( UNIT_FORMAT, content )
        self._parse()

    def _parse( self ):
        descriptor = self._readDescriptor()
        self._parseDescriptor( descriptor )
        self._skipGarbageEvent()
        self._parseEvents()

    def _readDescriptor( self ):
        try:
            descriptor, = next( self._iterator )
            return descriptor
        except StopIteration:
            raise _FileOver()

    def _parseDescriptor( self, descriptor ):
        highestByte = descriptor >> 24
        self._raw = ( highestByte & 0b00000100 ) >> 2
        self._timePerBin = descriptor & 0x00ffffff

    def _skipGarbageEvent( self ):
        next( self._iterator )

    def _parseEvents( self ):
        self._events = []
        for eventTuple in self._iterator:
            event = eventTuple[ 0 ]
            timestamp = event & 0x00ffffff
            channel = ( event >> 24 ) & 0b00011111
            self._events.append( ( channel, timestamp ) )

    @property
    def raw( self ):
        return self._raw

    @property
    def timePerBin( self ):
        return self._timePerBin

    @property
    def events( self ):
        return self._events

class SPCXParser:
    def __init__( self, filename ):
        self._file = open( filename, 'rb' )
        self._done = False
        self._spcs = []
        self._parse()

    def _parse( self ):
        while not self._done:
            spcUnitCount, = struct.unpack( '<L', self._file.read( UNIT_SIZE ) )
            self._parseSPC( spcUnitCount )

    def _parseSPC( self, spcUnitCount ):
        try:
            spc = SPC( spcUnitCount, self._file )
            self._spcs.append( spc )
        except _FileOver:
            self._done = True

    def __len__( self ):
        return len( self._spcs )


    def __iter__( self ):
        return iter( self._spcs )
