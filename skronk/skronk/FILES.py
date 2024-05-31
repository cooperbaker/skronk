import os


class files():

    def __init__( self ):
        self.list = []

    def ls( self, path ):
        self.list = os.listdir( path )
        print( self.list )

