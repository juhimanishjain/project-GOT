from flask import Flask, jsonify, make_response
from py2neo import Graph
from api_v1 import api_v1
from api_v2 import api_v2

import logging

logging.basicConfig(level=logging.INFO)
app=Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/v1')
app.register_blueprint(api_v2, url_prefix='/v2')

if __name__=='__main__':
  app.run()
