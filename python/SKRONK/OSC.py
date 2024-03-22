#-------------------------------------------------------------------------------
# OSC.py
# Open sound control object for python osc on raspberry pi
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher

#-------------------------------------------------------------------------------
# open_sound_control
#-------------------------------------------------------------------------------
class open_sound_control():

    # client
    out_ip   = '0.0.0.0'
    out_port = 0
    client   = 0

    # server
    in_ip      = '0.0.0.0'
    in_port    = 0
    server     = 0
    dispatcher = 0
    transport  = 0

    # constructor
    def __init__( self, in_ip, in_port, out_ip, out_port ):
        self.out_ip     = out_ip
        self.out_port   = out_port
        self.client     = udp_client.SimpleUDPClient( self.out_ip, self.out_port )
        self.in_ip      = in_ip
        self.in_port    = in_port
        self.dispatcher = Dispatcher()
        self.dispatcher.set_default_handler( self.parse )

    # send a message
    def send( self, addr, val ):
        self.client.send_message( addr, val )

    # received message parse callback
    def parse( address, *args ):
        print( f'{ address }: { args }' )

    # set parse callback
    def set_parse( self, parser ):
        self.dispatcher.set_default_handler( parser )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
