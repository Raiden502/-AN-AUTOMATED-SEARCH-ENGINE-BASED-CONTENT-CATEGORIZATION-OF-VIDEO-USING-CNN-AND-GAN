import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import python_files.fetch_videos as fetch_videos
import python_files.fetch_videos as upload_video

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def start():
    print("phase 1")
    if request.method == 'POST':
        try:
            f = request.files['file']
        except:
            f = 0
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join('./static/videos', filename))
            upload_video.upload_new_video(filename,0)
    r = list(os.listdir('./static/videos'))
    return render_template('index.html', power=r)


@app.route('/search', methods=['POST', 'GET'])
def search():
    for f in os.listdir('./static/output'):
        os.remove('C:/Users/aniru/PycharmProjects/majorproject_trail/static/output/' + f)
    print("phase 1 search")
    category_of_info = ""
    if request.method == 'GET':
        category_of_info = request.args.get('category')
        category_of_info.lower()
        print("category_of_info=", category_of_info)
    r = list(os.listdir('./static/videos'))
    if category_of_info is not None:
        print("at category")
        fetch_videos.search_list(category_of_info)
    r = list(os.listdir('./static/output'))
    print("the searched values", r)
    return render_template('search.html', power=r)


@app.route('/re_sync', methods=['POST', 'GET'])
def re_sync():
    upload_video.resync()
    print("pass")
    return "nothing"


if __name__ == '__main__':
    app.run(debug=True)
