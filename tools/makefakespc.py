import logging
import struct

logging.basicConfig( level = logging.DEBUG )

output = open( 'out.spcx', 'wb' )

content = open( 'example.spcx', 'rb' ).read()
spcs, = struct.unpack( '<L', content[ -4: ] )
logging.info( 'expecting {} spcs'.format( spcs ) )

def readSPC( content, unitsToRead ):
    units, = struct.unpack_from( '<L', content )
    UNIT_SIZE = 4
    FIRST_UNIT = 1
    remainder = content[ (units + FIRST_UNIT) * UNIT_SIZE: ]
    firstUnits = content[ UNIT_SIZE : UNIT_SIZE * (unitsToRead + 1) ]
    fakeBytes = struct.pack( '<L', unitsToRead ) + firstUnits
    return fakeBytes, remainder

remainder = content
TOTAL_SPCS = 3
for counter in range( TOTAL_SPCS ):
    logging.info( 'reading {}'.format( counter ) )
    fakeBytes, remainder = readSPC( remainder, counter + 3 )
    output.write( fakeBytes )

output.write( struct.pack( '<L', TOTAL_SPCS ) )
