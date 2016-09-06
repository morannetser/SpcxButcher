import unittest
from spcxbutcher import deadtimefilter

class FakeEvent:
    def __init__( self, timestamp ):
        self.timestamp = timestamp

class DeadtimeFilterTest( unittest.TestCase ):
    def test_records_should_be_at_least_deadtime_apart( self ):
        records = [ FakeEvent( timestamp ) for timestamp in [ 1, 3, 5, 8, 9, 10, 20, 22, 25, 40, 41, 42] ]
        filter5 = deadtimefilter.DeadtimeFilter( 5 )
        self.assertEqual( [ 1, 8, 20, 40 ], [ record.timestamp for record in filter( filter5, records ) ] )

        filter3 = deadtimefilter.DeadtimeFilter( 3 )
        self.assertEqual( [ 1, 5, 9, 20, 25, 40 ], [ record.timestamp for record in filter( filter3, records ) ] )

        filter0 = deadtimefilter.DeadtimeFilter( 0 )
        self.assertEqual( [ 1, 3, 5, 8, 9, 10, 20, 22, 25, 40, 41, 42], [ record.timestamp for record in filter( filter0, records ) ] )

        INFINITY = 1e100
        filterInfinity = deadtimefilter.DeadtimeFilter( INFINITY )
        self.assertEqual( [1,], [ record.timestamp for record in filter( filterInfinity, records ) ] )
