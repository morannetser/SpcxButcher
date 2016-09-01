import unittest
from spcxbutcher import spcxparser
import spcxbutcher.spc
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
        self.assertEqual( 3, len( tested ) )
        spcs = [ spc for spc in tested ]

        self.assertSPCContent(  spcs[ 0 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (5, 47638) ] )

        self.assertSPCContent(  spcs[ 1 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (8, 42779), (8, 47325) ] )

        self.assertSPCContent(  spcs[ 2 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (4, 47560), (13, 47947), (7, 48175) ] )

    def test_throw_if_number_of_spcs_different_from_expected_number( self ):
        SPCX_FILE_WITH_WRONG_EXPECTED_NUMBER = SMALL_SPCX_FILE_HEX[ :-8 ] + '04000000'
        spcxparser.open = FakeOpen( SPCX_FILE_WITH_WRONG_EXPECTED_NUMBER )
        self.assertRaises( Exception, spcxparser.SPCXParser, 'spcx_filename' )

    def test_support_timestamp_overflow( self ):
        spcxparser.open = FakeOpen( SPCX_WITH_TIMESTAMP_OVERFLOW )
        tested = spcxparser.SPCXParser( 'spcx_filename' )
        self.assertEqual( 2, len( tested ) )
        spcs = [ spc for spc in tested ]

        self.assertSPCContent(  spcs[ 0 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (5, 47638) ] )

        self.assertSPCContent(  spcs[ 1 ],
                                raw = 0,
                                timePerBin = 0x28302,
                                events = [ (4, 0xfffa27), (9, 0xfffb55), (5, 0x10002ac),
                                           (9, 0x1fff957), (7, 0x1fffa47), (5,0x20003cc) ] )

    def test_throw_exception_on_invalid_descriptor( self ):
        VALID_SPCX = SMALL_SPCX_FILE_HEX
        VALID_DESCRIPTOR = '028302c1'
        for invalidDescriptor in [ '028302d1', '028302c2', '028302cd' ]:
            invalidSPCX = VALID_SPCX.replace( VALID_DESCRIPTOR, invalidDescriptor )
            spcxparser.open = FakeOpen( invalidSPCX )
            self.assertRaises( spcxbutcher.spc.InvalidDescriptor, spcxparser.SPCXParser, 'spcx_filename' )

    def assertSPCContent( self, spc, raw, timePerBin, events ):
        self.assertEqual( raw, spc.raw )
        self.assertEqual( timePerBin, spc.timePerBin )
        self.assertEqual( events, spc.events )
