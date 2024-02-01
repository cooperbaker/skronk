from RPLCD.i2c import CharLCD
import time

lcd = CharLCD( i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8 )
lcd.clear()
lcd.write_string( 'skronk test' )

light = 1

while True:
    lcd.clear()
    lcd.write_string( 'skronk test' )
    lcd.backlight_enabled = True
    time.sleep( 0.8 )
    lcd.backlight_enabled = False
    time.sleep( 0.8 )
    lcd.clear()
    lcd.write_string( 'test skronk' )
    lcd.backlight_enabled = True
    time.sleep( 0.8 )
    lcd.backlight_enabled = False
    time.sleep( 0.8 )
