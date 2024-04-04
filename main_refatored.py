

from utils_refactored import VideoController
from pynput import keyboard
import time

video_controller = VideoController(video_source=0)
def on_press(key):
    global video_controller
    try:
        if key.char == 'b':
            video_controller.stop_processing_frame() 
            print("OFF")
            video_controller.align_markers_by_z([1,2])
        if key.char == 'n':
            video_controller.stop_processing_frame()
            id = input("Which id") 
            video_controller.align_cam(id)
        if key.char == 'w':
            video_controller.move_forward(10)
        if key.char == 's':
            video_controller.move_forward(-10)
        if key.char == 't':
            print('a')
        if key.char == 'o':
            video_controller.onoff()

    except AttributeError:
        # Handle special keys if necessarya
        pass
    
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
def main():
    global video_controller
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # Start listening on a separate thread
    try:
        time.sleep(1)
        video_controller.process_frame()
        #video_controller.align_markers_by_z([1,2])
    except KeyboardInterrupt:
        print("\nExiting application...")
    finally:
        video_controller.release_resources()
        listener.stop()

if __name__ == "__main__":
    main()

# This version of main.py demonstrates a clear and straightforward application flow,
# initializing the VideoController and handling the frame processing in a try-except block to
# gracefully handle interruptions and ensure resources are released properly.
