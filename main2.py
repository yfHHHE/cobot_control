import cv2
from utils_refactored import VideoController
import time

def main():
    global video_controller
    video_controller = VideoController(video_source=0)
    
    cv2.namedWindow("Control Window")
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('p'):  # Start processing
            video_controller.start_processing_frame()  # Make sure this method sets `self.active` to True and starts the loop
        if key == ord('o'):  # Start processing
            video_controller.start_processing_frame(2)  # Make sure this method sets `self.active` to True and starts the loop
        elif key == ord('b'):  # Stop processing and align markers
            video_controller.stop_processing_frame()  # This should stop the frame processing loop
            video_controller.align_markers_by_z([1,2])
        elif key == ord('q'):  # Quit program
            break
        elif key == ord('n'):  # Quit program
            print(1)
            video_controller.stop_processing_frame()
            print(1)
            video_controller.align_cam(4)


        elif key == ord('m'):  # Quit program
            video_controller.onoff()
    
    video_controller.release_resources()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()