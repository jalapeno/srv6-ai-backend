## Base queries

#### Get all collections
curl http://localhost:8000/api/v1/collections

## Graphs
#### Get specific graph data
curl http://localhost:8000/api/v1/collections/lsv4_graph
curl http://localhost:8000/api/v1/collections/lsv6_graph
curl http://localhost:8000/api/v1/collections/ipv4_graph
curl http://localhost:8000/api/v1/collections/ipv6_graph

#### Get graph info
curl http://localhost:8000/api/v1/collections/lsv4_graph/info
curl http://localhost:8000/api/v1/collections/lsv6_graph/info

#### Get just the edge connections for a graph
curl http://localhost:8000/api/v1/collections/ipv6_graph/edges
curl http://localhost:8000/api/v1/collections/ipv4_graph/edges
curl http://localhost:8000/api/v1/collections/lsv6_graph/edges
curl http://localhost:8000/api/v1/collections/lsv4_graph/edges

#### Get just the vertices for a graph
curl http://localhost:8000/api/v1/collections/ipv6_graph/vertices
curl http://localhost:8000/api/v1/collections/ipv4_graph/vertices
curl http://localhost:8000/api/v1/collections/lsv6_graph/vertices
curl http://localhost:8000/api/v1/collections/lsv4_graph/vertices

#### Get vertex keys
curl http://localhost:8000/api/v1/collections/ipv6_graph/vertices/keys
curl http://localhost:8000/api/v1/collections/ipv4_graph/vertices/keys

#### Get vertex ids
curl http://localhost:8000/api/v1/collections/ipv6_graph/vertices/ids
curl http://localhost:8000/api/v1/collections/ipv4_graph/vertices/ids

## Collections

#### Get data from any collection
curl "http://localhost:8000/api/v1/collection/ls_node"
curl "http://localhost:8000/api/v1/collection/ls_link"
curl "http://localhost:8000/api/v1/collection/ls_prefix"
curl "http://localhost:8000/api/v1/collection/ls_srv6_sid"

curl "http://localhost:8000/api/v1/collection/ebgp_peer_v4"
curl "http://localhost:8000/api/v1/collection/ebgp_peer_v6"
curl "http://localhost:8000/api/v1/collection/ebgp_prefix_v4"
curl "http://localhost:8000/api/v1/collection/ebgp_prefix_v6"

#### Get data with limits
curl "http://localhost:8000/api/v1/collection/ebgp_peer_v4?limit=10"
curl "http://localhost:8000/api/v1/collection/ebgp_peer_v6?limit=10"

#### Get data with a specific key
curl "http://localhost:8000/api/v1/collection/ebgp_peer_v4?filter_key=some_key"

#### Get just the keys from a collection
curl "http://localhost:8000/api/v1/collection/peer/keys"


#### Get all nodes with SRv6 SIDs
curl http://localhost:8000/api/v1/collection/ls_node_extended/srv6_nodes

#### Get details for a specific node
curl http://localhost:8000/api/v1/collection/ls_node_extended/node/2_0_0_0000.0001.0001


## Search

#### Search by ASN only
curl "http://localhost:8000/api/v1/collection/ls_node_extended/search?asn=65001"

#### Search by protocol only
curl "http://localhost:8000/api/v1/collection/ls_node_extended/search?protocol=IS-IS%20Level%202"

#### Search with multiple filters
curl "http://localhost:8000/api/v1/collection/ls_node_extended/search?asn=65001&srv6_enabled=true"

## Graphs

#### Find shortest path
curl "http://localhost:8000/api/v1/collections/ipv6_graph/shortest_path?from_node=ls_node_extended/2_0_0_0000.0001.0065&to_node=ls_node_extended/2_0_0_0000.0002.0067"

#### For outbound (default)
curl "http://localhost:8000/api/v1/collections/ipv6_graph/shortest_path?from_node=ls_node_extended/2_0_0_0000.0001.0065&to_node=ls_node_extended/2_0_0_0000.0002.0067"

#### For inbound
curl "http://localhost:8000/api/v1/collections/ipv6_graph/shortest_path?from_node=ls_node_extended/2_0_0_0000.0001.0065&to_node=ls_node_extended/2_0_0_0000.0002.0067&direction=inbound"

#### For any direction
curl "http://localhost:8000/api/v1/collections/ipv6_graph/shortest_path?from_node=ls_node_extended/2_0_0_0000.0001.0065&to_node=ls_node_extended/2_0_0_0000.0002.0067&direction=any"


#### prefix to prefix
curl "http://localhost:8000/api/v1/collections/ipv6_graph/shortest_path?from_node=ls_prefix/2_0_2_0_0_fc00:0:701:1::_64_0000.0001.0065&to_node=ls_prefix/2_0_2_0_0_fc00:0:701:1003::_64_0000.0002.0067&direction=any"



#### Traverse graph
curl "http://localhost:8000/api/v1/collections/ipv6_graph/traverse?start_node=ls_node_extended/2_0_0_0000.0001.0001&max_depth=2"

#### Get neighbors
curl "http://localhost:8000/api/v1/collections/ipv6_graph/neighbors?node=ls_node_extended/2_0_0_0000.0001.0001"