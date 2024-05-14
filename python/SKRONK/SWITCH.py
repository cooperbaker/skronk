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
# gpio setup
#-------------------------------------------------------------------------------
gpio = gpiod.Chip( 'gpiochip4', gpiod.Chip.OPEN_BY_NAME )


#-------------------------------------------------------------------------------
# switch class
#-------------------------------------------------------------------------------
class switch():

    # constructor
    # def callback( channel, state )
    def __init__( self, pins, callback ):
        self.obj  = []
        self.now  = []
        self.old  = []
        self.pin  = pins
        self.call = callback

        for i, pin in enumerate( self.pin ):
            obj = gpio.get_line( pin )
            obj.request( consumer=__file__, type=gpiod.LINE_REQ_DIR_IN )
            self.obj.append( obj )
            self.now.append( 0 )
            self.old.append( 0 )

    # destructor
    def cleanup( self ):
        self.thread.run = False

        for obj in self.obj:
            obj.release()

        gpio.close()

    # read button states
    def read( self ):
        for i, obj in enumerate( self.obj ):
            self.now[ i ] = int( not ( obj.get_value() ) )

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
