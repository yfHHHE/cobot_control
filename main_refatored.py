
from utils_refactored import VideoController

def main():
    video_controller = VideoController(video_source=0)
    try:
        video_controller.process_frame()
    except KeyboardInterrupt:
        print("\nExiting application...")
    finally:
        video_controller.release_resources()

if __name__ == "__main__":
    main()