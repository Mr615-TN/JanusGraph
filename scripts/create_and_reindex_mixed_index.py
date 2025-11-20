from gremlin_python.driver.client import Client
from gremlin_python.driver import serializer

GREMLIN_SERVER = "ws://localhost:8182/gremlin"
INDEX_NAME = "byBio"
PROPERTY_KEY = "bio"
MIXED_INDEX_BACKEND = "search"
REINDEX_TIMEOUT_SEC = 600  # adjust as needed

# Connect to Gremlin Server
client = Client(
    GREMLIN_SERVER,
    "g",
    message_serializer=serializer.GraphSONSerializersV3d0()
)

# 1️⃣ Create property key and index if missing
groovy_create_index = f'''
mgmt = graph.openManagement()
bioKey = mgmt.getPropertyKey('{PROPERTY_KEY}')
if (bioKey==null) {{
    bioKey = mgmt.makePropertyKey('{PROPERTY_KEY}').dataType(String.class).make()
}}
if (!mgmt.getGraphIndexes(Vertex.class).any{{ it.name().equals('{INDEX_NAME}') }}) {{
    mgmt.buildIndex('{INDEX_NAME}', Vertex.class)
        .addKey(bioKey, org.janusgraph.core.schema.Mapping.TEXT.asParameter())
        .buildMixedIndex('{MIXED_INDEX_BACKEND}')
}}
mgmt.commit()
"Index creation step completed"
'''
print(client.submit(groovy_create_index).all().result()[0])

# 2️⃣ Trigger reindex for existing data
groovy_reindex = f'''
mgmt = graph.openManagement()
mgmt.updateIndex(mgmt.getGraphIndex('{INDEX_NAME}'), SchemaAction.REINDEX).get()
mgmt.commit()
"Reindex triggered"
'''
print(client.submit(groovy_reindex).all().result()[0])

# 3️⃣ Wait until index is ENABLED
groovy_await_enabled = f'''
mgmt = graph.openManagement()
mgmt.awaitGraphIndexStatus(graph, '{INDEX_NAME}').status(SchemaStatus.ENABLED).timeout({REINDEX_TIMEOUT_SEC}).call()
mgmt.commit()
"Index {INDEX_NAME} is now ENABLED"
'''
print(client.submit(groovy_await_enabled).all().result()[0])

# Close client
client.close()

