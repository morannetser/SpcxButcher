import logging
import sys
import struct

logging.basicConfig( level = logging.DEBUG )

content = open( sys.argv[ 1 ], 'rb' ).read()
spcs, = struct.unpack( '<L', content[ -4: ] )
logging.info( 'expecting {} spcs'.format( spcs ) )

def readSPC( content ):
    logging.info( 'content is {} bytes'.format( len( content ) ) )
    units, = struct.unpack_from( '<L', content )
    logging.info( 'units = {}'.format( units ) )
    UNIT_SIZE = 4
    FIRST_UNIT = 1
    return content[ (units + FIRST_UNIT) * UNIT_SIZE: ]

remainder = content
for counter in range( spcs ):
    logging.info( 'reading {}'.format( counter ) )
    remainder = readSPC( remainder )


print( 'remainder is {} bytes long'.format( len( remainder ) ) )
