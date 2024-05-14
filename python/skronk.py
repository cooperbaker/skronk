#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Operating Script
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import time
from SKRONK.PINS    import *
from SKRONK.LCD     import lcd_disp
from SKRONK.SWITCH  import switch
from SKRONK.MCP3208 import mcp3208
from SKRONK.ENCODER import encoder
from SKRONK.LAN_IP  import lan_ip
from SKRONK.OSC     import osc_io
from SKRONK.THREAD  import thread


#-------------------------------------------------------------------------------
# open sound control config
#-------------------------------------------------------------------------------
# network
OSC_IN_IP    = lan_ip()
OSC_IN_PORT  = 1000
OSC_OUT_IP   = '10.0.0.3'
OSC_OUT_PORT = 1001

# internal
# OSC_IN_IP    = '127.0.0.1'
# OSC_IN_PORT  = 1000
# OSC_OUT_IP   = '127.0.0.1'
# OSC_OUT_PORT = 1001

# input addresses
OSC_LCD = '/lcd'
OSC_CMD = '/cmd'

# output addresses
OSC_ENC = '/enc/'
OSC_SW  = '/sw/'
OSC_ADC = '/adc/'


#-------------------------------------------------------------------------------
# lcd - for PCF8574 Family
#-------------------------------------------------------------------------------
lcd = lcd_disp( 20, 4, 15 )
lcd.clear()
lcd.write( lan_ip() )
lcd.write_xy( 16, 2, ':)' )


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# define osc message callback
def osc_message( address, *args ):
    if address == OSC_LCD:
        lcd.write( str( args[ 0 ] ) )
    elif address == OSC_CMD:
        if args[ 0 ] == 'lcd_off':
            lcd.off()
        elif args[ 0 ] == 'lcd_on':
            lcd.on()

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
# define change callbacks
def adc_change( channel, value ):
    osc.send( OSC_ADC + str( channel ), value )
    lcd.write_xy( 8, 3, '     ' )
    lcd.write_xy( 8, 3, str( channel ) + '~' + str( value ) )

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
    print( 'Skronk Hat' )
    print( ' \n' )
    print( 'ip : ' + lan_ip() )
    print( ' \n' )

    while True:
        time.sleep( 0.1 )

main()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
