import unittest
from spcxbutcher import spcxparser
import binascii

SMALL_SPCX_FILE = binascii.a2b_hex( '03000000028302c10000004016ba000504000000028302c1000000401ba70008ddb8000805000000028302c100000040c8b900044bbb000d2fbc000703000000' )
SPCX_FILE_HEX_DUMP = \
"""
00000000: 00000003 c1028302 40000000 0500ba16  ...........@....
00000010: 00000004 c1028302 40000000 0800a71b  ...........@....
00000020: 0800b8dd 00000005 c1028302 40000000  ...............@
00000030: 0400b9c8 0d00bb4b 0700bc2f 00000003  ....K.../.......
"""

import io

def fakeOpen( * args ):
    return io.BytesIO( SMALL_SPCX_FILE )

spcxparser.open = fakeOpen

class SpcxParserTest( unittest.TestCase ):
    def test_parse_correctly( self ):
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

    def assertSPCContent( self, spc, raw, timePerBin, events ):
        self.assertEqual( raw, spc.raw )
        self.assertEqual( timePerBin, spc.timePerBin )
        self.assertEqual( events, spc.events )
