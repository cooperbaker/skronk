#-------------------------------------------------------------------------------
# stat.py
# Menu page for system status
#
# displays cpu percent, mem percent, cpu temperature
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# imports
#-------------------------------------------------------------------------------
from .page import page
from ..utility import cpu, mem, temp

#-------------------------------------------------------------------------------
# stat class
#-------------------------------------------------------------------------------
class stat( page ):

    # constructor
    def __init__( self, system ):
        super().__init__( system )

        self.cpu = cpu()

    # tick callback
    def tick( self ):
        self.draw()

    # draw page
    def draw( self ):
        self.clear()
                        #  ....................
                        #  STAT____________<12>
                        #  ....................
                        #  cpu 99.9%.temp.99.9c
                        #  mem 99.9%...........
        self.write( 0, 0, 'STAT____________\x11\x01\x02\x10' )
        self.write( 0, 1, '                    ' )
        self.write( 0, 2, f'cpu { self.cpu.stat() }% temp { temp() }c' )
        self.write( 0, 3, f'mem { mem() }%           ' )
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
