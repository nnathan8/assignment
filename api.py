from flask import Flask, request, jsonify, redirect, render_template
from neo4j import GraphDatabase
import csv

# Establish a connection to the Neo4j database by reading credentials from a file
with open("cred.txt") as f1:
    data = csv.reader(f1, delimiter=",")
    for row in data:
        username = row[0]
        pwd = row[1]
        uri = row[2]
print(username, pwd, uri)

# Create a driver to interact with Neo4j database
driver = GraphDatabase.driver(uri=uri, auth=(username, pwd))
session = driver.session()
print(session)

# Initialize Flask application
api = Flask(__name__)

# Define a route to create a new employee node
@api.route("/create/<string:name>&<int:id>", methods=["GET", "POST"])
def create_node(name, id):
    # Cypher query to create an employee node with provided name and id
    q1 = """
    CREATE (n:Employee {NAME: $name, ID: $id})
    """
    map = {"name": name, "id": id}
    try:
        session.run(q1, map)
        return f"Employee node is created with employee name={name} and id={id}"
    except Exception as e:
        return str(e)

# Define a route to display all nodes
@api.route("/display", methods=["GET", "POST"])
def display_node():
    # Cypher query to match and return all nodes
    q1 = """
    MATCH (n) RETURN n{.*}
    """
    results = session.run(q1)
    data = results.data()
    return jsonify(data)

# Define a route to update an existing employee node
@api.route("/update/<string:name>&<string:city>", methods=["GET", "POST"])
def update_node(name, city):
    # Cypher query to update the city of an employee node based on the name
    q1 = """
    MATCH (n:Employee {NAME: $name}) SET n.city = $city
    """
    map = {"name": name, "city": city}
    try:
        session.run(q1, map)
        return f"Employee node is updated with employee name={name} and city={city}"
    except Exception as e:
        return str(e)

# Define a route to delete an employee node
@api.route("/delete/<string:name>", methods=["GET", "POST"])
def del_node(name):
    # Cypher query to delete an employee node based on the name
    q1 = """
    MATCH (n:Employee {NAME: $name}) DETACH DELETE n
    """
    map = {"name": name}
    try:
        session.run(q1, map)
        return f"Employee node is deleted with employee name={name}"
    except Exception as e:
        return str(e)

# Start the Flask application on port 5050
if __name__ == "__main__":
    api.run(port=5050)
