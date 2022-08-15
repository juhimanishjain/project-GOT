# Using raw cypher queries
import logging
from flask import Flask, jsonify, make_response, Blueprint
from py2neo import Graph

logging.basicConfig(level=logging.INFO)
app=Flask(__name__)
api_v1=Blueprint('api_v1', __name__, url_prefix='v1')
graph=Graph("bolt://localhost:7687", auth=("neo4j", "812050"))

@api_v1.route('/characters', methods=['GET'])
def get_all_characters():
  query_result=graph.run("MATCH (n: Character) return n")
  characters=[characters[0] for characters in query_result]
  return make_response(jsonify(characters), 200)

@api_v1.route('/characters/<id>', methods=['GET'])
def get_chaaracter_by_id(id):
  query_run=graph.run(
    "MATCH (n:Character) WHERE id(n)=$got_id RETURN n", got_id=int(id)
  )
  character = query_run.evaluate()
  character['id']=id
  return make_response(jsonify(character))

@api_v1.route('/characters/<name>/betrayed_by', methods=['GET'])
def get_betrayls(name: str):
  character=graph.run("MATCH (c:Characters) WHERE c.name=$name return c", name=name).evaluate()
  if not character:
    return make_response(
      jsonify(error=f"Couldn't find character with {name=}"), 400)
  cypher_query="MATCH (traitor)-[betrayal]->(victim: Character {name: $name}) RETURN traitor, betrayal, victim"
  query_result=graph.run(cypher_query, name=name)
  betrayals = [betrayal for betrayal in query_result]
  return make_response(jsonify(betrayals))

