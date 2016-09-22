import struct
import logging
from spcxbutcher import descriptor
from spcxbutcher import event
from spcxbutcher import hightime

UNIT_SIZE = 4
UNIT_FORMAT = '<L'
assert struct.calcsize( UNIT_FORMAT ) == UNIT_SIZE

class NoMoreSPCs( Exception ): pass

class SPC:
    def __init__( self, unitCount, file ):
        self._hightime = hightime.HighTime()
        content = file.read( UNIT_SIZE * unitCount )
        self._iterator = struct.iter_unpack( UNIT_FORMAT, content )
        self._parseDescriptor()
        self._skipGarbageEvent()

    def _parseDescriptor( self ):
        try:
            rawData, = next( self._iterator )
            self._descriptor = descriptor.Descriptor( rawData )
        except StopIteration:
            raise NoMoreSPCs()

    def _skipGarbageEvent( self ):
        next( self._iterator )

    def _parseEvents( self ):
        for rawData, in self._iterator:
            event.Event.verifyEventRecordHeader( rawData )
            self._hightime.inspect( rawData )
            if self._hightime.changed():
                continue
            yield event.Event( rawData, self._hightime.value )

    @property
    def raw( self ):
        return self._descriptor.raw

    @property
    def timePerBin( self ):
        return self._descriptor.timePerBin

    def __iter__( self ):
        return self._parseEvents()

def fromFile( unitCount, file ):
    try:
        return SPC( unitCount, file )
    except NoMoreSPCs:
        return None
