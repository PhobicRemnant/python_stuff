#from re import M
#from select import select
from email.mime import image
import socket, pickle, cv2

class Debugger:

    def __init__(self, port, host): 

        self.port = port                                                # TCP port number
        self.host = host                                                # Host IPv4 addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Set a TCP/IP service
        self.buffsize = 1024*16                                         # 16KB buffer size
        self.headsize = 7                                               # 7 character to define a 7 digit decimal number 


    # VIEWER
    # init: Listen to port and wait for connections
    # get image
    # show image
    def view(self):
        """
            Declare debugger as a streamer and send a stream of data to another debugger in 
            viewer mode
        """
        # Bind the port to the Debugger's host and port and listen for connections
        self.s.bind((self.host,self.port))
        self.s.listen(5)

        while True:

            conn, addr = self.s.accept()
            print(f'Connection with {addr} has been stablished')
            print(f'Initializing video stream')

            # get the image data
            # format the data to image
            # show image
            # waitKey(N) where N gives FPS to the user

            

            
    # STREAMER
    def stream(self,file):
        
        # Get stream/camera for image data in this case a file
        stream = cv2.VideoCapture(file)  


        # get input image from the data processing
        # prepare image to be sent
        # send image to the server
        pass
    
    
    # READ SENT IMAGE
    def get_image(self):
        pass
    # SENT IMAGE DATA
    def show_image(self):
        pass

     
