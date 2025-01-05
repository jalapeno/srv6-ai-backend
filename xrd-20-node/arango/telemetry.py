# Script writes site and link meta data into the Arango graphDB
# requires https://pypi.org/project/python-arango/
# python3 add_meta_data.py

import json
from arango import ArangoClient

user = "root"
pw = "jalapeno"
dbname = "jalapeno"

client = ArangoClient(hosts='http://198.18.133.111:30852')
db = client.db(dbname, username=user, password=pw)
gpus = db.collection('gpus')

if db.has_collection('ipv6_graph'):
    ipv6graph = db.collection('ipv6_graph')

if not db.has_collection('gpus'):
    gpus = db.create_collection('gpus')
else:
    gpus = db.collection('gpus')

ipv6graph.properties()
gpus.properties()

# Read and load the JSON file
with open('latency-util.json', 'r') as f:
    metrics_data = json.load(f)

# Insert each GPU document
for metric in metrics_data:
    try:
        ipv6graph.update(metric)
    except Exception as e:
        print(f"Error updating {metric['_key']}: {e}")

# example aql query
# update     {
#         "_key": "10.0.0.82_2001:db8:1:1::115",
#         "latency": 2,
#         "percent_util_out": 0.4,
#         "percent_util_in": 0.4,
#         "load": 0
#     } in ipv6_graph

# print("GPU documents added")

# with open('gpu-edge.json', 'r') as f:
#     gpu_edge_data = json.load(f)

# for edge in gpu_edge_data:
#     try:
#         ipv6graph.insert(edge)
#     except Exception as e:
#         print(f"Error inserting {edge['_key']}: {e}")

# print("GPU edges added to ipv6_graph")