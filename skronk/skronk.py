#-------------------------------------------------------------------------------
# skronk.py
# Skronk Hat Firmware
# http://nyquist.dev/skronk
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from skronk.display     import display
from skronk.mcp3208     import mcp3208
from skronk.menu        import menu
from skronk.osc         import osc
from skronk.pins        import sw_pins
from skronk.puredata    import puredata
from skronk.rainbow     import rainbow
from skronk.switch      import switch
from skronk.system      import system
from skronk.thread      import thread


#-------------------------------------------------------------------------------
# system
#-------------------------------------------------------------------------------
skronk = system()


#-------------------------------------------------------------------------------
# display
#-------------------------------------------------------------------------------
skronk.disp = display( 'oled', 20, 4, 30 )


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# input addresses
OSC_DISP = '/disp'  # display
OSC_CMD  = '/cmd'   # command

# output addresses
OSC_SW  = '/sw/'    # switches
OSC_ADC = '/adc/'   # analog to digital converters

# osc message handler callback
def osc_message( address, *args ):

    # show all osc input :
    # print( address + ' ' + str( args ) )

    # turn rnbo @meta {'osc':'/messages'} into normal osc messages
    address, *args = skronk.rnbo.osc_format( address, *args )

    # route osc messages to command handlers
    if address == OSC_DISP :
        skronk.disp.command( *args )
    elif address == OSC_CMD :
        skronk.command( *args )

# create osc server: open_sound_control( message_callback )
skronk.osc = osc( osc_message )


#-------------------------------------------------------------------------------
# rnbo
#-------------------------------------------------------------------------------
skronk.rnbo = rainbow( skronk.osc )


#-------------------------------------------------------------------------------
# pure data
#-------------------------------------------------------------------------------
skronk.pd = puredata()


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# switch event handler callback
def sw_event( channel, value ):

    # give events to menu
    skronk.menu.sw_event( channel, value )

    # only send osc messages if menu is not visible
    if not skronk.menu.visible :
        skronk.osc.send( OSC_SW + str( channel ), value )

    ### dev sandbox begin ------------------------------------------------------
    if ( channel == 8 ) and value :
        skronk.rnbo.off()
    if ( channel == 9 ) and value :
        print( 'rnbo active: ' + str( skronk.rnbo.active() ) )

    if ( channel == 10 ) and value :
        skronk.ssid()


    if ( channel == 15 ) and value :
        skronk.pd.load( '/home/pi/pd/jam.pd' )
    if ( channel == 16 ) and value :
        skronk.pd.stop()
    ### dev sandbox end --------------------------------------------------------

 # create switch object: switch( [ pin_numbers ], event_callback )
skronk.sw = switch( sw_pins, sw_event )


#-------------------------------------------------------------------------------
# adcs
#-------------------------------------------------------------------------------
# adc event handler callback
def adc_event( channel, value ):
    skronk.osc.send( OSC_ADC + str( channel ), value )

# adc1 event handler callback
def adc1_event( channel, value ):
    adc_event( channel, value )

# adc2 event handler callback
def adc2_event( channel, value ):
    adc_event( channel + 8, value )

# create adc objects: mcp3208( i2s_bus, i2s_device, event_callback )
skronk.adc1 = mcp3208( 0, 0, adc1_event )
skronk.adc2 = mcp3208( 0, 1, adc2_event )


#-------------------------------------------------------------------------------
# read thread
#-------------------------------------------------------------------------------
def read_thread():
    skronk.sw.read()
    skronk.adc1.read()
    skronk.adc2.read()

# create read thread at 1 msec interval
skronk.read = thread( read_thread, 1 )


#-------------------------------------------------------------------------------
# event thread
#-------------------------------------------------------------------------------
def event_thread():
    skronk.sw.events()
    skronk.adc1.events()
    skronk.adc2.events()

# create event thread at 1 msec interval
skronk.event = thread( event_thread, 1 )


#-------------------------------------------------------------------------------
# menu
#-------------------------------------------------------------------------------
menu( skronk )


#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
def main():
    skronk.hello()

main()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
