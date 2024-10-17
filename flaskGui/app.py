from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import io
import traceback
import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions from terminal_connect.py
from terminal_connect.terminal_connect import handleMessage, connectRouter, startListen, startTransmission, getBots, worker_objects

app = Flask(__name__)

# Initialize Pygame and joystick
# import pygame
# pygame.init()
# pygame.joystick.init()
# if pygame.joystick.get_count() == 0:
#     print("No joystick detected.")
# else:
#     joystick = pygame.joystick.Joystick(0)  # Get the first joystick
#     joystick.init()

@app.route('/')
def index():
    # Capture print statements
    log_stream = io.StringIO()
    sys.stdout = log_stream  # Redirect stdout to capture print statements

    # Get available bots
    #getBots()  # Call the function to get the bots
    workers = worker_objects  # Assuming worker_objects is updated in terminal_connect.py

    # Restore stdout
    sys.stdout = sys.__stdout__
    log_output = log_stream.getvalue()  # Get the captured output

    return render_template('index.html', workers=workers, log_output=log_output)

@app.route('/get_gps_data')
def get_gps_data():
    try:
        gps_data = {}
        print(f"worker_objects type: {type(worker_objects)}")
        print(f"worker_objects content: {worker_objects}")
        
        for worker in worker_objects:
            print(f"Worker type: {type(worker)}")
            print(f"Worker content: {worker_objects[worker]}")
            print(f"Worker GPS: {worker_objects[worker].gps}")
            
            gps_dict = worker_objects[worker].gps
            
            # Handle the case where gps_dict is None or not a dictionary
            if gps_dict is None or not isinstance(gps_dict, dict):
                lat, lon = None, None
            else:
                lat = gps_dict.get('lat')
                lon = gps_dict.get('lon')
            
            gps_data[worker] = {
                'lat': lat,
                'lon': lon
            }
        
        print("Sending GPS data:", gps_data)  # Debug print
        return jsonify(gps_data)
    except Exception as e:
        print(f"Error in get_gps_data route: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/select_bot', methods=['POST'])
def select_bot():
    bot_name = request.form['bot_name']
    startTransmission(bot_name)  # Start transmission for the selected bot
    return redirect(url_for('index'))

@app.route('/connect_router')
def connect_router():
    connectRouter()  # Connect to the router
    return redirect(url_for('index'))

@app.route('/start_listen')
def start_listen():
    startListen()  # Start listening for messages
    getBots()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)