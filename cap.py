import cv2
import os

# Create a folder for calibration images if it doesn't exist
folder = 'calibration_images'
if not os.path.exists(folder):
    os.makedirs(folder)

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 is typically the default camera

img_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow('Frame', frame)

    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == ord('j'):
        # 'j' pressed
        img_name = os.path.join(folder, f"opencv_frame_{img_counter}.png")
        cv2.imwrite(img_name, frame)
        print(f"{img_name} saved!")
        img_counter += 1

cap.release()
cv2.destroyAllWindows()
