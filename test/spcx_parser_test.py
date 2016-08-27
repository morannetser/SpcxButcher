import unittest
from spcxbutcher import spcxparser
import binascii

SMALL_SPCX_FILE_HEX = '03000000028302c10000004016ba000504000000028302c1000000401ba70008ddb8000805000000028302c100000040c8b900044bbb000d2fbc000703000000' 
SPCX_FILE_HEX_DUMP = \
"""
00000000: 00000003 c1028302 40000000 0500ba16  ...........@....
00000010: 00000004 c1028302 40000000 0800a71b  ...........@....
00000020: 0800b8dd 00000005 c1028302 40000000  ...............@
00000030: 0400b9c8 0d00bb4b 0700bc2f 00000003  ....K.../.......
"""

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

    def assertSPCContent( self, spc, raw, timePerBin, events ):
        self.assertEqual( raw, spc.raw )
        self.assertEqual( timePerBin, spc.timePerBin )
        self.assertEqual( events, spc.events )
