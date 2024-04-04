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
        self.latest_frame = self.preprocess_frame_for_detection(self.latest_frame)
        return self.ret, self.latest_frame

    def stop(self):
        self.running = False 
        self.read_thread.join()
        self.cap.release()

    def preprocess_frame_for_detection(self, frame):
        """
        Applies pre-processing techniques to the frame to reduce noise
        and enhance marker detection stability.
        
        Parameters:
            frame (numpy.ndarray): The original video frame.
        
        Returns:
            numpy.ndarray: The pre-processed video frame.
        """
        # Apply Gaussian Blur to smooth the image
        # Note: You might need to adjust the kernel size (5, 5) and sigma (0) based on your specific requirements
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        
        # Apply bilateral filter to reduce noise while keeping edges sharp
        # Note: You might need to adjust the filter parameters based on your specific requirements
        filtered = cv2.bilateralFilter(blurred, 9, 75, 75)
        
        # Enhance contrast if needed (optional, based on your environment's lighting conditions)
        # Convert to YUV and equalize the histogram of the Y channel
        yuv = cv2.cvtColor(filtered, cv2.COLOR_BGR2YUV)
        yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        contrast_enhanced = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        
        return contrast_enhanced