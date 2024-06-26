from typing import Any, Dict, List
from elasticsearch import Elasticsearch

class ElasticsearchIO:
    """
    A class for interacting with Elasticsearch.

    Args:
        host (str): The hostname or IP address of the Elasticsearch server.
        port (int): The port number of the Elasticsearch server.
        index (str): The name of the Elasticsearch index to work with.

    Attributes:
        host (str): The hostname or IP address of the Elasticsearch server.
        port (int): The port number of the Elasticsearch server.
        index (str): The name of the Elasticsearch index to work with.
        es (Elasticsearch): The Elasticsearch client instance.

    """

    def __init__(self, host: str, port: int, index: str):
        self.host = host
        self.port = port
        self.index = index
        self.es = Elasticsearch([{"host": host, "port": port}])

    def write(self, data: Dict[str, Any]):
        """
        Writes data to the Elasticsearch index.

        Args:
            data (Dict[str, Any]): The data to be written to the index.

        """
        self.es.index(index=self.index, body=data)

    def read(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reads data from the Elasticsearch index based on the given query.

        Args:
            query (Dict[str, Any]): The query to filter the data.

        Returns:
            List[Dict[str, Any]]: The list of documents matching the query.

        """
        return self.es.search(index=self.index, body=query)["hits"]["hits"]

    def delete(self, query: Dict[str, Any]):
        """
        Deletes data from the Elasticsearch index based on the given query.

        Args:
            query (Dict[str, Any]): The query to filter the data to be deleted.

        """
        self.es.delete_by_query(index=self.index, body=query)