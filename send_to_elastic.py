from elasticsearch import Elasticsearch


def connect_elasticsearch(hosts, username, password):
    """
    Connects to Elasticsearch cluster.

    Args:
      hosts: A list of Elasticsearch host addresses.

    Returns:
      An Elasticsearch client instance.
    """
    try:
        es = Elasticsearch(hosts=hosts, http_auth=(username, password), verify_certs=False)
        if es.ping():
            print("Connected to Elasticsearch")
            return es
        else:
            print("Failed to connect to Elasticsearch")
            return None
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None


def send_document(es, index, document):
    """
    Sends a document to a specified Elasticsearch index.

    Args:
      es: An Elasticsearch client instance.
      index: The name of the index to send the document to.
      document: The document to be sent.
    """
    try:
        response = es.index(index=index, document=document)
        print(f"Document sent to index {index} with ID {response['_id']}")
    except Exception as e:
        print(f"Error sending document to Elasticsearch: {e}")
