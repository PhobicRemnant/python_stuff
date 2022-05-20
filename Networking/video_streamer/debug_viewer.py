import cv2, socket, pickle, struct


def getNextFrame(s,buffsize, headsize):

    # Flush th
    dataclasses = b''
    # Awaiting new msger
    new_msg = True


    while True:
        
        # Read the packet size header
        while len(msg_buff) < struct.calcsize("Q"):
            # Read buffer
            msg = s.recv(buffsize)
            # Break if there is nothing in the buffer
            if not msg: break
            msg_buff += msg

        

        if new_msg:
            print("a new message")
            msglen = int(msg[:headsize])
            print(msglen)
            new_msg = False
        
        print(len(msg_buff) - headsize)
        if ( len(msg_buff) - headsize ) == msglen:
            print(f'frame received')
            data = pickle.loads(msg_buff[headsize:])
            
            break
    

    # Return data as a parameter
    return data


def getData(s,data, headsize):

    data = b''
    payload_size = struct.calcsize("Q")

    # Wait for the sent payload data
    while len(data) < payload_size:
        # Read from buffer
        pkg = s.recv(1024*4)
        if not pkg: break
        # Append to received data 
        data += pkg

    # Get the packet data size
    packet_data_size = data[:payload_size]
    # Separate data_size from header
    data = data[payload_size:]
    # Get data size
    data_size = struct.unpack("Q", packet_data_size)

    # Wait for buffer to fill up to the sent data size
    while len(data) < data_size:
        # Read from buffer
        data += s.recv(1024*4)

    # Get message
    msg = data[:data_size]
    # Store the read data to be read on the next iteration
    data = data[data_size:]
    
    return data, msg


# Define used port for the sockets
PORT = 5678         # A random port for now
HOST = "localhost"  

# Create socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Define a IPv4 socket using UDP for video
# Connect to the streamer server
s.connect((HOST, PORT))

# --------Main------------ 
#if __name__ == "__main__":

# Viewer loop
while True:
    
    # Declare data to store bytes and the payload size as a 8 byte long number
    data = b''
    payload_size = struct.calcsize("Q")
    
    # Wait for the sent payload data
    while len(data) < payload_size:
        # Read from buffer
        pkg = s.recv(1024*24)   # 24KB buffer size
        if not pkg: break
        # Append to received data 
        data += pkg

    # Get the packet data size
    packet_data_size = data[:payload_size]
    # Separate data_size from header
    data = data[payload_size:]
    # Get data size
    msg_size = struct.unpack("Q", packet_data_size)[0]
    # Wait for buffer to fill up to the sent data size
    while len(data) < msg_size:
        # Read from buffer
        data += s.recv(1024*24)

    # Get the message data
    msg = data[:msg_size]
    print(msg_size)
    # Store the read data to be read on the next iteration
    data = data[msg_size:]
    # Get the sent frame
    frame = pickle.loads(msg)

    # Show frame to local screen debug
    cv2.imshow("DebugViewer",frame)
    # Set 60FPS in the video display
    if cv2.waitKey(16) & 0xFF == ord('q'):      
        break
    
    
# Close transmission with server
s.shutdown(socket.SHUT_RD)
s.close()

# Destroy all the windows
cv2.destroyAllWindows()