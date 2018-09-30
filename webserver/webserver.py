import os, subprocess
from flask import Flask, render_template, request, flash, session, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static")
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'reds209ndsldssdsljdsldsdsljdsldksdksdsdfsfsfsfis'
#sess.init_app(app)
#app.secret_key()
app.secret_key = b'_5#y2L"F4P8z\n\xec]/'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/test/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.call(r"chmod o+w predictions.png", shell=True, cwd="/home/ubuntu/darknet")
            subprocess.call(r"./darknet detect cfg/yolov3.cfg yolov3.weights "+os.path.join(app.config['UPLOAD_FOLDER'], filename), shell=True, cwd="/home/ubuntu/darknet")
            #subprocess.call(r"./darknet detect cfg/yolov3.cfg yolov3.weights data/horses.jpg", shell=True, cwd="/home/ubuntu/darknet")
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("upload.html")
    #return 
    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@app.route('/see/<filename>')
def see_file(filename):
    # /var/www/html/webserver/static
    # /home/ubuntu/webserver/static
    return send_from_directory('/home/ubuntu/darknet', 'predictions.png')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('/home/ubuntu/darknet', 'predictions.png')

if __name__ == '__main__':
  app.run()
