import os
import subprocess
import signal



class pure_data():

    def __init__( self, path ):
        self.path = path
        self.file = ''
        self.list = []
        self.proc = 0

    def ls( self ):
        self.list = os.listdir( self.path )
        print( self.list )

    def run( self, file ):
        self.file = file
        # self.proc = subprocess.Popen( 'sudo /usr/bin/pd -nogui -alsa ' + self.path + '/'+ self.file, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # self.proc = subprocess.Popen( 'sudo /usr/bin/pd -nogui -alsa ' + self.path + '/'+ self.file, shell=True, stdin=subprocess.PIPE )
        # self.proc = subprocess.Popen( 'sudo /usr/bin/pd -nogui -alsa ', shell=True, stdin=subprocess.PIPE )

        self.proc = subprocess.Popen( 'sudo /usr/bin/pd -nogui -alsa ' + self.path + '/'+ self.file, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid )


        # self.proc = subprocess.Popen( 'sudo /usr/bin/pd -nogui -alsa ' + self.path + '/'+ self.file )

    def stop( self ):

### ??? HOW TO QUIT ? KILL ? UNLOAD

        os.killpg( os.getpgid( self.proc.pid ), signal.SIGTERM )

        self.proc.terminate()

        self.proc.kill()

        # os.killpg(os.getpgid( self.proc.pid), signal.SIGTERM)
        # self.proc.terminate()
        # self.proc.kill()

        # self.proc.send_signal( 15 )
        # self.proc.terminate()