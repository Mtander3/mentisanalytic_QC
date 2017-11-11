import os
import codecs
import numpy as np
import pandas
import string
from stemming.porter2 import stem
import unicodedata
import sys
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.decomposition import LatentDirichletAllocation


topics_print = []

import os
from flask import Flask, request, redirect, url_for, render_template, flash, session
#from flask.ext.session import Session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/mattanderson/Documents/QC_Hackathon_MA/app/speak_up/2017'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','html','rtf'])

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#sess = Session()


@app.route('/', methods = ['POST','GET'])
def home():
    return render_template("file2.html")

@app.route('/health_facilities_map', methods = ['GET','POST'])
def maps():
        if request.method == "GET":
            return render_template("health_facilities_map.html")

@app.route('/contact', methods = ['POST','GET'])
def contact():
    return render_template("contact.html")
def allowed_file(filename):
   return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/model', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    
    

    return '''

    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <style>
    .container {
        position: center;
    }

    .center {
        position: absolute;
        left: 10px;
        top: 50%;
        width: 100%;
        text-align: center;
        font-size: 18px;
    }

    img {
        width: 60%;
        height: auto;
        opacity: 1;
    }
</style>

    <img src='static/speak_up_wordcloud.jpeg'/>
    '''


from flask import send_from_directory

@app.route('/uploads/<filename>')

def uploaded_file(filename):
    exec(open("/Users/mattanderson/Documents/QC_Hackathon_MA/app/extract_speakup.py").read())
    return send_from_directory("/Users/mattanderson/Documents/QC_Hackathon_MA/app",
                               'topics.csv')




						   
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    #sess.init_app(app)
    app.run(debug = True)
