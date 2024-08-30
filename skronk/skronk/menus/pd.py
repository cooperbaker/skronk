#-------------------------------------------------------------------------------
# pd.py
# Menu page for Pure Data
#
# Load and stop Pure Data patches
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from .page import page


#-------------------------------------------------------------------------------
# pd class
#-------------------------------------------------------------------------------
class pd( page ):
    def __init__( self, skronk ):
        super().__init__( skronk )

        # patch list scroll offset
        self.offset = 0

    # draw page
    def draw( self ):
                        #  ....................
                        #  PD___<12>3^.filename
                        #  filename.5>.filename
                        #  5.load....|.filename
                        #  6.stop...4v.filename
        self.write( 0, 0, 'PD___\x11\x01\x02\x10\x03\x00         ' )
        self.write( 0, 1, '         \x05\x10\x10        ' )
        self.write( 0, 2, '\x05 load    |         ' )
        self.write( 0, 3, '\x06 stop   \x04\x07         ' )
        self.skronk.pd.ls()
        for i in range( self.skronk.pd.patches ):
            if i == self.PAGE_ROWS :
                break
            self.write( 12, i, self.skronk.pd.patch[ ( i + self.offset ) % self.skronk.pd.patches ][ : 8 ] )
        self.display()

    # sw1 - navigate left
    def sw1( self, value ):
        if value :
            self.left()

    # sw2 - navigate right
    def sw2( self, value ):
        if value :
            self.right()

    # sw3 - scroll down the patch list
    def sw3( self, value ):
        if value :
            self.offset = ( self.offset + self.skronk.pd.patches - 1 ) % self.skronk.pd.patches
            self.draw()

    # sw4 - scroll up the patch list
    def sw4( self, value ):
        if value :
            self.offset = ( self.offset + 1 ) % self.skronk.pd.patches
            self.draw()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
