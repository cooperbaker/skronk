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

    # class-wide static spi interface object
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
        self.steps     = 200

        # lowpass filter cascade
        self.y0 = [ 0 ] * 8
        self.y1 = [ 0 ] * 8
        self.y2 = [ 0 ] * 8
        self.y3 = [ 0 ] * 8
        self.a = 20 * 6.28318530718 / 1000 # frequency * two_pi / sample_rate

        # moving average filter
        self.avg_size = 20 # smaller = less lag
        self.avg_index = 0
        self.avg = [ [ 0 ] * 8 ] * self.avg_size

        # clipping filter
        self.clip_amt = 10
        self.clip_min = self.clip_amt
        self.clip_max = 4096 - self.clip_amt
        self.clip_rng = self.clip_max - self.clip_min




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

        # iir lowpass filter cascade : y = y + a * ( x - y1 )
        self.y0[ channel ] = self.y0[ channel ] + self.a * ( x                  - self.y0[ channel ] )
        self.y1[ channel ] = self.y1[ channel ] + self.a * ( self.y0[ channel ] - self.y1[ channel ] )
        self.y2[ channel ] = self.y2[ channel ] + self.a * ( self.y1[ channel ] - self.y2[ channel ] )
        self.y3[ channel ] = self.y3[ channel ] + self.a * ( self.y2[ channel ] - self.y3[ channel ] )
        y = self.y3[ channel ]

        # moving average filter
        self.avg_index += 1
        if self.avg_index >= self.avg_size:
            self.avg_index = 0
        self.avg[ self.avg_index ][ channel ] = y
        for i in range( self.avg_size - 1 ):
            y = y + self.avg[ i ][ channel ]
        y = y / self.avg_size

        # clip and normalize 0.0 to 1.0
        if y < self.clip_min:
            y = self.clip_min
        if y > self.clip_max:
            y = self.clip_max
        y = ( y - self.clip_min ) / self.clip_rng

        y = round( y * self.steps ) / self.steps
        return y


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
