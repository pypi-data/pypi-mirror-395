# Import

# Import Python standard libraries
import json  # Import json module for parsing JSON data
import logging  # Import logging module for event logging
from pathlib import Path  # Import Path class from pathlib module for handling file paths
from typing import Union, List, Optional  # Import type hinting classes rrom typing module
from urllib.parse import urlparse  # Import urlparse function from urllib.parse module for identifying URLs

# Import external packages
import requests  # Import Requests library for downloading from URLs
import networkx as nx  # Import NetworkX package for network creation

# Configure logging

logger = logging.getLogger('affiliation_builder')  # Create named logger
logger.addHandler(logging.NullHandler())  # Attach idle handler - no logging by default

# Define build() function

def build(  
    json_path: Union[str, Path],
    node_set_0_key: Optional[str],
    node_set_1_keys: Union[str, List[str]],
    identifier_key: str,
    node_set_1_identifier_key: Optional[str] = None
) -> nx.Graph:
    """
    Build a bipartite affiliation network from JSON data.
    
    Creates a bipartite NetworkX graph where node set 0 (e.g., events) connects
    to node set 1 (e.g., human and organization participants in event) through
    affiliation relationships.
    All JSON fields are preserved as node attributes.
    
    Parameters
    ----------
    json_path : str or Path
        Path to JSON file or URL (http/https).
    node_set_0_key : str or None
        JSON key containing node-set-0 items (NetworkX bipartite=0). 
        Use None if JSON is a direct array without a wrapping key.
    node_set_1_keys : str or list of str
        JSON key(s) for affiliated entities (NetworkX bipartite=1) in each node-set-0
        item.
    identifier_key : str
        JSON key to use as unique identifier for node-set-0 items.
    node_set_1_identifier_key : str or None, default=None
        JSON key to use as identifier for node set 1 items when they are objects
        (rather than simple values).
        If None, assumes node set 1 items are simple values (strings/numbers).
        If provided, extracts this key from each entity object and preserves
        all other keys as node attributes.
                
    Returns
    -------
    networkx.Graph
        Bipartite graph with two node sets connected by affiliation edges.
        
    Examples
    --------
    Build a network from JSON data with persons as entities:

    >>> URL = 'https://raw.githubusercontent.com/timofruehwirth/affiliation-builder/main/examples/example.json'
    >>> G = build(URL, 'events', 'persons', 'name', 'name')
    >>> G.number_of_nodes()
    14
    >>> G.number_of_edges()
    22

    Access node sets:

    >>> events = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
    >>> persons = {n for n, d in G.nodes(data=True) if d['bipartite'] == 1}
    >>> len(events)
    8
    >>> len(persons)
    6
    >>> 'Alice Smith' in persons
    True

    Node attributes are preserved:

    >>> G.nodes['Alice Smith']['affiliation']
    'University of Vienna'

    Build a network with multiple entity types (persons and organizations):

    >>> G = build(URL, 'events', ['persons', 'organizations'], 'name', 'name')
    >>> G.number_of_nodes()
    20
    >>> G.number_of_edges()
    35
    
    Notes
    -----
    Node set 0 has bipartite=0, node set 1 has bipartite=1. Edges only exist
    between nodes of different sets. Access node sets with:
    
        node_set_0 = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
        node_set_1 = {n for n, d in G.nodes(data=True) if d['bipartite'] == 1}

    When node_set_1_identifier_key is specified, all other attributes from entity 
    objects are preserved as node attributes, enabling rich metadata analysis.

    """

    # Log function call and arguments
    logger.info(f"Affiliation network builder started")
    logger.info(f"JSON source: {json_path}")
    logger.info(f"Node-set-0 key: '{node_set_0_key}'")
    logger.info(f"Node-set-1 keys: {node_set_1_keys}")
    logger.info(f"Identifier key: '{identifier_key}'")
    logger.info(f"Node-set-1 identifier key: '{node_set_1_identifier_key}'")

    # =========================================================================
    # Input validation
    # =========================================================================
    
    # Validate input types
    
    # Validate node_set_1_keys type
    if not isinstance(node_set_1_keys, (str, list)):  # Check data type
        logger.error(
            f"Invalid type for node_set_1_keys detected: {type(node_set_1_keys)}"  # Log type error
        )
        raise TypeError(
            f"node_set_1_keys must be string or list, "
            f"but got {type(node_set_1_keys).__name__}"  # Raise type error
        )
    
    # Validate identifier_key type
    if not isinstance(identifier_key, str):
        logger.error(
            f"Invalid type for identifier_key detected: {type(identifier_key)}"
        )
        raise TypeError(
            f"identifier_key must be string, "
            f"but got {type(identifier_key).__name__}"
        )
    
    # Validate node_set_1_identifier_key type (if provided)
    if node_set_1_identifier_key is not None and not isinstance(node_set_1_identifier_key, str):
        logger.error(
            f"Invalid type for node_set_1_identifier_key detected: {type(node_set_1_identifier_key)}"
        )
        raise TypeError(
            f"node_set_1_identifier_key must be string or None, "
            f"but got {type(node_set_1_identifier_key).__name__}"
        )
    
    # Validate node_set_0_key type
    if node_set_0_key is not None and not isinstance(node_set_0_key, str):
        logger.error(
            f"Invalid type for node_set_0_key detected: {type(node_set_0_key)}"
        )
        raise TypeError(
            f"node_set_0_key must be string or None, "
            f"but got {type(node_set_0_key).__name__}"
        )
    
    logger.debug("Input validation passed")

    # =========================================================================
    # STEP 1: Normalize node_set_1_keys to list
    # =========================================================================
    
    # Convert string to list

    if isinstance(node_set_1_keys, str):  # Check for string type
        node_set_1_keys = [node_set_1_keys]  # Convert to list
        logger.debug(f"Converting node_set_1_keys to list: {node_set_1_keys}")  # Log normalization

    # =========================================================================
    # STEP 2: Load JSON data (local file or URL)
    # =========================================================================
    
    # Determine data source and load data.

    is_url = False  # Set local source as default

    # Check URL source
    if isinstance(json_path, str):  # Check for string type
        parsed = urlparse(json_path)  # Parse URL
        is_url = parsed.scheme in ('http', 'https')  # Check URL scheme
    
    # Load from URL

    if is_url:
        logger.info(f"URL source detected, downloading JSON from: {json_path}")  # Log URL detection

        # Load and parse JSON from URL

        try:
            with requests.get(json_path, timeout=30) as response:  # Send request to server; set timeout to 30 seconds; return Response object
                response.raise_for_status()  # Raise exception for HTTP status code 4xx or 5xx
                data = response.json()  # Decode Response object as UTF-8 text; parse as JSON into Python list or dictionary
                logger.info(f"JSON successfully downloaded")  # Log successful download
                        
        except requests.exceptions.Timeout:  # Catch timeout exception
            logger.error(f"Request timed out")  # Log timeout error
            raise requests.exceptions.Timeout(
                f"Request timed out while accessing {json_path}"  # Re-raise with context
            )
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")  # Log connection error details
            raise requests.exceptions.ConnectionError(
                f"Could not connect to {json_path}"
            )
        
        except requests.exceptions.HTTPError as e:  # Catch HTTP exception raised by response.raise_for_status()
            logger.error(f"HTTP error: {e}")
            raise  # Re-raise without added context (URL already part of original error message)

        except json.JSONDecodeError as e:  # Catch JSON error
            logger.error(f"Downloaded content is not valid JSON")
            raise ValueError(
                f"Downloaded content from {json_path} is not valid JSON: {e.msg}"
            ) from e  # Re-raise as value error with original error message
        
        except requests.exceptions.RequestException as e:  # Catch any other error from Requests library
            logger.error(f"Unexpected error downloading from URL: {e}")
            raise

    # Load locally

    else:
        json_path = Path(json_path)  # Convert string to Path object (if necessary)
        logger.info(f"Local file path detected: {json_path}")  # Log file path detection

        # Check path exists
        if not json_path.exists():
            logger.error(f"File not found: {json_path}")
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        # Check path points to file
        if not json_path.is_file():
            logger.error(f"Not a file: {json_path}")
            raise ValueError(
                f"Path must point to a file, not a directory: {json_path}"
            )
        
        # Load and parse JSON from file path

        try:
            with json_path.open('r', encoding='utf-8') as f:  # Open for reading with UTF-8 encoding
                data = json.load(f)  # Parse JSON from file object; return list or dictionary
            
            logger.info(f"Local JSON file successfully loaded")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in file")
            raise ValueError(
                f"File {json_path} is not valid JSON: {e.msg}"
            ) from e
                
        except UnicodeDecodeError as e:  # Catch encoding error
            logger.error(f"File encoding error: {e}")
            raise ValueError(f"Unable to read file with UTF-8 encoding: {e}")
        
        except Exception as e:  # Catch any other error
            logger.error(f"Unexpected error loading JSON: {e}")
            raise

    # =========================================================================
    # STEP 3: Validate JSON structure and extract items
    # =========================================================================
    
    # Handle both direct arrays and wrapped objects in JSON.
    
    if isinstance(data, list): # Check for direct array format
        items = data  # Use data as-is
        logger.info(f"Direct array format with {len(items)} items detected")  # Log JSON structure
        
    elif isinstance(data, dict):  # Check for wrapped object format
        if node_set_0_key is None:  # Check for node-set-0 key
            logger.error("Wrapped object format detected, but node_set_0_key is None")  # Log missing key error
            raise ValueError(
                f"JSON is a wrapped object. node_set_0_key is required to specify "
                f"key pointing to data. Available keys: {list(data.keys())}"  # Show available keys
            )
        
        if node_set_0_key not in data: # Check node-set-0 key is valid
            logger.error(f"Key '{node_set_0_key}' not found")  # Log invalid key error
            raise ValueError(
                f"The key '{node_set_0_key}' was not found in the JSON data. "
                f"Available keys: {list(data.keys())}" 
            ) # Raise invalid key error

        if not isinstance(data[node_set_0_key], list):  # Check node-set-0 key is list
            logger.error(f"Value for '{node_set_0_key}' is not a list")  # Log invalid value error
            raise ValueError(
                f"The value for '{node_set_0_key}' must be a list, "
                f"but got {type(data[node_set_0_key]).__name__}"
            )  # Raise invalid value error
        
        items = data[node_set_0_key]  # Extract and assign list
        logger.info(f"Wrapped object format with {len(items)} items in '{node_set_0_key}' detected")  # Log successful extraction
                
    else:  # Handle invalid format
        logger.error(f"Unexpected data type: {type(data)}")  # Log invalid data type error
        raise ValueError(
            f"Expected list or dictionary, but got {type(data).__name__}"
        )
        
    if len(items) == 0:  # Check for empty data
        logger.warning(f"No items found in the data")  # Log warning, no error
    
    
    # =========================================================================
    # STEP 4: Create bipartite graph
    # =========================================================================
    
    G = nx.Graph()  # Initialize undirected NetworkX graph
    logger.info("NetworkX graph initialized")  # Log graph initialization
    
    
    # =========================================================================
    # STEP 5: Iterate through items and build network
    # =========================================================================

    for idx, item in enumerate(items):  # Index for logging; loop through index-item pairs

        # Check if item is dictionary
        if not isinstance(item, dict):
            logger.warning(
                f"Item at index {idx} not a dictionary, but {type(item).__name__}, skipping"
            )
            continue  # Continue loop with next item
                
        # Check for node-set-0 key
        if identifier_key not in item:
            logger.warning(
                f"Item at index {idx} missing '{identifier_key}' key, skipping. "
                f"Available keys: {list(item.keys())}"
            )
            continue
        
        node_id = item[identifier_key]  # Get node ID from identifier_key
        
        # Validate node ID
        if node_id is None or node_id == "":
            logger.warning(
                f"Item at index {idx} has empty or None identifier, skipping"
            )
            continue

        # Check if node ID is hashable (for NetworkX node processing)
        try:
            hash(node_id)
        except TypeError:  # Raise TypeError if not hashable
            logger.warning(
                f"Item at index {idx} has unhashable identifier '{node_id}', skipping"
            )
            continue
        
        # Remove entity list keys to avoid redundancy (with edges)
        item_attrs = item.copy()
        for key in node_set_1_keys:
            item_attrs.pop(key, None)
        
        item_attrs.pop(identifier_key, None)  # Remove identifier key to avoid redundancy

        # Add node-set-0 nodes to graph from IDs
        G.add_node(node_id, bipartite=0, **item_attrs)  # Add node with (non-entity-related) attributes
        logger.debug(f"Node-set-0 node '{node_id}' added")
        
        # Process each entity key
        for key in node_set_1_keys:  # Loop through list of keys
            if key not in item:
                logger.debug(f"Key '{key}' not found in item '{node_id}', skipping")
                continue  # Skip key that's missing in dictionary

            entities = item[key]  # Get entity list
            
            # Normalize un-listed entity to list
            if isinstance(entities, dict):
                entities = [entities]
                logger.debug(f"Single entity in '{key}' for item '{node_id}' normalized to list")
            elif not isinstance(entities, list):
                logger.warning(
                    f"Value for '{key}' in item '{node_id}' not a list or dict, "
                    f"but {type(entities).__name__}, skipping"
                )
                continue

            for entity in entities:  # Loop through entity list
                
                # Handle entities that are JSON objects

                if isinstance(entity, dict):  # Check if entity is object
                    
                    # Check for identifier key
                    if node_set_1_identifier_key is None:
                        logger.warning(
                            f"Entity in '{key}' for item '{node_id}' is object, "
                            f"but node_set_1_identifier_key is None. Specify which key "
                            f"to use as identifier, skipping: {entity}"
                        )
                        continue

                    # Check for identifier key in entity
                    if node_set_1_identifier_key not in entity:
                        logger.warning(
                            f"Entity in '{key}' for item '{node_id}' missing "
                            f"'{node_set_1_identifier_key}' key, skipping: {entity}"
                        )
                        continue
                    
                    entity_id = entity[node_set_1_identifier_key]  # Get node ID
                    
                    entity_attrs = entity.copy()  # Copy attributes
                    entity_attrs.pop(node_set_1_identifier_key, None)  # Remove identifier key to avoid redundancy

                else:
                    
                    # Handle entities that are simple JSON values
                    
                    entity_id = entity  # Get node ID
                    
                    entity_attrs = {}  # Create empty dictionary of graph node attributes

                # Validate graph node ID
                if entity_id is None or entity_id == "":
                    logger.warning(
                        f"Entity in '{key}' for item '{node_id}' has empty or None "
                        f"identifier, skipping: {entity}"
                    )
                    continue
                
                try:
                    hash(entity_id)
                except TypeError:
                    logger.warning(
                        f"Entity ID '{entity_id}' in '{key}' for item '{node_id}' "
                        f"is not hashable, skipping"
                    )
                    continue
                
                # Check for duplicate entity and log attribute overwriting
                if entity_id in G:
                    logger.debug(
                        f"Duplicate entity '{entity_id}' found, updating attributes"
                    )

                # Add entity node
                G.add_node(entity_id, bipartite=1, **entity_attrs)
                logger.debug(f"Node-set-1 node '{entity_id}' added")
                
                # Add edge between entity and item
                G.add_edge(node_id, entity_id)
                logger.debug(f"Edge between '{node_id}' and '{entity_id}' added")

    # =========================================================================
    # STEP 6: Log summary and return graph
    # =========================================================================

    # Count nodes in each set
    node_set_0_count = sum(1 for _, d in G.nodes(data=True) if d['bipartite'] == 0)  # Return and unpack (node ID, attributes dictionary) tuples; mark IDs as irrelevant; filter according to node set; count relevant nodes
    node_set_1_count = sum(1 for _, d in G.nodes(data=True) if d['bipartite'] == 1)

    node_set_0_label = f"({node_set_0_key})" if node_set_0_key else "(direct array)"  # Create node-set-0 label

    # Log summary
    logger.info("=" * 60)
    logger.info("Bipartite network construction complete")
    logger.info("=" * 60)
    logger.info(f"Total edges (affiliations): {G.number_of_edges()}")  # Log number of edges
    logger.info(f"Total nodes: {G.number_of_nodes()}")  # Log number of nodes
    logger.info(f"Node set 0 {node_set_0_label}: {node_set_0_count} nodes")  # Log number of node-set-0 nodes
    logger.info(f"Node set 1 ({node_set_1_keys}): {node_set_1_count} nodes")  # Log number of node-set-1 nodes
    logger.info("=" * 60)
    
    # Verify graph is bipartite
    if nx.is_bipartite(G):  # Check for bipartite attributes in nodes; check for edges within same node sets
        logger.info("✓ Graph structure is valid bipartite")
    else:
        logger.warning("⚠ Graph is not bipartite. There may be edges within the same set")
    
    return G  # Return NetworkX Graph object
