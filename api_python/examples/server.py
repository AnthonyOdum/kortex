#!/usr/bin/env python3
import sys,os

from flask import Flask, render_template
from cyberpunk_test_2 import main

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/start')
def start_demo():
    main()
    
    return 'demo complete'

if __name__ == '__main__':
    app.run(debug=True)