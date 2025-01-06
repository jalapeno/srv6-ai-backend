from arango import ArangoClient
import json
import argparse

user = "root"
pw = "jalapeno"
dbname = "jalapeno"

client = ArangoClient(hosts='http://198.18.133.111:30852')
db = client.db(dbname, username=user, password=pw)

if db.has_collection('bgp_node'):
    bgp_node = db.collection('bgp_node')
    bgp_node.truncate()

if db.has_collection('ebgp_prefix_v4'):
    ebgp_prefix_v4 = db.collection('ebgp_prefix_v4')
    ebgp_prefix_v4.truncate()

if db.has_collection('ebgp_prefix_v6'):
    ebgp_prefix_v6 = db.collection('ebgp_prefix_v6')
    ebgp_prefix_v6.truncate()

if db.has_collection('inet_prefix_v4'):
    inet_prefix_v4 = db.collection('inet_prefix_v4')
    inet_prefix_v4.truncate()

if db.has_collection('inet_prefix_v6'):
    inet_prefix_v6 = db.collection('inet_prefix_v6')
    inet_prefix_v6.truncate()

if db.has_collection('ipv4_graph'):
    ipv4_graph = db.collection('ipv4_graph')
    ipv4_graph.truncate()

if db.has_collection('ipv6_graph'):
    ipv6_graph = db.collection('ipv6_graph')
    ipv6_graph.truncate()
