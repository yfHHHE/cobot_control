
import cv2
import numpy as np

def harris_corner_detection_filter(frame):
    # Convert frame to grayscale if not already
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect corners using Harris Corner Detector
    corners = cv2.cornerHarris(gray_frame, 2, 3, 0.04)
    # Mark corners on the original frame
    frame[corners > 0.01 * corners.max()] = [0, 0, 255]
    return frame

def non_local_means_denoising_filter(frame):
    # Apply Non-local Means Denoising
    denoised_frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
    return denoised_frame

