from flask import Flask, request, send_file
from datetime import datetime
from waitress import serve
from models import write

app = Flask(__name__, template_folder=".")

def log_request():
    request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = {"request_method": request.method, 
         "request_date": request_date, 
         "request_uri": request.url,
         "ip": request.remote_addr}
    write(d)

@app.route("/memory")
def memory():
    log_request()
    return send_file('repo/memory.mp4', mimetype='mp4')



if __name__ == "__main__":
    print("Starting server!")
    #app.run(host="127.0.0.1", port=8080, debug=True)
    serve(app, host="0.0.0.0", port=80)