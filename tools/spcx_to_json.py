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

class JSONEncoder( json.JSONEncoder ):
    def default( self, thing ):
        if isinstance( thing, spcxbutcher.spcxparser.SPCXParser ):
            spcs = list( thing )
            return { "spcs": spcs }
        elif isinstance( thing, spcxbutcher.spc.SPC ):
            return spcDictionary( thing )

        return json.JSONEncoder.default( self, thing )

parser = argparse.ArgumentParser()
parser.add_argument( 'spcxfile' )
arguments = parser.parse_args()

logging.basicConfig( level = logging.DEBUG )

parsed = spcxbutcher.spcxparser.SPCXParser( arguments.spcxfile )
json.dump( parsed, sys.stdout, cls=JSONEncoder )
