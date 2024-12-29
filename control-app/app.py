from flask import Flask, render_template, jsonify
from arango import ArangoClient

app = Flask(__name__)

# Initialize ArangoDB connection
client = ArangoClient(hosts='http://198.18.133.104:30852')
db = client.db('jalapeno', username='root', password='jalapeno')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/graph')
def graph():
    return render_template('index.html')

@app.route('/api/graph')
def get_graph_data():
    # Example query - adjust according to your graph structure
    query = """
    FOR v IN vertices
        LET edges = (
            FOR e IN edges
            FILTER e._from == v._id OR e._to == v._id
            RETURN e
        )
        RETURN {
            nodes: v,
            edges: edges
        }
    """
    cursor = db.aql.execute(query)
    result = list(cursor)
    return jsonify(result)

@app.route('/api/instances')
def get_instances():
    try:
        print("Getting instances...")
        databases = [db for db in client.databases() if not db.startswith('_')]
        print(f"Found databases: {databases}")
        return jsonify(databases)
    except Exception as e:
        print(f"Error getting instances: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/graphs/<instance>')
def get_graphs(instance):
    try:
        print(f"Getting graphs for instance: {instance}")
        db = client.db(instance)
        collections = [c['name'] for c in db.collections() 
                      if not c['name'].startswith('_') and c['type'] == 'edge']
        print(f"Found collections: {collections}")
        return jsonify(collections)
    except Exception as e:
        print(f"Error getting graphs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/graph/<instance>/<graph>')
def get_graph(instance, graph):
    try:
        db = client.db(instance)
        
        # Get the edge collection first
        edge_collection = db.collection(graph)
        edges = [edge for edge in edge_collection.all()]
        
        # Get all vertices that are referenced in edges
        vertex_ids = set()
        for edge in edges:
            vertex_ids.add(edge['_from'].split('/')[0])  # Get collection name
            vertex_ids.add(edge['_to'].split('/')[0])    # Get collection name
            
        # Fetch vertices from each referenced collection
        all_vertices = []
        for collection_name in vertex_ids:
            try:
                collection = db.collection(collection_name)
                vertices = [vertex for vertex in collection.all()]
                all_vertices.extend(vertices)
            except Exception as e:
                print(f"Warning: Could not access collection {collection_name}: {str(e)}")
                continue
        
        print(f"Found {len(all_vertices)} vertices and {len(edges)} edges")
        
        return jsonify({
            'nodes': all_vertices,
            'edges': edges
        })
        
    except Exception as e:
        print(f"Error accessing graph: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 