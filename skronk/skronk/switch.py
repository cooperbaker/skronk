#-------------------------------------------------------------------------------
# switch.py
# GPIO switch reader for raspberry pi
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
# import gpiod
from gpiod import Chip, LINE_REQ_DIR_IN


#-------------------------------------------------------------------------------
# switch class
#-------------------------------------------------------------------------------
class switch():

    # class-wide static gpio interface object
    gpio = Chip( 'gpiochip4', Chip.OPEN_BY_NAME )

    # switch pins
    S1  = 5
    S2  = 25
    S3  = 6
    S4  = 24
    S5  = 12
    S6  = 23
    S7  = 13
    S8  = 22
    S9  = 19
    S10 = 27
    S11 = 16
    S12 = 18
    S13 = 26
    S14 = 17
    S15 = 20
    S16 = 4
    S17 = 21

    pin = [ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17 ]

    # constructor
    def __init__( self ):
        self.line     = []
        self.state    = []
        self.value    = []
        self.prev     = []

        # set up gpio line objects
        for i, pin in enumerate( self.pin ):
            obj = self.gpio.get_line( pin )
            obj.request( consumer = __file__, type = LINE_REQ_DIR_IN )
            self.line.append( obj )
            self.value.append( 0 )
            self.prev.append( 0 )
            self.state.append( int( 0 ) )

    # read button states - polling thread
    def read( self ):
        for i, line in enumerate( self.line ):
            # bit-shift debounce - shift in bits until enough consecutive bits match
            self.state[ i ] = ( ( self.state[ i ] << 1 ) | int( not line.get_value() ) ) & 0xF
            self.value[ i ] = 1 if self.state[ i ] == 0xF else 0

    # detect events and run callbacks - event thread
    def events( self ):
        for i, obj in enumerate( self.line ):
            # press detect
            if self.value[ i ] and ( self.value[ i ] != self.prev[ i ] ):
                self.callback( i + 1, 1 )
                self.prev[ i ] = self.value[ i ]

            # release detect
            if not( self.value[ i ] ) and ( self.value[ i ] != self.prev[ i ] ):
                self.callback( i + 1, 0 )
                self.prev[ i ] = self.value[ i ]

    # callback - event callback
    def callback( self, channel, value ):
        pass

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
