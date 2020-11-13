from flask import Flask, render_template,request, redirect, url_for, flash, send_from_directory, session
import os

UPLOAD_FOLDER = 'E:/proggraming/FileServer/Files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','pptx','docx', 'xlsx', 'py', 'cpp'}

app = Flask(__name__)
app.secret_key = 'FileServer'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def BeforeLogin():
    session['username'] = None
    return render_template('BeforeLogin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "soham" and password == "got_files":
            session['username'] = username
            return redirect('http://127.0.0.1:4885/mainPage')
        else:
            session['username'] = None
            return render_template('wrongLogin.html')
    else:
        return render_template('Login.html')

@app.route('/mainPage')
def seeAllFiles():
    if session['username'] == "soham":
        allFiles = list()
        files = os.listdir('E:/proggraming/FileServer/Files')
        for file in files:
            if '.' in file:
                print(file)
                allFiles.append(file)
            else:
                file += '.undefined'
                print(file)
                allFiles.append(file)
        return render_template('afterLogin.html', all = allFiles)
    else:
        return render_template('wrongLogin.html')


@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
    if session['username'] == "soham":
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                if ' ' in file.filename:
                    file.filename = file.filename.replace(' ', '_')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('uploadFiles.html')
    else:
        return render_template('wrongLogin.html')

@app.route('/logOut')
def LogOut():
    session['username'] = None
    return render_template('logout.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


app.run(port='4885', debug=True)