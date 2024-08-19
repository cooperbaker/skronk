#-------------------------------------------------------------------------------
# pure_data.py
# Pure Data interface object
#
# Cooper Baker (c) 2024
#
# pylint: disable = bare-except
# pylint: disable = subprocess-popen-preexec-fn
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from os         import getpgid, kill, killpg, setsid
from signal     import SIGTERM
from subprocess import Popen, PIPE
from pathlib    import Path


#-------------------------------------------------------------------------------
# audio device
#-------------------------------------------------------------------------------
# change this to match your system - list devices with the command:
# $ pd -stderr -listdev -nogui -send "pd quit"
AUDIO_DEVICE = 'USB Audio CODEC'


#-------------------------------------------------------------------------------
# pure_data class
#-------------------------------------------------------------------------------
class pure_data():

    # constructor
    def __init__( self ):
        self.proc = False

    # run - starts pd subprocess with patch at path
    def run( self, path ):
        if self.proc is False:
            # note: must run as root
            self.proc = Popen( [ '/usr/bin/pd',
                                 '-alsa',
                                 '-audiodev', self.dev_id( AUDIO_DEVICE ),
                                 '-blocksize', '64',
                                 '-sleepgrain', '1',
                                 '-realtime',
                                 '-nogui',
                                 '-path', str( Path( path ).parent.resolve() ),
                                 '-open', path ],
                                 preexec_fn = setsid )

    # dev_id - returns first id number of name from "pd -listdev", or 0
    def dev_id( self, name ):
        cmd = Popen( [ 'pd', '-stderr', '-listdev', '-nogui', '-send', 'pd quit' ], stderr = PIPE, text = True )
        out, err = cmd.communicate()
        err = err.split( '\n' )
        for line in err:
            if line.find( name ) > -1 :
                return str( line[ 0 ] )
        return '0'

    # stop - terminates pd subprocess
    def stop( self ):
        try:
            kill( self.proc.pid, SIGTERM )
            killpg( getpgid( self.proc.pid ), SIGTERM )
            self.proc.terminate()
            self.proc.wait()
            self.proc = False
        except:
            pass


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
