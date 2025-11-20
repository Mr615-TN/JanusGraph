import os
import csv
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __

# --- Setup JanusGraph Connection ---
graph = Graph()
connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
client = graph.traversal().withRemote(connection)

# --- CSV File ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, "../data/fun_people_long.csv")

# --- Helper Functions ---
def add_vertex(name, bio):
    """Add a person vertex if not exists."""
    existing = client.V().has("name", name).toList()
    if existing:
        return existing[0]
    return client.addV("person").property("name", name).property("bio", bio).next()

def add_edge(from_vertex, to_vertex):
    """Add a 'knows' edge if it doesn't exist."""
    # Check if edge already exists
    edge_count = client.V(from_vertex.id).outE("knows").where(
        __.inV().hasId(to_vertex.id)
    ).count().next()
    
    if edge_count == 0:
        # Use iterate() instead of next() to avoid deserializing the edge
        client.V(from_vertex.id).addE("knows").to(__.V(to_vertex.id)).iterate()


def get_neighbors(name):
    """Return neighbors of a person."""
    return client.V().has("name", name).out("knows").valueMap(True).toList()

def get_known_by(name):
    """Return people who know the given person."""
    # Using inE + outV for compatibility
    return client.V().has("name", name).inE("knows").outV().valueMap(True).toList()

# --- Import CSV ---
vertices = {}
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        person_vertex = add_vertex(row["name"], row.get("bio", ""))
        vertices[row["name"]] = person_vertex

# --- Add edges ---
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        knows_field = row.get("knows", "")
        if knows_field:
            friends = [name.strip() for name in knows_field.split(",") if name.strip()]
            for friend_name in friends:
                if friend_name in vertices:
                    add_edge(vertices[row["name"]], vertices[friend_name])

print("Imported vertices and edges successfully!\n")

# --- Print Summary ---
print("=== Graph Summary ===\n")
for name, vertex in vertices.items():
    neighbors = get_neighbors(name)
    neighbor_names = [n["name"][0] for n in neighbors]
    known_by = get_known_by(name)
    known_by_names = [n["name"][0] for n in known_by]
    print(f"{name} knows: {neighbor_names}")
    print(f"{name} is known by: {known_by_names}\n")
print("=== End of Summary ===")

# --- Close connection ---
connection.close()
