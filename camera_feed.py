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
    def harris_corner_detection_filter(self,frame):
        # Convert frame to grayscale if not already
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect corners using Harris Corner Detector
        corners = cv2.cornerHarris(gray_frame, 2, 3, 0.04)
        # Mark corners on the original frame
        frame[corners > 0.01 * corners.max()] = [0, 0, 255]
        return frame

    def non_local_means_denoising_filter(self,frame):
        # Apply Non-local Means Denoising
        denoised_frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        return denoised_frame
    def gaussian_pyramid_filter(self,frame):
        # Apply Gaussian pyramid
        pyramid = cv2.pyrDown(frame)
        return cv2.pyrUp(pyramid)

    def gaussian_blur_filter(self,frame):
        # Apply Gaussian blur
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return blurred_frame
    def preprocess_frame_for_detection(self, frame):
        # frame1 = self.gaussian_pyramid_filter(frame)
        # frame2 = self.gaussian_blur_filter(frame1)
        # return frame2
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
