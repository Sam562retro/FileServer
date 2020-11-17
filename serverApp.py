from flask import Flask, render_template,request, redirect, url_for, flash, send_from_directory, session
import os
from cryptography.fernet import Fernet

UPLOAD_FOLDER = 'E:/proggraming/FileServer/Files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','ppatx','docx', 'xlsx', 'py', 'cpp', 'xd', 'ai', 'mp4', 'avi','pptm', 'zip', 'accdb', 'ev3', 'prproj', 'css', 'js', 'ino'}

app = Flask(__name__)
app.secret_key = 'FileServer'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

key = load_key()

def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)

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
                filePath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filePath)
                encrypt(filePath, key)
        return render_template('uploadFiles.html')
    else:
        return render_template('wrongLogin.html')

@app.route('/logOut')
def LogOut():
    session['username'] = None
    return render_template('logout.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(filename)
    decrypt(filePath, key)
    a = send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    return a


app.run(port='4885', debug=True)
