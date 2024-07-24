#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Realtime Operating Script
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------

# name this process 'skronk'
with open( f'/proc/self/comm', 'w' ) as f: f.write( 'skronk' )


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import sys
import signal
from skronk.display             import display
from skronk.encoder             import encoder
from skronk.pure_data           import pure_data
from skronk.mcp3208             import mcp3208
from skronk.open_sound_control  import open_sound_control
from skronk.pins                import *
from skronk.switch              import switch
from skronk.thread              import thread
from skronk.wlan0_ip            import wlan0_ip


### unfinished:
from skronk.files import files

dir = files()
dir.ls( '/home/pi/pd' )

#-------------------------------------------------------------------------------
# open sound control config
#-------------------------------------------------------------------------------
# network
# OSC_IN_IP    = wlan0_ip()
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
OSC_SW  = '/sw/'
OSC_ADC = '/adc/'


#-------------------------------------------------------------------------------
# pure data
#-------------------------------------------------------------------------------
# create pure data object: pure_data()
pd = pure_data()


#-------------------------------------------------------------------------------
# display
#-------------------------------------------------------------------------------
# create display object: display( lcd/oled, cols, rows, fps )
# disp = display( 'oled', 20, 4, 30 )
disp = display( 'lcd', 20, 4, 10 )


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# osc message handler callback
def osc_message( address, *args ):
    if address == OSC_LCD:
        disp.write( 0, 0, str( args[ 0 ] ) )
    elif address == OSC_CMD:
        if args[ 0 ] == 'lcd_off':
            # disp.off() # oled
            disp.backlight_off() # lcd
        elif args[ 0 ] == 'lcd_on':
            # disp.on() # oled
            disp.backlight_on() # lcd

# create osc server: open_sound_control( in_ip, in_port, out_ip, out_port, message_callback )
osc = open_sound_control( OSC_IN_IP, OSC_IN_PORT, OSC_OUT_IP, OSC_OUT_PORT, osc_message )


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# switch event handler callback - edit this function to customize switch behavior
def sw_event( channel, value ):
    osc.send( OSC_SW + str( channel ), value )
    print( 'sw ' + str( channel ) + ' ' + str( value ) )

 # create switch object: switch( [ pin_numbers ], event_callback )
sw = switch( [ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17 ], sw_event )


#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
# adc event handler callback - edit this function to customize adc behavior
def adc_event( channel, value ):
    osc.send( OSC_ADC + str( channel ), value )
    disp.write( 6, 2, '         ' )
    disp.write( 6, 2, str( channel ) + ':' + str( value ) )

    # print( 'adc ' + str( channel ) + ' ' + str( value ) )

    if( channel == 14 and value == 1 ):
        pd.run( '/home/pi/pd/test.pd' )
    if( channel == 14 and value == 0 ):
        pd.stop()
    return

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
# shutdown
#-------------------------------------------------------------------------------
def shutdown():
    osc.server.shutdown()
    event_thread.stop()
    read_thread.stop()
    pd.stop()
    disp.shutdown()
    sys.exit()

# signal callback
def sig( signal, frame ):
    if signal ==  2: sig_name = 'SIGINT'
    if signal == 15: sig_name = 'SIGTERM'
    print( '\n\n' + sig_name + ' Received - Shutting Down...\n' )
    shutdown()

# register signal handler callbakcks
signal.signal( signal.SIGTERM, sig )
signal.signal( signal.SIGINT,  sig )


#-------------------------------------------------------------------------------
# main - main function
#-------------------------------------------------------------------------------

def main():
    print( ' \n' )
    print( 'Skronk Script @ ' + OSC_IN_IP )
    print( ' \n' )

    # disp.fade_blink( 0 )
    disp.write( 0, 0, OSC_IN_IP )
    pd.run( '/home/pi/pd/test.pd' )

    disp.write( 19, 3, disp.GLYPH_5 )

    # from time import sleep
    # values = [ 0 ] * 16
    # while True:
    #     for i in range( 8 ):
    #         values[ i     ] = adc1.value[ i ]
    #         values[ i + 8 ] = adc2.value[ i ]
    #     print('{0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} | {8:>4} | {9:>4} | {10:>4} | {11:>4} | {12:>4} | {13:>4} | {14:>4} | {15:>4}'.format( * values ) )
    #     sleep( 0.001 )



main()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
