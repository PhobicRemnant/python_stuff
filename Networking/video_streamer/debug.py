import socket, pickle, cv2, struct
from os import system

class Debugger:

    """
    Main debugger class that defines a data transmission node, either in the viewer or streamer modes,
    serving as client or server.

    Args:

    + port: The port numbner for the socket   -> 5678 by default
    + host: The host IP for the socker        -> localhost by default

    """

    def __init__(self, port=5678, host="localhost"): 

        self.port = port                                                # TCP port number
        self.host = host                                                # Host IPv4 addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Set a TCP/IP service
        self.buffsize = 1024*24                                         # 16KB buffer size
        self.headsize = 7                                               # 7 character to define a 7 digit decimal number 
        self.VGA_RES = (640,480)

    # Streamer client
    def streamer(self, filepath, show=False):
        """
            Set debugger as a viewer server so a streamer client can connect and send
            any data stream.

            Args: None
        """

        def packFrame(frame):
            """
            Pack frame to be sent over a socket
            """
            # Resize in VGA resolution
            frame = cv2.resize(frame,dsize=self.VGA_RES)                           
            # Serialize frame data 
            msg = pickle.dumps(frame)
            # Pack data with a header that contains the data lenght
            pkg = struct.pack("Q", len(msg)) + msg
            
            return pkg

        try:
            # Connect to server
            self.s.connect((self.host, self.port))
            print("Connection to viewer successful")
        except:
            # Stop streaming and exit
            print("No viewer connected\nShutting down...")
            
            return

        # Get stream/camera for image data 
        stream = cv2.VideoCapture(filepath)  

        # Handle file access error
        if not stream.isOpened():
            print("Cannot open the file")
            exit()
        else:
            print("File opened...")

        # Stream loop
        while stream.isOpened():
            
            # Get processed frame
            ret, frame = stream.read()                             
            # Prepare frame for packing
            pkg = packFrame(frame)
                
            # Try to send data to viewer if the channel is open
            #try:
                # Send data to viewer
            self.s.sendall(pkg)
            """
            except:
                #Quit the streaming loop if en exception is raised
                print("Client disconnected.")
                break
            """
            # Enable visualization for the streamer
            if show:
                # Show frame to local screen debug
                cv2.imshow("Streamer Feed",frame) 
                if cv2.waitKey(15) & 0xFF == ord('q'):                  
                    break
    
        # Close transmission with server
        self.s.shutdown(socket.SHUT_RD)
        self.s.close()

        # Destroy all the windows
        cv2.destroyAllWindows()
                        
    # Viewer Server
    def viewer(self):
        """
        Set debugger as streamer, this will get capture from filepath(or camera) and stream the 
        data to a viewer
        """
        
        # Bind socket to port and host
        self.s.bind((self.host, self.port)) 
        self.s.listen(5)
        
        # Payload size as a 8 byte long number
        payload_size = struct.calcsize("Q")

        print("Entering viewer mode")
        # Viewer connection waiting loop
        while True:


            sel = input("Start viewer server?[Y/n]")

            if sel.lower() == "y":
            
                # Wait for viewer
                conn, addr = self.s.accept()
                print(f'Client {addr[0]} connected in {addr[1]}.')
                print(f'Starting video feed...')
                # Declare data to store bytes 
                data = b''

                while conn:
                
                    # Wait for the sent payload data
                    while len(data) < payload_size:
                        # Read from buffer
                        pkg = conn.recv(self.buffsize)   
                        if not pkg: break
                        # Append to received data 
                        data += pkg

                    # Get the packet data size
                    packet_data_size = data[:payload_size]
                    # Separate data_size from header
                    data = data[payload_size:]
                    try:
                        # Get data size
                        msg_size = struct.unpack("Q", packet_data_size)[0]
                        # Wait for buffer to fill up to the sent data size
                    except:
                        print("Connection error")
                        break

                    while len(data) < msg_size:
                        # Read from buffer
                        data += conn.recv(self.buffsize)

                    # Get the message data
                    msg = data[:msg_size]
                    # Store the read data to be read on the next iteration
                    data = data[msg_size:]
                    # Get the sent frame
                    frame = pickle.loads(msg)

                    # Show frame to local screen debug
                    cv2.imshow("Video Feed",frame)
                    # Set 60FPS in the video display
                    if cv2.waitKey(16) & 0xFF == ord('q'):      
                        break               
                # Outside the loop 
                print("Connection terminated")
                # Close connection with client since the stream has ended
                conn.close()

                # After the loop release the cap object
                cv2.destroyAllWindows()
            elif sel.lower() == "n":
                break
            else:
                print("Invalid option")
                continue

        print("Shutting server down")
        # Close transmission with server
        self.s.shutdown(socket.SHUT_RD)
        self.s.close()