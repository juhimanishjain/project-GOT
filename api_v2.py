# Using object graph mappers
import json
import logging
from flask import Flask, jsonify, make_response, Blueprint, Response, request
from py2neo import Graph
import json
from py2neo.matching import *

logging.basicConfig(level=logging.INFO)
app=Flask(__name__)
api_v2=Blueprint('api_v2', __name__, url_prefix='v1')
graph=Graph("bolt://localhost:7687", auth=("neo4j", "812050"))

@api_v2.route('/characters', methods=['GET'])
def get_all_characters():
  nodes = NodeMatcher(graph)
  characters = nodes.match("Character").all()
  return make_response(jsonify(characters), 200)

@api_v2.route('/characters/<id>', methods=['GET'])
def get_chaaracter_by_id(id):
  nodes = NodeMatcher(graph)
  try:
    character=nodes[int(id)]
  except KeyError:
    return make_response(jsonify({"error":f"couldn't find the character with the id = {int(id)}"}), 400)
  return make_response(jsonify(character))

@api_v2.route('/characters/', methods=['POST'])
def get_characters_by_properties_v2(name: str):
  nodes = NodeMatcher(graph)
  properties = json.loads(request.data)
  nodes_match = nodes.match("Character", **properties).all()
  return Response(json.dumps(nodes_match), mimetype="application/json")

