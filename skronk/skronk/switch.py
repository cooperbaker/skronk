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
        self.obj      = []
        self.now      = []
        self.old      = []
        self.pin      = pins
        self.callback = callback

        # set up gpio line objects
        for i, pin in enumerate( self.pin ):
            obj = self.gpio.get_line( pin )
            obj.request( consumer = __file__, type = LINE_REQ_DIR_IN )
            self.obj.append( obj )
            self.now.append( 0 )
            self.old.append( 0 )

    # read button states - polling thread
    def read( self ):
        for i, obj in enumerate( self.obj ):
            self.now[ i ] = int( not obj.get_value() )

    # detect events and run callbacks - event thread
    def events( self ):
        for i, obj in enumerate( self.obj ):
            # press detect
            if self.now[ i ] and ( self.now[ i ] != self.old[ i ] ):
                self.callback( i + 1, 1 )
                self.old[ i ] = self.now[ i ]

            # release detect
            if not( self.now[ i ] ) and ( self.now[ i ] != self.old[ i ] ):
                self.callback( i + 1, 0 )
                self.old[ i ] = self.now[ i ]


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
