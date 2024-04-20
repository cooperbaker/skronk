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

from RPLCD.i2c            import CharLCD
from SKRONK.PINS          import *
from SKRONK.SWITCH        import switch
from SKRONK.MCP3208       import mcp3208
from SKRONK.ENCODER       import encoder
from SKRONK.LAN_IP        import lan_ip
from SKRONK.OSC           import osc_io
from SKRONK.THREAD        import thread


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------

# network
OSC_IN_IP    = lan_ip()
OSC_IN_PORT  = 1000
OSC_OUT_IP   = '10.0.0.3'
OSC_OUT_PORT = 1001

# message addresses
OSC_ENC = '/enc/'
OSC_SW  = '/sw/'
OSC_ADC = '/adc/'
OSC_LCD = '/lcd'
OSC_CMD = '/cmd'

# instantiate osc server
osc = osc_io( OSC_IN_IP, OSC_IN_PORT, OSC_OUT_IP, OSC_OUT_PORT )

# define message parse callback
def osc_parse( address, *args ):

    if address == OSC_LCD:
        lcd.home()
        lcd.write_string( str( args[ 0 ] ) )
        print( OSC_LCD + ' ' + str( args[ 0 ] ) )

    elif address == OSC_CMD:
        print( 'cmd' )

    elif address:
        print( f'{ address }: { args }' )

# assign message parse callback
osc.set_parse( osc_parse )


#-------------------------------------------------------------------------------
# run flag
#-------------------------------------------------------------------------------
run = True


#-------------------------------------------------------------------------------
# lcd
#-------------------------------------------------------------------------------
lcd = CharLCD( i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8 )
lcd.clear()
lcd.write_string( lan_ip() )


#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
# make adc objects: mcp3208( i2s_bus, i2s_device )
adc1 = mcp3208( 0, 0 )
adc2 = mcp3208( 0, 1 )

# define change callbacks
def adc1_change( channel, value ):
    osc.send( OSC_ADC + str( channel ), value )
    # lcd.home()
    # lcd.write_string( 'ADC ' + str( channel ) + ' ' + str( value ) + '    ' )
    # print( 'ADC ' + str( channel ) + ' : ' + str( value ) )

def adc2_change( channel, value ):
    osc.send( OSC_ADC + str( channel + 8 ), value )
    # lcd.home()
    # lcd.write_string( 'ADC ' + str( channel + 8 ) + ' ' + str( value )  + '    ' )
    # print( 'ADC ' + str( channel + 8 ) + ' : ' + str( value ) )


# assign callbacks
adc1.change = adc1_change
adc2.change = adc2_change

# define adc read callback
def adc_read():
    adc1.read()
    adc2.read()

# start adc read thread
adc_thread = thread( adc_read, 1 )


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# make switch object: switch( [ pin_numbers ] )
sw = switch( [ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12 ] )

# define on/off callbacks
def sw_on( channel ):
    osc.send( OSC_SW + str( channel ), 1 )

def sw_off( channel ):
    osc.send( OSC_SW + str( channel ), 0 )

# assign callbacks
sw.on  = sw_on
sw.off = sw_off

# start switch read thread
sw_thread = thread( sw.read, 1 )


#-------------------------------------------------------------------------------
# encoders
#-------------------------------------------------------------------------------
# make encoder objects: encoder( pin_a, pin_b )
enc1 = encoder( E1A, E1B )
enc2 = encoder( E2A, E2B )

# define inc/dec callbacks
def enc1_inc():
    osc.send( OSC_ENC + '1', 1 )

def enc1_dec():
    osc.send( OSC_ENC + '1', 0 )

def enc2_inc():
    osc.send( OSC_ENC + '2', 1 )

def enc2_dec():
    osc.send( OSC_ENC + '2', 0 )

# assign callbacks
enc1.inc = enc1_inc
enc1.dec = enc1_dec
enc2.inc = enc2_inc
enc2.dec = enc2_dec

# define encoder read callback
def enc_read():
    enc1.read()
    enc2.read()

# start encoder read thread
enc_thread = thread( enc_read, 1 )


#-------------------------------------------------------------------------------
# main - main function
#-------------------------------------------------------------------------------
def main():

    while run:
        # lcd.home()
        # lcd.write_string( str( round( adc1.value[ 0 ], 3 ) ) )
        time.sleep( 0.1 )

main()

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
