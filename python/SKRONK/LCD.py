import time
import threading
from RPLCD.i2c import CharLCD

class lcd_disp():
    def __init__( self, cols, rows, fps ):
        self.data   = False
        self.cols = cols
        self.rows = rows
        self.string = ' ' * rows * cols
        self.lcd    = CharLCD( i2c_expander='PCF8574', address=0x27, port=1, cols=cols, rows=rows, dotsize=8 )
        self.sleep  = 1 / fps
        self.thread = threading.Thread( target = self.draw )
        self.thread.start()

    def on( self ):
        self.lcd.backlight_enabled = True

    def off( self ):
        self.lcd.backlight_enabled = False

    def clear( self ):
        self.lcd.clear()

    def write( self, string ):
        self.write_xy( 0, 0, string )

    def write_xy( self, x, y, string ):
        str = self.string[ 0 : x + y * self.cols ] + string + self.string[ x + y * self.cols + len( string ) : len( self.string ) ]
        self.string = str
        self.data = True


    def draw( self ):
        while True:
            if self.data:
                string = self.string
                self.lcd.home()
                self.lcd.write_string( string )
                self.data = False
            time.sleep( self.sleep )

