from flask import Flask, render_template, jsonify
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader

app = Flask(__name__)

# Flask route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to get worker data in JSON format
@app.route('/workers')
def get_workers():
    return jsonify(workers_data)

# Function to create the worker display box
def render_worker(name, active, gps, clickable):
    return {
        'name': name,
        'active': active,
        'gps': gps,
        'clickable': clickable
    }


def messageDigst(msg):
    try:
        msg = json.loads(msg)
        print("Turned into Json")
    except:
        try:
            msg = eval(msg)
            print("Turned into Dict")
        except Exception as e:
            if isinstance(msg,str):
                return
            print("Neither dict or Json: ",e)
    if msg["msg_name"] == "register":
        createWorker(msg)
    elif msg["msg_name"] == "register_list":
        createWorkers(msg)
    elif msg["msg_name"] == "GPS":
        print("Updating ",msg["tx_id"]," GPS location")

# Start the ZeroMQ subscriber in a background thread
if __name__ == '__main__':
    zmqObj = zmqHeader.ZMQ_CONNECTION(
        TX_ID="MOTHER",
        RX_ID="ROUTER",
        SERVER_IP="tcp://3.22.90.156:5555",
        message_handler=messageDigst
    )

    zmqObj.connectZMQ()
    zmqObj.startListenThread()

    # Start listening to messages
    #threading.Thread(target=zmqObj.startListenThread(), args=(render_worker,), daemon=True).start()
    app.run(debug=True)
