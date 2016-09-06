import unittest
from spcxbutcher import perchannelfilter

class FakeEvent:
    def __init__( self, channel, timestamp ):
        self.channel = channel
        self.timestamp = timestamp

class DropSpecificTimestamp:
    def __init__( self, toDrop ):
        self.toDrop = toDrop
        self.calledWith = []

    def __call__( self, record ):
        self.calledWith.append( ( record.channel, record.timestamp ) )
        return record.timestamp != self.toDrop

class PerChannelFilter( unittest.TestCase ):
    def test_applies_filter_to_records_separated_by_channel( self ):
        EVENTS = [ (3, 10), (1, 20), (1, 30), (2, 40), (2, 50), (1, 60), (1, 70), (3, 80) ]
        records = [ FakeEvent( channel, timestamp ) for ( channel, timestamp ) in EVENTS ]

        drop20 = DropSpecificTimestamp( 20 )
        drop40 = DropSpecificTimestamp( 40 )
        drop100 = DropSpecificTimestamp( 100 )
        tested = perchannelfilter.PerChannelFilter( { 1: drop20, 2: drop40, 3: drop100 } )

        filtered = filter( tested, records )
        results = [ ( record.channel, record.timestamp ) for record in filtered ]
        self.assertEqual( [ (3, 10), (1, 30), (2, 50), (1, 60), (1, 70), (3, 80) ], results )
        self.assertEqual( [ (1, 20), (1, 30), (1, 60), (1, 70) ], drop20.calledWith )
        self.assertEqual( [ (2, 40), (2, 50) ], drop40.calledWith )
        self.assertEqual( [ (3, 10), (3, 80) ], drop100.calledWith )
