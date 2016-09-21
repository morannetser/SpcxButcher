import logging
import json
import argparse
import spcxbutcher.spcxparser
import sys

def eventTuple( event ):
    return event.gap, event.channel, event.timestamp

def spcDictionary( spc ):
    return { 'raw': spc.raw,
                'timePerBin': spc.timePerBin,
                'events': [ eventTuple( event ) for event in spc ] }


parser = argparse.ArgumentParser()
parser.add_argument( 'spcxfile' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

parsed = spcxbutcher.spcxparser.SPCXParser( arguments.spcxfile )
spcs = [ spcDictionary( spc ) for spc in parsed ]

json.dump( spcs, sys.stdout )
