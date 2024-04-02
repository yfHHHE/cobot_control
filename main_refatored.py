

from utils_refactored import VideoController
from pynput import keyboard
def on_press(key):
    global feedback_loop_control
    try:
        if key.char == 'a':
            VideoController.align_markers_by_z()
    except AttributeError:
        # Handle special keys if necessary
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
def main():
    video_controller = VideoController(video_source=0)
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # Start listening on a separate thread
    try:
        video_controller.process_frame()
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
