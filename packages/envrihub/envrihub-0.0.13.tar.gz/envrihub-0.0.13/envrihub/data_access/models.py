from abc import ABC, abstractmethod
import logging
import os
import requests
from prance import ResolvingParser


from .utils import call_restful_api
from ..decorators import delegates

class DataAccessObject(ABC):
    '''abstract class for any object that allows to access data in the ENVRI HUB'''

    @abstractmethod
    def access(self, **kwargs):
        pass

class FileAccessObject(DataAccessObject):

    def __init__(self, url):
        self.url = url

    @delegates(requests.get)
    def access(self, stream = True, **kwargs)->bytes:
        '''Allows to retrieve the file contents as bytes'''
        return requests.get(self.url, stream=stream, **kwargs).content
    
    def download(self, path='.tempfile', stream = True, **kwargs):
        '''
        Dowloads the file to a specified file system location

        Paramters
        ---------
        path:str defualt:".tempfile"
            a file system location to store the file

        '''
        response = requests.get(self.url, stream=stream, **kwargs)
        try:
            # the "good" path: stuff is wrapped in a http response with shit and giggles
            if "content-disposition" in response.headers:
                content_disposition = response.headers["content-disposition"]
                if content_disposition in ['inline', 'attachment']:
                    filename = path
                else:
                    filename = content_disposition.split("filename=")[1]
            else:
                filename = path
            with open(filename, mode="wb") as file:
                file.write(response.content)
                logging.info(f"Downloaded file {filename}")
        except:
            # the "wtf" path: the response is just a string
            with open(path, mode="wb") as file:
                file.write(response)
                logging.info(f"Downloaded file {filename}")
            



class RESTfulAPIDataAccess(DataAccessObject):

    def __init__(self, base_address):
        self.base_address = base_address
        
    @delegates(call_restful_api)
    def access(self, **kwargs):
        return call_restful_api(self.base_address, **kwargs)

class RESTfulAPIwithAPIKeyDataAccess(RESTfulAPIDataAccess):

    def __init__(self, base_address, key_name):
        self._service_key = os.environ.get(key_name)
        if self._service_key is None:
            logging.warning(f'API key {key_name} not found in global environment')
        

class OpenAPI3DataAccess(RESTfulAPIDataAccess):
    
    def __init__(self, **kwargs):
        super().__init__(self.servers.preferred_server)
    
    def access(self, method, **kwargs):
        return getattr(self, method)(**kwargs)
        