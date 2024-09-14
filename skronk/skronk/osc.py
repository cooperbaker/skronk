#-------------------------------------------------------------------------------
# osc.py
# Threaded full-duplex open sound control client/server
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from threading import stack_size, Thread
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer


#-------------------------------------------------------------------------------
# osc
#-------------------------------------------------------------------------------
class osc():

    # port config
    rnbo_port = 1234
    in_port   = 1235
    pd_port   = 1236
    in_ip     = '127.0.0.1'
    out_ip    = in_ip

    #constructor
    def __init__( self, message_callback ):

        # clients
        self.client_pd   = SimpleUDPClient( self.out_ip, self.pd_port )
        self.client_rnbo = SimpleUDPClient( self.out_ip, self.rnbo_port )

        # server
        self.dispatcher = Dispatcher()
        self.dispatcher.set_default_handler( message_callback )
        self.server     = ThreadingOSCUDPServer( ( self.in_ip, self.in_port ), self.dispatcher )

        stack_size( 65536 )
        Thread( target = self.server.serve_forever ).start()

    # send - send a message
    def send( self, addr, val ):
        self.client_pd.send_message( addr, val )
        self.client_rnbo.send_message( addr, val )

    # callback - set default message handler callback
    def callback( self, message_callback ):
        self.dispatcher.set_default_handler( message_callback )

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
