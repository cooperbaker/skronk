#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Realtime Operating Script
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from skronk.display             import display
from skronk.encoder             import encoder
from skronk.pure_data           import pure_data
from skronk.rainbow             import rainbow
from skronk.mcp3208             import mcp3208
from skronk.open_sound_control  import open_sound_control
from skronk.pins                import *
from skronk.switch              import switch
from skronk.thread              import thread
from skronk.system              import system


#-------------------------------------------------------------------------------
# process name
#-------------------------------------------------------------------------------
with open( f'/proc/self/comm', 'w' ) as f: f.write( 'skronk' )


#-------------------------------------------------------------------------------
# dev sandbox area
#-------------------------------------------------------------------------------
from skronk.files import files
dir = files()
# dir.ls( '/home/pi/skronk/skronk' )

from skronk.menu import menu
sk_menu = menu()


#-------------------------------------------------------------------------------
# pure data
#-------------------------------------------------------------------------------
# create pure data object: pure_data()
pd = pure_data()


#-------------------------------------------------------------------------------
# rnbo
#-------------------------------------------------------------------------------
# create rnbo object: rainbow()
rnbo = rainbow()


#-------------------------------------------------------------------------------
# display
#-------------------------------------------------------------------------------
# create display object: display( lcd/oled, cols, rows, fps )
disp = display( 'oled', 20, 4, 30 )
# disp = display( 'lcd', 20, 4, 10 )


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# input addresses
OSC_DISP = '/disp' # display
OSC_CMD  = '/cmd'  # command

# output addresses
OSC_SW  = '/sw/'    # switches
OSC_ADC = '/adc/'   # analog to digital converters

# osc message handler callback
def osc_message( address, *args ):

    # turn rnbo @meta {'osc':'/messages'} into normal osc messages
    address, *args = rnbo.osc_message( address, *args )

    # route osc messages to command handlers
    if address == OSC_DISP :
        disp.command( *args )
    elif address == OSC_CMD :
        skronk.command( *args )

# create osc server: open_sound_control( message_callback )
osc = open_sound_control( osc_message )


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# switch event handler callback - edit this function to customize switch behavior
def sw_event( channel, value ):
    osc.send( OSC_SW + str( channel ), value )

    # dev sandbox --------------------------------------------------------------
    if ( channel == 17 ) and ( value ):
        disp.set_buffer( sk_menu.main.buffer )
    else:
        disp.set_buffer( disp.buffer )
    if( channel == 7 ) and value :
        osc.send( '/rnbo/inst/control/unload', [ 'i', -1 ] )
        print( 'unload' )
    if( channel == 8 ) and value :
        osc.send( '/rnbo/inst/control/load', [ 0, 'osc_messages' ]  )
        print( 'load' )
    # dev sandbox end ----------------------------------------------------------

 # create switch object: switch( [ pin_numbers ], event_callback )
sw = switch( [ S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15, S16, S17 ], sw_event )


#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
# adc event handler callback - edit this function to customize adc behavior
def adc_event( channel, value ):
    osc.send( OSC_ADC + str( channel ), value )

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
def read_thread():
    sw.read()
    adc1.read()
    adc2.read()

# create read thread at 1 msec interval
read = thread( read_thread, 1 )


#-------------------------------------------------------------------------------
# event thread
#-------------------------------------------------------------------------------
def event_thread():
    sw.events()
    adc1.events()
    adc2.events()

# create event thread at 1 msec interval
event = thread( event_thread, 1 )


#-------------------------------------------------------------------------------
# system
#-------------------------------------------------------------------------------
# create system object - system( skronk objects )
skronk = system( osc, disp, pd, rnbo, read, event )


#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
def main():
    print( ' \n' )
    print( 'Skronk @ ' + skronk.wlan0_ip() + ':' + str( osc.in_port ) )
    print( ' \n' )

    # ask rnbo to send this script osc messages
    osc.send( '/rnbo/listeners/add', osc.in_ip + ':' + str( osc.in_port ) )

    disp.write(  2, 1, 'Skronk ' + chr( 0b10100000 ) )
    disp.write(  2, 2, skronk.wlan0_ip() + ':' + str( osc.in_port ) )
    disp.write(  0, 0, chr( 0b10010000 ) )
    disp.write( 19, 0, chr( 0b10010000 ) )
    disp.write(  0, 3, chr( 0b10010000 ) )
    disp.write( 19, 3, chr( 0b10010000 ) )

main()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
