#-------------------------------------------------------------------------------
# char_buf.py
# 2D character buffer
#
# Cooper Baker (c) 2024
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# char_buf class
#-------------------------------------------------------------------------------
class char_buf():

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


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
