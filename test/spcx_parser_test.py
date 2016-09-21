import unittest
from spcxbutcher import spcxparser
import spcxbutcher.spc
import spcxbutcher.descriptor
import spcxbutcher.event
import binascii

SMALL_SPCX_FILE_HEX = ''.join(
       ['03000000', '028302c1', '00000040', '16ba0005',
        '04000000', '028302c1', '00000040', '1ba70008', 'ddb80008',
        '05000000', '028302c1', '00000040', 'c8b90004', '4bbb000d', '2fbc0007',
        '03000000'] )

SPCX_WITH_TIMESTAMP_OVERFLOW  = ''.join( 
['03000000', '028302c1', '00000040', '16ba0005',
 '0a000000', '028302c1', '00000040', '27faff04', '55fbff09', '01000040', 'ac020005', '57f9ff09', '47faff07', '02000040', 'cc030005',
 '02000000'] )

SPCX_WITH_TIMESTAMP_OVERFLOW_3_SPCS  = ''.join( 
['03000000', '028302c1', '00000040', '16ba0005',
 '0a000000', '028302c1', '00000040', '27faff04', '55fbff09', '01000040', 'ac020005', '57f9ff09', '47faff07', '02000040', 'cc030005',
 '03000000', '028302c1', '00000040', '16ba0005',
 '03000000'] )

SPCX_WITH_NONZERO_GAP = ''.join(
       ['03000000', '028302c1', '00000040', '16ba0025',
        '04000000', '028302c1', '00000040', '1ba70028', 'ddb80008',
        '05000000', '028302c1', '00000040', 'c8b90024', '4bbb000d', '2fbc0007',
        '03000000'] )

import io

class FakeOpen:
    def __init__( self, content ):
        self._content = content

    def __call__( self, * args ):
        binary = binascii.a2b_hex( self._content )
        return io.BytesIO( binary )


class SpcxParserTest( unittest.TestCase ):
    def test_parse_correctly( self ):
        spcxparser.open = FakeOpen( SMALL_SPCX_FILE_HEX )
        tested = spcxparser.SPCXParser( 'spcx_filename' )
        spcs = [ spc for spc in tested ]
        self.assertEqual( 3, len( spcs ) )

        self.assertSPCContent(  spcs[ 0 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (3, 47638, 0) ] )

        self.assertSPCContent(  spcs[ 1 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (6, 42779, 0), (6, 47325, 0) ] )

        self.assertSPCContent(  spcs[ 2 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (2, 47560, 0), (9, 47947, 0), (5, 48175, 0) ] )

    def test_throw_if_number_of_spcs_different_from_expected_number( self ):
        SPCX_FILE_WITH_WRONG_EXPECTED_NUMBER = SMALL_SPCX_FILE_HEX[ :-8 ] + '04000000'
        spcxparser.open = FakeOpen( SPCX_FILE_WITH_WRONG_EXPECTED_NUMBER )
        self.assertRaises( Exception, self.parseAndIterate, 'spcx_filename' )

    def test_support_timestamp_overflow( self ):
        spcxparser.open = FakeOpen( SPCX_WITH_TIMESTAMP_OVERFLOW )
        tested = spcxparser.SPCXParser( 'spcx_filename' )
        spcs = [ spc for spc in tested ]
        self.assertEqual( 2, len( spcs ) )

        self.assertSPCContent(  spcs[ 0 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (3, 47638, 0) ] )

        self.assertSPCContent(  spcs[ 1 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (2, 0xfffa27, 0), (7, 0xfffb55, 0), (3, 0x10002ac, 0),
                                           (7, 0x1fff957, 0), (5, 0x1fffa47, 0), (3, 0x20003cc, 0) ] )

    def test_bugfix_timestamp_base_reset_for_each_spc( self ):
        spcxparser.open = FakeOpen( SPCX_WITH_TIMESTAMP_OVERFLOW_3_SPCS )
        tested = spcxparser.SPCXParser( 'spcx_filename' )
        spcs = [ spc for spc in tested ]
        self.assertEqual( 3, len( spcs ) )

        self.assertSPCContent(  spcs[ 0 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (3, 47638, 0) ] )

        self.assertSPCContent(  spcs[ 1 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (2, 0xfffa27, 0), (7, 0xfffb55, 0), (3, 0x10002ac, 0),
                                           (7, 0x1fff957, 0), (5, 0x1fffa47, 0), (3, 0x20003cc, 0) ] )

        self.assertSPCContent(  spcs[ 2 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (3, 47638, 0) ] )

    def test_parse_gap_correctly_when_it_is_not_zero( self ):
        spcxparser.open = FakeOpen( SPCX_WITH_NONZERO_GAP )
        tested = spcxparser.SPCXParser( 'spcx_filename' )
        spcs = [ spc for spc in tested ]
        self.assertEqual( 3, len( spcs ) )

        self.assertSPCContent(  spcs[ 0 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (3, 47638, 1) ] )

        self.assertSPCContent(  spcs[ 1 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (6, 42779, 1), (6, 47325, 0) ] )

        self.assertSPCContent(  spcs[ 2 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (2, 47560, 1), (9, 47947, 0), (5, 48175, 0) ] )

    def test_throw_exception_on_invalid_descriptor( self ):
        VALID_SPCX = SMALL_SPCX_FILE_HEX
        VALID_DESCRIPTOR = '028302c1'
        for invalidDescriptor in [ '028302d1', '028302c2', '028302cd' ]:
            invalidSPCX = VALID_SPCX.replace( VALID_DESCRIPTOR, invalidDescriptor )
            spcxparser.open = FakeOpen( invalidSPCX )
            self.assertRaises( spcxbutcher.descriptor.InvalidDescriptor, self.parseAndIterate, 'spcx_filename' )

    def test_throw_exception_on_invalid_event( self ):
        VALID_SPCX = SMALL_SPCX_FILE_HEX
        VALID_EVENT = '1ba70008'
        for invalidEvent in [  '1ba70088', '1ba700c8' ]:
            invalidSPCX = VALID_SPCX.replace( VALID_EVENT, invalidEvent )
            spcxparser.open = FakeOpen( invalidSPCX )
            self.assertRaises( spcxbutcher.event.InvalidEventRecord, self.parseAndIterate, 'spcx_filename' )

    def assertSPCContent( self, spc, raw, timePerBin, events ):
        self.assertEqual( raw, spc.raw )
        self.assertEqual( timePerBin, spc.timePerBin )
        actualEvents = [ event for event in spc ]
        self.assertEqual( events, actualEvents )

    def parseAndIterate( self, filename ):
        parser = spcxparser.SPCXParser( filename )
        for spc in parser:
            event = list( spc )
