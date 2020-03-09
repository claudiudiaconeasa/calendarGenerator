import os
from flask import Flask, request, send_file
from uuid import uuid4
from werkzeug.utils import secure_filename
import creator

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/generate', methods=['POST'])
def generate_pdf():
    file = request.files['file']
    idName = str(uuid4())
    filename = secure_filename(idName + '.csv')
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    creator.main_program(os.path.join(app.config['UPLOAD_FOLDER'], filename), idName)
    return send_file(secure_filename(idName + '.pdf'))

if __name__ == '__main__':
    app.run()
