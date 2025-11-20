from gremlin_python.driver import client, serializer
import sys

# Gremlin Server connection (adjust host/port if needed)
JANUS_HOST = "localhost"
JANUS_PORT = "8182"

g_client = client.Client(
    f"ws://{JANUS_HOST}:{JANUS_PORT}/gremlin",
    "g",
    message_serializer=serializer.GraphSONSerializersV3d0()
)

def check_index_status(index_name, key_name):
    groovy = f"""
    mgmt = graph.openManagement()
    status = mgmt.getGraphIndex("{index_name}").getIndexStatus(mgmt.getPropertyKey("{key_name}"))
    mgmt.commit()
    status.toString()
    """
    return g_client.submit(groovy).all().result()[0]

def reindex(index_name):
    groovy = f"""
    mgmt = graph.openManagement()
    future = mgmt.updateIndex(mgmt.getGraphIndex("{index_name}"), SchemaAction.REINDEX).get()
    mgmt.commit()
    "Reindex triggered"
    """
    return g_client.submit(groovy).all().result()[0]

def await_enabled(index_name, timeout_sec=600):
    groovy = f"""
    mgmt = graph.openManagement()
    mgmt.awaitGraphIndexStatus(graph, "{index_name}").status(SchemaStatus.ENABLED).timeout({timeout_sec}).call()
    mgmt.commit()
    "Index {index_name} ENABLED"
    """
    return g_client.submit(groovy).all().result()[0]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 index_manager.py <action> <index_name> [property_key]")
        print("Actions: check, reindex, await")
        sys.exit(1)

    action = sys.argv[1]
    index_name = sys.argv[2]

    if action == "check":
        if len(sys.argv) < 4:
            print("Need property key for check")
            sys.exit(1)
        key_name = sys.argv[3]
        print("Index Status:", check_index_status(index_name, key_name))

    elif action == "reindex":
        print(reindex(index_name))

    elif action == "await":
        print(await_enabled(index_name))

    else:
        print("Invalid action. Use: check, reindex, await")

