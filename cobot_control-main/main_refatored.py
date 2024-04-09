
from Utils_Refactored_2 import VideoController
from pynput import keyboard
import math
video_controller = VideoController()
def on_press(key):
    global feedback_loop_control
    global video_controller 
    try:
        if key.char == 'e' :
            video_controller.align_markers_by_z()
        if key.char == 'w':
            print(1)
            video_controller.move_forward(40) # Move Forward
        if key.char == 's':
            video_controller.move_forward(-40) # Move Backwards
        if key.char == 'a':
            video_controller.move_left(10) # Move Left
        if key.char == 'd':
            video_controller.move_left(-10) # Move Right
        if key.char == "p":
            video_controller.printcoords() # Printing of Co-ordinates
        if key.char == "r":
            video_controller.increaseheight(40) # Increase of Height
        if key.char == "f":
            video_controller.increaseheight(-40) # Decrease of Height
        if key.char == "6":
            video_controller.rotateclaw(-40) # Rotate Clockwise
        if key.char == "4":
            video_controller.rotateclaw(10) # Rotate Counter-Clockwise
        
    ## Moving The Claws Parallel to the Inclined Surface after taking in Input for Angle and Height
        if key.char == "2": 
            angle_deg= float(input("What is the angle between claw and screen?")) # Moving Along Inclined Surface Downwards
            angle= math.radians(angle_deg)
            video_controller.correctedheight(angle,-10)
        if key.char == "8": 
            angle_deg= float(input("What is the angle between claw and screen?")) # Moving Along Inclined Surface Upwards
            angle= math.radians(angle_deg)
            video_controller.correctedheight(angle,10)
        elif key.char == "m" : # Quit program
            video_controller.onoff()
        elif key.char == "q":  # Quit program
            raise("Quit")

 
    except AttributeError:
        # Handle special keys if necessary
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
