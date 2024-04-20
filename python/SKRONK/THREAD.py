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
        self.run      = True
        self.thread   = threading.Thread( target = self.driver )
        self.thread.start()

    # thread driver
    def driver( self ):
        while self.run:
            self.callback()
            time.sleep( self.sleep )

    # stop thread
    def stop( self ):
        self.run = False


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
