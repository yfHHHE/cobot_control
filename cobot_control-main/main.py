# Original Code
'''import cv2
from aruco import ArucoDetector
from utils import VideoController
def main():
    # Initialize the video capture from the camera.
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    # Initialize the ArucoDetector
    detector = ArucoDetector()
    #controller = VideoController(detector)

    def x_filter(frame):




        pass


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        

        #frame = x_filter(frame)

        # Detect markers in the current frame
        corners, ids, _ = detector.detect_marker_corners(frame)
        
        # If markers are detected, draw them
        if ids is not None:
            detector.draw_marker(frame, corners, ids)
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        # if key == ord('p'):
        #     controller.pause_video()
        # elif key == ord('q'):
        #     controller.exit_video()
        #     break
        # elif key == ord('i'):
        #     controller.printcd()

        # elif key == ord('o'):
        #     controller.onoff()
        # elif key == ord('w'):
        #     text = int(input("Input number of aruco code"))
        #     print(detector.get_average_tvec(text))
        
        # elif key == ord('a'):
        #     a = controller.findAngle()
        #     print(a)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()'''

# Code with Gaussian Filter

'''import cv2
from aruco import ArucoDetector
from utils import VideoController

def main():
    # Initialize the video capture from the camera.
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    # Initialize the ArucoDetector
    detector = ArucoDetector()
    #controller = VideoController(detector)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Apply Gaussian blur to the frame
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # Detect markers in the current frame
        corners, ids, _ = detector.detect_marker_corners(frame)
        
        # If markers are detected, draw them
        if ids is not None:
            detector.draw_marker(frame, corners, ids)
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # Uncomment and modify the following lines as needed based on your controller's functions
        # if key == ord('p'):
        #     controller.pause_video()
        # elif key == ord('i'):
        #     controller.print_info()
        # elif key == ord('o'):
        #     controller.toggle_overlay()
        # elif key == ord('w'):
        #     text = int(input("Input number of aruco code"))
        #     print(detector.get_average_tvec(text))
        # elif key == ord('a'):
        #     print(controller.find_angle())

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()'''

### Median Blur
'''import cv2
from aruco import ArucoDetector
from utils import VideoController

def main():
    # Initialize the video capture from the camera.
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    # Initialize the ArucoDetector
    detector = ArucoDetector()
    #controller = VideoController(detector)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Apply Median blur to the frame
        frame = cv2.medianBlur(frame, 5)  # You can adjust the kernel size if needed

        # Detect markers in the current frame
        corners, ids, _ = detector.detect_marker_corners(frame)
        
        # If markers are detected, draw them
        if ids is not None:
            detector.draw_marker(frame, corners, ids)
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # Uncomment and modify the following lines as needed based on your controller's functions
        # if key == ord('p'):
        #     controller.pause_video()
        # elif key == ord('i'):
        #     controller.print_info()
        # elif key == ord('o'):
        #     controller.toggle_overlay()
        # elif key == ord('w'):
        #     text = int(input("Input number of aruco code"))
        #     print(detector.get_average_tvec(text))
        # elif key == ord('a'):
        #     print(controller.find_angle())

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()'''

### Bilateral Filter

'''import cv2
from aruco import ArucoDetector
from utils import VideoController

def main():
    # Initialize the video capture from the camera.
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    # Initialize the ArucoDetector
    detector = ArucoDetector()
    #controller = VideoController(detector)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Apply Bilateral filter to the frame
        frame = cv2.bilateralFilter(frame, 9, 75, 75)  # You can adjust these parameters

        # Detect markers in the current frame
        corners, ids, _ = detector.detect_marker_corners(frame)
        
        # If markers are detected, draw them
        if ids is not None:
            detector.draw_marker(frame, corners, ids)
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # Uncomment and modify the following lines as needed based on your controller's functions
        # if key == ord('p'):
        #     controller.pause_video()
        # elif key == ord('i'):
        #     controller.print_info()
        # elif key == ord('o'):
        #     controller.toggle_overlay()
        # elif key == ord('w'):
        #     text = int(input("Input number of aruco code"))
        #     print(detector.get_average_tvec(text))
        # elif key == ord('a'):
        #     print(controller.find_angle())

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()'''

### Temporal Averaging
import cv2
import numpy as np
from aruco import ArucoDetector
from utils import VideoController

def main():
    # Initialize the video capture from the camera.
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    # Initialize the ArucoDetector
    detector = ArucoDetector()
    # Uncomment the next line if you have a VideoController
    # controller = VideoController(detector)

    # Initialize an accumulator for frame averaging
    acc = None
    alpha = 0.02  # Adjust the alpha for more history consideration

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Convert frame to float for accurate accumulation
        float_frame = frame.astype(np.float32)

        # Initialize the accumulator with the first frame if it's not already initialized
        if acc is None:
            acc = np.zeros_like(float_frame)

        # Update the running average
        cv2.accumulateWeighted(float_frame, acc, alpha)

        # Convert the accumulated float image back to an 8-bit image
        avg_frame = cv2.convertScaleAbs(acc)

        # Detect markers in the averaged frame
        corners, ids, _ = detector.detect_marker_corners(avg_frame)
        
        # If markers are detected, draw them on the original frame (for clearer display)
        if ids is not None:
            detector.draw_marker(frame, corners, ids)
            print("Markers detected")
        else:
            print("No markers detected")
        
        # Display the resulting frame
        cv2.imshow('Frame', avg_frame)
        
        # Manage user input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # Additional controls can be uncommented and adjusted as needed
        # elif key == ord('p'):
        #     controller.pause_video()
        # elif key == ord('i'):
        #     controller.print_info()
        # elif key == ord('o'):
        #     controller.toggle_overlay()
        # elif key == ord('w'):
        #     text = int(input("Input number of aruco code"))
        #     print(detector.get_average_tvec(text))
        # elif key == ord('a'):
        #     print(controller.find_angle())

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
