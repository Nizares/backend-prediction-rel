import cv2 as cv
import time
import numpy as np
import os

cap = cv.VideoCapture(0)
pTime = 0
cTime = 0
count = 0
folderHand = input("Masukkan ABCDE..: ")


def save_image(folderName,img):
    path = 'lutpi\datasets'
    # Join the path and folder name to create the full directory path
    full_path = os.path.join(path, folderName)

    if not os.path.exists(full_path):
        os.makedirs(full_path)
    folderCount = len(os.listdir(full_path))
    count =  folderCount + 1
    filename = f'{full_path}/hand_{count}.png'
    cv.imwrite(filename, img)



while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    # Create a window to open and retrieve screen resolution


    width, height = 800, 600  # You can adjust the dimensions as needed
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Define the bounding box parameters
    left = 100  # Adjust the left position as needed
    top = height // 4  # Place it in the middle of the screen's height
    box_width = 250  # Adjust the width of the bounding box
    box_height = 250  # Adjust the height of the bounding box
    color = (0, 255, 0)  # BGR color (green in this case)
    thickness = 2

    # Draw the bounding box
    cv.rectangle(img, (left, top), (left + box_width, top + box_height), color, thickness)


    # Wait for a key press
    key = cv.waitKey(1) & 0xFF

    # Check if the 's' key is pressed
    if key == ord('s'):
        handImg = img[top + thickness:top + box_height - thickness, left + thickness:left + box_width - thickness]
        save_image(folderHand,handImg)

    if key == ord('q'):
        break
        cv.destroyAllWindows()

    # Write FPS to the screen
    cv.putText(img, str(int(fps)), (10, 70),
                cv.FONT_HERSHEY_PLAIN, fontScale=3,
                color=(255, 0, 255), thickness=2)
    cv.imshow("Image",img)


    
