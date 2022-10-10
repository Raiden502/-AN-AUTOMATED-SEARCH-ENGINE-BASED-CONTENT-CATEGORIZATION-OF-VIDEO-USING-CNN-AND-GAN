import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from modelclassifier import predict as pre
import os
from moviepy.editor import VideoFileClip
import cv2



def upload_new_video(new_video,al):
    file_information = open('./static/json/files.json', 'r')
    files = json.load(file_information)
    if(al==1):
        pass
    else:
        files["videos"].append([new_video, 0])

    for i in range(len(files["videos"])):
        if files["videos"][i][1] == 0:
            print("updating",files["videos"][i][0])
            update_clip(files["videos"][i][0])
            files["videos"][i][1] = 1
    print("back at here")
    file_information = open('./static/json/files.json', 'w')
    file_information.write(json.dumps(files))


def resync():
    clipsz =  {"dog": [], "horse": [], "elephant": [], "butterfly": [], "chicken": [], "cat": [], "cow": [], "sheep": [], "squirrel": [], "spider": []}
    print(clipsz)
    data=json.dumps(clipsz)
    print("data in fetch=",data)
    clip_information = open('./static/json/clips.json', 'w')
    try:
        clip_information.write(data)
        print("passing")
    except:
        print("here is error")
    file_information = open('./static/json/files.json', 'r')
    files = json.load(file_information)
    for i in range(len(files["videos"])):
        files["videos"][i][1] = 0
    print("file info",files)
    clip_information = open('./static/json/clips.json', 'r')
    print("pavan",json.load(clip_information))
    for i in range(len(files["videos"])):
        upload_new_video(files["videos"][i][0],1)
    print(files)
    print("ok")
    file_information = open('./static/json/files.json', 'w')
    file_information.write(json.dumps(files))




def update_clip(new_video):
    clip_information = open('./static/json/clips.json', 'r')
    clips = json.load(clip_information)
    print("inside clips",clips)
    print(os.listdir('./static/videos'))
    # Difference, Subset size, no.of skips(n-1)
    # Difference > no.of skips

    filen = './static/videos/' + new_video
    clip = VideoFileClip(filen)
    obj = pre.Classifier(90, 60,int(clip.duration*clip.fps))
    obj.predict_vedio(filen)
    a = obj.longest_sequence()
    f = {}
    new_names= {"cane": "dog", "cavallo": "horse", "elefante": "elephant", "farfalla": "butterfly", "gallina": "chicken", "gatto": "cat", "mucca": "cow", "pecora": "sheep", "scoiattolo": "squirrel", "cavallo": "horse", "ragno": "spider"}
    for i in a:
        for j in a[i]:
            print("==============",i)
            ii = new_names[i]
            if ii not in f:
                f[ii] = [[j[0], j[-1]]]
            else:
                f[ii].append([j[0], j[-1]])
    print("data in clips = ", f)
    for key, values in f.items():
        if {new_video: values} not in clips[key]:
            clips[key].append({new_video: values})
    clip_information = open('./static/json/clips.json', 'w')
    clip_information.write(json.dumps(clips))



def show_videos(name, time):
    # print("here in show_videos")
    # # ffmpeg_extract_subclip("./static/videos/"+name, 8, 14, targetname="./static/output/"+name)
    # ffmpeg_extract_subclip(filename="./static/videos/" + name, t1=time[0], t2=time[-1],
    #                        targetname="./static/output/" + name[:-3] + str(time) + ".mp4")
    file = "./static/videos/"+name
    video = cv2.VideoCapture(file)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    print(fps)
    i, j = time[0],time[-1]
    i, j = int(i / fps), int(j / fps)
    print(i, j)
    clip = VideoFileClip(file)
    clip = clip.subclip(i, j)
    clip.write_videofile("./static/output/" + name[:-3] + str(time) + ".mp4")

def search_list(key):
    print("in fetch_videos",key)
    clip_information = open('./static/json/clips.json', 'r')
    clips = json.load(clip_information)
    print(clips)
    try:
        fin = (clips[key.lower()])
    except:
        return None
    print("fin is at here", fin)
    result = []
    for elements in fin:
        for i, j in elements.items():
            for k in j:
                print(i,j,k)
                show_videos(i, k)
            result.append(i[:-3] + str(k) + ".mp4")
    print(fin)
    return result
