import struct
import logging

UNIT_SIZE = 4
UNIT_FORMAT = '<L'
assert struct.calcsize( UNIT_FORMAT ) == UNIT_SIZE

class _NoMoreSPCs( Exception ): pass

class InvalidDescriptor( Exception ):
    pass

class InvalidEventRecord( Exception ):
    pass

class SPC:
    def __init__( self, unitCount, file ):
        self._hightime = 0
        content = file.read( UNIT_SIZE * unitCount )
        self._iterator = struct.iter_unpack( UNIT_FORMAT, content )
        self._parse()

    def _parse( self ):
        descriptor = self._readDescriptor()
        self._validate( descriptor )
        self._parseDescriptor( descriptor )
        self._skipGarbageEvent()
        self._parseEvents()

    def _readDescriptor( self ):
        try:
            descriptor, = next( self._iterator )
            return descriptor
        except StopIteration:
            raise _NoMoreSPCs()

    def _validate( self, descriptor ):
        bit = {}
        for position in [ 24, 25, 27 ]:
            value = ( 1 << position ) & descriptor
            bit[ position ] = value >> position

        high4bits = 0xf0000000 & descriptor
        valid = high4bits == 0xc0000000\
                and bit[ 24 ] == 1 \
                and bit[ 25 ] == 0 \
                and bit[ 27 ] == 0

        if not valid:
            raise InvalidDescriptor( 'Invalid descriptor {:08x}'.format( descriptor ) )

    def _parseDescriptor( self, descriptor ):
        highestByte = descriptor >> 24
        self._raw = ( highestByte & 0b00000100 ) >> 2
        self._timePerBin = descriptor & 0x00ffffff

    def _skipGarbageEvent( self ):
        next( self._iterator )

    def _parseEvents( self ):
        self._events = []
        for event, in self._iterator:
            self._verifyEventRecordHeader( event )
            if self._hightimeChange( event ):
                newHightime = self._extractHightime( event )
                if ( newHightime - self._hightime ) != ( 1 << 24 ):
                    logging.warning( 'high timestamp bits changed more than expected! from {} to {}'.format( self._hightime, newHightime ) )
                self._hightime = newHightime
                continue
            timestamp = event & 0x00ffffff
            channel = ( event >> 24 ) & 0b00011111
            gap = event >> 29
            self._events.append( ( channel, self._hightime + timestamp, gap ) )

    def _verifyEventRecordHeader( self, event ):
        highestTwoBits = ( event & 0xc0000000 ) >> 30
        if highestTwoBits not in [ 0b00, 0b01 ]:
            raise InvalidEventRecord( 'invalid event record: {:08x}'.format( event ) )

    def _hightimeChange( self, event ):
        mark = event & 0xc0000000
        return mark == 0x40000000

    def _extractHightime( self, event ):
        hightimeBits = 0x3fffffff & event
        return hightimeBits << 24

    @property
    def raw( self ):
        return self._raw

    @property
    def timePerBin( self ):
        return self._timePerBin

    @property
    def events( self ):
        return self._events

def fromFile( unitCount, file ):
    try:
        return SPC( unitCount, file )
    except _NoMoreSPCs:
        return None
