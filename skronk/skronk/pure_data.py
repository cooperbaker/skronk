import os
from signal import SIGTERM
from subprocess import Popen
from pathlib import Path

class pure_data():

    def __init__( self ):
        self.proc = False

    def run( self, path ):
        if self.proc == False:
            # note: must run as root
            self.proc = Popen( [ '/usr/bin/pd', '-alsa', '-blocksize', '64', '-sleepgrain', '0', '-realtime', '-nogui', '-path', str( Path( path ).parent.resolve() ), '-open', path ], preexec_fn=os.setsid )

    def stop( self ):
        try:
            os.kill( self.proc.pid, SIGTERM )
            os.killpg( os.getpgid( self.proc.pid ), SIGTERM )
            self.proc.terminate()
            self.proc.wait()
            self.proc = False
        except:
            None

