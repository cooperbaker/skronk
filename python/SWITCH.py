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

    # locals
    pin = []
    obj = []
    now = []
    old = []

    # constructor
    def __init__( self, pins ):
        self.pin = pins
        for i, pin in enumerate( self.pin ):
            obj = gpio.get_line( pin )
            obj.request( consumer=__file__, type=gpiod.LINE_REQ_DIR_IN )
            self.obj.append( obj )
            self.now.append( 0 )
            self.old.append( 0 )

    # destructor
    def cleanup( self ):
        for obj in self.obj:
            obj.release()

    # read button states
    def read( self ):
        for i, obj in enumerate( self.obj ):
            self.now[ i ] = int( not ( obj.get_value() ) )

            # press detect
            if self.now[ i ] and ( self.now[ i ] != self.old[ i ] ):
                self.on( i + 1 )
                self.old[ i ] = self.now[ i ]

            # release detect
            if not( self.now[ i ] ) and ( self.now[ i ] != self.old[ i ] ):
                self.off( i + 1 )
                self.old[ i ] = self.now[ i ]

    # on handler callback
    def on( self, channel ):
        print( 'Switch %s on' % channel )

    # off handler callback
    def off( self, channel ):
        print( 'Switch %s off' % channel )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
