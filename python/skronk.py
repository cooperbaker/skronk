#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Open Sound Control Interface
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import asyncio

from pythonosc.osc_server import AsyncIOOSCUDPServer
from RPLCD.i2c            import CharLCD
from SKRONK.PINS          import *
from SKRONK.SWITCH        import switch
from SKRONK.MCP3208       import mcp3208
from SKRONK.ENCODER       import encoder
from SKRONK.LAN_IP        import lan_ip
from SKRONK.OSC           import open_sound_control


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

# make osc object: open_sound_control( in_ip, in_port, out_ip, out_port )
osc = open_sound_control( lan_ip(), OSC_IN_PORT, '10.0.0.3', OSC_OUT_PORT )

# define osc parse callback
def osc_parse( address, *args ):
    if address == OSC_LCD:
        lcd.home()
        lcd.write_string( str( args[ 0 ] ) )
        print( OSC_LCD + ' ' + str( args[ 0 ] ) )
    else:
        print( f'{ address }: { args }' )

# assign callback
osc.set_parse( osc_parse )


#-------------------------------------------------------------------------------
# data sample rate
#-------------------------------------------------------------------------------
SAMPLE_RATE_HZ = 1000
sleep          = 1 / SAMPLE_RATE_HZ
run            = True


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


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# make switch object: switch( [ pin_numbers ] )
sw = switch( [ B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12 ] )

# define on/off callbacks
def sw_on( channel ):
    osc.send( OSC_SW + str( channel ), 1 )
    # print( 'Switch %s on' % channel )

def sw_off( channel ):
    osc.send( OSC_SW + str( channel ), 0 )
    # print( 'Switch %s off' % channel )

# assign callbacks
sw.on  = sw_on
sw.off = sw_off


#-------------------------------------------------------------------------------
# encoders
#-------------------------------------------------------------------------------
# make encoder objects: encoder( pin_a, pin_b )
enc1 = encoder( E1A, E1B )
enc2 = encoder( E2A, E2B )

# define inc/dec callbacks
def enc1_inc():
    osc.send( OSC_ENC + '1', 1 )
    # print( 'Encoder 1 Inc' )

def enc1_dec():
    osc.send( OSC_ENC + '1', 0 )
    # print( 'Encoder 1 Dec' )

def enc2_inc():
    osc.send( OSC_ENC + '2', 1 )
    # print( 'Encoder 2 Inc' )

def enc2_dec():
    osc.send( OSC_ENC + '2', 0 )
    # print( 'Encoder 2 Dec' )

# assign callbacks
enc1.inc = enc1_inc
enc1.dec = enc1_dec
enc2.inc = enc2_inc
enc2.dec = enc2_dec


#-------------------------------------------------------------------------------
# main - async main function
#-------------------------------------------------------------------------------
async def main():

    while run:
        sw.read()
        enc1.read()
        enc2.read()
        adc1.read()
        adc2.read()
        # lcd.home()
        # lcd.write_string( str( round( adc1.value[ 0 ], 3 ) ) )
        await asyncio.sleep( sleep )


#-------------------------------------------------------------------------------
# init - async init function
#-------------------------------------------------------------------------------
async def init():

    # start osc server
    osc.server = AsyncIOOSCUDPServer( ( osc.in_ip, osc.in_port ), osc.dispatcher, asyncio.get_event_loop() )
    osc.transport, protocol = await osc.server.create_serve_endpoint()

    # main function
    await main()

    # stop osc server
    osc.transport.close()


# start the async tasks
asyncio.run( init() )

#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
