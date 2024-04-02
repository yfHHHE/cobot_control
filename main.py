import cv2
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
    controller = VideoController(detector)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break
        
        # Detect markers in the current frame
        corners, ids, _ = detector.detect_marker_corners(frame)
        
        # If markers are detected, draw them
        if ids is not None:
            detector.draw_marker(frame, corners, ids)
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):
            controller.pause_video()
        elif key == ord('q'):
            controller.exit_video()
            break
        elif key == ord('i'):
            controller.printcd()

        elif key == ord('o'):
            controller.onoff()
        elif key == ord('w'):
            text = int(input("Input number of aruco code"))
            print(detector.get_average_tvec(text))
        
        elif key == ord('a'):
            a = controller.findAngle()
            print(a)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
