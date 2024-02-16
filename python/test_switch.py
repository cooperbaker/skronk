#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from SWITCH import switch
import time


#-------------------------------------------------------------------------------
# pin definitions
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

# make a switch reader
sw = switch( [ B1 , B2 , B3 , B4 , B5 , B6 , B7 , B8 , B9 , B10 , B11 , B12, E1A, E1B, E2A, E2B ] )

# on / off callbacks
def on( channel ):
    print( 'Switch %s on' % channel )

def off( channel ):
    print( 'Switch %s off' % channel )

sw.on  = on
sw.off = off

def main():
    print()
    print( 'Skronk Hat Switch Tester - Ctrl-C to Exit' )
    print()
    while True:
        sw.read()

        # 16 channel full read theoretical frequency : 520 5/6 Hz
        # run at 500Hz
        time.sleep( 0.002 )

main()

sw.cleanup()