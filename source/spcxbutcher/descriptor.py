class InvalidDescriptor( Exception ):
    pass

class Descriptor:
    def __init__( self, rawData ):
        self._validate( rawData )
        self._parseDescriptor( rawData )

    def _validate( self, rawData ):
        bit = {}
        for position in [ 24, 25, 27 ]:
            value = ( 1 << position ) & rawData
            bit[ position ] = value >> position

        high4bits = 0xf0000000 & rawData
        valid = high4bits == 0xc0000000\
                and bit[ 24 ] == 1 \
                and bit[ 25 ] == 0 \
                and bit[ 27 ] == 0

        if not valid:
            raise InvalidDescriptor( 'Invalid descriptor {:08x}'.format( rawData ) )

    def _parseDescriptor( self, descriptor ):
        highestByte = descriptor >> 24
        self._raw = ( highestByte & 0b00000100 ) >> 2
        self._timePerBin = descriptor & 0x00ffffff

    @property
    def raw( self ):
        return self._raw

    @property
    def timePerBin( self ):
        return self._timePerBin
