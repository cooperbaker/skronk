#-------------------------------------------------------------------------------
# menu.py
# Menu object for skronk
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from .thread     import thread
from .menus.net  import net
from .menus.pd   import pd
from .menus.rnbo import rnbo
from .menus.stat import stat


#-------------------------------------------------------------------------------
# menu class
#-------------------------------------------------------------------------------
class menu():

    # toggle switch for menu activation
    MENU_SWITCH = 17

    # tick rate
    TICK_MSEC = 333.333

    # constructor
    def __init__( self, skronk ):

        # store the skronk object
        self.skronk = skronk

        # create pages
        self.net  = net ( skronk )
        self.stat = stat( skronk )
        self.pd   = pd  ( skronk )
        self.rnbo = rnbo( skronk )

        # set up page navigation: nav( up, down, left, right )
        self.net.nav ( None, None, self.rnbo, self.stat )
        self.stat.nav( None, None, self.net,  self.pd   )
        self.pd.nav  ( None, None, self.stat, self.rnbo )
        self.rnbo.nav( None, None, self.pd,   self.net  )

        # current active page
        self.page = self.stat

        # visible flag
        self.visible = 0

        # page tick() thread
        self.tick_thread = thread( self.tick, self.TICK_MSEC )

    # tick - threaded callback to run visible page tick() method
    def tick( self ):
        if self.visible :
            self.page.tick()

    # stop - stop the tick thread
    def stop( self ):
        self.tick_thread.stop()

    # sw_event - switch event callback handler
    def sw_event( self, channel, value ):
        if ( channel == self.MENU_SWITCH ) and value :
            self.toggle()
        # only give events to page if menu is visible
        if self.visible and ( channel != self.MENU_SWITCH ) :
            self.page.sw_event( channel, value )

    # toggle - activate / deactivate the page
    def toggle( self ):
        # grip it and flip it
        self.visible = not( self.visible )
        if self.visible :
            self.page.tick()
            self.page.draw()
            self.skronk.disp.set_buffer( self.page.buffer )
        else :
            self.skronk.disp.set_buffer( self.skronk.disp.buffer )

    # set_page - set the active page
    def set_page( self, page ):
        if page :
            self.page = page
            if self.visible :
                self.page.tick()
                self.page.draw()
                self.skronk.disp.set_buffer( self.page.buffer )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
