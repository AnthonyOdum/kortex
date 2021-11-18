#!/usr/bin/env python3
import sys,os

from flask import Flask, render_template, request, redirect, url_for
from cyberpunk_test_2 import main
from robotics_test import robotics_test
from server_test_2 import server_test
from cyberpunk_test import robot_demo
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/start')
def start_demo():
    robotics_test()
    
    return 'demo complete'

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