import os
from flask import Flask, request, send_file
from uuid import uuid4
from werkzeug.utils import secure_filename
import creator

UPLOAD_FOLDER = '/home/claudiu/calendarGenerator/callirhoe/uploads'

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@application.route('/generate', methods=['POST'])
def generate_pdf():
    file = request.files['file']
    idName = str(uuid4())
    filename = secure_filename(idName + '.csv')
    file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

    creator.main_program(os.path.join(application.config['UPLOAD_FOLDER'], filename), idName)
    return send_file(secure_filename(idName + '.pdf'))

@application.route('/')
def home():
    return 'hello'

