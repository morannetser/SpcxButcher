import logging
import argparse
import spcxbutcher.spcxparser
import spcxbutcher.deadtimefilter
import spcxbutcher.perchannelfilter

parser = argparse.ArgumentParser()
parser.add_argument( 'spcxfile' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

spcx = spcxbutcher.spcxparser.SPCXParser( arguments.spcxfile )

for spc in spcx:
    filters = {}
    for i in range( 1, 11 ):
        filters[ i ] = spcxbutcher.deadtimefilter.DeadtimeFilter( i * spc.timePerBin )

    perChannelFilter = spcxbutcher.perchannelfilter.PerChannelFilter( filters )
    for event in filter( perChannelFilter, spc ):
        print( '{}\t{}\t{}'.format( event.lvttl, event.timestamp, event.gap ) )
