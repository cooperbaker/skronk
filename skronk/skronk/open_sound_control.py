#-------------------------------------------------------------------------------
# open_sound_control.py
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
class open_sound_control():

    # port config
    rnbo_port = 1234
    in_port   = 1235
    pd_port   = 1236
    in_ip     = '127.0.0.1'
    out_ip    = in_ip

    #constructor
    def __init__( self, message_callback ):

        self.message = message_callback

        # clients
        self.client_pd   = udp_client.SimpleUDPClient( self.out_ip, self.pd_port )
        self.client_rnbo = udp_client.SimpleUDPClient( self.out_ip, self.rnbo_port )

        # server
        self.dispatcher = Dispatcher()
        self.dispatcher.set_default_handler( self.message )
        self.server     = osc_server.ThreadingOSCUDPServer( ( self.in_ip, self.in_port ), self.dispatcher )

        threading.stack_size( 65536 )
        threading.Thread( target = self.server.serve_forever ).start()

    # send a message
    def send( self, addr, val ):
        self.client_pd.send_message( addr, val )
        self.client_rnbo.send_message( addr, val )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
