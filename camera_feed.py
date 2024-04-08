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
            frame = self.preprocess_frame_for_detection(frame)
            if self.ret:
                self.latest_frame = frame

    def get_frame(self):
        return self.ret, self.latest_frame

    def stop(self):
        self.running = False 
        self.read_thread.join()
        self.cap.release()

    def preprocess_frame_for_detection(self, frame):
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Apply mild Gaussian Blur to reduce noise while preserving edges
        blurred = cv2.GaussianBlur(grayscale, (3, 3), 0)
        
        # Enhance edges using adaptive thresholding
        # sharp_edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                     cv2.THRESH_BINARY, 11, 5)
        
        # Optional: Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast_enhanced = clahe.apply(blurred)
        
        # Note: The following step of Canny edge detection is shown as an illustrative option.
        # It might not be directly beneficial for ArUco detection as it produces an edge map, not a grayscale image.
        # edges = cv2.Canny(contrast_enhanced, 100, 200)
    
        return contrast_enhanced
