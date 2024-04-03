import cv2
import threading

class CameraFeed:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        self.latest_frame = None
        self.ret = False
        self.running = True
        self.read_thread = threading.Thread(target=self.update_frame, daemon=True)
        self.read_thread.start()

    def update_frame(self):
        while self.running:
            self.ret, frame = self.cap.read()
            if self.ret:
                self.latest_frame = frame

    def get_frame(self):
        return self.ret, self.latest_frame

    def stop(self):
        self.running = False
        self.read_thread.join()
        self.cap.release()