import logging

class HighTime:
    def __init__( self ):
        self._hightime = 0
        self._changed = False

    def inspect( self, rawData ):
        self._changed = False
        if self._change( rawData ):
            self._changed = True
            self._update( rawData )

    @property
    def value( self ):
        return self._hightime

    def changed( self ):
        return self._changed

    def _change( self, rawData ):
        mark = rawData & 0xc0000000
        return mark == 0x40000000

    def _update( self, rawData ):
        newHightime = self._extractHightime( rawData )
        if ( newHightime - self._hightime ) != ( 1 << 24 ):
            logging.warning( 'high timestamp bits changed more than expected! from {:08x} to {:08x}'.format( self._hightime, newHightime ) )
        self._hightime = newHightime

    def _extractHightime( self, rawData ):
        hightimeBits = 0x3fffffff & rawData
        return hightimeBits << 24
