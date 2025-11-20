# fulltext_search.py
# Demonstrates indexing a vertex with 'bio' text and performing a full-text search via mixed index
from gremlin_python.driver.client import Client
from uuid import uuid4
import time

GREMLIN_SERVER = "ws://localhost:8182/gremlin"
client = Client(GREMLIN_SERVER, 'g')

def add_person_with_bio(name, bio):
    uid = str(uuid4())
    script = f"""g.addV('person').property('uuid','{uid}').property('name','{name}').property('bio',""" + '"' + f"{bio}" + '"' + ")"""
    client.submit(script).all().result()
    return uid

if __name__ == '__main__':
    # add some vertices
    add_person_with_bio('Alice','Alice is a software engineer who loves graph databases and search.')
    add_person_with_bio('Bob','Bob is a data scientist working with text and NLP.')
    # small sleep to allow index to refresh in dev single-node elasticsearch
    time.sleep(2)
    # Execute full-text search using the mixed index (search is the index name configured)
    # Use a text predicate 'textContains' equivalent via JanusGraph textContains predicate in groovy
    res = client.submit("g.V().has('bio',org.janusgraph.core.attribute.Text.textContains('graph databases')).valueMap(true)").all().result()
    print('Search results:', res)
    client.close()
