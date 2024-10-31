#-------------------------------------------------------------------------------
# display.py
# I2C driver for PCA8574 + HD44780 lcd or US2066 oled character displays
#
# disp = display(  'lcd', 16, 2, 10 ) : 16x2 lcd  @ 10fps
# disp = display( 'oled', 20, 4, 30 ) : 20x4 oled @ 30fps
#                                     : 20x4 full frame ≈ 25 msec i2c tx time
# Cooper Baker (c) 2024
#
# pylint: disable = line-too-long
#-------------------------------------------------------------------------------


# buffer overlay...

#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from threading import stack_size, Thread
from time import sleep, clock_gettime, CLOCK_MONOTONIC
from smbus2 import SMBus
from .buffer import buffer
from .utility import hello, goodbye


#-------------------------------------------------------------------------------
# display class
#-------------------------------------------------------------------------------
class display():

    # static i2c interface object
    i2c = SMBus( 1 )

    #---------------------------------------------------------------------------
    # constants
    #---------------------------------------------------------------------------
    LCD                       = 'lcd'   # HD44780 lcd controller with PCA8574 expander
    OLED                      = 'oled'  # US2066 oled controller
    LCD_I2C_ADDR              = 0x27    # default lcd i2c address
    OLED_I2C_ADDR             = 0x3c    # default oled i2c address
    OLED_COMMAND              = 0x80    # oled constants
    OLED_DATA                 = 0x40    #
    OLED_SET_BRIGHTNESS       = 0X81    #
    OLED_SET_FADE             = 0x23    # address for fade out command
    OLED_FADE_OFF             = 0X00    # value for fade off
    OLED_FADE_ON              = 0X20    # value for fade on
    OLED_FADE_BLINK           = 0X30    # value for fade blink
    LCD_BACKLIGHT_ON          = 0x08    # PCA8574 backlight on bit
    LCD_BACKLIGHT_OFF         = 0x00    # PCA8574 backlight off
    LCD_ENABLE_ON             = 0x04    # PCA8574 enable bit on
    LCD_ENABLE_OFF            = 0x00    # PCA8574 enable bit off
    LCD_READ                  = 0x02    # PCA8574 read bit
    LCD_WRITE                 = 0x00    # PCA8574 write bit
    LCD_DATA                  = 0x01    # PCA8574 data register select bit
    LCD_COMMAND               = 0x00    # PCA8574 command register select bit
    LCD_CLEAR_DISPLAY         = 0x01    # lcd commands
    LCD_RETURN_HOME           = 0x02    #
    LCD_ENTRY_MODE            = 0x04    #
    LCD_DISPLAY_CONTROL       = 0x08    #
    LCD_SHIFT                 = 0x10    #
    LCD_FUNCTION_SET          = 0x20    #
    LCD_SET_CGRAM_ADDR        = 0x40    #
    LCD_SET_DDRAM_ADDR        = 0x80    #
    LCD_DISPLAY_LEFT_TO_RIGHT = 0x02    # bits for entry_mode_cmd
    LCD_DISPLAY_RIGHT_TO_LEFT = 0X00    #
    LCD_DISPLAY_SHIFT_ON      = 0x01    #
    LCD_DISPLAY_SHIFT_OFF     = 0x00    #
    LCD_DISPLAY_ON            = 0x04    # bits for disp_ctl_cmd
    LCD_DISPLAY_OFF           = 0x00    #
    LCD_CURSOR_ON             = 0x02    #
    LCD_CURSOR_OFF            = 0x00    #
    LCD_CURSOR_BLINK_ON       = 0x01    #
    LCD_CURSOR_BLINK_OFF      = 0x00    #
    LCD_8_BIT_MODE            = 0x10    # bits for func_set_cmd
    LCD_4_BIT_MODE            = 0x00    #
    LCD_2_LINES               = 0x08    #
    LCD_1_LINE                = 0x00    #
    LCD_5x10_DOTS             = 0x04    #
    LCD_5x8_DOTS              = 0x00    #
    LCD_DISPLAY_SHIFT         = 0x08    # bits for shifting display and cursor
    LCD_CURSOR_SHIFT          = 0x00    #
    LCD_SHIFT_RIGHT           = 0x04    #
    LCD_SHIFT_LEFT            = 0x00    #

    #---------------------------------------------------------------------------
    # custom glyphs
    #---------------------------------------------------------------------------
    UP         = '\x00'
    UP_BYTES   = [  0b00000 ,
                    0b00100 ,
                    0b00100 ,
                    0b01110 ,
                    0b01110 ,
                    0b11111 ,
                    0b00000 ,
                    0b00000 ]

    DN         = '\x07'
    DN_BYTES   = [  0b00000 ,
                    0b11111 ,
                    0b01110 ,
                    0b01110 ,
                    0b00100 ,
                    0b00100 ,
                    0b00000 ,
                    0b00000 ]

    S1         = '\x01'
    S1_BYTES   = [  0b00000 ,
                    0b00100 ,
                    0b11100 ,
                    0b01100 ,
                    0b01100 ,
                    0b11110 ,
                    0b00000 ,
                    0b00000 ]
    S2         = '\x02'
    S2_BYTES   = [  0b00000 ,
                    0b01100 ,
                    0b11110 ,
                    0b00110 ,
                    0b01100 ,
                    0b11110 ,
                    0b00000 ,
                    0b00000 ]
    S3         = '\x03'
    S3_BYTES   = [  0b00000 ,
                    0b11110 ,
                    0b00100 ,
                    0b01110 ,
                    0b00110 ,
                    0b11100 ,
                    0b00000 ,
                    0b00000 ]
    S4         = '\x04'
    S4_BYTES   = [  0b00000 ,
                    0b00110 ,
                    0b01010 ,
                    0b10110 ,
                    0b11110 ,
                    0b00110 ,
                    0b00000 ,
                    0b00000 ]
    S5         = '\x05'
    S5_BYTES   = [  0b00000 ,
                    0b11110 ,
                    0b11000 ,
                    0b11110 ,
                    0b00110 ,
                    0b11100 ,
                    0b00000 ,
                    0b00000 ]
    S6         = '\x06'
    S6_BYTES   = [  0b00000 ,
                    0b01100 ,
                    0b11000 ,
                    0b11110 ,
                    0b11010 ,
                    0b01100 ,
                    0b00000 ,
                    0b00000 ]


    #---------------------------------------------------------------------------
    # constructor
    # display(  'lcd', 16, 2, 10 ) : 16x2 lcd  @ 10fps
    # display( 'oled', 20, 4, 30 ) : 20x4 oled @ 30fps
    #                              : 20x4 full frame ≈ 25 msec i2c tx time
    #---------------------------------------------------------------------------
    def __init__( self, type, cols, rows, fps ):

        self.spin           = True
        self.update         = False
        self.type           = type
        self.fps            = 1 / fps
        self.rows           = rows
        self.cols           = cols
        self.buffer         = buffer( cols, rows )
        self.draw_buffer    = self.buffer
        self.i2c_addr       = 0
        self.backlight_ctl  = self.LCD_BACKLIGHT_ON
        self.entry_mode_cmd = 0
        self.disp_ctl_cmd   = 0
        self.func_set_cmd   = 0

        if self.type == self.LCD:
            self.i2c_addr = self.LCD_I2C_ADDR
            self.init_lcd()
        elif self.type == self.OLED:
            self.i2c_addr = self.OLED_I2C_ADDR
            self.init_oled()

        self.store_glyph( 0, self.UP_BYTES )
        self.store_glyph( 7, self.DN_BYTES )
        self.store_glyph( 1, self.S1_BYTES )
        self.store_glyph( 2, self.S2_BYTES )
        self.store_glyph( 3, self.S3_BYTES )
        self.store_glyph( 4, self.S4_BYTES )
        self.store_glyph( 5, self.S5_BYTES )
        self.store_glyph( 6, self.S6_BYTES )

        stack_size( 65536 )
        Thread( target = self.run, name = 'display' ).start()
        hello( self )

    # command - command handler
    def command( self, *args ):
        if     args[ 0 ] == 'string':   # string 0 0 info                   ~ write info at ( column 0, row 0 )
            if args[ 1 ] == 'clear' :   # string clear 10 0 0 info          ~ clear 10 spaces at ( 0, 0 ) then write info
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' ' * int( args[ 2 ] ) )
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' '.join( map( str, args[ 5 : ] ) ) )
            else:
                self.write( int( args[ 1 ] ), int( args[ 2 ] ), ' '.join( map( str, args[ 3 : ] ) ) )
        elif   args[ 0 ] == 'int'   :   # int 0 0 label i                   ~ write label and int at ( 0, 0 )
            if args[ 1 ] == 'clear' :   # int clear 10 0 0 label i          ~ clear 10 spaces at ( 0, 0 ) then write label and int
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' ' * int( args[ 2 ] ) )
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' '.join( map( str, args[ 5 : -1 ] ) ) + ' {:.0f}'.format( args[ -1 ] ) )
            else:
                self.write( int( args[ 1 ] ), int( args[ 2 ] ), ' '.join( map( str, args[ 3 : -1 ] ) ) + ' {:.0f}'.format( args[ -1 ] ) )
        elif   args[ 0 ] == 'float' :   # float 0 0 label f                 ~ write label and float at ( 0, 0 )
            if args[ 1 ] == 'clear' :   # float clear 10 0 0 label f        ~ clear 10 spaces at ( 0, 0 ) then write label and float
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' ' * int( args[ 2 ] ) )
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' '.join( map( str, args[ 5 : -1 ] ) ) + ' {:.3f}'.format( args[ -1 ] ) )
            else:
                self.write( int( args[ 1 ] ), int( args[ 2 ] ), ' '.join( map( str, args[ 3 : -1 ] ) ) + ' {:.3f}'.format( args[ -1 ] ) )
        elif   args[ 0 ] == 'list'  :   # list 0 0 a b c i                  ~ write item i at ( 0, 0 )
            if args[ 1 ] == 'clear' :   # list clear 10 0 0 a b c i         ~ clear 10 spaces at ( 0, 0 ) then write item i
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), ' ' * int( args[ 2 ] ) )
                self.write( int( args[ 3 ] ), int( args[ 4 ] ), str( args[ int( args[ -1 ] ) + 5 ] ) )
            else:
                self.write( int( args[ 1 ] ), int( args[ 2 ] ), str( args[ int( args[ -1 ] ) + 3 ] ) )
        elif   args[ 0 ] == 'format':   # format 3.1f 0 0 label n           ~ write label and formatted number at ( 0, 0 )
            if args[ 1 ] == 'clear' :   # format clear 3.1f 10 0 0 label n  ~ clear 10 spaces at ( 0, 0 ) then write label and formatted number
                self.write( int( args[ 4 ] ), int( args[ 5 ] ), ' ' * int( args[ 3 ] ) )
                self.write( int( args[ 4 ] ), int( args[ 5 ] ), ' '.join( map( str, args[ 6 : -1 ] ) ) + ( ' {:' + args[ 2 ] + '}' ).format( args[ -1 ] ) )
            else:
                self.write( int( args[ 2 ] ), int( args[ 3 ] ), ' '.join( map( str, args[ 4 : -1 ] ) ) + ( ' {:' + args[ 1 ] + '}' ).format( args[ -1 ] ) )
        elif args[ 0 ] == 'clear'   :   # clear the display
            self.clear()
        elif args[ 0 ] == 'on'      :   # turn on the display
            self.on()
        elif args[ 0 ] == 'off'     :   # turn off the display
            self.off()


    #---------------------------------------------------------------------------
    # character buffer methods
    #---------------------------------------------------------------------------
    # write - write a string to the internal character buffer at ( col, row ) location
    def write( self, col, row, string ):
        self.buffer.write( col, row, string )
        self.update = True

    # clear - clear the internal character buffer
    def clear( self ):
        self.buffer.clear()
        self.update = True

    # draw - draw the draw_buffer to the display
    def draw( self ):
        self.update = True

    # set_buffer - set the buffer to draw to the display (internal or external)
    def set_buffer( self, buffer ):
        self.draw_buffer = buffer
        self.update = True

    # run - character buffer draw thread callback at fps interval
    def run( self ):
        start_time = 0
        while self.spin:
            start_time = clock_gettime( CLOCK_MONOTONIC )
            if self.update:
                self.update = False
                buffer = str( self.draw_buffer.buffer )
                # 4 row lcd needs interleaved rows
                if ( self.rows == 4 ) and ( self.type == self.LCD ) :
                    buffer = buffer[ 0 : 20 ] + buffer[ 40 : 60 ] + buffer[ 20 : 40 ] + buffer[ 60 : 80 ]
                self.home()
                for char in buffer:
                    self.data( ord( char ) )
            sleep( max( 0, self.fps - ( clock_gettime( CLOCK_MONOTONIC ) - start_time ) ) )

    # shutdown - stop draw thread and turn off display
    def shutdown( self ):
        goodbye( self )
        sleep( 0.5 )
        self.spin = False
        if self.type == 'lcd'  :
            self.backlight_off()
        if self.type == 'oled' :
            self.brightness( 0 )
        self.clear()
        self.off()


    #---------------------------------------------------------------------------
    # direct draw methods
    #---------------------------------------------------------------------------

    # write - write an ascii character (value) to the display
    def write_char( self, value ):
        self.data( ord( value ) ) # maybe do ord() with numpy?

    # write a string ( formatting options - https:#mkaz.tech/python-string-format.html )
    def write_string( self, value ):
        for char in value:
            self.write_char( char )

    # clear - clear the display
    def clear_disp( self ):
        self.cmd( self.LCD_CLEAR_DISPLAY )
        sleep( 0.002 ) # 1.53ms pause

    # home - move cursor to upper left corner
    def home( self ):
        self.move( 0, 0 )

    # move - move cursor to ( col, row )
    def move( self, col, row ):
        if row > self.rows :
            row = self.rows
        if self.rows <= 2 :
            row_offset = [ 0x00, 0x40 ]
            self.cmd( self.LCD_SET_DDRAM_ADDR | ( col + row_offset[ row ] ) )
        else:
            if self.type == self.LCD :
                row_offset = [ 0x00, 0x40, 0x14, 0x54 ]
                self.cmd( self.LCD_SET_DDRAM_ADDR | ( col + row_offset[ row ] ) )
            else:
                row_offset = [ 0x00, 0x20, 0x40, 0x60 ]
                self.cmd( self.LCD_SET_DDRAM_ADDR | ( col + row_offset[ row ] ) )

    # off - display off
    def off( self ):
        if self.type == self.LCD :
            self.backlight_off()
        self.disp_ctl_cmd &= ~self.LCD_DISPLAY_ON
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

    # on - display on
    def on( self ):
        if self.type == self.LCD :
            self.backlight_on()
        self.disp_ctl_cmd |= self.LCD_DISPLAY_ON
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

    # cursor_off - hide cursor
    def cursor_off( self ):
        self.disp_ctl_cmd &= ~self.LCD_CURSOR_ON
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

    # cursor_on - show cursor
    def cursor_on( self ):
        self.disp_ctl_cmd |= self.LCD_CURSOR_ON
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

    # cursor_blink_off - solid cursor
    def cursor_blink_off( self ):
        self.disp_ctl_cmd &= ~self.LCD_CURSOR_BLINK_ON
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

    # cursor_blink_on - blinking cursor
    def cursor_blink_on( self ):
        self.disp_ctl_cmd |= self.LCD_CURSOR_BLINK_ON
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

    # display_shift_left - shift display and cursor left
    def display_shift_left( self ):
        self.cmd( self.LCD_SHIFT | self.LCD_DISPLAY_SHIFT | self.LCD_SHIFT_LEFT )

    # display_shift_left - shift display and cursor right
    def display_shift_right( self ):
        self.cmd( self.LCD_SHIFT | self.LCD_DISPLAY_SHIFT | self.LCD_SHIFT_RIGHT )

    # cursor_shift_left - shift cursor left and change the address counter
    def cursor_shift_left( self ):
        self.cmd( self.LCD_SHIFT | self.LCD_CURSOR_SHIFT | self.LCD_SHIFT_LEFT )

    # cursor_shift_right - shift cursor right and change the address counter
    def cursor_shift_right( self ):
        self.cmd( self.LCD_SHIFT | self.LCD_CURSOR_SHIFT | self.LCD_SHIFT_RIGHT )

    # left_to_right - set text flow left to right ( default )
    def left_to_right( self ):
        self.entry_mode_cmd |= self.LCD_DISPLAY_LEFT_TO_RIGHT
        self.cmd( self.LCD_ENTRY_MODE |self.entry_mode_cmd )

    # right_to_left - set text flow right to left
    def right_to_left( self ):
        self.entry_mode_cmd &= ~self.LCD_DISPLAY_LEFT_TO_RIGHT
        self.cmd( self.LCD_ENTRY_MODE |self.entry_mode_cmd )

    # display_shift_on - shift entire display by newly written characters
    def display_shift_on( self ):
        self.entry_mode_cmd |= self.LCD_DISPLAY_SHIFT_ON
        self.cmd( self.LCD_ENTRY_MODE |self.entry_mode_cmd )

    # display_shift_off - newly written characters do not shift entire display ( default )
    def display_shift_off( self ):
        self.entry_mode_cmd &= ~self.LCD_DISPLAY_SHIFT_ON
        self.cmd( self.LCD_ENTRY_MODE |self.entry_mode_cmd )

    # store_char - store a custom character in display CGRAM ( address: 0 - 7 )
    def store_glyph( self, address, map ):
        address &= 0x7
        self.cmd( self.LCD_SET_CGRAM_ADDR | ( address << 3 ) )
        for i in range( 8 ):
            self.data( map[ i ] )

    # backlight_off - turn the backlight off ( lcd only )
    def backlight_off( self ):
        self.backlight_ctl = self.LCD_BACKLIGHT_OFF
        self.lcd_byte( self.backlight_ctl )

    # backlight_on - turn the backlight on ( lcd only )
    def backlight_on( self ):
        self.backlight_ctl = self.LCD_BACKLIGHT_ON
        self.lcd_byte( self.backlight_ctl )

    # oled_cmd_start - send bytes to start an oled command
    def oled_cmd_start( self ):
        self.cmd( 0x80 )
        self.cmd( 0x2A ) # set RE = 1
        self.cmd( 0x80 )
        self.cmd( 0x79 ) # set SD = 1

    # oled_cmd_stop - send bytes to stop an oled command
    def oled_cmd_stop( self ):
        self.cmd( 0x80 )
        self.cmd( 0x78 ) # set SD = 0
        self.cmd( 0x80 )
        self.cmd( 0x28 ) # set RE = 0

    # brightness - set display brightness ( oled only )
    def brightness( self, value ):
        self.oled_cmd_start()
        self.cmd( self.OLED_SET_BRIGHTNESS )
        self.cmd( value )
        self.oled_cmd_stop()

    # fade_off - turn off fade ( oled only )
    def fade_off( self ):
        self.oled_cmd_start()
        self.cmd( self.OLED_SET_FADE )
        self.cmd( self.OLED_FADE_OFF )
        self.oled_cmd_stop()

    # fade_once - turn on fade once ( rate: 0 - 15 ) ( oled only )
    def fade_once( self, rate ):
        self.oled_cmd_start()
        self.cmd( self.OLED_SET_FADE )
        self.cmd( self.OLED_FADE_ON | ( 0x0f & rate ) )
        self.oled_cmd_stop()

    # fade_blink - turn on fade blink ( rate: 0 - 15 ) ( oled only )
    def fade_blink( self, rate ):
        self.oled_cmd_start()
        self.cmd( self.OLED_SET_FADE )
        self.cmd( self.OLED_FADE_BLINK | ( 0x0f & rate ) )
        self.oled_cmd_stop()


    #---------------------------------------------------------------------------
    # internal methods
    #---------------------------------------------------------------------------

    # cmd - send a command to the display
    def cmd( self, command ):
        if self.type == self.LCD :
            self.lcd_cmd( command )
        elif self.type == self.OLED :
            self.oled_cmd( command )

    # data - send data to the display
    def data( self, data ):
        if self.type == self.LCD :
            self.lcd_data( data )
        elif self.type == self.OLED :
            self.oled_data( data )

    # lcd_byte - send one byte to the LCD module
    def lcd_byte( self, byte ):
        self.i2c.write_byte( self.i2c_addr, byte )

    # lcd_cmd - send a command to the lcd
    def lcd_cmd( self, command ):
        lsb = (   command         & 0xf0) | self.backlight_ctl | self.LCD_COMMAND
        msb = ( ( command << 4 )  & 0xf0) | self.backlight_ctl | self.LCD_COMMAND
        self.lcd_byte( lsb                      )   # write 4 bits with enable bit cleared
        self.lcd_byte( lsb | self.LCD_ENABLE_ON )   # write 4 bits with enable bit set
        self.lcd_byte( lsb                      )   # write 4 bits with enable bit cleared
        self.lcd_byte( msb                      )   # write 4 bits with enable bit cleared
        self.lcd_byte( msb | self.LCD_ENABLE_ON )   # write 4 bits with enable bit set
        self.lcd_byte( msb                      )   # write 4 bits with enable bit cleared

    # lcd_data - send data to the lcd
    def lcd_data( self, data ):
        lsb = (   data         & 0xf0) | self.backlight_ctl | self.LCD_DATA
        msb = ( ( data << 4 )  & 0xf0) | self.backlight_ctl | self.LCD_DATA
        self.lcd_byte( lsb                      )   # write 4 bits with enable bit cleared
        self.lcd_byte( lsb | self.LCD_ENABLE_ON )   # write 4 bits with enable bit set
        self.lcd_byte( lsb                      )   # write 4 bits with enable bit cleared
        self.lcd_byte( msb                      )   # write 4 bits with enable bit cleared
        self.lcd_byte( msb | self.LCD_ENABLE_ON )   # write 4 bits with enable bit set
        self.lcd_byte( msb                      )   # write 4 bits with enable bit cleared

    # oled_cmd - send an oled command
    def oled_cmd( self, command ):
            self.i2c.write_byte_data( self.i2c_addr, self.OLED_COMMAND, command )

    # oled_data - send oled data
    def oled_data( self, data ):
            self.i2c.write_byte_data( self.i2c_addr, self.OLED_DATA, data )

    # init_oled - initialize the oled display
    def init_oled( self ):
        sleep( 0.1 )            # wait for the display to power up
        self.cmd ( 0x2A )       # Set RE bit ( RE = 1, IS = 0, SD = 0 )
        self.cmd ( 0x71 )       # Function Selection A
        self.data( 0x5C )       # 5C = enable regulator ( 5V I/O ), 00 = disable regulator ( 3.3V I/O )
        self.cmd ( 0x28 )       # Clear RE bit ( RE = 0, IS = 0, SD = 0 )
        self.cmd ( 0x08 )       # Sleep Mode On ( display, cursor, blink = off ) during this setup
        self.cmd ( 0x2A )       # Set RE bit ( RE = 1, IS = 0, SD = 0 )
        self.cmd ( 0x79 )       # Set SD bit ( RE = 1, IS = 0, SD = 1 )
        self.cmd ( 0xD5 )       # Set Display Clock Divide Ratio / Oscillator Frequency
        self.cmd ( 0x70 )       # --> set the Freq to 70h
        self.cmd ( 0x78 )       # Clear SD bit ( RE = 1, IS = 0, SD = 0 )
        if( self.rows > 2 ):    # Extended Function Set:
            self.cmd( 0x09 )    # Set 5 x 8 chars, display inversion cleared, 3 / 4 line display
        else:
            self.cmd( 0x08 )    # Set 5 x 8 chars, cursor inversion cleared, 1 / 2 line display
        self.cmd ( 0x06 )       # Set Advanced Entry Mode: COM0 -> COM31, SEG99 -> SEG0
        self.cmd ( 0x72 )       # Function Selection B:
        # self.data( 0x00 )       # --> Select ROM A and CGRAM 8 ( which allows for custom characters )
        self.data( 0x04 )       # --> Select ROM B and CGRAM 8 ( which allows for custom characters )
        # self.data( 0x08 )       # --> Select ROM C and CGRAM 8 ( which allows for custom characters )
        self.cmd ( 0x79 )       # Set SD bit ( RE = 1, IS = 0, SD = 1 )
        self.cmd ( 0xDA )       # Set SEG Pins Hardware Configuration:
        self.cmd ( 0x10 )       # --> Enable SEG Left, Seq SEG pin config
        self.cmd ( 0xDC )       # Function Selection C
        self.cmd ( 0x00 )       # --> Internal VSL, GPIO pin HiZ, input disabled
        self.cmd ( 0x81 )       # Set Contrast ( brightness )
        self.cmd ( 0xFF )       # --> max value = 0xFF
        self.cmd ( 0xD9 )       # Set Phase Length
        self.cmd ( 0xF1 )       # --> Phase 2 = 15 ( 0xF0 ), Phase 1 = 1 ( power on = 0x78 )
        self.cmd ( 0xDB )       # set VCOMH deselect Level
        self.cmd ( 0x40 )       # --> 1 x Vcc ( previously 0x30 )
        self.cmd ( 0x78 )       # Clear SD bit ( RE = 1, IS = 0, SD = 0 )
        self.cmd ( 0x28 )       # Clear RE and IS ( RE = 0, IS = 0, SD = 0 )
        self.cmd ( 0x01 )       # clear display
        self.cmd ( 0x80 )       # Set DDRAM Address to 0x80 ( line 1 start )
        sleep( 0.1 )            # let the display settle

        # function set command
        self.func_set_cmd = self.LCD_1_LINE | self.LCD_5x8_DOTS
        if( self.rows > 1 ): self.func_set_cmd |= self.LCD_2_LINES
        self.cmd( self.LCD_FUNCTION_SET | self.func_set_cmd )

        # display control - display on, no cursor, no blinking
        self.disp_ctl_cmd = self.LCD_DISPLAY_ON | self.LCD_CURSOR_OFF | self.LCD_CURSOR_BLINK_OFF
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

        # entry mode command - left to right, shift off
        self.entry_mode_cmd = self.LCD_DISPLAY_LEFT_TO_RIGHT | self.LCD_DISPLAY_SHIFT_OFF
        self.cmd( self.LCD_ENTRY_MODE | self.entry_mode_cmd )

        # clear the display
        self.clear()
        self.home()

    # init_lcd - initialize the lcd display
    def init_lcd( self ):
        sleep(.100)                                 # wait for lcd to power up
        data = self.backlight_ctl                   # set all of the outputs on the PCA8574 chip to 0, except the backlight bit if on
        self.lcd_byte( self.backlight_ctl )
        sleep( 1 )
        data = 0x30 | self.backlight_ctl            # put lcd in 4 bit mode
        self.lcd_byte( data )
        self.lcd_byte( data | self.LCD_ENABLE_ON )  # set the enable bit and write again
        sleep(.001)
        self.lcd_byte( data | self.LCD_ENABLE_OFF ) # clear the enable bit and write again
        sleep(.004300)                              # wait min 4.1ms
        data = 0x30 | self.backlight_ctl            # put lcd in 4 bit mode again
        self.lcd_byte( data )
        self.lcd_byte( data | self.LCD_ENABLE_ON )  # set the enable bit and write again
        sleep(.001)
        self.lcd_byte( data | self.LCD_ENABLE_OFF ) # clear the enable bit and write again
        sleep(.004300)                              # wait min 4.1ms
        data = 0x30 | self.backlight_ctl            # put lcd in 4 bit mode again
        self.lcd_byte( data )
        self.lcd_byte( data | self.LCD_ENABLE_ON )  # set the enable bit and write again
        sleep(.001)
        self.lcd_byte( data | self.LCD_ENABLE_OFF ) # clear the enable bit and write again
        sleep(.004300)                              # wait min 4.1ms
        data = 0x20 | self.backlight_ctl            # set up 4 bit interface
        self.lcd_byte( data )
        self.lcd_byte( data | self.LCD_ENABLE_ON )  # set the enable bit and write again
        sleep(.001)
        self.lcd_byte( data | self.LCD_ENABLE_OFF ) # clear the enable bit and write again
        sleep(.001)

        # function set command
        self.func_set_cmd = self.LCD_4_BIT_MODE | self.LCD_1_LINE | self.LCD_5x8_DOTS
        if self.rows > 1: self.func_set_cmd |= self.LCD_2_LINES

        self.cmd( self.LCD_FUNCTION_SET | self.func_set_cmd )

        # display control - display on, no cursor, no blinking
        self.disp_ctl_cmd = self.LCD_DISPLAY_ON | self.LCD_CURSOR_OFF | self.LCD_CURSOR_BLINK_OFF
        self.cmd( self.LCD_DISPLAY_CONTROL | self.disp_ctl_cmd )

        # entry mode command - left to right, shift off
        self.entry_mode_cmd = self.LCD_DISPLAY_LEFT_TO_RIGHT | self.LCD_DISPLAY_SHIFT_OFF
        self.cmd( self.LCD_ENTRY_MODE | self.entry_mode_cmd )

        # clear the display
        self.clear()
        self.home()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
