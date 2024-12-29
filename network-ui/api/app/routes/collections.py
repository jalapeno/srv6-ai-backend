from fastapi import APIRouter, HTTPException
from arango import ArangoClient
from ..config.settings import Settings
from typing import Optional, List

router = APIRouter()
settings = Settings()

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

@router.get("/collection/{collection_name}")
async def get_collection_data(
    collection_name: str,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
    filter_key: Optional[str] = None
):
    """
    Query any collection in the database with optional filtering
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        collection = db.collection(collection_name)
        
        # Build AQL query based on parameters
        aql = f"FOR doc IN {collection_name}"
        
        # Add filter if specified
        if filter_key:
            aql += f" FILTER doc._key == @key"
        
        # Add limit and skip
        if skip:
            aql += f" SKIP {skip}"
        if limit:
            aql += f" LIMIT {limit}"
        
        aql += " RETURN doc"
        
        # Execute query
        cursor = db.aql.execute(
            aql,
            bind_vars={'key': filter_key} if filter_key else None
        )
        
        results = [doc for doc in cursor]
        
        return {
            'collection': collection_name,
            'count': len(results),
            'data': results
        }
        
    except Exception as e:
        print(f"Error querying collection: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collection/{collection_name}/keys")
async def get_collection_keys(collection_name: str):
    """
    Get just the _key values from a collection
    """
    try:
        db = get_db()
        if not db.has_collection(collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"Collection {collection_name} not found"
            )
        
        aql = f"""
        FOR doc IN {collection_name}
        RETURN doc._key
        """
        
        cursor = db.aql.execute(aql)
        keys = [key for key in cursor]
        
        return {
            'collection': collection_name,
            'key_count': len(keys),
            'keys': keys
        }
        
    except Exception as e:
        print(f"Error getting collection keys: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collection/ls_node_extended/srv6_nodes")
async def get_srv6_node_data():
    """
    Get SRv6 SID information and node names from ls_node_extended collection
    """
    try:
        db = get_db()
        if not db.has_collection('ls_node_extended'):
            raise HTTPException(
                status_code=404,
                detail="ls_node_extended collection not found"
            )
        
        # AQL query to get node names and SRv6 information
        aql = """
        FOR node IN ls_node_extended
            FILTER node.sids != null
            RETURN {
                key: node._key,
                node_name: node.name,
                router_id: node.router_id,
                asn: node.asn,
                srv6_sids: node.sids
            }
        """
        
        cursor = db.aql.execute(aql)
        results = [doc for doc in cursor]
        
        return {
            'count': len(results),
            'nodes': results
        }
        
    except Exception as e:
        print(f"Error getting SRv6 node data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collection/ls_node_extended/node/{node_name}")
async def get_node_details(node_name: str):
    """
    Get detailed information for a specific node
    """
    try:
        db = get_db()
        if not db.has_collection('ls_node_extended'):
            raise HTTPException(
                status_code=404,
                detail="ls_node_extended collection not found"
            )
        
        # AQL query to get specific node details
        aql = """
        FOR node IN ls_node_extended
            FILTER node._key == @node_name
            RETURN {
                key: node._key,
                node_name: node.name,
                router_id: node.router_id,
                asn: node.asn,
                srv6_sids: node.sids,
                protocol: node.protocol,
                area_id: node.area_id,
                domain_id: node.domain_id,
                protocol_id: node.protocol_id
            }
        """
        
        cursor = db.aql.execute(aql, bind_vars={'node_name': node_name})
        results = [doc for doc in cursor]
        
        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"Node {node_name} not found"
            )
        
        return results[0]
        
    except Exception as e:
        print(f"Error getting node details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/collection/ls_node_extended/search")
async def search_nodes(
    asn: Optional[int] = None,
    protocol: Optional[str] = None,
    srv6_enabled: Optional[bool] = None
):
    """
    Search nodes with various filters
    """
    try:
        db = get_db()
        if not db.has_collection('ls_node_extended'):
            raise HTTPException(
                status_code=404,
                detail="ls_node_extended collection not found"
            )
        
        # Build AQL query based on filters
        aql = "FOR node IN ls_node_extended"
        filters = []
        bind_vars = {}
        
        if asn is not None:
            filters.append("node.asn == @asn")
            bind_vars['asn'] = asn
        if protocol:
            filters.append("node.protocol == @protocol")
            bind_vars['protocol'] = protocol
        if srv6_enabled is not None:
            if srv6_enabled:
                filters.append("node.sids != null")
            else:
                filters.append("node.sids == null")
        
        if filters:
            aql += " FILTER " + " AND ".join(filters)
        
        aql += """ 
        RETURN {
            node_name: node._key,
            router_id: node.router_id,
            asn: node.asn,
            protocol: node.protocol,
            srv6_enabled: node.sids != null
        }
        """
        
        cursor = db.aql.execute(aql, bind_vars=bind_vars)
        results = [doc for doc in cursor]
        
        return {
            'count': len(results),
            'nodes': results
        }
        
    except Exception as e:
        print(f"Error searching nodes: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 