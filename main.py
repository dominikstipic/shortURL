from flask import Flask, request, send_file, render_template
from datetime import datetime
from waitress import serve
import logging
from utils import get_ip_address

app = Flask(__name__, template_folder=".")
logger = logging.getLogger("doms")
logging.basicConfig(filename="example.log", level=logging.INFO)
logging.getLogger('werkzeug').disabled = True

def log_request(resource_name):
    ip = get_ip_address()
    if ip == request.remote_addr:
        entity = "me"
    else:
        entity = "other"
    request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = {"resource_name": resource_name,
         "request_method": request.method, 
         "request_date": request_date, 
         "request_uri": request.url,
         "ip": request.remote_addr,
         "entity": entity}
    logger = logging.getLogger("doms")
    logger.info("{0}".format(d))

@app.route("/")
def index():
    return render_template('htmls/index.html')


@app.route("/is")
def iron_standard():
    log_request("is")
    return send_file('repo/is.png', mimetype='png')

@app.route("/grb")
def grb():
    log_request("grb")
    return send_file('repo/grb.png', mimetype='png')

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



if __name__ == "__main__":
    print("Starting server!")
    #app.run(host="127.0.0.1", port=8080, debug=True)
    serve(app, host="0.0.0.0", port=80)