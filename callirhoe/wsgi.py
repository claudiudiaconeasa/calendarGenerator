from main import application
import os
import logging

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)

application.logger.info(os.getcwd())

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=1337)
