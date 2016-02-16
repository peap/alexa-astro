#!/usr/bin/env python
import logging

from flask import Flask, request, jsonify

from alexa import get_response

logging.basicConfig(level=logging.WARN)

app = Flask(__name__)


# TODO: add POST route just for Alexa requests; main page GET should be webpage

@app.route('/', methods=['GET'])
def homepage():
    return 'hey!'


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    # TODO: verify it's Alexa calling us
    try:
        alexa_response = get_response(request.json)
    except ValueError:
        # TODO: return valid response for Alexa
        response_data = {'error': True}
    else:
        response_data = alexa_response.to_dict()
    return jsonify(response_data)


if __name__ == '__main__':
    import sys
    # TODO: show usage if no argv[1]
    app.config['SERVER_NAME'] = sys.argv[1]
    print('launching server')
    app.run()
