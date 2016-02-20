#!/usr/bin/env python
import logging

from flask import Flask, jsonify, render_template, request

from app.alexa import AlexaResponse, get_response

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    try:
        alexa_response = get_response(request)
    except ValueError:
        alexa_response = AlexaResponse('Bad request, sorry.')
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
