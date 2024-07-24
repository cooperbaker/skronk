#-------------------------------------------------------------------------------
# thread.py
# Threaded callback at millisecond intervals
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import threading
from time import sleep, clock_gettime, CLOCK_MONOTONIC


#-------------------------------------------------------------------------------
# thread class
#-------------------------------------------------------------------------------
class thread():

    # constructor
    def __init__( self, callback, milliseconds ):
        self.callback = callback
        self.sleep    = milliseconds / 1000
        self.spin     = True

        threading.stack_size( 65536 )
        threading.Thread( target = self.run ).start()

    # run a callback loop with a sleep timer
    def run( self ):
        start_time = 0
        while self.spin:
            start_time = clock_gettime( CLOCK_MONOTONIC )
            self.callback()
            sleep( max( 0, self.sleep - ( clock_gettime( CLOCK_MONOTONIC ) - start_time ) ) )

    # stop thread
    def stop( self ):
        self.spin = False


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
