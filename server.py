from flask import Flask, request, render_template, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import time
import random

app = Flask(__name__)
data_dir = os.getcwd() + '/data'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['file']
    file_name = image.filename
    if '.' in file_name and file_name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'bmp']:
        ext = file_name.split('.')[-1]
        new_file_name = f'{time.strftime("%Y%m%d-%H%M%S-") + str(random.randint(0, 99))}.{ext}'
        image.save(data_dir+'/'+new_file_name)
    return redirect('/')

@app.route('/image/<file_name>')
def image(file_name):
    image_list = os.listdir(data_dir)
    secured_file_name = secure_filename(file_name)
    
    for image in image_list:
        if image.split('.')[0] == secured_file_name:
            return send_from_directory(data_dir, image)

    return redirect('/')

@app.route('/imagelist')
def image_list():
    return jsonify({'image_list':[a.split('.')[0] for a in os.listdir(data_dir)]})

if __name__ == '__main__':
    app.run(debug=True)
