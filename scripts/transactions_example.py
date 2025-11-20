# transactions_example.py
# Demonstrates transaction-like behavior using sessioned transactions in Gremlin Server via 'session' bindings.
from gremlin_python.driver.client import Client
from gremlin_python.driver import serializer

# Create a sessioned client to keep transaction open across multiple requests
client = Client("ws://localhost:8182/gremlin", 'g', username=None, password=None, message_serializer=serializer.GraphSONSerializersV2d0())

# Gremlin Server must be configured to allow session-based transactions (sessionManager)
session_id = 'tx-session-1'

def add_then_commit(name):
    # Open session with bindings
    with client.session(session_id) as session_client:
        session_client.submit("g.addV('person').property('name', 'TempPerson')").all().result()
        # commit by closing the session, or explicitly call graph.tx().commit() if Gremlin Server allows
        session_client.submit('graph.tx().commit()').all().result()
    return True

if __name__ == '__main__':
    print(add_then_commit('TempPerson'))
    client.close()
