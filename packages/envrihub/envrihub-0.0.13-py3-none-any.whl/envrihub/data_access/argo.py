'''Methods and classes to access Argo data'''
import argopy
import numpy as np
import time
from datetime import datetime
from argopy import DataFetcher
from SPARQLWrapper import SPARQLWrapper, JSON
from .models import DataAccessObject

def to_argo_datetime(dt:datetime):
    '''converts a Python datetime to the Argo format, i.e. 2007-09-01'''
    return dt.isoformat()

class ArgoError(Exception):
    def __init__(self, message):            
        super().__init__(message)

class InvalidArgoFormatError(ArgoError):
    def __init__(self, message):            
        super().__init__(message)

class ArgoDAO(DataAccessObject):

    def __init__(self, src, ds='phy', mode= 'standard'):
        argopy.set_options(src=src,ds=ds,mode=mode)
        self.__datafetcher = DataFetcher()
        super().__init__()
    
    def set_options(self, **kwargs):
        argopy.set_options(**kwargs)
        # proably we need to re-instantiate the data fetcher class at this point
        self.__datafetcher = DataFetcher()

    def __export(self, f, format, **kwargs):
        if format in ['xarray', 'xr']:
            return f.to_xarray(**kwargs)
        elif format in ['pandas', 'dataframe', 'csv', 'df']:
            return f.to_dataframe(**kwargs)
        elif format in ['dataset', 'netcdf', 'ecmwf']:
            return f.to_dataset(**kwargs)
        else:
            raise InvalidArgoFormatError(f'Format {format} is not recognized by Argopy, try "xarray", "dataframe" or "netcdf".')

    def access(self, method = 'region', **kwargs):
        '''
        Access pethod to the Argo web services

        Parameters
        ----------
        method:str, default:'region'
            The Argopy method you want to use to access your data. It can be either
            'region', 'float', or 'profile'. Check out Argo's documentation for more
            information https://argopy.readthedocs.io/en/latest/api.html#id3

        out_format:str, default:'xarray'
            the output format you want to be returned, it can be either 'xarray',
            'dataframe', or 'netcdf'.

        lon_west:float
            western bounding cube limit, expressed in WGS84 coordinates
        
        lon_east:float
            eastern bounding cube limit, expressed in WGS84 coordinates
        
        lat_south:float
            southern bounding cube limit, expressed in WGS84 coordinates
        
        lat_north:float
            northern bounding cube limit, expressed in WGS84 coordinates
        
        depth_min:float
            bottom bounding cube limit, expressed in meters
        
        depth_max:float
            top bounding cube limit, expressed in WGS84 meters
        
        date_min:datetime
            time interval lower bound
        
        date_max:detetime
            time interval upper bound
        '''
        
        if method in ['region', 'demo']:
            return self.region(**kwargs)
        elif method in ['float']:
            return self.float_access(**kwargs)
    
    def region(self, lon_west,lon_east,lat_south,lat_north,depth_min,depth_max,date_min,date_max, out_format='xarray', **kwargs):
        '''
        Access method to the Argo web services

        Parameters
        ----------
        lon_west:float
            western bounding cube limit, expressed in WGS84 coordinates
        
        lon_east:float
            eastern bounding cube limit, expressed in WGS84 coordinates
        
        lat_south:float
            southern bounding cube limit, expressed in WGS84 coordinates
        
        lat_north:float
            northern bounding cube limit, expressed in WGS84 coordinates
        
        depth_min:float
            bottom bounding cube limit, expressed in meters
        
        depth_max:float
            top bounding cube limit, expressed in WGS84 meters
        
        date_min:datetime
            time interval lower bound
        
        date_max:detetime
            time interval upper bound
        
        out_format:str, default:'xarray'
            the output format you want to be returned, it can be either 'xarray',
            'dataframe', or 'netcdf'.
        ''' 
        f = self.__datafetcher.region([lon_west,lon_east,lat_south,lat_north,depth_min,depth_max,date_min,date_max])
        return self.__export(f, out_format, **kwargs)
    
    def float_access(self, wmo, out_format, **kwargs):
        '''
        Retrieves data from one or more specific float in the Argo monitoring network

        Parameters
        ----------
        wms:float or list
            WMS identifier(s) of the float(s) to load data from

        out_format:str, default:'xarray'
            the output format you want to be returned, it can be either 'xarray',
            'dataframe', or 'netcdf'.
        '''
        f = self.__datafetcher.float(wmo)
        return self.__export(f, out_format, **kwargs)

    