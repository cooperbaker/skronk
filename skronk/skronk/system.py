#-------------------------------------------------------------------------------
# system.py
# System interface for skronk
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from sys    import exit as sys_exit
from signal import signal, SIGINT, SIGTERM
from fcntl  import ioctl
from socket import socket, inet_ntoa, AF_INET, SOCK_DGRAM
from struct import pack

#-------------------------------------------------------------------------------
# system class
#-------------------------------------------------------------------------------
class system():

    # skronk objects
    osc   = None
    disp  = None
    pd    = None
    rnbo  = None
    event = None
    read  = None

    def __init__( self, osc, disp, pd, rnbo, read, event ):
        # store skronk objects
        self.osc   = osc
        self.disp  = disp
        self.pd    = pd
        self.rnbo  = rnbo
        self.event = event
        self.read  = read

        # install signal callbacks
        signal( SIGTERM, self.sig )
        signal( SIGINT,  self.sig )

    # command - command handler ( args is array of words )
    def command( self, *args ):
        if args[ 0 ] == 'off':
            self.shutdown()

    # wlan0_ip - report lan wifi ip address
    def wlan0_ip( self ):
        sock         = socket( AF_INET, SOCK_DGRAM )
        packed_iface = pack( '256s', 'wlan0'.encode( 'utf_8' ) )
        packed_addr  = ioctl( sock.fileno(), 0x8915, packed_iface )[ 20 : 24 ]
        return inet_ntoa( packed_addr )

    # sig - os signal handler callback
    def sig( self, sig, frame ):
        name = 0
        if sig ==  2:
            name = 'SIGINT'
        if sig == 15:
            name = 'SIGTERM'
        if name :
            print( '\n\n' + name + ' Received\n' )
            self.shutdown()

    # shutdown - exit skronk
    def shutdown( self ):
        self.osc.server.shutdown()
        self.event.stop()
        self.read.stop()
        self.pd.stop()
        self.disp.shutdown()
        sys_exit()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
