#-------------------------------------------------------------------------------
# rnbo.py
#
# Skronk Menu Page For RNBO
# Load and stop RNBO patches
#
# Cooper Baker (c) 2024
# http://nyquist.dev/skronk
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from .page import page


#-------------------------------------------------------------------------------
# rnbo class
#-------------------------------------------------------------------------------
class rnbo( page ):
    def __init__( self, system ):
        super().__init__( system )

        # patch list scroll offset
        self.offset = 0

    # def tick( self ):
    #     if self.system.pd.proc :
    #         self.system.pd.stop
    #     else :
    #         self.system.rnbo.load( 'name' )

    # draw page
    def draw( self ):
                        #  ....................
                        #  RNBO_<12>3^.filename
                        #  filename.5>>filename
                        #  5.load....|.filename
                        #  6.stop...4v.filename
        self.write( 0, 0, 'RNBO_\x11\x01\x02\x10\x03\x00         ' )
        self.write( 0, 1, '         \x05\x10\x10        ' )
        self.write( 0, 2, '\x05 load    |         ' )
        self.write( 0, 3, '\x06 stop   \x04\x07         ' )
        self.system.rnbo.ls()
        for i in range( self.system.rnbo.patches ):
            if i == self.PAGE_ROWS :
                break
            self.write( 12, i, self.system.rnbo.patch[ ( i + self.offset ) % self.system.rnbo.patches ][ : 8 ] )
        self.write( 0, 1, self.system.rnbo.current_patch()[ : 8 ] )
        self.display()

    # sw1 - navigate left
    def sw1( self, value ):
        if value :
            self.left()

    # sw2 - navigate right
    def sw2( self, value ):
        if value :
            self.right()

    # sw3 - scroll up the patch list
    def sw3( self, value ):
        if value :
            if self.system.rnbo.patches :
                self.offset = ( self.offset + self.system.rnbo.patches - 1 ) % self.system.rnbo.patches
                self.draw()

    # sw4 - scroll down the patch list
    def sw4( self, value ):
        if value :
            if self.system.rnbo.patches :
                self.offset = ( self.offset + 1 ) % self.system.rnbo.patches
                self.draw()

    # sw5 - load patch
    def sw5( self, value ):
        if value :
            if self.system.rnbo.patches :
                self.system.rnbo.load( self.system.rnbo.patch[ ( self.offset + 1 ) % self.system.rnbo.patches ] )
                self.system.menu.toggle()

    # sw6 - stop patch
    def sw6( self, value ):
        if value :
            self.system.rnbo.stop()
            self.draw()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
