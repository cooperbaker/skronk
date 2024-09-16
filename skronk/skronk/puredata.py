#-------------------------------------------------------------------------------
# puredata.py
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
from os         import getpgid, kill, killpg, setsid, scandir, path
from signal     import SIGTERM
from subprocess import Popen, PIPE
from pathlib    import Path


#-------------------------------------------------------------------------------
# pure_data class
#-------------------------------------------------------------------------------
class puredata():

    # constructor
    def __init__( self ):

        # alsa audio device
        # change this to match your system - list devices with the command:
        # $ pd -stderr -listdev -nogui -send "pd quit"
        self.device = 'USB Audio CODEC' # Behringer UCA202

        # patch path
        self.path    = '/home/pi/pd'
        self.patch   = []
        self.patches = 0

        # process handle
        self.proc = False

    # load - starts pd subprocess and opens patch at path
    def load( self, path ):
        if self.proc is False:
            # note: must run as root
            self.proc = Popen( [ '/usr/bin/pd',
                                 '-alsa',
                                 '-audiodev', self.dev_id( self.device ),
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

    # ls - fill self.patch[] with names of available patches
    def ls( self ):
        self.patch   = []
        self.patches = 0
        name         = {}
        for node in scandir( self.path ) :
            if node.is_file :
                name = path.splitext( node.name )
                if( name[ 1 ] == '.pd' ) :
                    self.patch.append( name[ 0 ] )
        self.patch.sort( key = lambda x:x[ 0 ] )
        while len( self.patch ) < 4 :
            self.patch.append( '' )
        self.patches = len( self.patch )

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
