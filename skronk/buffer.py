#-------------------------------------------------------------------------------
# buffer.py
#
# Skronk 2D Character Buffer
#
# Cooper Baker (c) 2024
# http://nyquist.dev/skronk
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# buffer class
#-------------------------------------------------------------------------------
class buffer():

    # constructor
    def __init__( self, cols, rows ):
        self.cols   = cols
        self.rows   = rows
        self.size   = self.cols * self.rows
        self.buffer = ' ' * self.size

    # clear - fill buffer with spaces
    def clear( self ):
        self.buffer = ' ' * self.size

    # write - write string into buffer at ( col, row ) location
    def write( self, col, row, string ):
        self.buffer = self.buffer[ 0 : col + row * self.cols ] + string + self.buffer[ col + row * self.cols + len( string ) : self.size ]

    # layer - mix buffer with internal buffer ( ' ' is transparent )
    def layer( self, buffer ):
        buf = []
        for top, bot in zip( buffer, self.buffer ):
            if top != ' ' :
                buf.append( top )
            else :
                buf.append( bot )
        self.buffer = ''.join( buf )


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
