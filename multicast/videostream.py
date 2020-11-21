# imports
import cv2
import sys
import time
import socket
import struct
import logging

import msgpack
import msgpack_numpy as mn
import numpy as np


# class
class VideoStream:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.capture = None
        self.framerate = 1 / 30
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def setupClient(self, ttl=2):
        # set the Multicast TTL parameter
        ttl = struct.pack('b', ttl)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def setupServer(self):
        # bind the socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))

        # subscribe to multicast address
        group = socket.inet_aton(self.ip)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def setCapture(self, device):
        if device.startswith("cam-"):
            self.capture = cv2.VideoCapture(int(device.split('-')[1]))
        else:
            self.capture = cv2.VideoCapture(device)

        if not self.capture.isOpened():
            logging.error(f"Unable to open device {device}")
            self.capture.release()
            sys.exit(1)

    def _resize(self, frame, scale):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        return frame

    def _encode(self, frame):
        frame = np.ascontiguousarray(frame, dtype=frame.dtype)
        data = msgpack.packb(frame, default=mn.encode)
        return data

    def _send(self, data, blocksize=4096):
        size = len(data)

        while size > blocksize:
            block = data[:blocksize]
            self.sock.sendto(block, (self.ip, self.port))
            
            # remove already sent data
            data = data[blocksize:]
            size = size - blocksize
        
        # send the last block
        self.sock.sendto(data, (self.ip, self.port))

    def startClient(self):
        last_time = time.monotonic()

        while True:
            try:
                ret, frame = self.capture.read()

                if not ret:
                    break

                # resize the image
                frame = self._resize(frame, 0.3)

                # encode the image
                data = self._encode(frame)

                # send the data
                self._send(data)

                # display the source image
                cv2.imshow("Source", frame)

                # wait for a key press
                key = cv2.waitKey(10)
                if key == 27:
                    break

                # ensure we display 30 fr/s
                while (time.monotonic() - last_time) <= self.framerate:
                    time.sleep(0.01)
                last_time = time.monotonic()

            except KeyboardInterrupt:
                break

    def startServer(self, client_id):
        frame = b''
        while True:
            try:
                # read the image from the network
                data, addr = self.sock.recvfrom(4096)
                
                if data:
                    frame += data
                    if len(data) < 4096:

                        # display the image
                        try:
                            image = msgpack.unpackb(frame, object_hook=mn.decode)
                            cv2.imshow(f"Target #{client_id}", image)
                        except:
                            pass

                        # wait for a key press
                        key = cv2.waitKey(10)
                        if key == 27:
                            break

                        # reset the variable
                        frame = b''

            except KeyboardInterrupt:
                break

    def shutdown(self):
        if self.capture:
            self.capture.release()
        cv2.destroyAllWindows()  
