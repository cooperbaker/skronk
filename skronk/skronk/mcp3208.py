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
        self.steps     = 200
        self.value     = [ 0 ] * 8
        self.value_old = [ 0 ] * 8

        # lowpass filter cascade
        self.y0 = [ 0 ] * 8
        self.y1 = [ 0 ] * 8
        self.y2 = [ 0 ] * 8
        self.y3 = [ 0 ] * 8
        self.a  = 20 * 6.28318530718 / 1000 # frequency * two_pi / sample_rate

        # moving average filter
        self.avg_size = 20 # smaller = less lag
        self.avg_index = 0
        self.avg = [ [ 0 ] * 8 ] * self.avg_size

        # clipping filter
        self.clip_amt = 16
        self.clip_min = self.clip_amt
        self.clip_max = 4096 - self.clip_amt
        self.clip_rng = self.clip_max - self.clip_min

        # raw adc registers
        self.adc0 = [ 0 ] * 3
        self.adc1 = [ 0 ] * 3
        self.adc2 = [ 0 ] * 3
        self.adc3 = [ 0 ] * 3
        self.adc4 = [ 0 ] * 3
        self.adc5 = [ 0 ] * 3
        self.adc6 = [ 0 ] * 3
        self.adc7 = [ 0 ] * 3

    # read and filter adc values - polling thread
    def read( self ):

        # MCP3208 datasheet page 3 : 2.0 MHz clock with 5V supply
        # 24 bit word @ 2MHz       = 0.012 msec per word i.e. 83.333 kHz sample rate
        #  8 channels @ 83.3kHz    = 0.096 msec or 27.777kHz per chip
        # 16 channels @ 83.3kHz    = 0.192 msec or 13.888kHz for two chips
        # 0.192 msec + 0.808 sleep = 1 msec or 1kHz for 16 channels or two chips
        # Note: Python is not capable of realtime precison at millisecond
        # intervals, and adc reads occur with a somewhat jittery sample rate.
        # On a raspberry pi 5, 1kHz seems to be the best read interval for 2 chips

        # open the chip
        self.spi.open( self.bus, self.device )
        self.spi.max_speed_hz = 2000000

        # request three bytes of data from the adc channel conversion registers
        self.adc0 = self.spi.xfer2( [ 6 | ( 0 & 4 ) >> 2, ( 0 & 3 ) << 6, 0 ] )
        self.adc1 = self.spi.xfer2( [ 6 | ( 1 & 4 ) >> 2, ( 1 & 3 ) << 6, 0 ] )
        self.adc2 = self.spi.xfer2( [ 6 | ( 2 & 4 ) >> 2, ( 2 & 3 ) << 6, 0 ] )
        self.adc3 = self.spi.xfer2( [ 6 | ( 3 & 4 ) >> 2, ( 3 & 3 ) << 6, 0 ] )
        self.adc4 = self.spi.xfer2( [ 6 | ( 4 & 4 ) >> 2, ( 4 & 3 ) << 6, 0 ] )
        self.adc5 = self.spi.xfer2( [ 6 | ( 5 & 4 ) >> 2, ( 5 & 3 ) << 6, 0 ] )
        self.adc6 = self.spi.xfer2( [ 6 | ( 6 & 4 ) >> 2, ( 6 & 3 ) << 6, 0 ] )
        self.adc7 = self.spi.xfer2( [ 6 | ( 7 & 4 ) >> 2, ( 7 & 3 ) << 6, 0 ] )

        # close the chip
        self.spi.close()

        # assemble and filter returned adc data
        # value = ( ( ( adc[ 1 ] & 15 ) << 8 ) + adc[ 2 ] ) & 0x0FFF
        self.value[ 0 ] = self.filter( 0, ( ( ( self.adc0[ 1 ] & 15 ) << 8 ) + self.adc0[ 2 ] ) & 0x0FFF )
        self.value[ 1 ] = self.filter( 1, ( ( ( self.adc1[ 1 ] & 15 ) << 8 ) + self.adc1[ 2 ] ) & 0x0FFF )
        self.value[ 2 ] = self.filter( 2, ( ( ( self.adc2[ 1 ] & 15 ) << 8 ) + self.adc2[ 2 ] ) & 0x0FFF )
        self.value[ 3 ] = self.filter( 3, ( ( ( self.adc3[ 1 ] & 15 ) << 8 ) + self.adc3[ 2 ] ) & 0x0FFF )
        self.value[ 4 ] = self.filter( 4, ( ( ( self.adc4[ 1 ] & 15 ) << 8 ) + self.adc4[ 2 ] ) & 0x0FFF )
        self.value[ 5 ] = self.filter( 5, ( ( ( self.adc5[ 1 ] & 15 ) << 8 ) + self.adc5[ 2 ] ) & 0x0FFF )
        self.value[ 6 ] = self.filter( 6, ( ( ( self.adc6[ 1 ] & 15 ) << 8 ) + self.adc6[ 2 ] ) & 0x0FFF )
        self.value[ 7 ] = self.filter( 7, ( ( ( self.adc7[ 1 ] & 15 ) << 8 ) + self.adc7[ 2 ] ) & 0x0FFF )

    # detect events and run callbacks - event thread
    def events( self ):
        # run callbacks based on changed values
        for channel in range( 8 ):
            if self.value[ channel ] != self.value_old[ channel ]:
                self.callback( channel + 1, self.value[ channel ] )
            self.value_old[ channel ] = self.value[ channel ]

    # adc input filter
    def filter( self, channel, x ):

        # iir lowpass filter cascade : y = y1 + a * ( x - y1 )
        self.y0[ channel ] = self.y0[ channel ] + self.a * (                  x - self.y0[ channel ] )
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

        return int( y * self.steps ) / self.steps


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
