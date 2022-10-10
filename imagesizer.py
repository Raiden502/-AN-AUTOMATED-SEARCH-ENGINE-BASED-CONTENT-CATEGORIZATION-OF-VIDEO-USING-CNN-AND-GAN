import os
import cv2

x,y,z = 100,400,800
for i in os.listdir(r"D:/running"):
	img = cv2.imread(r"D:/running"+"/"+i)
	crop_img = img[x:z, y:y+z]
	cv2.imwrite("D:/runningcropped"+"/"+i,crop_img)
print("done")

'''
x,y,z = 100,400,800
j=0
for i in os.listdir(r"D:/walking")
	if(j<603):
		img = cv2.imread(r"D:/walking"+"/"+i)
		crop_img = img[1000:3000, 100:900]
		cv2.imwrite("D:/walkingcropped"+"/"+i,crop_img)
		j+=1
		print(j,i)
	else:
		img = cv2.imread(r"D:/walking"+"/"+i)
		crop_img = img[x:z, y:y+z]
		cv2.imwrite("D:/walkingcropped"+"/"+i,crop_img)
		j+=1
	
print("done")
'''