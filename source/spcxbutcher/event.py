import logging

class InvalidEventRecord( Exception ):
    pass

class Event:
    _hightime = 0

    def __init__( self, rawData ):
        self._verifyEventRecordHeader( rawData )
        if self._hightimeChange( rawData ):
            self.type = 'high time change'
            self._updateHightime( rawData )
            return
        self.type = 'event'
        timestamp = rawData & 0x00ffffff
        self.lvttl = self._lvttl( rawData )
        self.gap = rawData >> 29
        self.timestamp = self._hightime + timestamp

    def __repr__( self ):
        return str( ( self.lvttl, self.timestamp, self.gap ) )

    def _hightimeChange( self, rawData ):
        mark = rawData & 0xc0000000
        return mark == 0x40000000

    def _verifyEventRecordHeader( self, rawData ):
        highestTwoBits = ( rawData & 0xc0000000 ) >> 30
        if highestTwoBits not in [ 0b00, 0b01 ]:
            raise InvalidEventRecord( 'invalid rawData record: {:08x}'.format( rawData ) )

    @classmethod
    def _updateHightime( cls, rawData ):
        newHightime = cls._extractHightime( rawData )
        if ( newHightime - cls._hightime ) != ( 1 << 24 ):
            logging.warning( 'high timestamp bits changed more than expected! from {:08x} to {:08x}'.format( cls._hightime, newHightime ) )
        cls._hightime = newHightime

    @classmethod
    def _extractHightime( cls, rawData ):
        hightimeBits = 0x3fffffff & rawData
        return hightimeBits << 24

    @classmethod
    def resetHightime( cls ):
        cls._hightime = 0

    @property
    def channel( self ):
        return self.lvttl

    def _lvttl( self, event ):
        channel = ( event >> 24 ) & 0b00011111
        if channel < 3 or channel > 14:
            raise Exception( "unexpected channel value: {}".format( channel ) )
        if channel <= 10:
            return channel - 2
        else:
            return channel - 4

    def __eq__( self, _tuple ):
        return ( self.lvttl, self.timestamp, self.gap ) == _tuple
