import zmq
import json
import os
import sys
import tkinter as tk
from tkinter import ttk

# Add the common directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import common.zmqHeader as zmqHeader

# Function to process and print messages
def messagePrint(msg):
    try:
        print(msg)
        msg = json.loads(msg)
        tx_id = msg.get("tx_id", "Unknown")
        content = msg.get("content", {})
        if tx_id in worker_labels:
            worker_labels[tx_id].config(text=f"Worker {tx_id}\nLat: {content.get('latitude', 'N/A')}\nLon: {content.get('longitude', 'N/A')}")
        else:
            create_worker_box(tx_id, content)
    except Exception as e:
        print(f"Error: {e}\nNOT JSON: {msg}")

# Function to create a worker box
def create_worker_box(tx_id, content):
    frame = tk.Frame(root, bd=2, relief="sunken")
    label = tk.Label(frame, text=f"Worker {tx_id}\nLat: {content.get('latitude', 'N/A')}\nLon: {content.get('longitude', 'N/A')}", padx=10, pady=10)
    label.pack()
    frame.pack(pady=5, padx=5, fill="x")
    worker_labels[tx_id] = label

# Function to handle worker selection
def controlWorker():
    # This function can be filled with logic to control the selected worker
    pass

# Initialize the ZMQ connection
zmqObj = zmqHeader.ZMQ_CONNECTION(
    TX_ID="MOTHER",
    RX_ID="ROUTER",
    SERVER_IP="tcp://3.22.90.156:5555",
    message_handler=messagePrint
)

zmqObj.connectZMQ()

# Start listening to messages
zmqObj.startListenThread()

# Initialize Tkinter
root = tk.Tk()
root.title("Worker Manager")

# Create a dictionary to hold the labels for each worker
worker_labels = {}

# Start the Tkinter main loop
root.mainloop()
