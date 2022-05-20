import cv2, socket, pickle, struct, os

# Get stream/camera for image data 
vstream = cv2.VideoCapture(os.environ['HOME'] + "/Videos/aoeo.mp4")  

# Handle file access error
if not vstream.isOpened():
    print("Cannot open the file")
    exit()


# Define VGA resolution to simulate the camera resolution
VGA_RES = (640,480)
# Define used port for the sockets
PORT = 5678         # A random port for now
HOST = "localhost"

# Create listening socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
# Define a IPv4 socket using UDP for video and listen 
s.bind((HOST, PORT)) 
s.listen(5)

# --------Main------------ 
#if __name__ == "__main__":

while True:
    # Wait for viewer
    conn, addr = s.accept()
    if conn:
        # Streamer loop
        while vstream.isOpened():
            # Get processed frame
            ret, frame = vstream.read()                             
            # Resize in VGA resolution
            #frame = cv2.resize(frame,dsize=VGA_RES)                           
            # Serialize frame data 
            msg = pickle.dumps(frame)
            print(len(msg))
            # Pack data with a header that contains the data lenght
            pkg = struct.pack("Q", len(msg)) + msg
            # Send data to viewer
            conn.send(pkg)

            # Show frame to local screen debug
            cv2.imshow("DebugStreamer",frame) 
            if cv2.waitKey(16) & 0xFF == ord('q'):                  
                break
            #cv2.waitKey(16)
        
    # Close connection with client since the stream has ended
    conn.close()
    # After the loop release the cap object
    vstream.release()
    # Destroy all the windows
    cv2.destroyAllWindows()