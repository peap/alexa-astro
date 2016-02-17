#!/usr/bin/env python
import logging

from flask import Flask, jsonify, render_template, request

from alexa import AlexaResponse, get_response

logging.basicConfig(level=logging.WARN)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    # TODO: verify it's Alexa calling us
    try:
        alexa_response = get_response(request.json)
    except ValueError:
        alexa_response = AlexaResponse('Bad request, sorry.')
    return jsonify(alexa_response.to_dict())


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: ./server.py host:port\n')
        sys.exit(1)
    app.config.update({
        'SERVER_NAME': sys.argv[1],
        'DEBUG': True,
    })
    app.run()
