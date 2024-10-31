#-------------------------------------------------------------------------------
# system.py
# System object for skronk
#
# Cooper Baker (c) 2024
#
# pylint: disable = bare-except
# pylint: disable = multiple-statements
# pylint: disable = unspecified-encoding
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from sys        import exit as sys_exit
from signal     import signal, SIGHUP, SIGINT, SIGQUIT, SIGABRT, SIGTERM
from shutil     import which
from logging    import disable, WARNING
from .mcp3208   import mcp3208
from .osc       import osc
from .puredata  import puredata
from .rainbow   import rainbow
from .switch    import switch
from .thread    import thread


#-------------------------------------------------------------------------------
# system class
#-------------------------------------------------------------------------------
class system():

    # skronk version
    version = 0.9

    # constructor
    def __init__( self ):

        # install signal handler
        signal( SIGHUP,  self.sig )
        signal( SIGINT,  self.sig )
        signal( SIGQUIT, self.sig )
        signal( SIGABRT, self.sig )
        signal( SIGTERM, self.sig )

        # linux process name
        with open( '/proc/self/comm', 'w' ) as f: f.write( 'skronk' )

        # disable warning logging to prevent pythonosc console spam
        disable( WARNING )

        # check for pd and rnbo
        self.has_pd   = which( '/usr/bin/pd' )
        self.has_rnbo = which( '/usr/bin/rnbooscquery' )

        # objects
        self.adc1  = mcp3208( 0, 0 )
        self.adc2  = mcp3208( 0, 1 )
        self.osc   = osc()
        self.pd    = puredata()
        self.rnbo  = rainbow( self )
        self.sw    = switch()
        self.read  = thread( self.read_thread, 1 )
        self.event = thread( self.event_thread, 1 )
        self.disp  = None
        self.menu  = None

        # announce
        print()
        print( 'Skronk Hat Firmware ' + str( self.version ) )
        print( 'https://nyquist.dev/skronk' )
        print( '(c) 2024 Cooper Baker' )
        print()


    # command - command handler ( args is list of words/values )
    def command( self, *args ):
        if args[ 0 ] == 'off':
            self.shutdown()

    # read_thread - switch / adc read callback
    def read_thread( self ):
        self.sw.read()
        self.adc1.read()
        self.adc2.read()

    # event_thread - switch / adc event callback
    def event_thread( self ):
        self.sw.events()
        self.adc1.events()
        self.adc2.events()

    # sig - os signal handler callback
    def sig( self, sig, frame ):
        name = 0
        if   sig ==  1 : name = 'SIGHUP'
        elif sig ==  2 : name = 'SIGINT'
        elif sig ==  3 : name = 'SIGQUIT'
        elif sig ==  6 : name = 'SIGABRT'
        elif sig == 15 : name = 'SIGTERM'
        if name :
            print( '\n\n' + name + ' Received - Goodbye\n' )
            try:
                self.shutdown()
            except:
                pass

    # shutdown - exit skronk
    def shutdown( self ):
        self.osc.server.shutdown()
        self.event.stop()
        self.read.stop()
        self.pd.stop()
        self.menu.stop()
        self.disp.shutdown()
        sys_exit()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
