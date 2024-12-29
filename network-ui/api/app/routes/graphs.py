from fastapi import APIRouter, HTTPException
from typing import List
from arango import ArangoClient
from ..config.settings import Settings

router = APIRouter()
settings = Settings()

KNOWN_COLLECTIONS = {
    'graphs': [
        'ipv4_graph',
        'ipv6_graph',
        'lsv4_graph',
        'lsv6_graph'
    ],
    'prefixes': [
        'ebgp_prefix_v4',
        'ebgp_prefix_v6'
    ],
    'peers': [
        'ebgp_peer_v4',
        'ebgp_peer_v6'
    ]
}

def get_db():
    client = ArangoClient(hosts=settings.database_server)
    try:
        db = client.db(
            settings.database_name,
            username=settings.username,
            password=settings.password
        )
        return db
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to database: {str(e)}"
        )

@router.get("/collections")
async def get_all_collections():
    """
    Get a list of all collections in the database
    """
    try:
        db = get_db()
        # Get all collections
        collections = db.collections()
        
        # Filter out system collections (those starting with '_')
        user_collections = [
            {
                'name': c['name'],
                'type': c['type'],
                'status': c['status'],
                'count': db.collection(c['name']).count()
            }
            for c in collections
            if not c['name'].startswith('_')
        ]
        
        return {
            'collections': user_collections,
            'total_count': len(user_collections)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collections/{collection_name}")
async def get_collection_data(collection_name: str):
    """
    Get data from any collection (graph, prefix, or peer)
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        collection = db.collection(collection_name)
        data = [doc for doc in collection.all()]
        
        # If it's a graph collection, also get vertices
        if collection_name in KNOWN_COLLECTIONS['graphs']:
            vertex_collections = set()
            for edge in data:
                vertex_collections.add(edge['_from'].split('/')[0])
                vertex_collections.add(edge['_to'].split('/')[0])
            
            vertices = []
            for vertex_col in vertex_collections:
                try:
                    if db.has_collection(vertex_col):
                        vertices.extend([v for v in db.collection(vertex_col).all()])
                except Exception as e:
                    print(f"Warning: Could not fetch vertices from {vertex_col}: {e}")
            
            return {
                "type": "graph",
                "edges": data,
                "vertices": vertices
            }
        else:
            return {
                "type": "collection",
                "data": data
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collections/{collection_name}/info")
async def get_collection_info(collection_name: str):
    """
    Get metadata about any collection
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        collection = db.collection(collection_name)
        collection_type = "unknown"
        for category, collections in KNOWN_COLLECTIONS.items():
            if collection_name in collections:
                collection_type = category
                break
        
        return {
            "name": collection_name,
            "type": collection_type,
            "count": collection.count(),
            "properties": collection.properties()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collections/{collection_name}/edges")
async def get_edge_connections(collection_name: str):
    """
    Get only the _from and _to fields from a graph collection
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        collection = db.collection(collection_name)
        
        # Debug print
        print(f"Collection properties: {collection.properties()}")
        
        # Get all edges with error handling
        try:
            edges = []
            cursor = collection.all()
            for edge in cursor:
                if '_from' in edge and '_to' in edge:
                    edges.append({
                        '_from': edge['_from'],
                        '_to': edge['_to']
                    })
                else:
                    print(f"Warning: Edge missing _from or _to: {edge}")
            
            print(f"Found {len(edges)} edges")
            
            return {
                'collection': collection_name,
                'edge_count': len(edges),
                'edges': edges
            }
            
        except Exception as e:
            print(f"Error processing edges: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing edges: {str(e)}"
            )
            
    except Exception as e:
        print(f"Error in get_edge_connections: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 

@router.get("/collections/{collection_name}/vertices")
async def get_vertex_info(collection_name: str):
    """
    Get vertex information from a graph collection's edges
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        collection = db.collection(collection_name)
        
        # Debug print
        print(f"Processing vertices for collection: {collection_name}")
        
        try:
            # Get all edges to find vertex collections
            vertex_collections = set()
            vertex_info = {}
            
            # First pass: collect all vertex collections
            for edge in collection.all():
                if '_from' in edge and '_to' in edge:
                    from_collection = edge['_from'].split('/')[0]
                    to_collection = edge['_to'].split('/')[0]
                    vertex_collections.add(from_collection)
                    vertex_collections.add(to_collection)
            
            print(f"Found vertex collections: {vertex_collections}")
            
            # Second pass: get vertices from each collection
            for vertex_col in vertex_collections:
                try:
                    if db.has_collection(vertex_col):
                        vertices = []
                        for vertex in db.collection(vertex_col).all():
                            vertices.append({
                                '_id': vertex['_id'],
                                '_key': vertex['_key'],
                                'collection': vertex_col
                            })
                        vertex_info[vertex_col] = vertices
                        print(f"Processed {len(vertices)} vertices from {vertex_col}")
                except Exception as e:
                    print(f"Error processing collection {vertex_col}: {str(e)}")
                    vertex_info[vertex_col] = {"error": str(e)}
            
            return {
                'collection': collection_name,
                'vertex_collections': list(vertex_collections),
                'total_vertices': sum(len(vertices) for vertices in vertex_info.values() 
                                   if isinstance(vertices, list)),
                'vertices_by_collection': vertex_info
            }
            
        except Exception as e:
            print(f"Error processing vertices: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing vertices: {str(e)}"
            )
            
    except Exception as e:
        print(f"Error in get_vertex_info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 

@router.get("/collections/{collection_name}/shortest_path")
async def get_shortest_path(
    collection_name: str,
    from_node: str,
    to_node: str,
    direction: str = "outbound"  # or "inbound", "any"
):
    """
    Find shortest path between two nodes in a graph
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        # Validate direction parameter
        if direction.lower() not in ["outbound", "inbound", "any"]:
            raise HTTPException(
                status_code=400,
                detail="Direction must be 'outbound', 'inbound', or 'any'"
            )
        
        # AQL query for shortest path
        aql = f"""
        WITH ls_node_extended
        FOR v, e IN {direction.upper()}
            SHORTEST_PATH @from_v TO @to_v
            @graph_name
            RETURN {{
                vertices: v._key,
                sids: v.sids,
                edges: e ? e._key : null,
                latency: e.latency,
                percent_util: e.percent_util,
                hopcount: LENGTH(v)
            }}
        """
        
        cursor = db.aql.execute(
            aql,
            bind_vars={
                'from_v': from_node,
                'to_v': to_node,
                'graph_name': collection_name
            }
        )
        
        results = [doc for doc in cursor]
        
        if not results:
            return {
                "found": False,
                "message": "No path found between specified nodes"
            }
        
        return {
            "found": True,
            "path": results,
            "direction": direction
        }
        
    except Exception as e:
        print(f"Error finding shortest path: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collections/{collection_name}/traverse")
async def traverse_graph(
    collection_name: str,
    start_node: str,
    min_depth: int = 1,
    max_depth: int = 3,
    direction: str = "outbound"  # or "inbound", "any"
):
    """
    Traverse graph from a starting node
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        # AQL query for traversal
        aql = """
        FOR v, e, p IN @min_depth..@max_depth @direction @graph_name
            START @start_vertex
            RETURN {
                vertex: v._key,
                edge: e ? e._key : null,
                path: p.vertices[*]._key,
                depth: LENGTH(p.vertices) - 1
            }
        """
        
        cursor = db.aql.execute(
            aql,
            bind_vars={
                'start_vertex': start_node,
                'min_depth': min_depth,
                'max_depth': max_depth,
                'direction': direction,
                'graph_name': collection_name
            }
        )
        
        results = [doc for doc in cursor]
        
        return {
            "start_node": start_node,
            "paths_found": len(results),
            "traversal_results": results
        }
        
    except Exception as e:
        print(f"Error traversing graph: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collections/{collection_name}/neighbors")
async def get_neighbors(
    collection_name: str,
    node: str,
    direction: str = "outbound",  # or "inbound", "any"
    depth: int = 1
):
    """
    Get immediate neighbors of a node
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        # AQL query for neighbors
        aql = """
        FOR v, e IN 1..@depth @direction @graph_name
            START @start_vertex
            RETURN {
                neighbor: v._key,
                edge: e._key,
                direction: @direction
            }
        """
        
        cursor = db.aql.execute(
            aql,
            bind_vars={
                'start_vertex': node,
                'depth': depth,
                'direction': direction,
                'graph_name': collection_name
            }
        )
        
        results = [doc for doc in cursor]
        
        return {
            "node": node,
            "neighbor_count": len(results),
            "neighbors": results
        }
        
    except Exception as e:
        print(f"Error getting neighbors: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 

@router.get("/collections/{collection_name}/vertices/keys")
async def get_vertex_keys(collection_name: str):
    """
    Get just the keys of vertices referenced in a graph collection
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        collection = db.collection(collection_name)
        
        # Debug print
        print(f"Getting vertex keys for collection: {collection_name}")
        
        try:
            # Get all edges to find vertex collections
            vertex_keys = set()
            
            # First pass: collect all unique vertex keys from edges
            aql = f"""
            FOR edge IN {collection_name}
                COLLECT AGGREGATE 
                    from_keys = UNIQUE(PARSE_IDENTIFIER(edge._from).key),
                    to_keys = UNIQUE(PARSE_IDENTIFIER(edge._to).key)
                RETURN {{
                    keys: UNION_DISTINCT(from_keys, to_keys)
                }}
            """
            
            cursor = db.aql.execute(aql)
            results = [doc for doc in cursor]
            
            if results and results[0]['keys']:
                return {
                    'collection': collection_name,
                    'vertex_count': len(results[0]['keys']),
                    'vertex_keys': sorted(results[0]['keys'])
                }
            else:
                return {
                    'collection': collection_name,
                    'vertex_count': 0,
                    'vertex_keys': []
                }
            
        except Exception as e:
            print(f"Error processing vertex keys: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing vertex keys: {str(e)}"
            )
            
    except Exception as e:
        print(f"Error in get_vertex_keys: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 

@router.get("/collections/{collection_name}/vertices/ids")
async def get_vertex_ids(collection_name: str):
    """
    Get both _key and _id for vertices referenced in a graph collection
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        # Debug print
        print(f"Getting vertex IDs for collection: {collection_name}")
        
        try:
            aql = f"""
            FOR edge IN {collection_name}
                COLLECT AGGREGATE 
                    from_vertices = UNIQUE({{_id: edge._from, _key: PARSE_IDENTIFIER(edge._from).key}}),
                    to_vertices = UNIQUE({{_id: edge._to, _key: PARSE_IDENTIFIER(edge._to).key}})
                RETURN {{
                    vertices: UNION_DISTINCT(from_vertices, to_vertices)
                }}
            """
            
            cursor = db.aql.execute(aql)
            results = [doc for doc in cursor]
            
            if results and results[0]['vertices']:
                # Sort by _key for consistency
                sorted_vertices = sorted(results[0]['vertices'], key=lambda x: x['_key'])
                return {
                    'collection': collection_name,
                    'vertex_count': len(sorted_vertices),
                    'vertices': sorted_vertices
                }
            else:
                return {
                    'collection': collection_name,
                    'vertex_count': 0,
                    'vertices': []
                }
            
        except Exception as e:
            print(f"Error processing vertex IDs: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing vertex IDs: {str(e)}"
            )
            
    except Exception as e:
        print(f"Error in get_vertex_ids: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 