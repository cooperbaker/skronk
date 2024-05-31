#-------------------------------------------------------------------------------
# SWITCH.py
# GPIO switch reader for raspberry pi
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import gpiod


#-------------------------------------------------------------------------------
# switch class
#-------------------------------------------------------------------------------
class switch():

    # class-wide static gpio interface object
    gpio = gpiod.Chip( 'gpiochip4', gpiod.Chip.OPEN_BY_NAME )

    # constructor
    # def callback( channel, state )
    def __init__( self, pins, callback ):
        self.obj  = []
        self.now  = []
        self.old  = []
        self.pin  = pins
        self.call = callback

        # set up gpio line objects
        for i, pin in enumerate( self.pin ):
            obj = self.gpio.get_line( pin )
            obj.request( consumer=__file__, type=gpiod.LINE_REQ_DIR_IN )
            self.obj.append( obj )
            self.now.append( 0 )
            self.old.append( 0 )

    # read button states - polling thread
    def read( self ):
        for i, obj in enumerate( self.obj ):
            self.now[ i ] = int( not ( obj.get_value() ) )

    # detect events and run callbacks - event thread
    def events( self ):
        for i, obj in enumerate( self.obj ):
            # press detect
            if self.now[ i ] and ( self.now[ i ] != self.old[ i ] ):
                self.call( i + 1, 1 )
                self.old[ i ] = self.now[ i ]

            # release detect
            if not( self.now[ i ] ) and ( self.now[ i ] != self.old[ i ] ):
                self.call( i + 1, 0 )
                self.old[ i ] = self.now[ i ]


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
