# pylint: disable = bare-except
# pylint: disable = unspecified-encoding

from fcntl      import ioctl
from socket     import socket, inet_ntoa, AF_INET, SOCK_DGRAM, gethostname
from struct     import pack
from time       import sleep
from subprocess import check_output

# cpu - percent cpu usage string
class cpu():
    def __init__( self ):
        self.work = 0
        self.idle = 0

    def stat( self ):
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

# hostname - hostname string
def hostname():
    return gethostname()

# ip - ip address string ( name: 'eth0', 'wlan0' )
def ip( name ):
    sock  = socket( AF_INET, SOCK_DGRAM )
    iface = pack( '256s', name.encode( 'utf_8' ) )
    try:
        addr = inet_ntoa( ioctl( sock.fileno(), 0x8915, iface )[ 20 : 24 ] )
    except:
        addr = '0:0:0:0'
    return addr

# mac - mac address string ( interface_name: 'eth0', 'wlan0' )
def mac( interface_name ):
    f = open( '/sys/class/net/' + interface_name + '/address','r' )
    m = f.readline()
    f.close()
    return m

# mem - percent mem usage string
def mem():
    f     = open( '/proc/meminfo','r' )
    total = f.readline()
    free  = f.readline()
    f.close()
    total = total.split()
    free  = free.split()
    return '{:4.1f}'.format( float( free[ 1 ] ) / ( float( total[ 1 ] ) ) )

# ssid - name string of wifi access point
def ssid() :
    name = check_output( 'nmcli -c no -f ap.ssid device show wlan0', shell=True, text=True ).split()
    if name[ 1 ] :
        return name[ 1 ]
    return ''

# temp - cpu celsius degrees string
def temp():
    f = open( '/sys/class/thermal/thermal_zone0/temp' ) # millidegrees celsius
    c = f.readline()
    f.close()
    return '{:4.1f}'.format( float( c ) / 1000.0 )

# hello - show hello message
def hello( display ):
    display.clear()
    display.write( 7, 1, 'Hello' )
    if display.type is display.OLED :
        display.write(  0, 0, '\x17' )
        display.write( 19, 0, '\x17' )
        display.write(  0, 3, '\x17' )
        display.write( 19, 3, '\x17' )
    else :
        display.write(  0, 0, '\x91' )
        display.write( 19, 0, '\x91' )
        display.write(  0, 3, '\x91' )
        display.write( 19, 3, '\x91' )
    display.set_buffer( display.buffer )
    sleep( 0.5 )
    display.clear()

# goodbye - show goodbye message
def goodbye( display ):
    display.clear()
    display.write( 6, 1, 'Goodbye' )
    if display.type is display.OLED :
        display.write(  0, 0, '\x17' )
        display.write( 19, 0, '\x17' )
        display.write(  0, 3, '\x17' )
        display.write( 19, 3, '\x17' )
    else :
        display.write(  0, 0, '\x91' )
        display.write( 19, 0, '\x91' )
        display.write(  0, 3, '\x91' )
        display.write( 19, 3, '\x91' )
    display.set_buffer( display.buffer )
    sleep( 0.5 )