#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Realtime Operating Script
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
# display
#-------------------------------------------------------------------------------
# make display object: display( lcd/oled, cols, rows, fps )
disp = display( 'oled', 20, 4, 30 )


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# osc message handler callback
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
# switch event handler callback - edit to customize switch event behavior
def sw_event( channel, value ):
    osc.send( OSC_SW + str( channel ), value )
    print( 'sw ' + str( channel ) + ' ' + str( value ) )

 # create switch object: switch( [ pin_numbers ], event_callback )
sw = switch( [ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12 ], sw_event )


#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
# adc event handler callback - edit to customize adc event behavior
def adc_event( channel, value ):
    osc.send( OSC_ADC + str( channel ), value )
    disp.buf_write( 6, 3, '         ' )
    disp.buf_write( 6, 3, str( channel ) + ':' + str( value ) )

# adc1 event handler callback
def adc1_event( channel, value ):
    adc_event( channel, value )

# adc2 event handler callback
def adc2_event( channel, value ):
    adc_event( channel + 8, value )

# create adc objects: mcp3208( i2s_bus, i2s_device, event_callback )
adc1 = mcp3208( 0, 0, adc1_event )
adc2 = mcp3208( 0, 1, adc2_event )


#-------------------------------------------------------------------------------
# read thread
#-------------------------------------------------------------------------------
def read():
    sw.read()
    adc1.read()
    adc2.read()

# create read thread at 1 msec interval
read_thread = thread( read, 1 )


#-------------------------------------------------------------------------------
# event thread
#-------------------------------------------------------------------------------
def events():
    sw.events()
    adc1.events()
    adc2.events()

# create event thread at 1 msec interval
event_thread = thread( events, 1 )


#-------------------------------------------------------------------------------
# main - main function
#-------------------------------------------------------------------------------
def main():

    print( ' \n' )
    print( 'Skronk Hat @ ' + OSC_IN_IP )
    print( ' \n' )

    disp.fade_blink( 0 )
    disp.buf_write( 0, 0, OSC_IN_IP )

    while True:
        sleep( 0.1 )

main()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
