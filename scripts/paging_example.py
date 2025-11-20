# paging_example.py
# Demonstrates pagination using range or limit/skip.
from gremlin_python.driver.client import Client

client = Client('ws://localhost:8182/gremlin', 'g')

def paginate_vertices(limit=10, offset=0):
    script = f"g.V().hasLabel('person').order().by('name').range({offset},{offset+limit}).valueMap(true)"
    return client.submit(script).all().result()

if __name__ == '__main__':
    print(paginate_vertices(5,0))
    client.close()
