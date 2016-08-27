import logging
import argparse
import spcxbutcher.spcxparser

def printSPC( spc ):
    print( '=== SPC ===' )
    print( 'events: {}'.format( len( spc.events ) ) )
    print( 'raw: {}'.format( spc.raw ) )
    print( 'timePerBin: {}'.format( spc.timePerBin ) )
    print( "channel\ttimestamp" )
    for channel, timestamp in spc.events:
        print( '{}\t{:x}'.format( channel, timestamp ) )


parser = argparse.ArgumentParser()
parser.add_argument( 'spcxfile' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

parsed = spcxbutcher.spcxparser.SPCXParser( arguments.spcxfile )
print( '{} SPCs'.format( len( parsed ) ) )
for spc in parsed:
    printSPC( spc )
