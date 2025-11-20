from gremlin_python.driver.client import Client
from gremlin_python.driver import serializer

GREMLIN_SERVER = "ws://localhost:8182/gremlin"

client = Client(
    GREMLIN_SERVER,
    "g",
    message_serializer=serializer.GraphSONSerializersV3d0()
)

# 1️⃣ Add vertices safely
groovy_add_vertices = """
alice = g.V().has('name','Alice').tryNext().orElseGet{
    graph.addVertex(label,'person','name','Alice','bio','Software engineer')
}
bob = g.V().has('name','Bob').tryNext().orElseGet{
    graph.addVertex(label,'person','name','Bob','bio','Data scientist')
}
carol = g.V().has('name','Carol').tryNext().orElseGet{
    graph.addVertex(label,'person','name','Carol','bio','ML researcher')
}

if (!g.V(alice.id()).out('knows').hasId(bob.id()).hasNext()) {
    alice.addEdge('knows', bob)
}
if (!g.V(bob.id()).out('knows').hasId(carol.id()).hasNext()) {
    bob.addEdge('knows', carol)
}

graph.tx().commit()
"Added vertices and edges successfully"
"""
print(client.submit(groovy_add_vertices).all().result()[0])

# 2️⃣ Traversal example: neighbors of Alice
groovy_neighbors = """
alice_id = g.V().has('name','Alice').id().next()
g.V(alice_id).out('knows').valueMap('name','bio')
"""
neighbors = client.submit(groovy_neighbors).all().result()
print("Neighbors of Alice:", neighbors)

# 3️⃣ Traversal example: neighbors of Bob
groovy_neighbors_bob = """
bob_id = g.V().has('name','Bob').id().next()
g.V(bob_id).out('knows').valueMap('name','bio')
"""
neighbors_bob = client.submit(groovy_neighbors_bob).all().result()
print("Neighbors of Bob:", neighbors_bob)

# 4️⃣ People who know Alice (fixed)
groovy_knows_alice = """
alice_id = g.V().has('name','Alice').id().next()
g.V().inE('knows').where(outV().hasId(alice_id)).outV().valueMap('name','bio')
"""
knows_alice = client.submit(groovy_knows_alice).all().result()
print("People who know Alice:", knows_alice)

client.close()

