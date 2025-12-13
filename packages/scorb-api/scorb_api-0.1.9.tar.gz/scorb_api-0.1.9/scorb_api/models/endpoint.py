"""Module to represent the endpoints of Scorb API."""
from abc import abstractmethod

from scorb_api.helpers.http import HTTPRequest


class Endpoint():
    """
        Scorb API endpoint class\n 
        This abstract class represent an endpoint.\n
        That has some urls to diferent http methods, a body data that will send through the http request and a expected response
    """
    def __init__(self, header_auth) -> None:
        self.base_url = ""
        self.header_auth = header_auth
        self.http_request = HTTPRequest() 

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def create(self, body):
        pass

    @abstractmethod
    def update(self, body):
        pass

    @abstractmethod
    def upsert(self, body):
        pass

    @abstractmethod
    def delete(self, id):
        pass
