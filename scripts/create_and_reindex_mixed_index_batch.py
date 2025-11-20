from gremlin_python.driver.client import Client
from gremlin_python.driver import serializer
import time

GREMLIN_SERVER = "ws://localhost:8182/gremlin"
INDEX_NAME = "byBio"
PROPERTY_KEY = "bio"
MIXED_INDEX_BACKEND = "search"
BATCH_SIZE = 1000  # number of vertices per batch
SLEEP_SEC = 2      # sleep between batches

# Connect to Gremlin Server
client = Client(
    GREMLIN_SERVER,
    "g",
    message_serializer=serializer.GraphSONSerializersV3d0()
)

# 1️⃣ Create property key and mixed index if missing
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

# 2️⃣ Count vertices with 'bio' property
groovy_count = f"g.V().has('{PROPERTY_KEY}').count()"
total_vertices = client.submit(groovy_count).all().result()[0]
print(f"Total vertices with '{PROPERTY_KEY}': {total_vertices}")

# 3️⃣ Reindex in batches (touch each vertex to trigger mixed index)
for start in range(0, total_vertices, BATCH_SIZE):
    end = start + BATCH_SIZE
    groovy_batch = f"""
    g.V().has('{PROPERTY_KEY}').range({start},{end}).forEach{{ v -> 
        v.property('{PROPERTY_KEY}', v.value('{PROPERTY_KEY}')) 
    }}
    "Processed vertices {start} to {end}"
    """
    result = client.submit(groovy_batch).all().result()[0]
    print(result)
    time.sleep(SLEEP_SEC)

# 4️⃣ Optionally: check index status
groovy_status = f"""
mgmt = graph.openManagement()
index = mgmt.getGraphIndex('{INDEX_NAME}')
mgmt.commit()
'{INDEX_NAME} is created and reindexed in batches'
"""
print(client.submit(groovy_status).all().result()[0])

# Close client
client.close()

