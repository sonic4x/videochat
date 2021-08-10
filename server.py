import socket, videosocket
from videofeed import VideoFeed
import queue
import threading
import time
class Server:
    def __init__(self, video_data_que):
        self.video_data_que = video_data_que
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", 6000))
        self.server_socket.listen(5)
        # self.videofeed = VideoFeed(1,"server",1)
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

    def start_with_queue(self):
        # while 1:
            client_socket, address = self.server_socket.accept()
            print("I got a connection from ", address)
            video_frames_collector = VideoFramesCollector(client_socket, self.video_data_que)
            video_frames_collector.start()

class VideoFramesCollector(threading.Thread):
    def __init__(self,client_socket, video_data_que):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.video_data_que = video_data_que
    def run(self):
        vsock = videosocket.videosocket(self.client_socket)
        while True:
            frame=vsock.vreceive()

            self.video_data_que.put(frame)

class VideoPlayer(threading.Thread):

    def __init__(self,video_data_que):
        threading.Thread.__init__(self)
        self.video_data_que = video_data_que
        self.videofeed = VideoFeed(1,"Doom",2)

    def run(self):
        while True:
            # videodataquesize = self.videodataque.qsize()
            # if videodataquesize > 1:
            #     self.playbackrate = 0
            while not self.video_data_que.empty():
                videoframe = self.video_data_que.get()

                try:
                    self.videofeed.set_video_frame(videoframe)
                except Exception as e:
                    # logfile = open("log.txt", 'a+')
                    # print("%s  Output_Error: %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), e),
                    #       file=logfile)
                    # cv2.destroyWindow('server')
                    # logfile.close()
                    continue


def main():
    video_data_que = queue.Queue()
    server = Server(video_data_que)
    server.start_with_queue()
    video_player = VideoPlayer(video_data_que)
    video_player.start()

if __name__ == "__main__":
    main()
