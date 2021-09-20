from flask import flash, request, redirect, render_template, url_for
from app.routes.auth import auth
from werkzeug.utils import secure_filename
from app import app
import os 
import json


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


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/read_files")
@auth.login_required
def read_files():    
    '''
    Test endpoint using curl
    curl -v localhost:4747/read_files
    '''
    file_folder = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return {"message" : file_folder}


@app.route("/bulk_upload", methods=["POST"])
@auth.login_required
def bulk_upload():    
    '''
    Test endpoint using curl
    curl -v -X POST -F files=@'Assignment 2.pdf' -F files=@'test3' localhost:4747/bulk_upload
    '''
    if 'files' not in request.files:
        return 'No files found.'
    unploaded_files = []
    files = request.files.getlist('files')
    for file in files:
        filename = secure_filename(file.filename)
        if os.path.exists((os.path.join(app.config['UPLOAD_FOLDER'], filename))):
            print(f"{filename} - already exists.")
            unploaded_files.append(filename)
            continue
        if allowed_file(filename):
            print(f'{filename} - is being saved.')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            # flash('Wrong file format.')
            # return redirect(url_for("index"), code=422)
            return {"message": f"Issue with file format, Allowed format - {ALLOWED_EXTENSIONS}"}

    if unploaded_files:
        # flash(f'File with same name already exists - {unploaded_files}')
        # return redirect(url_for("index"), code=422)
        return {"message": f"File name with same already exoists -{unploaded_files}"}
    return {"message" : "Upload succesfull."}

@app.route("/bulk_delete", methods=['POST'])
@auth.login_required
def delete_files():
    '''
    Get list of image to delete, using json
    and then remove from the system.
    curl -v -H "Content-Type: application/json" -X POST -d '{"name": "working", "file_names":["test3"]}' localhost:4747/delete_files
    '''
    issue_in_deleting_files = []
    data = json.loads(request.data)
    for file_name in data['file_names']:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        if os.path.exists(file_path):
            try:
                print(f'{file_name} - Deleted')
                os.remove(file_path)
            except Exception as e:
                issue_in_deleting_files.append(file_name)
                continue
    
    if issue_in_deleting_files:
        return {"message":f'Some File Had Issue while removing : {issue_in_deleting_files}'}
    return {"message": 'Files deleted'}