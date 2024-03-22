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
    spi     = spidev.SpiDev()
    bus     = 0
    device  = 0
    val     = [ 0 ] * 8
    val_old = [ 0 ] * 8
    value   = [ 0 ] * 8

    # lowpass filter
    y      = [ 0 ] * 8
    a      = 0.08    # 0 to 1 : larger = less lag

    # moving average filter
    # avg    = [ [ 0 ] * 10 ] * 8

    # constructor
    def __init__( self, bus, device ):
        self.bus = bus
        self.device = device

    def read( self ):
        for i in range( 8 ):

            self.val[ i ] = self.read_ch( i )

            # jit = 0
            # if self.val[ i ] < self.val_old[ i ]:
            #     jit = self.val_old[ i ] - self.val[ i ]
            # elif self.val[ i ] > self.val_old[ i ]:
            #     jit = self.val[ i ] - self.val_old[ i ]

            # if( jit > 10 ):
            #     self.value[ i ] = self.val[ i ]

            self.value[ i ] = self.val[ i ]


            self.val_old[ i ] = self.val[ i ]


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

        # return val
        return self.filter( channel, val )

    # adc input filter
    def filter( self, channel, x ):
        # lowpass
        self.y[ channel ] = self.a * x + ( 1 - self.a ) * self.y[ channel ]

        return round( self.y[ channel ] )

        # self.avg[ channel ][ 9 ] = self.avg[ channel ][ 8 ]
        # self.avg[ channel ][ 8 ] = self.avg[ channel ][ 7 ]
        # self.avg[ channel ][ 7 ] = self.avg[ channel ][ 6 ]
        # self.avg[ channel ][ 6 ] = self.avg[ channel ][ 5 ]
        # self.avg[ channel ][ 5 ] = self.avg[ channel ][ 4 ]
        # self.avg[ channel ][ 4 ] = self.avg[ channel ][ 3 ]
        # self.avg[ channel ][ 3 ] = self.avg[ channel ][ 2 ]
        # self.avg[ channel ][ 2 ] = self.avg[ channel ][ 1 ]
        # self.avg[ channel ][ 1 ] = self.avg[ channel ][ 0 ]
        # self.avg[ channel ][ 0 ] = self.y[ channel ]

        # return round( self.avg[ channel ][ 0 ] + self.avg[ channel ][ 1 ] + self.avg[ channel ][ 2 ] + self.avg[ channel ][ 3 ] + self.avg[ channel ][ 4 ] + self.avg[ channel ][ 5 ] + self.avg[ channel ][ 6 ] + self.avg[ channel ][ 7 ] + self.avg[ channel ][ 8 ] + self.avg[ channel ][ 9 ] ) / 10

    # destructor
    def cleanup( self ):
        self.spi.close()

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
