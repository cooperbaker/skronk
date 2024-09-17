#-------------------------------------------------------------------------------
# system.py
# System object for skronk
#
# Cooper Baker (c) 2024
#
# pylint: disable = bare-except
# pylint: disable = multiple-statements
# pylint: disable = unspecified-encoding
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from sys        import exit as sys_exit
from signal     import signal, SIGHUP, SIGINT, SIGQUIT, SIGABRT, SIGTERM
from fcntl      import ioctl
from socket     import socket, inet_ntoa, AF_INET, SOCK_DGRAM, gethostname
from struct     import pack
from time       import sleep
from shutil     import which
from subprocess import check_output
from logging    import disable, WARNING

from .mcp3208   import mcp3208
from .osc       import osc
from .puredata  import puredata
from .rainbow   import rainbow
from .switch    import switch
from .thread    import thread


#-------------------------------------------------------------------------------
# system class
#-------------------------------------------------------------------------------
class system():

    # skronk version
    version = 0.9

    # constructor
    def __init__( self ):

        # install signal callbacks
        signal( SIGHUP,  self.sig )
        signal( SIGINT,  self.sig )
        signal( SIGQUIT, self.sig )
        signal( SIGABRT, self.sig )
        signal( SIGTERM, self.sig )

        # linux process name
        with open( '/proc/self/comm', 'w' ) as f: f.write( 'skronk' )

        # disable warning logging to prevent pythonosc console spam
        disable( WARNING )

        # check for pd and rnbo
        self.has_pd   = which( '/usr/bin/pd' )
        self.has_rnbo = which( '/usr/bin/rnbooscquery' )

        # objects
        self.adc1  = mcp3208( 0, 0 )
        self.adc2  = mcp3208( 0, 1 )
        self.osc   = osc()
        self.pd    = puredata()
        self.rnbo  = rainbow( self )
        self.sw    = switch()
        self.read  = thread( self.read_thread, 1 )
        self.event = thread( self.event_thread, 1 )
        self.disp  = None
        self.menu  = None

        # cpu percent calc vars
        self.work = 0
        self.idle = 0

    # command - command handler ( args is list of words/values )
    def command( self, *args ):
        if args[ 0 ] == 'off':
            self.shutdown()

    # read_thread - switch / adc read callback
    def read_thread( self ):
        self.sw.read()
        self.adc1.read()
        self.adc2.read()

    # event_thread - switch / adc event callback
    def event_thread( self ):
        self.sw.events()
        self.adc1.events()
        self.adc2.events()

    # ip - ip address string ( name: 'eth0', 'wlan0' )
    def ip( self, name ):
        sock  = socket( AF_INET, SOCK_DGRAM )
        iface = pack( '256s', name.encode( 'utf_8' ) )
        try:
            addr = inet_ntoa( ioctl( sock.fileno(), 0x8915, iface )[ 20 : 24 ] )
        except:
            addr = '0:0:0:0'
        return addr

    # ssid - name string of wifi access point
    def ssid( self ) :
        name = check_output( 'nmcli -c no -f ap.ssid device show wlan0', shell=True, text=True ).split()
        if name[ 1 ] :
            return name[ 1 ]
        return ''

    # mac - mac address string ( name: 'eth0', 'wlan0' )
    def mac( self, name ):
        f = open( '/sys/class/net/' + name + '/address','r' )
        m = f.readline()
        f.close()
        return m

    # hostname - hostname string
    def hostname( self ):
        return gethostname()

    # cpu - percent cpu usage string
    def cpu( self ):
        f   = open( '/proc/stat','r' )
        cpu = f.readline()
        f.close()
        cpu       = cpu.split()
        work      = int( cpu[ 1 ] ) + int( cpu[ 2 ] ) + int( cpu[ 3 ] )
        idle      = int( cpu[ 4 ] )
        d_work    = work - self.work
        d_idle    = idle - self.idle
        self.work = work
        self.idle = idle
        return '{:4.1f}'.format( ( float( d_work + 0.000000001 ) / ( d_idle + d_work + 0.000000001 )  ) * 100.0 )

    # mem - percent mem usage string
    def mem( self ):
        f     = open( '/proc/meminfo','r' )
        total = f.readline()
        free  = f.readline()
        f.close()
        total = total.split()
        free  = free.split()
        return '{:4.1f}'.format( float( free[ 1 ] ) / ( float( total[ 1 ] ) ) )

    # temp - cpu celsius degrees string
    def temp( self ):
        f = open( '/sys/class/thermal/thermal_zone0/temp' ) # millidegrees celsius
        c = f.readline()
        f.close()
        return '{:4.1f}'.format( float( c ) / 1000.0 )

    # hello - display hello message
    def hello( self ):
        self.disp.clear()
        self.disp.write( 7, 1, 'Hello' )
        if self.disp.type is self.disp.OLED :
            self.disp.write(  0, 0, '\x17' )
            self.disp.write( 19, 0, '\x17' )
            self.disp.write(  0, 3, '\x17' )
            self.disp.write( 19, 3, '\x17' )
        else :
            self.disp.write(  0, 0, '\x91' )
            self.disp.write( 19, 0, '\x91' )
            self.disp.write(  0, 3, '\x91' )
            self.disp.write( 19, 3, '\x91' )
        self.disp.set_buffer( self.disp.buffer )
        sleep( 0.5 )
        self.disp.clear()

    # goodbye - display goodbye message
    def goodbye( self ):
        self.disp.clear()
        self.disp.write( 6, 1, 'Goodbye' )
        if self.disp.type is self.disp.OLED :
            self.disp.write(  0, 0, '\x17' )
            self.disp.write( 19, 0, '\x17' )
            self.disp.write(  0, 3, '\x17' )
            self.disp.write( 19, 3, '\x17' )
        else :
            self.disp.write(  0, 0, '\x91' )
            self.disp.write( 19, 0, '\x91' )
            self.disp.write(  0, 3, '\x91' )
            self.disp.write( 19, 3, '\x91' )
        self.disp.set_buffer( self.disp.buffer )
        sleep( 0.5 )

    # sig - os signal handler callback
    def sig( self, sig, frame ):
        name = 0
        if   sig ==  1 : name = 'SIGHUP'
        elif sig ==  2 : name = 'SIGINT'
        elif sig ==  3 : name = 'SIGQUIT'
        elif sig ==  6 : name = 'SIGABRT'
        elif sig == 15 : name = 'SIGTERM'
        if name :
            print( '\n\n' + name + ' Received\n' )
            try:
                self.shutdown()
            except:
                pass

    # shutdown - exit skronk
    def shutdown( self ):
        self.osc.server.shutdown()
        self.event.stop()
        self.read.stop()
        self.pd.stop()
        self.menu.stop()
        self.goodbye()
        self.disp.shutdown()
        sys_exit()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
