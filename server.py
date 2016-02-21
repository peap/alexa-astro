#!/usr/bin/env python
import logging

from flask import abort, jsonify, render_template, request

from app import app
from app.alexa import AlexaRequest
from app.handlers import dispatch

logging.basicConfig(level=logging.INFO)
logging.getLogger('requests').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    try:
        alexa_request = AlexaRequest(request)
    except ValueError:
        abort(400)

    if alexa_request.is_valid():
        alexa_response = dispatch(alexa_request)
    else:
        abort(403)

    return jsonify(alexa_response.to_dict())


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: ./server.py host:port\n')
        sys.exit(1)
    host, port = sys.argv[1].split(':')
    sys.stdout.write('Starting server at {0}:{1}\n'.format(host, port))
    app.config.update({
        'HOST': host,
        'PORT': port,
        'DEBUG': True,
    })
    app.run(host=host, port=int(port))
