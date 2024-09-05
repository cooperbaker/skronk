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
from json           import loads

#-------------------------------------------------------------------------------
# rainbow class
#-------------------------------------------------------------------------------
class rainbow():

    # constructor
    def __init__( self, osc ):

        self.osc = osc

        # local rnbo @ http://127.0.0.1:5678
        self.ip = '127.0.0.1'
        self.port = 5678
        self.url = 'http://' + self.ip + ':' + str( self.port )

        # patches and presets
        self.patch   = []
        self.patches = 0
        self.preset  = []
        self.presets = 0

        # tell rnbo skronk is listening so rnbo will send osc messages
        osc.send( '/rnbo/listeners/add', osc.in_ip + ':' + str( osc.in_port ) )

    # osc_format - turn rnbo @meta {'osc':'/messages'} into normal osc messages
    def osc_format( self, address, *args ):
        rnbo_meta = address.split( ' ' )
        if len( rnbo_meta ) > 1 :
            address = rnbo_meta[ 0 ]
            if args :
                args = rnbo_meta[ 1 : ] + [ args[ 0 ] ]
            else :
                args = rnbo_meta[ 1 : ]
        return address, *args

    # ls - fill self.patch[] with names of available patches
    def ls( self ):
        self.patches = 0
        self.patch   = []
        try :
            json = loads( urlopen( self.url + '/rnbo/patchers' ).read() )
            for name in json[ 'CONTENTS' ]:
                self.patch.append( name )
            self.patch.sort( key = lambda x:x[ 0 ] )
            while len( self.patches ) < 4 :
                self.patch.append( '' )
            self.patches = len( self.patch )
        except :
            self.patch = []
            self.patches = 0

    # current_patch - return current patch name string
    def current_patch( self ):
        try :
            json = loads( urlopen( self.url + '/rnbo/inst/0/name' ).read() )
            return json[ 'VALUE' ]
        except:
            return ''

### TEST -----------------------------------------------------------------------
    def ls_preset( self ):
        self.presets = 0
        self.preset = []
        try :
            json = loads( urlopen( self.url + '/rnbo/inst/0/presets/entries' ).read() )
            for name in json[ 'CONTENTS' ]:
                self.preset.append( name )
            self.preset.sort( key = lambda x:x[ 0 ] )
            while len( self.preset ) < 4 :
                self.preset.append( '' )
            self.presets = len( self.preset )
        except :
            self.preset = []
            self.presets = 0

    # current_preset - return current patch name string
    def current_preset( self ):
        try :
            json = loads( urlopen( self.url + '/rnbo/inst/0/presets/loaded' ).read() )
            return json[ 'VALUE' ]
        except:
            return ''

### TEST END -------------------------------------------------------------------


    # active - report state of rnbo/jack
    def active( self ):
        try :
            json = loads( urlopen( self.url + '/rnbo/jack/active' ).read() )
            state = json[ 'TYPE' ]
        except :
            state = 'F'
        if state == 'T' :
            return 1
        return 0

    # load - load a patch ( activates jack if inactive )
    def load( self, patch ):
        self.osc.send( '/rnbo/inst/control/load', [ 0, patch ]  )

    # stop - unload a patch
    def stop( self ):
        self.osc.send( '/rnbo/inst/control/unload', [ 'i', 0 ] )

    # off - deactivate jack
    def off( self ):
        self.osc.send( '/rnbo/jack/active', 0 )


#-------------------------------------------------------------------------------
# to do ...
#-------------------------------------------------------------------------------
    # def on( self ):
    #     self.osc.send( '/rnbo/jack/active', 1 )


    # def device( self, name ):
        # osc.send( '/rnbo/jack/config/card', [ 's', name ] )
        # osc.send( '/rnbo/jack/active, 0' )
        # osc.send( '/rnbo/jack/active, 1' )

    # def get_devices( self ):


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------

