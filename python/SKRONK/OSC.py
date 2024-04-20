#-------------------------------------------------------------------------------
# OSC.py
# Threaded full-duplex open sound control client/server
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import threading

from pythonosc            import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc            import osc_server


#-------------------------------------------------------------------------------
# osc_io class
#-------------------------------------------------------------------------------
class osc_io():

    #constructor
    def __init__( self, in_ip, in_port, out_ip, out_port ):

        # network info
        self.out_ip     = out_ip
        self.out_port   = out_port
        self.in_ip      = in_ip
        self.in_port    = in_port

        # client
        self.client     = udp_client.SimpleUDPClient( self.out_ip, self.out_port )

        # server
        self.dispatcher = Dispatcher()
        self.dispatcher.set_default_handler( self.parse )
        self.server     = osc_server.ThreadingOSCUDPServer( ( self.in_ip, self.in_port ), self.dispatcher )
        self.thread     = threading.Thread( target = self.server.serve_forever )
        self.thread.start()

    # send a message
    def send( self, addr, val ):
        self.client.send_message( addr, val )

    # default received message parse callback
    def parse( address, *args ):
        print( f'{ address }: { args }' )

    # set parse callback
    def set_parse( self, parser ):
        self.dispatcher.set_default_handler( parser )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
