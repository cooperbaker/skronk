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
from skronk.menu        import menu
from skronk.system      import system


#-------------------------------------------------------------------------------
# system object
#-------------------------------------------------------------------------------
skronk = system()


#-------------------------------------------------------------------------------
# display object ( type, cols, rows, fps )
#-------------------------------------------------------------------------------
skronk.disp = display( 'oled', 20, 4, 30 )


#-------------------------------------------------------------------------------
# menu object
#-------------------------------------------------------------------------------
skronk.menu = menu( skronk )


#-------------------------------------------------------------------------------
# open sound control
#-------------------------------------------------------------------------------
# input addresses
OSC_DISP = '/disp'  # display
OSC_RNBO = '/rnbo'  # rnbo
OSC_CMD  = '/cmd'   # command

# output addresses
OSC_SW  = '/sw/'    # switches
OSC_ADC = '/adc/'   # analog to digital converters

# osc message handler callback
def osc_message( address, *args ):

    # turn rnbo @meta {'osc':'/messages'} into normal osc messages
    address, *args = skronk.rnbo.osc_format( address, *args )

    # route osc messages to command handlers
    if   address == OSC_DISP : skronk.disp.command( *args )
    elif address == OSC_RNBO : skronk.rnbo.command( *args )
    elif address == OSC_CMD  : skronk.command( *args )

# set osc message callback
skronk.osc.callback( osc_message )


#-------------------------------------------------------------------------------
# switches
#-------------------------------------------------------------------------------
# define switch event handler callback
def sw_event( channel, value ):

    # give events to menu
    skronk.menu.sw_event( channel, value )

    # only send osc messages if menu is not visible
    if not skronk.menu.visible :
        skronk.osc.send( OSC_SW + str( channel ), value )

# set switch callback
skronk.sw.callback = sw_event


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

# set adc callbacks
skronk.adc1.callback = adc1_event
skronk.adc2.callback = adc2_event


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
