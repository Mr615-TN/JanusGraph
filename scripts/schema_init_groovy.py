# schema_init_groovy.py
# Submits a Gremlin-Groovy schema creation string to Gremlin Server using gremlinpython Client.
from gremlin_python.driver.client import Client

GREMLIN_SERVER = "ws://localhost:8182/gremlin"
client = Client(GREMLIN_SERVER, 'g')

groovy = '''
mgmt = graph.openManagement()
if (!mgmt.containsPropertyKey("uuid")) {
  uuid = mgmt.makePropertyKey("uuid").dataType(String.class).cardinality(org.janusgraph.core.Cardinality.SINGLE).make()
}
if (!mgmt.containsPropertyKey("name")) {
  name = mgmt.makePropertyKey("name").dataType(String.class).make()
}
if (!mgmt.containsPropertyKey("bio")) {
  bio = mgmt.makePropertyKey("bio").dataType(String.class).make()
}
if (!mgmt.containsVertexLabel("person")) {
  mgmt.makeVertexLabel("person").make()
}
if (!mgmt.containsPropertyKey("age")) {
  age = mgmt.makePropertyKey("age").dataType(Integer.class).make()
}
if (!mgmt.getGraphIndexes(Vertex.class).any{ it.name().equals("byUuid") }) {
  mgmt.buildIndex("byUuid", Vertex.class).addKey(mgmt.getPropertyKey("uuid")).unique().buildCompositeIndex()
}
mgmt.commit()
'''

print("Submitting schema...")
res = client.submit(groovy).all().result()
print("Result:", res)
client.close()
