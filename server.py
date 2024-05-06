from flask import Flask, request, render_template, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import hashlib
import os
import time
import random

app = Flask(__name__)
data_dir = os.getcwd() + '/data'
password = hashlib.sha256("play".encode()).hexdigest()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['file']
    tried_pw = request.form['pw']
    print(tried_pw)
    file_name = image.filename
    if tried_pw == password and '.' in file_name and file_name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'bmp']:
        ext = file_name.split('.')[-1]
        new_file_name = f'{time.strftime("%Y%m%d-%H%M%S-") + str(random.randint(0, 99))}.{ext}'
        image.save(data_dir+'/'+new_file_name)
    return redirect('/')

@app.route('/image/<file_name>/<tried_pw>')
def image(file_name, tried_pw):
    if tried_pw == password:
        image_list = os.listdir(data_dir)
        secured_file_name = secure_filename(file_name)
        
        for image in image_list:
            if image.split('.')[0] == secured_file_name:
                return send_from_directory(data_dir, image)

    return redirect('/')

@app.route('/imagelist/<tried_pw>')
def image_list(tried_pw):
    if tried_pw == password:
        return jsonify({'image_list':[a.split('.')[0] for a in os.listdir(data_dir)]})
    return redirect('/')

if __name__ == '__main__':
    app.run()
