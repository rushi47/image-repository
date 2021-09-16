from flask import flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from app import app
import os 


app.secret_key = "secret key"

#move to confi ini
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extension 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True



@app.route("/bulk_upload", methods=["POST"])
def bulk_upload():
    print("Filessss Object ... XXX")
    print(request.files)
    
    if 'files' not in request.files:
        flash('No files found')
        return 'No files found.'
    unploaded_files = []
    files = request.files.getlist('files')
    for file in files:
        filename = secure_filename(file.filename)
        if os.path.exists((os.path.join(app.config['UPLOAD_FOLDER'], filename))):
            print(f"am heree.. {filename} already exists.")
            unploaded_files.append(filename)
            continue
        else:
            print(f'{filename} - is being saved.')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if unploaded_files:
        return f'Duplicate files, please upload following files with different name: {unploaded_files}'    
    
    return 'Upload succesfull.'