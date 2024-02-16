#-------------------------------------------------------------------------------
# MCP3208.py
# mcp3208 spi reader for raspberry pi
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import spidev

#-------------------------------------------------------------------------------
# mcp3208 class
#-------------------------------------------------------------------------------
class mcp3208():

    # spi
    spi    = spidev.SpiDev()
    bus    = 0
    device = 0
    value  = [ 0 ] * 8

    # lowpass filter
    y      = [ 0 ] * 8
    a      = 0.05 # 0 to 1 : larger = less lag

    # constructor
    def __init__( self, bus, device ):
        self.bus = bus
        self.device = device

    def read( self ):
        for i in range( 8 ):
            self.value[ i ] = self.read_ch( i )

    # read the value of a channel
    def read_ch( self, channel ):
        # mask 3 channel bits
        channel &= 0b00000111

        # get two bytes from the adc channel conversion registers
        self.spi.open( self.bus, self.device )
        self.spi.max_speed_hz = 100000
        self.spi.mode = 0
        adc = self.spi.xfer2( [ 6 | ( channel & 4 ) >> 2, ( channel & 3 ) << 6, 0 ] )
        self.spi.close()

        # shift the returned 2 bytes into a single 12 bit value
        val = ( ( adc[ 1 ] & 15 ) << 8 ) + adc[ 2 ]

        # mask 12 bits of the value
        val = val & 0x0FFF

        return self.filter( channel, val )

    # adc input filter
    def filter( self, channel, x ):
        # lowpass
        self.y[ channel ] = self.a * x + ( 1 - self.a ) * self.y[ channel ]
        return self.y[ channel ]

    # destructor
    def cleanup( self ):
        self.spi.close()

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
