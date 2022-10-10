# Importing all necessary libraries
import cv2
import os

k = input("enter file: ")
h = input("enter name: ")
source = input("enter file directory path to store: ")
cam = cv2.VideoCapture(k)
bb = os.path.join(source + h)
try:

    # creating a folder named data
    if not os.path.exists(bb):
        os.makedirs(bb)
        currentframe = 0
    else:
        dirFiles = []
        for f in os.listdir(bb):
            a, b = f.split(".")
            dirFiles.append(int(a))
        currentframe = max(dirFiles)

# if not created then raise error
except OSError:
    print('Error: Creating directory of data')

while (True):
    ret, frame = cam.read()
    if ret:
        name = bb + '/' + str(currentframe) + '.jpg'
        print('Creating...' + name)
        cv2.imwrite(name, frame)
        currentframe += 1
    else:
        break
cam.release()
cv2.destroyAllWindows()
