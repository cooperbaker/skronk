#-------------------------------------------------------------------------------
# rainbow.py
# RNBO interface object
#
# Cooper Baker (c) 2024
#
# pylint: disable = bare-except
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from urllib.request import urlopen
from json import loads
from os import system


#-------------------------------------------------------------------------------
# rainbow class
#-------------------------------------------------------------------------------
class rainbow():

    # constructor
    def __init__( self ):

        # patch names
        self.patch = []
        self.active = False

    # osc_message - turn rnbo @meta {'osc':'/messages'} into normal osc messages
    def osc_message( self, address, *args ):
        rnbo_meta = address.split( ' ' )
        if len( rnbo_meta ) > 1 :
            address = rnbo_meta[ 0 ]
            if args :
                args = rnbo_meta[ 1 : ] + [ args[ 0 ] ]
            else :
                args = rnbo_meta[ 1 : ]
        return address, *args

    # get_patchers - get names of available patchers and update self.active flag
    def get_patchers( self ):
        try:
            json = loads( urlopen( 'http://127.0.0.1:5678/rnbo/patchers' ).read() )
            self.patch = []
            for name in json[ 'CONTENTS' ]:
                self.patch.append( name )
            self.active = True
        except:
            self.active = False
            print( 'error: get_patchers() - rnbo is not responding... ' )


#-------------------------------------------------------------------------------
# to do ...
#-------------------------------------------------------------------------------

    # def load( self, name ):
        # osc.send( '/rnbo/inst/control/unload', [ 'i', -1 ] )

    # def unload( self, patch ):
        # osc.send( '/rnbo/inst/control/load', [ 0, patch ]  )


    # def device( self, name ):
        # osc.send( '/rnbo/jack/config/card', [ 's', name ] )
        # osc.send( '/rnbo/jack/active, 0' )
        # osc.send( '/rnbo/jack/active, 1' )

    # def get_devices( self ):


    # def stop( self ):
    #     system( 'sudo systemctl stop rnbooscquery.service' )

    # def start( self ):
        # system( 'sudo systemctl start rnbooscquery.service' )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
