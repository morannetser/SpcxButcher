import struct
import logging
from spcxbutcher import descriptor

UNIT_SIZE = 4
UNIT_FORMAT = '<L'
assert struct.calcsize( UNIT_FORMAT ) == UNIT_SIZE

class _NoMoreSPCs( Exception ): pass

class InvalidEventRecord( Exception ):
    pass

class SPC:
    def __init__( self, unitCount, file ):
        self._hightime = 0
        content = file.read( UNIT_SIZE * unitCount )
        self._iterator = struct.iter_unpack( UNIT_FORMAT, content )
        self._parse()

    def _parse( self ):
        try:
            rawData, = next( self._iterator )
            self._descriptor = descriptor.Descriptor( rawData )
        except StopIteration:
            raise _NoMoreSPCs()
        self._skipGarbageEvent()
        self._parseEvents()

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
            lvttl = self._lvttl( event )
            gap = event >> 29
            self._events.append( ( lvttl, self._hightime + timestamp, gap ) )

    def _lvttl( self, event ):
        channel = ( event >> 24 ) & 0b00011111
        if channel < 3 or channel > 14:
            raise Exception( "unexpected channel value: {}".format( channel ) )
        if channel <= 10:
            return channel - 2
        else:
            return channel - 4

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
        return self._descriptor.raw

    @property
    def timePerBin( self ):
        return self._descriptor.timePerBin

    @property
    def events( self ):
        return self._events

def fromFile( unitCount, file ):
    try:
        return SPC( unitCount, file )
    except _NoMoreSPCs:
        return None
