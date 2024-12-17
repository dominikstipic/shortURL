from flask import Flask, request, send_file, render_template
import flask
from datetime import datetime
from waitress import serve
import logging
from werkzeug.routing import BaseConverter

app = Flask(__name__, template_folder=".")
logger = logging.getLogger("doms")
logging.basicConfig(filename="example.log", level=logging.INFO)
logging.getLogger('werkzeug').disabled = True

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

#######################################

def log_request(resource_name, entity_name):
    request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = {"resource_name": resource_name,
         "request_method": request.method, 
         "request_date": request_date, 
         "request_uri": request.url,
         "user_agent": request.user_agent,
         "cookies": request.cookies,
         "user_agent": request.user_agent,
         "cookies": request.cookies,
         "ip": request.remote_addr,
         "entity": entity_name}
    logger = logging.getLogger("doms")
    logger.info("{0}".format(d))

@app.route("/")
def index():
    return render_template('htmls/index.html')

@app.route('/is/<regex("[a-zA-Z0-9_]+"):entity>', methods=['GET'])
def iron_standard(entity):
    print("Product")
    log_request("is", entity)
    return send_file('repo/is.png', mimetype='png')


@app.route('/me/<regex("[a-zA-Z0-9_]+"):entity>', methods=['GET'])
def me(entity):
    print("ME")
    log_request("ME", entity)
    return send_file('repo/cv.png', mimetype='png')

@app.route('/feud/<regex("[a-zA-Z0-9_]+"):entity>', methods=['GET'])
def grb(entity):
    print("Feudal")
    log_request("feud", entity)
    return send_file('repo/grb.png', mimetype='png')

@app.route('/octo/<regex("[a-zA-Z0-9_]+"):entity>', methods=['GET'])
def octo(entity):
    print("Octo")
    log_request("octo", entity)
    return send_file('repo/octo.png', mimetype='png')

@app.route("/memory")
def memory():
    log_request("memory")
    return send_file('repo/memory.mp4', mimetype='mp4')

@app.route("/user/<id>")
def qr_scan(id):
    print(id)
    return "200"

@app.route("/registration", methods=["POST"])
def registration():
    user_data = request.json
    print(user_data)
    return "200"

@app.route("/vimeo/book", methods=["POST"])
def vimeo():
    return flask.redirect("https://vimeo.com/1030737980", code=302)

@app.route("/authentication", methods=["POST"])
def auth(credentials):
    print(credentials)
    user_data = request.json
    print(user_data)
    return "200"

@app.route("/test", methods=["GET"])
def test():
    log_request("test")
    return "200"


if __name__ == "__main__":
    print("Starting server!")
    #serve(app, host="0.0.0.0", port=82)
    app.run(host="127.0.0.1", port=8080, debug=True)