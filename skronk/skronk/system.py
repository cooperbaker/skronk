#-------------------------------------------------------------------------------
# system.py
# System object for skronk
#
# Cooper Baker (c) 2024
# pylint: disable = bare-except
# pylint: disable = multiple-statements
# pylint: disable = unspecified-encoding
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from sys    import exit as sys_exit
from signal import signal, SIGHUP, SIGINT, SIGQUIT, SIGABRT, SIGTERM
from fcntl  import ioctl
from socket import socket, inet_ntoa, AF_INET, SOCK_DGRAM, gethostname
from struct import pack
from time   import sleep
from shutil import which


#-------------------------------------------------------------------------------
# system class
#-------------------------------------------------------------------------------
class system():

    # skronk version
    version = 0.9

    # constructor
    def __init__( self ):

        # linux process name
        with open( '/proc/self/comm', 'w' ) as f: f.write( 'skronk' )

        # check for pd and rnbo
        self.has_pd   = which( '/usr/bin/pd' )
        self.has_rnbo = which( '/usr/bin/rnbooscquery' )

        # object handles
        self.adc1  = None
        self.adc2  = None
        self.disp  = None
        self.event = None
        self.menu  = None
        self.osc   = None
        self.pd    = None
        self.read  = None
        self.rnbo  = None
        self.sw    = None

        # install signal callbacks
        signal( SIGHUP,  self.sig )
        signal( SIGINT,  self.sig )
        signal( SIGQUIT, self.sig )
        signal( SIGABRT, self.sig )
        signal( SIGTERM, self.sig )

        # cpu percent calc vars
        self.work = 0
        self.idle = 0

    # command - command handler ( args is list of words/values )
    def command( self, *args ):
        if args[ 0 ] == 'off':
            self.shutdown()

    # ip - ip address string ( name: 'eth0', 'wlan0' )
    def ip( self, name ):
        sock  = socket( AF_INET, SOCK_DGRAM )
        iface = pack( '256s', name.encode( 'utf_8' ) )
        try:
            addr = inet_ntoa( ioctl( sock.fileno(), 0x8915, iface )[ 20 : 24 ] )
        except:
            addr = '0:0:0:0'
        return addr

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
        self.disp.write( 0, 0, self.hostname() )
        self.disp.write( 0, 1, self.ip( 'wlan0' ) )
        self.disp.write( 0, 2, self.mac( 'wlan0' ) )
        self.disp.write( 0, 3, 'skronk firmware ' + str( self.version ) )

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
        sleep( 0.5 )
        self.disp.shutdown()
        sys_exit()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------

