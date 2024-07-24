import os
from skronk.char_buf import char_buf


class files():

    def __init__( self ):
        self.list = ''
        self.path = ''
        self.buffer = char_buf( 20, 4 )

    def ls( self, path  ):
        self.path = path
        self.list = list( os.scandir( self.path ) )
        self.list.sort( key=lambda node: node.name )

        for item in self.list :
            if item.is_file():
                print( item.name )
            if item.is_dir():
                print( item.name + '/' )




