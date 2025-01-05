# Script writes site and link meta data into the Arango graphDB
# requires https://pypi.org/project/python-arango/
# python3 add_meta_data.py

from arango import ArangoClient
import json
import argparse

user = "root"
pw = "jalapeno"
dbname = "jalapeno"

client = ArangoClient(hosts='http://198.18.133.111:30852')
db = client.db(dbname, username=user, password=pw)

if db.has_collection('igp_node'):
    igp = db.collection('igp_node')

if db.has_collection('bgp_node'):
    bgp = db.collection('bgp_node')

if db.has_collection('peer'):
    peer = db.collection('peer')

if db.has_collection('ipv4_graph'):
    ipv4graph = db.collection('ipv4_graph')

if db.has_collection('ipv6_graph'):
    ipv6graph = db.collection('ipv6_graph')

igp.properties()
bgp.properties()
peer.properties()
ipv4graph.properties()
ipv6graph.properties()

def parse_args():
    """
    Parse command line arguments
    Returns:
        args: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Insert/Update data in ArangoDB')
    parser.add_argument('-d', '--data', nargs='+', 
                       choices=['peer', 'bgp', 'prefix', 'gpu', 'gpu-edges', 'metrics', 'all'],
                       help='Specify which data to insert/update: peer, bgp, prefix, gpu, gpu-edges, metrics, or all')
    return parser.parse_args()

def insert_peer_data(db, peer_file_path):
    """
    Insert peer data from sonic-peer.json into the jalapeno database
    Args:
        db: ArangoDB database connection
        peer_file_path: Path to the sonic-peer.json file
    """
    try:
        # Read the peer data from JSON file
        with open(peer_file_path, 'r') as f:
            peer_data = json.load(f)
        
        # Create peer collection if it doesn't exist
        if not db.has_collection('peer'):
            db.create_collection('peer')
        
        peer_collection = db.collection('peer')
        
        # AQL query to insert/update peer data
        aql = """
        FOR peer in @peers
            UPSERT { _key: peer._key }
            INSERT peer
            REPLACE peer
            IN peer
            RETURN NEW
        """
        
        # Execute AQL query
        db.aql.execute(aql, bind_vars={'peers': peer_data})
        print(f"Successfully inserted/updated {len(peer_data)} peer records")
        
    except Exception as e:
        print(f"Error inserting peer data: {str(e)}")

def insert_bgp_data(db, bgp_file_path):
    """
    Insert/Update BGP node data with SRv6 SIDs and CLOS tier data from bgp-node.json into the jalapeno database
    Args:
        db: ArangoDB database connection
        bgp_file_path: Path to the bgp-node.json file
    """
    try:
        # Read the BGP data from JSON file
        with open(bgp_file_path, 'r') as f:
            bgp_data = json.load(f)
        
        # Ensure bgp_node collection exists
        if not db.has_collection('bgp_node'):
            db.create_collection('bgp_node')
        
        bgp_collection = db.collection('bgp_node')
        
        # AQL query to insert/update BGP data
        aql = """
        FOR node in @bgp_nodes
            UPSERT { _key: node._key }
            INSERT node
            UPDATE node
            IN bgp_node
            RETURN NEW
        """
        
        # Execute AQL query
        db.aql.execute(aql, bind_vars={'bgp_nodes': bgp_data})
        print(f"Successfully inserted/updated {len(bgp_data)} BGP node records")
        
    except Exception as e:
        print(f"Error inserting BGP data: {str(e)}")

def update_prefix_tiers(db):
    """
    Update documents in ebgp_prefix_v4 (prefix_len=24) and ebgp_prefix_v6 (prefix_len=64)
    collections to add the tier: 'dc-prefix' field
    Args:
        db: ArangoDB database connection
    """
    try:
        # Define collections and their prefix length requirements
        collection_filters = {
            'ebgp_prefix_v4': 24,
            'ebgp_prefix_v6': 64
        }
        
        for collection_name, prefix_len in collection_filters.items():
            if not db.has_collection(collection_name):
                print(f"Collection {collection_name} does not exist, skipping...")
                continue
            
            # AQL query to update only documents with specific prefix length
            aql = f"""
            FOR doc IN {collection_name}
                FILTER doc.prefix_len == {prefix_len}
                UPDATE doc WITH {{ tier: 'dc-prefix' }} IN {collection_name}
                RETURN NEW
            """
            
            result = db.aql.execute(aql)
            count = len(list(result))
            print(f"Successfully updated {count} documents with prefix_len={prefix_len} in {collection_name}")
            
    except Exception as e:
        print(f"Error updating prefix tiers: {str(e)}")

def insert_gpu_data(db, gpu_file_path):
    """
    Insert GPU data from gpus.json into the jalapeno database
    Args:
        db: ArangoDB database connection
        gpu_file_path: Path to the gpus.json file
    """
    try:
        # Read the GPU data from JSON file
        with open(gpu_file_path, 'r') as f:
            gpu_data = json.load(f)
        
        # Create gpus collection if it doesn't exist
        if not db.has_collection('gpus'):
            db.create_collection('gpus')
        
        gpu_collection = db.collection('gpus')
        
        # AQL query to insert/update GPU data
        aql = """
        FOR gpu in @gpus
            UPSERT { _key: gpu._key }
            INSERT gpu
            REPLACE gpu
            IN gpus
            RETURN NEW
        """
        
        # Execute AQL query
        db.aql.execute(aql, bind_vars={'gpus': gpu_data})
        print(f"Successfully inserted/updated {len(gpu_data)} GPU records")
        
    except Exception as e:
        print(f"Error inserting GPU data: {str(e)}")

def insert_gpu_edges_v6(db, edge_file_path):
    """
    Insert GPU IPv6 edge data from gpu-edge-v6.json into the ipv6_graph collection
    Args:
        db: ArangoDB database connection
        edge_file_path: Path to the gpu-edge-v6.json file
    """
    try:
        # Read the edge data from JSON file
        with open(edge_file_path, 'r') as f:
            edge_data = json.load(f)
        
        # Ensure ipv6_graph collection exists
        if not db.has_collection('ipv6_graph'):
            db.create_collection('ipv6_graph', edge=True)  # Note: edge=True for edge collection
        
        edge_collection = db.collection('ipv6_graph')
        
        # AQL query to insert/update edge data
        aql = """
        FOR edge in @edges
            UPSERT { _key: edge._key }
            INSERT edge
            REPLACE edge
            IN ipv6_graph
            RETURN NEW
        """
        
        # Execute AQL query
        db.aql.execute(aql, bind_vars={'edges': edge_data})
        print(f"Successfully inserted/updated {len(edge_data)} GPU IPv6 edge records")
        
    except Exception as e:
        print(f"Error inserting GPU IPv6 edge data: {str(e)}")

def update_ipv6_metrics(db, metrics_file_path):
    """
    Insert telemetry data from latency-util.json into the jalapeno database
    Args:
        db: ArangoDB database connection
        metrics_file_path: Path to the latency-util.json file
    """
    try:
        # Read the BGP data from JSON file
        with open(metrics_file_path, 'r') as f:
            metrics_data = json.load(f)
        
        # Ensure ipv6_graph collection exists
        if not db.has_collection('ipv6_graph'):
            db.create_collection('ipv6_graph')
        
        ipv6_collection = db.collection('ipv6_graph')
        
        # AQL query to insert/update BGP data
        aql = """
        FOR edge in @edges
            UPSERT { _key: edge._key }
            INSERT edge
            UPDATE edge
            IN ipv6_graph
            RETURN NEW
        """
        
        # Execute AQL query
        db.aql.execute(aql, bind_vars={'edges': metrics_data})
        print(f"Successfully inserted/updated {len(metrics_data)} edge records")

    except Exception as e:
        print(f"Error inserting telemetry data: {str(e)}")

# Add this at the end of your file to test the function
if __name__ == "__main__":
    args = parse_args()
    
    # If no arguments provided or 'all' specified, run everything
    if not args.data or 'all' in args.data:
        print("\nInserting peer data...")
        insert_peer_data(db, "sonic-peer.json")
        print("\nInserting BGP data...")
        insert_bgp_data(db, "bgp-node.json")
        print("\nUpdating prefix tiers...")
        update_prefix_tiers(db)
        print("\nInserting GPU data...")
        insert_gpu_data(db, "gpus.json")
        print("\nInserting GPU IPv6 edge data...")
        insert_gpu_edges_v6(db, "gpu-edge-v6.json")
        print("\nUpdating IPv6 edge metrics...")
        update_ipv6_metrics(db, "latency-util.json")
    else:
        # Run only specified functions
        if 'peer' in args.data:
            print("\nInserting peer data...")
            insert_peer_data(db, "sonic-peer.json")
        if 'bgp' in args.data:
            print("\nInserting BGP data...")
            insert_bgp_data(db, "bgp-node.json")
        if 'prefix' in args.data:
            print("\nUpdating prefix tiers...")
            update_prefix_tiers(db)
        if 'gpu' in args.data:
            print("\nInserting GPU data...")
            insert_gpu_data(db, "gpus.json")
        if 'gpu-edges' in args.data:
            print("\nInserting GPU IPv6 edge data...")
            insert_gpu_edges_v6(db, "gpu-edge-v6.json")
        if 'metrics' in args.data:
            print("\nUpdating IPv6 edge metrics...")
            update_ipv6_metrics(db, "latency-util.json")