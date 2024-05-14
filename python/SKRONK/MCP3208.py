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

    # class-wide static spi object
    spi = spidev.SpiDev()

    # constructor
    # def callback( channel, value ):
    def __init__( self, bus, device, callback ):

        # init vars
        self.bus      = bus
        self.device   = device
        self.callback = callback

        # channel values
        self.value     = [ 0 ] * 8
        self.value_old = [ 0 ] * 8

        # lowpass filter
        self.y = [ 0 ] * 8
        self.a = 0.03  # 0 to 1 : larger = less lag

        # moving average filter
        self.avg_size = 50 # smaller = less lag
        self.avg = [ [ 0 ] * 8 ] * self.avg_size

    # read and filter adc values
    def read( self ):

        # open the chip
        self.spi.open( self.bus, self.device )
        self.spi.max_speed_hz = 1000000

        # get values
        for channel in range( 8 ):
            # request three bytes from the adc channel conversion registers
            adc = self.spi.xfer2( [ 6 | ( channel & 4 ) >> 2, ( channel & 3 ) << 6, 0 ] )

            # shift and mask returned bytes two and three into a single 12 bit value
            self.value[ channel ] = ( ( ( adc[ 1 ] & 15 ) << 8 ) + adc[ 2 ] ) & 0x0FFF

            # filter the value
            self.value[ channel ] = self.filter( channel, self.value[ channel ] )

        #close the chip
        self.spi.close()

        # run callback based on changed values
        for channel in range( 8 ):
            if self.value[ channel ] != self.value_old[ channel ]:
                self.callback( channel, self.value[ channel ] )

            self.value_old[ channel ] = self.value[ channel ]


    # adc input filter
    def filter( self, channel, x ):

        # moving average filter
        for i in range( self.avg_size - 1, 0, -1 ):
            self.avg[ i ][ channel ] = self.avg[ i - 1 ][ channel ]

        self.avg[ 0 ][ channel ] = x

        x_avg = 0

        for i in range( self.avg_size ):
            x_avg = x_avg + self.avg[ i ][ channel ]

        x_avg = x_avg / self.avg_size

        # lowpass filter
        self.y[ channel ] = self.a * x_avg + ( 1 - self.a ) * self.y[ channel ]

        # return a scaled integer 0 to 100
        y = round( ( self.y[ channel ] / 4096 ) * 100 )

        return y


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
