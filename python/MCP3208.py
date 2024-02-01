#-------------------------------------------------------------------------------
# mcp3208.py
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

    # locals
    spi    = spidev.SpiDev()
    bus    = 0
    device = 0

    # constructor
    def __init__( self, bus, device ):
        self.bus = bus
        self.device = device
        self.spi.open( self.bus, self.device )
        self.spi.max_speed_hz = 100000
        self.spi.mode = 0
        self.spi.close()

    # read the value of a channel
    def read( self, channel ):
        # mask 3 channel bits
        channel &= 0b00000111

        # get two bytes from the adc channel conversion registers
        self.spi.open( self.bus, self.device )
        adc = self.spi.xfer2( [ 6 | ( channel & 4 ) >> 2, ( channel & 3 ) << 6, 0 ] )
        self.spi.close()

        # shift the returned 2 bytes into a single 12 bit value
        val = ( ( adc[ 1 ] & 15 ) << 8 ) + adc[ 2 ]

        # mask 12 bits of the value
        return ( val & 0x0FFF )

    # destructor
    def cleanup():
        self.spi.close()

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
