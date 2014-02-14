from flask import Flask, request, redirect, url_for, jsonify,\
    send_from_directory

from werkzeug.utils import secure_filename
from settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, DEBUG
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.DEBUG = DEBUG



def allowed_file(filename):
    """checks to see if file format is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcom to fapi. All your file are belong to us.')


@app.route('/upload', methods=['POST'])
def upload_file():
    """upload a file to the server"""
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                filename=filename))
        return jsonify(message="File uploaded successfully.")
    
    except:
        return jsonify(message="Error uploading file."), 500
        

#for testing only, as Nginx or Apache would be serving the static files (faster, less overhead).
@app.route('/<filename>')
def uploaded_file(filename):
    """returns the uploaded file."""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    except IOError as e:
        return jsonify(message=e), 500


if __name__ == "__main__":
    app.run()