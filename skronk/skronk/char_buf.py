#-------------------------------------------------------------------------------
# char_buf.py
# Character buffer
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

    # clear - fill the character buffer with spaces
    def clear( self ):
        self.buffer = ' ' * self.size

    # write - write a string into the character buffer at ( col, row ) location
    def write( self, col, row, string ):
        self.buffer = self.buffer[ 0 : col + row * self.cols ] + string + self.buffer[ col + row * self.cols + len( string ) : self.size ]


#-------------------------------------------------------------------------------
# eof
#-------------------------------------------------------------------------------
