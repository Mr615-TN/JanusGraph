#!/usr/bin/env python3
"""
reset_on_usb.py  –  wipe the graph while JanusGraph stays up
"""
from gremlin_python.driver.client import Client

def wipe():
    client = Client('ws://localhost:8182/gremlin', 'g')
    # drop every vertex (edges go automatically)
    client.submit("g.V().drop()").all().result()
    print("✅  Graph is now empty – USB data cleared in-place.")

if __name__ == '__main__':
    wipe()
