import logging
import argparse
import struct

parser = argparse.ArgumentParser()
parser.add_argument( 'inputFile' )
parser.add_argument( 'outputFile' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

output = open( arguments.outputFile, 'wb' )

content = open( arguments.inputFile, 'rb' ).read()
spcs, = struct.unpack( '<L', content[ -4: ] )
logging.info( 'expecting {} spcs'.format( spcs ) )

def readSPC( content, unitsToRead ):
    units, = struct.unpack_from( '<L', content )
    UNIT_SIZE = 4
    SPC_COUNT = 1
    remainder = content[ (units + SPC_COUNT) * UNIT_SIZE: ]
    firstSPCUnits = content[ UNIT_SIZE : UNIT_SIZE * (unitsToRead + 1) ]
    fakeBytes = struct.pack( '<L', unitsToRead ) + firstSPCUnits
    return fakeBytes, remainder

remainder = content
TOTAL_SPCS = 3
for counter in range( TOTAL_SPCS ):
    logging.info( 'reading {}'.format( counter ) )
    fakeBytes, remainder = readSPC( remainder, counter + 3 )
    output.write( fakeBytes )

output.write( struct.pack( '<L', TOTAL_SPCS ) )
