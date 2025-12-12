from abc import ABC, abstractmethod
import inspect
import logging

import requests

from envrihub.data_access.catalogue_metadata_client import build_epos_catalogue_metadata_access
from envrihub.data_access.models import DataAccessObject, FileAccessObject, RESTfulAPIDataAccess
from envrihub.data_access.open_api_client import build_web_service_client
from envrihub.decorators import delegates

# Exception definition bonanza
class DistributionError(Exception):
    def __init__(self, message):            
        super().__init__(message)

class NullDistributionTypeError(DistributionError):
    def __init__(self, message, resource_id):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        logging.error(f'Resource {resource_id} has no type attribute')

class InvalidDistributionTypeError(DistributionError):
    def __init__(self, message, resource_id, type_value):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        logging.error(f'Resource {resource_id} has invalid type attribute {type_value}')

class InvalidServiceDocumentationError(DistributionError):
    def __init__(self, message, resource_id, url):
        super().__init__(message)
        logging.error(f'Resource {resource_id} documentation at {url} cannot be used to create a data access client')


class CoSObject(ABC):
    pass

class Distribution(CoSObject):
    
    def __init__(self, href:str, title:str, id:str, uid:str, description:str = None, serviceDocumentation:str = None, type=None, build_dao=True):
        self.href = href
        self.id = id
        try:
            self.metadata = self._get_details()
            if self.metadata.get('serviceDocumentation') is not None:
                self.service_documentation = self.metadata.get('serviceDocumentation')
            else:
                self.service_documentation = serviceDocumentation
            if self.metadata.get('type') is not None:
                self.type = self.metadata.get('type')
            else:
                self.type = type
        except:
            logging.error(f'Cannot access metadata at {href}')
            self.service_documentation = serviceDocumentation
            self.type = type

        self.title = title
        self.uid = uid
        self.description =description
        # we'll instance this as soon as it would be required
        if build_dao:
            self._build_dao()
        else:
            self.dao = None

    def _get_details(self):
        response_detail = requests.get(self.href)
        return response_detail.json()
    
    def _build_dao(self):
        if self.type is None:
            raise NullDistributionTypeError('Null type attribute in current Distribution', self.uid)
        elif self.type == 'WEB_SERVICE':
            service_provider = self.metadata.get('serviceProvider')
            # if it is a well known service provider with custom built classes, we'll use them
            # TODO: the case/switch
            declared_parameters = self.metadata.get('serviceParameters')
            base_url = self.metadata.get('endpoint')
            # if people bothered to describe parameters, we'll go with them
            if (base_url is not None) and (declared_parameters is not None):
                # fetch the application type
                classname = self.metadata.get('serviceName').translate({ord(c): None for c in '/!@#*+-%&|[]()$ \r\n\t'})
                content_type=None
                afs = self.metadata.get('availableFormats')
                for af in afs:
                    content_type = af.get('format')
                try:
                    self.dao = build_epos_catalogue_metadata_access(base_url, declared_parameters, content_type,self.description, classname)(base_url)
                except ValueError as ve:
                    logging.warning(ve)
                    logging.warning('Parameters names do not respect Python naming conventions, instantiating a generic REST client')
                    self.dao = RESTfulAPIDataAccess(base_url)
            # otherwise, it's OpenAPI
            else:
                try:
                    self.dao = build_web_service_client(self.service_documentation)()
                except Exception as e:
                    raise InvalidServiceDocumentationError(e, self.uid, self.service_documentation)
        elif self.type == 'DOWNLOADABLE_FILE':
            self.dao = FileAccessObject(self.metadata.get('downloadURL'))
        else:
            raise InvalidDistributionTypeError('Null type attribute in current Distribution', self.uid, self.type)

    @classmethod
    def from_dict(cls, env):
        '''This is mostly used to build the object from the output returned by Web Services'''
        return cls(**{
                k: v for k, v in env.items() 
                if k in inspect.signature(cls).parameters
            })
    
    def access(self, **kwargs):
        return self.dao.access(**kwargs)
    
    def get_dato(self):
        return self.dao
    
    def is_downloadable(self):
        return self.type == 'DOWNLOADABLE_FILE'
    


