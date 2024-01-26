#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import gpiod
import time


#-------------------------------------------------------------------------------
# pin definitions
#-------------------------------------------------------------------------------

# buttons
#-------------------------------------------------------------------------------
B1  = 4
B2  = 5
B3  = 6
B4  = 12
B5  = 13
B6  = 16
B7  = 17
B8  = 19
B9  = 20
B10 = 21
B11 = 22
B12 = 23

# encoders
#-------------------------------------------------------------------------------
E1A = 24
E1B = 25
E2A = 26
E2B = 27

# leds
#-------------------------------------------------------------------------------
LED = 18

# i2s
#-------------------------------------------------------------------------------
SDA  = 2
SCL  = 3
MISO = 9
MOSI = 10
SCLK = 11


#-------------------------------------------------------------------------------
# gpio setup
#-------------------------------------------------------------------------------
gpio = gpiod.Chip( 'gpiochip4', gpiod.Chip.OPEN_BY_NAME )


#-------------------------------------------------------------------------------
# Buttons class
#-------------------------------------------------------------------------------
class Buttons:
    pin = []
    obj = []
    now = []
    old = []
    num = []

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
                self.handle_press( i )
                self.old[ i ] = self.now[ i ]

            # release detect
            if not( self.now[ i ] ) and ( self.now[ i ] != self.old[ i ] ):
                self.handle_release( i )
                self.old[ i ] = self.now[ i ]

    # press handler
    def handle_press( self, num ):
        print( 'Button %s DOWN' % num )

    # release handler
    def handle_release( self, num ):
        print( 'Button %s UP' % num )

b = Buttons( [ B1 , B2 , B3 , B4 , B5 , B6 , B7 , B8 , B9 , B10 , B11 , B12, E1A, E1B, E2A, E2B ] )

def main():
    print()
    print( 'Skronk Hat Button Tester - Ctrl-C to Exit' )
    print()
    while True:
        b.read()
        time.sleep( 0.001 )

main()

b.cleanup()