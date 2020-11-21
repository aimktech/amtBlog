# imports
import os
from videostream import VideoStream

# globals
MCAST_IP = '224.1.2.3'
MCAST_PORT = 5005

# begin
stream = VideoStream(MCAST_IP, MCAST_PORT)
stream.setupServer()
stream.startServer(os.getpid())
stream.shutdown()

