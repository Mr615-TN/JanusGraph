# bulk_loader_simple.py
# Simple parallel bulk loader: creates many vertices in batches via gremlinpython.
from gremlin_python.driver.client import Client
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

client = Client('ws://localhost:8182/gremlin', 'g')

def add_person_batch(batch):
    scripts = []
    for name,bio in batch:
        uid = str(uuid4())
        scripts.append(f"g.addV('person').property('uuid','{uid}').property('name','{name}').property('bio','{bio}')")
    # submit as multiple requests or one big script joined by newlines
    joined = "\n".join(scripts)
    return client.submit(joined).all().result()

def bulk_load(items, batch_size=100, workers=4):
    batches = [items[i:i+batch_size] for i in range(0,len(items),batch_size)]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for res in ex.map(add_person_batch, batches):
            pass
    return True

if __name__ == '__main__':
    items = [(f'Person{i}', f'Bio for person {i}') for i in range(500)]
    bulk_load(items, batch_size=50, workers=8)
    client.close()
