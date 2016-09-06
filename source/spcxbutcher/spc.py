import struct
import logging
from spcxbutcher import descriptor
from spcxbutcher import event

UNIT_SIZE = 4
UNIT_FORMAT = '<L'
assert struct.calcsize( UNIT_FORMAT ) == UNIT_SIZE

class _NoMoreSPCs( Exception ): pass

class SPC:
    def __init__( self, unitCount, file ):
        content = file.read( UNIT_SIZE * unitCount )
        self._iterator = struct.iter_unpack( UNIT_FORMAT, content )
        self._parse()

    def _parse( self ):
        self._parseDescriptor()
        self._skipGarbageEvent()
        self._parseEvents()

    def _parseDescriptor( self ):
        try:
            rawData, = next( self._iterator )
            self._descriptor = descriptor.Descriptor( rawData )
        except StopIteration:
            raise _NoMoreSPCs()

    def _skipGarbageEvent( self ):
        next( self._iterator )

    def _parseEvents( self ):
        self._events = []
        for rawData, in self._iterator:
            candidate = event.Event( rawData )
            if candidate.type != 'event':
                continue
            self._events.append( candidate )

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
