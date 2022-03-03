from flask import Flask, render_template, jsonify, request, Response, redirect, url_for, abort, session, send_file
import argparse
import sys
import json
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
from datetime import datetime
from itertools import zip_longest
gevent.monkey.patch_all()
import os
from os.path import join, dirname, realpath
import time
import preprocess
import ip_process
import ai_process
from networklog import NetworkLog
import secrets


app = Flask(__name__)

global networklogs
# To be confirmed on the final iteration
# Leave all the code here for after backend is done ****
#networklog_by_key = {networklog.key: networklog for networklog in networklogs}
#networklog_by_attack = {networklog.attack: networklog for networklog in networklogs}
#networklogAttack = []
#networklogHTML = []
#for i in networklogs:
    #if i.attack not in networklogAttack:
        #networklogAttack.append(i.attack)
#longest = range(len(networklogs))
#zipped = zip_longest(networklogs, networklogAttack, longest, fillvalue='?')
#for i in zipped:
    #networklogHTML.append(i)

# temporary only
networklogs = [
    NetworkLog('0', '192.168.10.21',      'Singapore',   37.9045286, -122.1445772, 'Ransomware'),
    NetworkLog('1', '192.167.21.21', 'Malaysia', 37.8884474, -122.1155922, 'Ransomware'),
    NetworkLog('2', '1.23.12.1',     'Japan', 25.9093673, -126.0580063, 'Ddos'),
    NetworkLog('3', '192.167.21.25', 'Korea', 1.43801, 103.789, 'Ddos'),
]
networklog_by_key = {networklog.key: networklog for networklog in networklogs}

# For uploading files
# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
app.config['UPLOAD_FOLDER'] =  'static/files'
app.config['SECRET_KEY'] =  secrets.token_hex(16)


###################### Upload Page ################################################################
@app.route("/" )
def upload():
    return render_template('index.html')

# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file

      return redirect(url_for('processing'))

###################### Upload Page END ############################################################


###################### Processing #################################################################
@app.route("/processing")
def processing():
    # do all processing here
    # Preprocess data
    # Feed into IP api
    # Feed into AI model
    # Generate CSV
    # Return networklogs and go to home page
    
    print(ip_process.geolocation("223.25.69.206"))
    return redirect(url_for('home'))
###################### Processing End #############################################################
###################### Main Page ################################################################
@app.route("/home")
def home():
    return render_template('home.html', networklogs=networklogs)

@app.route("/home/<keycode>")
def homeShowDetails(keycode):
    networklog = networklog_by_key.get(keycode)
    if networklog:
        return render_template('info.html', networklog=networklog)
    else:
        abort(404)

@app.route("/home/heatmap")
def heatmap():
    return render_template('heatmap.html', networklogs=networklogs)

@app.route('/home/download')
def download():
   path = "static/download/output.csv" 
   return send_file(path , as_attachment=True)

###################### Main Page End############################################################





if __name__ == '__main__':
   try:

        host = '0.0.0.0'
        port = 80
        parser = argparse.ArgumentParser()
        parser.add_argument('port',type=int)

        args = parser.parse_args()
        if args.port:
            port = args.port

        http_server = WSGIServer((host, port), app)
        app.debug = True
        http_server.serve_forever()
   except:
        print("Exception while running web server")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
