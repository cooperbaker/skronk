#-------------------------------------------------------------------------------
# page.py
# Superclass for menu pages
#
# Cooper Baker (c) 2024
# pylint: disable = multiple-statements
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from ..buffer import buffer


#-------------------------------------------------------------------------------
# page class
#-------------------------------------------------------------------------------
class page():

    # display dimensions
    PAGE_COLS = 20
    PAGE_ROWS = 4

    # constructor
    def __init__( self, skronk ):

        # skronk object
        self.skronk = skronk

        # menu navigation
        self.up_page    = None
        self.down_page  = None
        self.left_page  = None
        self.right_page = None

        # page display buffer
        self.buffer = buffer( self.PAGE_COLS, self.PAGE_ROWS )

        # sugar lets you type less
        self.write   = self.buffer.write   # write to the page buffer
        self.clear   = self.buffer.clear   # clear the page buffer
        self.display = skronk.disp.draw    # display the page buffer

    # nav - configure page navigation
    def nav( self, up, down, left, right ):
        self.up_page    = up
        self.down_page  = down
        self.left_page  = left
        self.right_page = right

    # navigation - go to a page
    def up   ( self ): self.skronk.menu.set_page( self.up_page    )
    def down ( self ): self.skronk.menu.set_page( self.down_page  )
    def left ( self ): self.skronk.menu.set_page( self.left_page  )
    def right( self ): self.skronk.menu.set_page( self.right_page )

    # draw - draw the page
    def draw( self ): pass

    # tick - run repeatedly when page is active
    def tick( self ): pass

    # sw## - switch event callbacks
    def sw1 ( self, value ): pass
    def sw2 ( self, value ): pass
    def sw3 ( self, value ): pass
    def sw4 ( self, value ): pass
    def sw5 ( self, value ): pass
    def sw6 ( self, value ): pass
    def sw7 ( self, value ): pass
    def sw8 ( self, value ): pass
    def sw9 ( self, value ): pass
    def sw10( self, value ): pass
    def sw11( self, value ): pass
    def sw12( self, value ): pass
    def sw13( self, value ): pass
    def sw14( self, value ): pass
    def sw15( self, value ): pass
    def sw16( self, value ): pass
    def sw17( self, value ): pass

    # sw_event - route switch event callbacks
    def sw_event( self, channel, value ):
        if   channel ==  1 : self.sw1 ( value )
        elif channel ==  2 : self.sw2 ( value )
        elif channel ==  3 : self.sw3 ( value )
        elif channel ==  4 : self.sw4 ( value )
        elif channel ==  5 : self.sw5 ( value )
        elif channel ==  6 : self.sw6 ( value )
        elif channel ==  7 : self.sw7 ( value )
        elif channel ==  8 : self.sw8 ( value )
        elif channel ==  9 : self.sw9 ( value )
        elif channel == 10 : self.sw10( value )
        elif channel == 11 : self.sw11( value )
        elif channel == 12 : self.sw12( value )
        elif channel == 13 : self.sw13( value )
        elif channel == 14 : self.sw14( value )
        elif channel == 15 : self.sw15( value )
        elif channel == 16 : self.sw16( value )
        elif channel == 17 : self.sw17( value )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
