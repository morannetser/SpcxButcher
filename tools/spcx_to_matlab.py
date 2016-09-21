import logging
import time
import scipy.io
import argparse
import spcxbutcher.spcxparser

def eventTuple( event ):
    return event.gap, event.channel, event.timestamp

def spcDictionary( spc, index ):
    result = {  'spc_{}'.format(index): { 'raw': spc.raw,
                         'timePerBin': spc.timePerBin,
                         'events': [ eventTuple( event ) for event in spc ] } }
    return result

parser = argparse.ArgumentParser()
parser.add_argument( 'spcxfile' )
parser.add_argument( 'prefix' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

start = time.time()
parsed = spcxbutcher.spcxparser.SPCXParser( arguments.spcxfile )
for i, spc in enumerate( parsed ):
    outFile = '{}.{}.mat'.format( arguments.prefix, i )
    scipy.io.savemat( outFile, spcDictionary( spc, i ) )
    minutes = ( time.time() - start ) / 60.0
    rate = minutes / ( i + 1 )
    logging.info( 'time elapsed: {:3.2} minutes ({:3.2} min/spc)'.format( minutes, rate ) )
