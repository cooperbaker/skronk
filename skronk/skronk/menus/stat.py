#-------------------------------------------------------------------------------
# stat.py
# Menu page for skronk
# displays cpu percent, mem percent, cpu temperature
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from .page import page


#-------------------------------------------------------------------------------
# stat class
#-------------------------------------------------------------------------------
class stat( page ):

    # constructor
    def __init__( self, skronk ):
        super().__init__( skronk )

    # tick callback
    def tick( self ):
        self.draw()

    # draw page
    def draw( self ):
        self.clear()
                        #  ....................
                        #  STAT____________<12>
                        #  patch.filename......
                        #  cpu 99.9%.temp.99.9c
                        #  mem 99.9%...........
        self.write( 0, 0, 'STAT____________\x11\x01\x02\x10' )
        self.write( 0, 1, 'patch               ' )
        self.write( 0, 2, f'cpu { self.skronk.cpu() }% temp { self.skronk.temp() }c' )
        self.write( 0, 3, f'mem { self.skronk.mem() }%           ' )
        self.display()

    # sw1 - navigate left
    def sw1( self, value ):
        if value :
            self.left()

    # sw2 - navigate right
    def sw2( self, value ):
        if value :
            self.right()


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
