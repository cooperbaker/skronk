#-------------------------------------------------------------------------------
# ENCODER.py
# GPIO rotary encoder reader for raspberry pi
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


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
        self.enc = RotaryEncoder( a, b, max_steps=32 )

    # read encoder steps
    def read( self ):
        self.old = self.val
        self.val += self.enc.steps
        self.enc.steps = 0

        if( self.val > self.old ):
            for i in range( 0, ( self.val - self.old ) ):
                self.inc()

        if( self.val < self.old ):
            for i in range( 0, ( self.old - self.val ) ):
                self.dec()

    # increment handler callback
    def inc( self ):
        print( 'encoder increment' )

    # decrement handler callback
    def dec( self ):
        print( 'encoder decrement' )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
