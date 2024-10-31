#-------------------------------------------------------------------------------
# net.py
# Menu page for network info
#
# displays network info
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from .page import page
from ..utility import hostname, ip, mac, ssid

#-------------------------------------------------------------------------------
# net class
#-------------------------------------------------------------------------------
class net( page ):

    # constructor
    def __init__( self, system ):
        super().__init__( system )

    # # tick callback
    # def tick( self ):
    #     self.draw()

    # draw page
    def draw( self ):
        self.clear()
                        #  ....................
                        #  NET_____________<12>
                        #  000.000.000.000.....
                        #  hostname.ssid.......
                        #  00.00.00.00.00.00...
        hostname_ssid = hostname() + ' @ ' + ssid()
        self.write( 0, 0, 'NET_____________\x11\x01\x02\x10' )
        self.write( 0, 1, ip( 'wlan0' ) )
        self.write( 0, 2, f'{hostname_ssid:20s}' )
        self.write( 0, 3, mac( 'wlan0' ) )
        self.display()

    # sw1 - navigate left
    def sw1( self, value ):
        if value :
            self.left()

    # sw2 - navigate right
    def sw2( self, value ):
        if value :
            self.right()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
