import socket, pickle, cv2, struct
from os import system
from enum import Enum

__version__ = "0.1v"

class networkNode:

    """
    Main TCP/IP communication class that defines a data transmission node serving as client or server.

    Args:

    + port: The port numbner for the socket   -> 5678 by default
    + host: The host IP for the socker        -> localhost by default

    """

    def __init__(self, port=5678, host="localhost", buffsize=1024*24): 

        self.port = port                                                # TCP port number
        self.host = host                                                # Host IPv4 addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Set a TCP/IP service
        self.buffsize = buffsize                                        # 16KB buffer size
        self.VGA_RES = (640,480)
        self.data = b''                                                 # Data buffer
        self.status = None                                              # Node status: Server/Client
        self.conn = None                                                # Client socket connection (Server)
        self.addr = None                                                # Client socket address    (Server)
        self.n_type = None                                              # Node definition type as a client or a server

    def packFrame(self,frame):
        """
        Pack frame to be sent over a socket
        """
        # Resize in VGA resolution
        frame = cv2.resize(frame,dsize=self.VGA_RES)                           
        # Serialize frame data 
        msg = pickle.dumps(frame)
        print(len(msg))
        # Pack data with a header that contains the data lenght
        pkg = struct.pack("Q", len(msg)) + msg
        
        return pkg
    # Streamer client
    def send_frame(self, frame):
        """
            Send debugger in streamer mode, this will connect the debugger with a viewer server
            and start sending video data.

            Args: 
            + frame : OpenCV frame, usually a numpy.array type
        """            
        # Prepare frame for packing
        pkg = self.packFrame(frame)
            
        # Try to send data to viewer if the channel is open
        #try:
            # Send data to viewer
        self.s.sendall(pkg)      
    
    def clientConnect(self):
        try:
            # Connect to server
            self.s.connect((self.host, self.port))
            print("Connection to viewer successful")
            self.status = self.StramerStatus.STREAMING
        except:
            # Stop streaming and exit
            print("No viewer connected\nShutting down...")
            return
        
    def serverWaitConn(self):
        # Wait for viewer
        self.conn, addr = self.s.accept()
        print(f'Client {addr[0]} connected in {addr[1]}.')
        print(f'Starting video feed...')
        self.status = self.ViewerStatus.PLAYING

    def serverSideClose(self):
        # Outside the loop 
        print("Connection terminated")
        # Close connection with client since the stream has ended
        self.conn.close()
    # Viewer Server
    def wait_for_frame(self):
        """
        Set debugger in viewer mode, the debugger will wait for a client to send a stream.  
        Will stop playing once the stream stops.
        """

 
        # Wait for the sent payload data
        # Payload size of 8 bytes
        while len(self.data) < struct.calcsize("Q"):
            # Read from buffer
            pkg = self.conn.recv(self.buffsize)   
            if not pkg: break
            # Append to received data 
            self.data += pkg

        # Get the packet data size
        packet_data_size = self.data[:struct.calcsize("Q")]
        # Separate data_size from header
        self.data = self.data[struct.calcsize("Q"):]
        
        
        try:
            # Get data size
            msg_size = struct.unpack("Q", packet_data_size)[0]
            # Wait for buffer to fill up to the sent data size
        except Exception as exc:
            print(f"Exception: {exc}")
            print("Stream sender disconnected")
            print("Going back to listening mode")
            self.status = ViewerStatus.LISTEN
            return 

        while len(self.data) < msg_size:
            # Read from buffer
            self.data += self.conn.recv(self.buffsize)

        # Get the message data
        msg = self.data[:msg_size]
        # Store the read data to be read on the next iteration
        self.data = self.data[msg_size:]
        # Get the sent frame
        frame = pickle.loads(msg)

        # Show frame to local screen debug
        cv2.imshow("Video Feed",frame)
        # Set 60FPS in the video display
        cv2.waitKey(16)   
                
    def listen(self):

        print("Debugger entering listening mode")
        print("Listening...")
        # Bind socket to port and host
        self.s.bind((self.host, self.port)) 
        # Enter listening mode
        self.status = self.ViewerStatus.LISTEN
        self.s.listen(5)

    def displayExit():
        # After the loop release the cap object
        cv2.destroyAllWindows()

    def close(self,):
        """
        Close 
        """
        print("Shutting down")
        # Close transmission with server
        self.s.shutdown(socket.SHUT_RD)
        self.s.close()

    class ViewerStatus(Enum):
        """
        Different status of a listening debugger
        """
        IDLE = 0        # Not connected
        LISTEN = 1      # Waiting for connection
        PLAYING = 2     # Playing video feed from streamer

    class StramerStatus(Enum):
        """
        Different status of a streaming debugger
        """
        IDLE = 0        # Not connected
        STREAMING = 1   # Sending frames to viewer server
