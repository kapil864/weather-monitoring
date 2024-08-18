from elasticsearch import Elasticsearch
import json


def connect_elasticsearch(hosts: str, username: str, password: str):
    """
    Connects to Elasticsearch cluster.

    Args:
      hosts: A list of Elasticsearch host addresses.

    Returns:
      An Elasticsearch client instance.
    """
    try:
        es = Elasticsearch(hosts=hosts, http_auth=(
            username, password), verify_certs=False)
        if es.ping():
            print("Connected to Elasticsearch")
            return es
        else:
            print("Failed to connect to Elasticsearch")
            return None
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None


def send_document(es: Elasticsearch, index: str, document: dict):
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


def load_aggreagate_query():
    file = open('elastic_queries/aggreate_query.json', 'r')
    query = json.load(file)
    file.close()
    return query


def load_delete_query():
    file = open('elastic_queries/delete_query.json', 'r')
    query = json.load(file)
    file.close()
    return query


def execute_delete_query(es: Elasticsearch, index: str, query: dict):
    return es.delete_by_query(index=index, body=query)


def execute_search_query(es: Elasticsearch, index: str, query: dict):
    return es.search(index=index, body=query)
