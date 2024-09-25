import cv2 as cv
import time
import numpy as np
import os

# 0 / camera device number default
# 1 / camera device number external
cap = cv.VideoCapture(1)
pTime = 0
cTime = 0
count = 0
folderHand = input("Masukkan ABCDE..: ")


def save_image(folderName,img,count):
    path = 'datasets/'
    # Join the path and folder name to create the full directory path
    full_path = os.path.join(path, folderName)

    if not os.path.exists(full_path):
        os.makedirs(full_path)
    folderCount = len(os.listdir(full_path))
    count =  folderCount + count
    filename = f'{full_path}/hand_{count}.png'
    cv.imwrite(filename, img)



while True:
    success, img = cap.read()

    img = cv.flip(img, 1)
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    # Create a window to open and retrieve screen resolution


    width, height = 120, 720  # You can adjust the dimensions as needed
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
        for i in range(100):
            save_image(folderHand,handImg,i)
        break
        cv.destroyAllWindows()

    # Write FPS to the screen
    cv.putText(img, str(int(fps)), (10, 70),
                cv.FONT_HERSHEY_PLAIN, fontScale=3,
                color=(255, 0, 255), thickness=2)

    cv.imshow("Image",img)

# import cv2 as cv
# import time
# import numpy as np
# import os

# cap = cv.VideoCapture(3)
# pTime = 0
# cTime = 0
# count = 0
# folderHand = input("Masukkan ABCDE..: ")

# def save_image(folderName,img,count):
#     path = 'datasets/'
#     # Join the path and folder name to create the full directory path
#     full_path = os.path.join(path, folderName)

#     if not os.path.exists(full_path):
#         os.makedirs(full_path)
#     folderCount = len(os.listdir(full_path))
#     count =  folderCount + count
#     filename = f'{full_path}/hand_{count}.png'
#     cv.imwrite(filename, img)

# while True:
#     success, img = cap.read()

#     if not success:
#         print("Gagal mengambil frame dari kamera.")
#         break

#     img = cv.flip(img, 1)

#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime

#     # Mendapatkan dimensi frame yang sebenarnya
#     height, width, _ = img.shape

#     # Definisikan parameter bounding box
#     left = 100  # Sesuaikan posisi kiri sesuai kebutuhan
#     top = height // 4  # Letakkan di tengah tinggi layar
#     box_width = 250  # Sesuaikan lebar bounding box
#     box_height = 250  # Sesuaikan tinggi bounding box
#     color = (0, 255, 0)  # Warna BGR (hijau dalam hal ini)
#     thickness = 2

#     # Gambar bounding box
#     cv.rectangle(img, (left, top), (left + box_width, top + box_height), color, thickness)

#     # Tunggu untuk menekan tombol
#     key = cv.waitKey(1) & 0xFF

#     if key == ord('s'):
#         handImg = img[top + thickness : top + box_height - thickness, left + thickness : left + box_width - thickness]
#         for i in range(100):
#             save_image(folderHand, handImg, i)
#         break

#     # Menulis FPS ke layar
#     cv.putText(img, str(int(fps)), (10, 70),
#                 cv.FONT_HERSHEY_PLAIN, fontScale=3,
#                 color=(255, 0, 255), thickness=2)

#     cv.imshow("Image", img)

# cv.destroyAllWindows()
# cap.release()