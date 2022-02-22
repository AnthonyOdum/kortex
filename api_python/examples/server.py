#!/usr/bin/env python3
import sys,os

from flask import Flask, render_template, request, redirect, url_for
from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient
from cyberpunk_test_2 import main, example_move_to_home_position
from server_test import robotics_test
from server_test_2 import server_test
from cyberpunk_test import robot_demo, robot_panning


app = Flask(__name__)

@app.route('/')
def index():
    robot_panning()
    return 'I am alive!'
    
@app.route('/panning', methods=['GET', 'POST'])
def pan():
    if(request.method == 'POST'):
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
    robot_panning(x,y,z)

@app.route('/start')
def start_demo():
    robotics_test()
    
    return 'demo complete'

@app.route('/home')
def go_home():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    args = utilities.parseConnectionArguments()
    
    # Create connection to the device and get the router
    with utilities.DeviceConnection.createTcpConnection(args) as router:

        # Create required services
        base = BaseClient(router)
        

        # Example core
        success = True
        success &= example_move_to_home_position(base)
    
    return redirect('http://localhost:3000/')
    



@app.route('/move', methods=['GET', 'POST'])
def start_other_demo():
    if(request.method == 'POST'):
        x = request.form.get('x')
        y = request.form.get('y')
        z = request.form.get('z')
    server_test(x,y,z)

    return redirect('http://localhost:3000/')

@app.route('/moveRobot', methods=['GET', 'POST'])
def start_other_other_demo():
    if(request.method == 'POST'):
        x = float(request.form.get('x'))
        y = float(request.form.get('y'))
        z = float(request.form.get('z'))
    robot_demo(x,y,z)

    return redirect('http://localhost:3000/')

if __name__ == '__main__':
    app.run(debug=True)