import logging
import argparse
import spcxbutcher.spcxparser
import spcxbutcher.deadtimefilter
import spcxbutcher.perchannelfilter

try:
    import scipy.io
except ImportError:
    logging.error( "this tools requires that you have `scipy' installed" )
    quit(1)

def eventTuple( event ):
    return event.gap, event.channel, event.timestamp

def spcDictionary( spc, index, perChannelFilter ):
    filtered = filter( perChannelFilter, spc )
    result = {  'spc_{}'.format(index): { 'raw': spc.raw,
                         'timePerBin': spc.timePerBin,
                         'events': [ eventTuple( event ) for event in filtered ] } }
    return result

def setupFiltering( spc ):
    for channel in range( 1, 11 ):
        filters[ channel ] = spcxbutcher.deadtimefilter.DeadtimeFilter( channel * spc.timePerBin )
    perChannelFilter = spcxbutcher.perchannelfilter.PerChannelFilter( filters )
    return perChannelFilter

parser = argparse.ArgumentParser()
parser.add_argument( 'spcxfile' )
parser.add_argument( 'outputPrefix' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

spcx = spcxbutcher.spcxparser.SPCXParser( arguments.spcxfile )

for i, spc in enumerate( spcx ):
    filters = {}

    perChannelFilter = setupFiltering( spc )

    outFile = '{}.{}.mat'.format( arguments.outputPrefix, i )
    logging.info( 'writing {}'.format( outFile ) )
    scipy.io.savemat( outFile, spcDictionary( spc, i, perChannelFilter ) )
