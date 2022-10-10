from moviepy.editor import *
import cv2

file = "static/videos/videoplayback_Trim.mp4"
video = cv2.VideoCapture(file)
fps = int(video.get(cv2.CAP_PROP_FPS))
print(fps)
i,j=1331,2563
i,j = int(i/fps),int(j/fps)
print(i,j)
clip  = VideoFileClip(file)
clip = clip.subclip(i,j)
clip.write_videofile("C:\\Users\\aniru\\Desktop\\1111.mp4")