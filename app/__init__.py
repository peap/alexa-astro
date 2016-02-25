from flask import Flask, abort, jsonify, render_template, request

from app import settings


app = Flask('alexa-astro')
app.config.from_object(settings)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('home.html')


@app.route('/alexa/', methods=['POST'])
def incoming_alexa_request():
    from app.alexa import AlexaRequest
    from app.handlers import dispatch
    try:
        alexa_request = AlexaRequest(request)
    except ValueError:
        abort(400)

    if alexa_request.is_valid():
        alexa_response = dispatch(alexa_request)
    else:
        abort(403)

    return jsonify(alexa_response.to_dict())
