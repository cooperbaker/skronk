from MCP3208 import mcp3208
import time

adc1 = mcp3208( 0, 0 )
adc2 = mcp3208( 0, 1 )

while True:
    values = [ 0 ] * 16

    for i in range( 8 ):
        values[ i ] = adc1.read( i )

    for i in range( 8, 15 ):
        values[ i ] = adc2.read( i - 8 )

    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} | {8:>4} | {9:>4} | {10:>4} | {11:>4} | {12:>4} | {13:>4} | {14:>4} | {15:>4} |'.format( * values ) )

    # Pause for a millisecond
    time.sleep(0.001)

