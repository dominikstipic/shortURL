from flask import Flask, request, send_file, render_template
import flask
from datetime import datetime
from waitress import serve
import logging
import json
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

MY_IP = None

def clean_string(s):
    result = ""
    for i in range(len(s)):
        c = s[i]
        if c == '"':continue
        else:
            result+=c
    return result

def log_request(resource_name, entity_name, self_request_check=True):
    if self_request_check:
        global MY_IP
        foreign_ip = clean_string(request.remote_addr)
        if foreign_ip == MY_IP:
            print("local request")
            return
    request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = {"resource_name": resource_name,
         "request_method": request.method, 
         "request_date": request_date, 
         "request_uri": request.url,
         "user-agent": request.headers.get('User-Agent'),
         "my_ip": MY_IP,
         "ip": foreign_ip,
         "entity": entity_name,
         "cookies": None}
    cookies_dict = {}
    for k,v in request.cookies.items(): cookies_dict[k] = v
    d["cookies"] = cookies_dict
    d["cookies_length"] = len(cookies_dict)
    logger = logging.getLogger("doms")
    logger.info("{0}".format(d))

def get_log_request():
    request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = {"request_method": request.method, 
         "request_date": request_date, 
         "request_uri": request.url,
         "origin": request.origin,
         "headers": dict(request.headers),
         "referrer": request.referrer,
         "user-agent": request.headers.get('User-Agent'),
         "my_ip": request.remote_addr,
         "cookies": None}
    cookies_dict = {}
    for k,v in request.cookies.items(): cookies_dict[k] = v
    d["cookies"] = cookies_dict
    d["cookies_length"] = len(cookies_dict)
    return d

def transform_log_to_json_list(log_path) -> list:
    result = []
    with open(log_path, "r") as fp:
        lines = fp.readlines()
        for row in lines:
            row = row.replace("INFO:doms:","")
            row = row.replace("'", '"')
            dictionary = json.loads(row)
            result.append(dictionary)
    return result

#######################################

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

@app.route('/test/<regex("[a-zA-Z0-9_]+?"):entity>', methods=['GET'])
def test(entity):
    log_request("test", entity)
    result = []
    with open("example.log") as fp:
        result = fp.readlines()
    return result

@app.route('/ip', methods=['POST'])
def ip():
    global MY_IP
    data = request.data.decode()
    data = clean_string(data)
    MY_IP = data
    print(f"current ip address: {data}")
    return "200"

@app.route('/live', methods=['GET'])
def is_live():
    return get_log_request()

@app.route('/logs', methods=['GET'])
def get_logs():
    log_request()
    return transform_log_to_json_list("example.log")

if __name__ == "__main__":
    print("Starting server!")
    #serve(app, host="0.0.0.0", port=82)
    app.run(host="127.0.0.1", port=8080, debug=True)