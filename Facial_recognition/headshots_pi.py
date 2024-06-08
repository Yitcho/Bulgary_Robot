"""
Author: Mahdi Kaffel

Description: This script would allow you to take headshots and create your own dataset
"""
import cv2
import os
from picamera2 import Picamera2, Preview
from time import sleep

name = 'Koshojin-Sama' #replace with your name
img_counter = 0

# Save directory
save_dir = f"dataset/{name}"
# Create directory if it does not exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Initialize camera
picam2 = Picamera2()
# Configure the camera
config = picam2.create_preview_configuration(main={"size":(600,450)})
picam2.configure(config)
# Start the camera
picam2.start()

print("Press Space to take a photo, ESC to exit.")

while True:
    # Capture a frame
    frame = picam2.capture_array()
    # Display the frame
    cv2.imshow("Press space to take a photo",frame)
    
    k = cv2.waitKey(1)
    if k % 256 == 27: # ESC pressed
        print("Escape hit, closing ..")
        break
    elif k % 256 == 32: # SPACE pressed
        img_name = f"{save_dir}/image_{img_counter}.jpg"
        try:
            cv2.imwrite(img_name,frame)
            print(f"{img_name} written!")
            img_counter += 1
        except Exception as e:
            print(f"Failed to save image:{e}")
    
    
cv2.destroyAllWindows()
picam2.stop()