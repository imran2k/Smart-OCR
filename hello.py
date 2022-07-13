from __future__ import division, print_function
from flask import Flask,request, render_template
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import numpy as np
import cv2
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
import sys
import os.path
import glob
import random

app = Flask(__name__, static_url_path='')



@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        PDF_file = file_path
        pages = convert_from_path(PDF_file, 500) 
        image_counter = 1
        for page in pages: 
            filename = "page_"+str(image_counter)+".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1
        filelimit = image_counter-1
        # Creating a text file to write the output
        basepath = os.path.dirname(__file__)
        file_path2 = os.path.join(
            basepath, 'outputs', "output"+str(random.randint(1, 100000))+".txt")
        f = open(file_path2, "a") 
        for i in range(1, filelimit + 1): 
            filename = "page_"+str(i)+".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace('-\n', '')     
            f.write(text) 
        f.close()
    return file_path2


if __name__ == '__main__':
 port = int(os.getenv('PORT', 8000))
 #app.run(host='0.0.0.0', port=port, debug=True)
 http_server = WSGIServer(('0.0.0.0', port), app)
 http_server.serve_forever()
app.run(debug=True)

