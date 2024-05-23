#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Operating Script
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from time           import sleep
from SKRONK.DISPLAY import display
from SKRONK.ENCODER import encoder
from SKRONK.LAN_IP  import lan_ip
from SKRONK.MCP3208 import mcp3208
from SKRONK.OSC     import osc_io
from SKRONK.PINS    import *
from SKRONK.SWITCH  import switch
from SKRONK.THREAD  import thread


#-------------------------------------------------------------------------------
# open sound control config
#-------------------------------------------------------------------------------
# network
# OSC_IN_IP    = lan_ip()
# OSC_IN_PORT  = 1000
# OSC_OUT_IP   = '10.0.0.3'
# OSC_OUT_PORT = 1001

# internal
OSC_IN_IP    = '127.0.0.1'
OSC_IN_PORT  = 1000
OSC_OUT_IP   = '127.0.0.1'
OSC_OUT_PORT = 1001

# input addresses
OSC_LCD = '/lcd'
OSC_CMD = '/cmd'

# output addresses
OSC_ENC = '/enc/'
OSC_SW  = '/sw/'
OSC_ADC = '/adc/'


#-------------------------------------------------------------------------------
# display - display( lcd/oled, cols, rows, fps )
#-------------------------------------------------------------------------------
disp = display( 'oled', 20, 4, 30 )
disp.clear()


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# define osc message callback
def osc_message( address, *args ):
    if address == OSC_LCD:
        disp.buf_fill( str( args[ 0 ] ) )
    elif address == OSC_CMD:
        if args[ 0 ] == 'lcd_off':
            disp.off()
        elif args[ 0 ] == 'lcd_on':
            disp.on()

# make osc server: osc_io( in_ip, in_port, out_ip, out_port, message_callback )
osc = osc_io( OSC_IN_IP, OSC_IN_PORT, OSC_OUT_IP, OSC_OUT_PORT, osc_message )


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# define change handler callback
def sw_change( channel, state ):
    osc.send( OSC_SW + str( channel ), state )

# make switch object: switch( [ pin_numbers ], change_callback )
sw = switch( [ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12 ], sw_change )

# start switch read thread at 1 msec interval
sw_thread = thread( sw.read, 1 )


#-------------------------------------------------------------------------------
# encoders
#-------------------------------------------------------------------------------
# define change callbacks
def enc_change( channel, direction ):
    osc.send( OSC_ENC + str( channel ), direction )

def enc1_change( direction ):
    enc_change( 1, direction )

def enc2_change( direction ):
    enc_change( 2, direction )

# make encoder objects: encoder( pin_a, pin_b, change_callback )
enc1 = encoder( E1A, E1B, enc1_change )
enc2 = encoder( E2A, E2B, enc2_change )

# define read callback for threading
def enc_read():
    enc1.read()
    enc2.read()

# start encoder read thread at 1 msec interval
enc_thread = thread( enc_read, 1 )


#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
#define change callbacks
def adc_change( channel, value ):
    osc.send( OSC_ADC + str( channel ), value )
    disp.buf_write( 6, 3, '         ' )
    disp.buf_write( 6, 3, str( channel ) + ':' + str( value ) )

def adc1_change( channel, value ):
    adc_change( channel, value )

def adc2_change( channel, value ):
    adc_change( channel + 8, value )

# make adc objects: mcp3208( i2s_bus, i2s_device, change_callback )
adc1 = mcp3208( 0, 0, adc1_change )
adc2 = mcp3208( 0, 1, adc2_change )

# define adc read callback for threading
def adc_read():
    adc1.read()
    adc2.read()

# start adc read thread at 1 msec interval
adc_thread = thread( adc_read, 1 )


#-------------------------------------------------------------------------------
# main - main function
#-------------------------------------------------------------------------------
def main():

    print( ' \n' )
    print( 'Skronk Hat @ ' + OSC_IN_IP )
    print( ' \n' )

    disp.fade_blink( 0 )
    disp.buf_write( 0, 0, OSC_IN_IP )

    # x  = 0
    # xi = 0.048
    # y  = 0
    # yi = 0.024

    while True:
        # disp.buf_write( int( x ), int( y ), '  ' )
        # x = x + xi
        # if( x < 0 or x > 19 ):
        #     xi = xi * -1
        # y = y + yi
        # if( y < 0 or y > 4 ):
        #     yi = yi * -1

        # disp.buf_write( int( x ), int( y ), '()' )
        # sleep( 0.001 )

        print( adc1.value[ 4 ] )

        sleep( 0.1 )

main()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
