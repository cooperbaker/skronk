#-------------------------------------------------------------------------------
# pure_data.py
# Pure Data subprocess
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import os
from signal import SIGTERM
from subprocess import Popen
from pathlib import Path


#-------------------------------------------------------------------------------
# pure_data class
#-------------------------------------------------------------------------------
class pure_data():

    # constructor
    def __init__( self ):
        self.proc = False

    # run - starts pd subprocess with patch at path
    def run( self, path ):
        if self.proc == False:
            # note: must run as root
            self.proc = Popen( [ '/usr/bin/pd', '-alsa', '-blocksize', '64', '-sleepgrain', '0', '-realtime', '-nogui', '-path', str( Path( path ).parent.resolve() ), '-open', path ], preexec_fn=os.setsid )

    # stop - terminates pd subprocess
    def stop( self ):
        try:
            os.kill( self.proc.pid, SIGTERM )
            os.killpg( os.getpgid( self.proc.pid ), SIGTERM )
            self.proc.terminate()
            self.proc.wait()
            self.proc = False
        except:
            None


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
