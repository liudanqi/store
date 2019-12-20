#!/usr/bin/env python3

import os
import sys

from flask import Flask

from user.front import bp
from flask_bootstrap import Bootstrap
#app.config.from_pyfile('config')
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

if __name__ == '__main__':
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.register_blueprint(bp)
    app.config.from_pyfile('C:\\Users\\starr\\bookstore\\config.py')
    app.run()
