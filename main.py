from flask import Flask, request, send_file, render_template
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

@app.route("/me")
def me():
    return send_file('repo/me.png', mimetype='png') 

@app.route("/registration", methods=["POST"])
def registration():
    user_data = request.json
    print(user_data)
    return "200"

if __name__ == "__main__":
    print("Starting server!")
    app.run(host="127.0.0.1", port=8080, debug=True)
    #serve(app, host="0.0.0.0", port=80)