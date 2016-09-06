import unittest
from spcxbutcher import deadtimefilter

class FakeEvent:
    def __init__( self, timestamp ):
        self.timestamp = timestamp

class DeadtimeFilterTest( unittest.TestCase ):
    def test_records_should_be_at_least_deadtime_apart( self ):
        records = [ FakeEvent( timestamp ) for timestamp in [ 1, 3, 5, 8, 9, 10, 20, 22, 25, 40, 41, 42] ]
        filtered5 = deadtimefilter.deadtimeFilter( records, 5 )
        self.assertEqual( [ 1, 8, 20, 40 ], [ record.timestamp for record in filtered5 ] )

        filtered3 = deadtimefilter.deadtimeFilter( records, 3 )
        self.assertEqual( [ 1, 5, 9, 20, 25, 40 ], [ record.timestamp for record in filtered3 ] )

        filtered0 = deadtimefilter.deadtimeFilter( records, 0 )
        self.assertEqual( [ 1, 3, 5, 8, 9, 10, 20, 22, 25, 40, 41, 42], [ record.timestamp for record in filtered0 ] )

        INFINITY = 1e100
        filteredInfinity = deadtimefilter.deadtimeFilter( records, INFINITY )
        self.assertEqual( [1,], [ record.timestamp for record in filteredInfinity ] )
