#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from gpiozero import RotaryEncoder


#-------------------------------------------------------------------------------
# encoder class
#-------------------------------------------------------------------------------
class encoder():
    enc = 0
    val = 0
    old = 0

    #constructor
    def __init__( self, a, b ):
        self.enc = RotaryEncoder( a, b, max_steps=24)

    # read encoder steps
    def read( self ):
        self.old = self.val
        self.val += self.enc.steps
        self.enc.steps = 0

        if( self.val > self.old ):
            for i in range( 0, ( self.val - self.old ) ):
                self.inc( self.val )

        if( self.val < self.old ):
            for i in range( 0, ( self.old - self.val ) ):
                self.dec( self.val )

    # increment handler callback
    def inc( self, val ):
        print( "inc - %s" % val )

    # decrement handler callback
    def dec( self, val ):
        print( "dec - %s" % val )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
