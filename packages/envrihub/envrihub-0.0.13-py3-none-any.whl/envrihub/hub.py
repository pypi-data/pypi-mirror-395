from datetime import datetime
from collections.abc import Iterator
from .cos.catalogue import EposCatalogue
import shapely
import logging

from .cos.models import Distribution


class Hub():

    def __init__(self, **kwargs):
        self.catalogue = EposCatalogue(**kwargs)
    
    def search_catalogue(self, query:str = '', start_date:datetime=None, end_date:datetime=None, geography = None, exv = None, provider=None, **kwargs)->Iterator[Distribution]:
        '''
        Parameters
        ----------
        query:str

        start_date:datetime 
            Beginning of time interval of interest

        end_date: datetime
            End of time interval of interest
        geography: str | shapely.Geometry | tuple
            geographcial bounds in WKT format, with WGS84 coordinates. Altenratively
            also Shapely Geometry objects and tuples of cooridnates can be accepted

        exv:str|list[str]
            essential variables to lookup

        provider: str
            Data provider to restrict search to

        '''
        # parse wkt geogrpahy into a Shape
        if isinstance(geography, str):
            try:
                polygon=shapely.from_wkt(geography )
                bbox = polygon.bounds
            except:
                logging.error('Invalid WKT geography')
        elif isinstance(geography, shapely.Geometry):
            bbox = geography.bounds
        elif isinstance(geography, tuple):
            if len(geography)>0:
                bbox = geography
            else:
                bbox = None
        else:
            bbox = None 
        # here we are not using yield from becasue we may want to add some further
        # processing/reshaping here in the near future...
        for i in self.catalogue.search(query=query, bbox=bbox, startDate=start_date, endDate=end_date, exvs=exv, organisations=provider, **kwargs):
            yield i

    def fetch_from_catalogue(self, resource_id)->Distribution:
        '''Retrieves a specific resource from the catalogue'''
        return self.catalogue.retrieve_resource(resource_id)