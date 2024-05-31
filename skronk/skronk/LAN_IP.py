#-------------------------------------------------------------------------------
# LAN_IP.py
# Reports local area network wifi ip address of a raspberry pi
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
import fcntl
import socket
import struct


#-------------------------------------------------------------------------------
# lan_ip - returns local network ip address of wlan0
#-------------------------------------------------------------------------------
def lan_ip():
    sock         = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    packed_iface = struct.pack( '256s', 'wlan0'.encode( 'utf_8' ) )
    packed_addr  = fcntl.ioctl( sock.fileno(), 0x8915, packed_iface )[ 20 : 24 ]

    return socket.inet_ntoa( packed_addr )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
