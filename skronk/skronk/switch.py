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

    # constructor
    # def callback( channel, state )
    def __init__( self, pins, callback ):
        self.line     = []
        self.value    = []
        self.prev     = []
        self.pin      = pins
        self.callback = callback

        self.state = []

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


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
