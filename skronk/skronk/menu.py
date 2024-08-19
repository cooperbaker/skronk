from skronk.char_buf import char_buf

class page():

    def __init__( self ):
        self.buffer = char_buf( 20, 4 )
        self.draw()

    def draw( self ):
        self.buffer.write( 0, 0, '- Menu Page --------' )
        self.buffer.write( 0, 1, '--------------------' )
        self.buffer.write( 0, 2, '--------------------' )
        self.buffer.write( 0, 3, '--------------------' )

    # switch event callbacks
    def a( self ):
        pass
    def b( self ):
        pass
    def c( self ):
        pass
    def d( self ):
        pass
    def e( self ):
        pass
    def f( self ):
        pass
    def g( self ):
        pass
    def h( self ):
        pass

    # sw_event - select switch events and run callbacks
    def sw_event( self, channel, value ):
        if ( channel == 1 ) and value :
            self.a()
        if ( channel == 2 ) and value :
            self.b()
        if ( channel == 3 ) and value :
            self.c()
        if ( channel == 4 ) and value :
            self.d()
        if ( channel == 5 ) and value :
            self.e()
        if ( channel == 6 ) and value :
            self.f()
        if ( channel == 7 ) and value :
            self.g()
        if ( channel == 8 ) and value :
            self.h()

class menu():

    def __init__( self ):
        self.main = page()