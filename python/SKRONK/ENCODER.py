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

    # constructor
    # def callback( state )
    def __init__( self, a, b, callback ):
        self.val      = 0
        self.old      = 0
        self.enc      = RotaryEncoder( a, b, max_steps=32 )
        self.callback = callback

    # read encoder steps
    def read( self ):
        self.old = self.val
        self.val += self.enc.steps
        self.enc.steps = 0

        if( self.val > self.old ):
            for i in range( 0, ( self.val - self.old ) ):
                self.callback( 1 )

        if( self.val < self.old ):
            for i in range( 0, ( self.old - self.val ) ):
                self.callback( 0 )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
