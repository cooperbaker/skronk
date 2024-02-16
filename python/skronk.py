#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from PINS    import *
from SWITCH  import switch
from MCP3208 import mcp3208
from ENCODER import encoder
from OSC_MSG import osc_msg
import time


#-------------------------------------------------------------------------------
# driver loop sample rate
#-------------------------------------------------------------------------------
SAMPLE_RATE_HZ = 500
sleep          = 1 / SAMPLE_RATE_HZ

#-------------------------------------------------------------------------------
# osc
#-------------------------------------------------------------------------------

# network
OSC_IP   = '10.0.0.3'
OSC_PORT = 1234

# message addresses
OSC_ENC = '/enc/'
OSC_SW  = '/sw/'
OSC_ADC = '/adc/'
OSC_LED = '/led/'
OSC_LCD = '/lcd/'

osc = osc_msg( OSC_IP, OSC_PORT )



#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
adc1 = mcp3208( 0, 0 )
adc2 = mcp3208( 0, 1 )


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
sw = switch( [ B1 , B2 , B3 , B4 , B5 , B6 , B7 , B8 , B9 , B10 , B11 , B12 ] )

# on / off callbacks
def sw_on( channel ):
    osc.send( OSC_SW + str( channel ), 1 )
    print( 'Switch %s on' % channel )

def sw_off( channel ):
    osc.send( OSC_SW + str( channel ), 0 )
    print( 'Switch %s off' % channel )

# assign callbacks
sw.on  = sw_on
sw.off = sw_off


#-------------------------------------------------------------------------------
# encoders
#-------------------------------------------------------------------------------
enc1 = encoder( E1A, E1B )
enc2 = encoder( E2A, E2B )

# inc / dec callbacks
def enc1_inc():
    osc.send( OSC_ENC + '1', 1 )
    print( 'Encoder 1 Inc' )

def enc1_dec():
    osc.send( OSC_ENC + '1', -1 )
    print( 'Encoder 1 Dec' )

def enc2_inc():
    osc.send( OSC_ENC + '1', 1 )
    print( 'Encoder 2 Inc' )

def enc2_dec():
    osc.send( OSC_ENC + '1', -1 )
    print( 'Encoder 2 Dec' )

# assign callbacks
enc1.inc = enc1_inc
enc1.dec = enc1_dec
enc2.inc = enc2_inc
enc2.dec = enc2_dec


#-------------------------------------------------------------------------------
# driver loop
#-------------------------------------------------------------------------------
while True:

    sw.read()

    enc1.read()
    enc2.read()

    adc1.read()
    adc2.read()

    time.sleep( sleep )

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
