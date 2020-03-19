import os
import multiprocessing
from flask import Flask, request, send_file, Response
from uuid import uuid4
from werkzeug.utils import secure_filename
import creator
from flask_cors import CORS

UPLOAD_FOLDER = '/home/claudiu/calendarGenerator/callirhoe/uploads'

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(application)

process_mapper = {}

@application.route('/generate', methods=['POST'])
def generate_pdf():
    file = request.files['file']
    idName = str(uuid4())
    filename = secure_filename(idName + '.csv')
    file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))

    #creator.main_program(os.path.join(application.config['UPLOAD_FOLDER'], filename), idName)
    p = multiprocessing.Process(target=creator.main_program, args=(os.path.join(application.config['UPLOAD_FOLDER'], filename), idName))
    p.start()

    process_mapper[idName] = p

    #return send_file(secure_filename(idName + '.pdf'))
    return idName


@application.route('/poll')
def poll_pdf():
    idName = request.args['idname']
    filename = secure_filename(idName + '.pdf')
    
    if idName not in process_mapper.keys():
        return 'Id not found'

    if process_mapper[idName].is_alive():
        calendar_ready = False
    else:
        if os.path.exists(os.path.join(filename)):
            calendar_ready = True
        else:
            calendar_ready = False

    if calendar_ready:
        return send_file(filename)
    else:
        return 'Calendar not generated yet'

@application.route('/')
def home():
    return 'hello'

