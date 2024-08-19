#-------------------------------------------------------------------------------
# encoder.py
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
    # def callback( value )
    def __init__( self, a, b, callback ):
        self.val      = 0
        self.old      = 0
        self.enc      = RotaryEncoder( a, b, max_steps = 32 )
        self.callback = callback

    # read encoder steps - polling thread
    def read( self ):
        self.val += self.enc.steps
        self.enc.steps = 0

    # detect events and run callbacks - event thread
    def events( self ):
        if( self.val > self.old ):
            self.old = self.val
            for i in range( 0, ( self.val - self.old ) ):
                self.callback( 1 )

        if( self.val < self.old ):
            self.old = self.val
            for i in range( 0, ( self.old - self.val ) ):
                self.callback( 0 )


#-------------------------------------------------------------------------------
# example implementation
#-------------------------------------------------------------------------------
# encoder event handler callback - edit this function to customize encoder behavior
# def enc_event( channel, value ):
#     osc.send( OSC_ENC + str( channel ), direction )
#
# encoder 1 event handler callback
# def enc1_event( value ):
#     enc_change( 1, value )
#
# encoder 2 event handler callback
# def enc2_event( value ):
#     enc_change( 2, value )
#
# create encoder objects: encoder( pin_a, pin_b, event_callback )
# enc1 = encoder( E1A, E1B, enc1_change )
# enc2 = encoder( E2A, E2B, enc2_change )
# . . .
#
# read thread
# def read():
#     enc1.read()
#     enc2.read()
#     . . .
#
# event thread
# def events():
#     enc1.events()
#     enc2.events()
#     . . .


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
