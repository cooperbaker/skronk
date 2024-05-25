#-------------------------------------------------------------------------------
# THREAD.py
# Threaded callback at millisecond intervals
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import threading
import time


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
        start = 0
        while self.spin:
            start = time.clock_gettime( time.CLOCK_MONOTONIC )
            self.callback()
            time.sleep( max( 0, self.sleep - ( time.clock_gettime( time.CLOCK_MONOTONIC ) - start ) ) )

    # stop thread
    def stop( self ):
        self.spin = False


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
