# Create a mixed index mapping (text) for 'bio' property to allow full-text search via Elasticsearch
from gremlin_python.driver.client import Client
from gremlin_python.driver import serializer

GREMLIN_SERVER = "ws://localhost:8182/gremlin"
client = Client(GREMLIN_SERVER, 'g', message_serializer=serializer.GraphSONSerializersV3d0())

groovy = '''
mgmt = graph.openManagement()
bioKey = mgmt.getPropertyKey('bio')
if (bioKey==null) {
  bioKey = mgmt.makePropertyKey('bio').dataType(String.class).make()
}

// Check if index already exists
if (!mgmt.getGraphIndexes(Vertex.class).any{ it.name().equals('byBio') }) {
  mgmt.buildIndex('byBio', Vertex.class)
      .addKey(bioKey, org.janusgraph.core.schema.Mapping.TEXT.asParameter())
      .buildMixedIndex('search')
}
mgmt.commit()
'''

print(client.submit(groovy).all().result())
client.close()

