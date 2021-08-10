import socket, videosocket
from videofeed import VideoFeed

class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", 6000))
        self.server_socket.listen(5)
        self.videofeed = VideoFeed(1,"server",1)
        print("TCPServer Waiting for client on port 6000")

    def start(self):
        while 1:
            client_socket, address = self.server_socket.accept()
            print("I got a connection from ", address)
            vsock = videosocket.videosocket(client_socket)
            while True:
                frame=vsock.vreceive()
                self.videofeed.set_frame(frame)
                frame=self.videofeed.get_frame()
                vsock.vsend(frame)

    def start2(self):
        while 1:
            client_socket, address = self.server_socket.accept()
            print("I got a connection from ", address)
            vsock = videosocket.videosocket(client_socket)
            while True:
                frame=vsock.vreceive()
                self.videofeed.set_frame(frame)

                #send ack
                ack=b'ack'
                vsock.vsend(ack)

    def start3(self):
        while 1:
            client_socket, address = self.server_socket.accept()
            print("I got a connection from ", address)
            vsock = videosocket.videosocket(client_socket)
            while True:
                frame=vsock.vreceive()
                self.videofeed.set_frame_cv_version(frame)
                
                #send ack
                ack=b'ack'
                vsock.vsend(ack)
    
    def start4(self):
        while 1:
            client_socket, address = self.server_socket.accept()
            print("I got a connection from ", address)
            vsock = videosocket.videosocket(client_socket)
            while True:
                frame=vsock.vreceive()
                self.videofeed.set_video_frame(frame)



if __name__ == "__main__":
    server = Server()
    server.start4()
