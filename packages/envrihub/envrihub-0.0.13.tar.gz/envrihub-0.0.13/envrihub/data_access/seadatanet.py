import logging
import requests
import json
import pandas as pd
import os
from datetime import datetime
from SPARQLWrapper import SPARQLWrapper, JSON

from .models import DataAccessObject

token_var_name = 'SEADATANET_BEACON_API_TOKEN'


def to_seadatanet_datetime(dt:datetime):
    '''converts a Python datetime to the Seadatanet format, i.e. 2007-09-01'''
    return dt.strftime('%Y-%m-%d')

def _format_seadatanet_query_body(mindate, maxdate, minlon, maxlon, minlat, maxlat, mindepth, maxdepth, matching_p01s: list[str]):
    query_parameters = []
    query_parameters.append("LONGITUDE")
    query_parameters.append("LATITUDE")
    query_parameters.append("TIME")
    query_parameters.append({"function": "coalesce", "args": ["DEPTH", "PRES"], "alias": "DEPTH"})
    query_parameters.append("SDN_STATION")
    query_parameters.append("SDN_EDMO_CODE")
    query_parameters.append("SDN_LOCAL_CDI_ID")
    for p01 in matching_p01s:
        query_parameters.append(p01)

    filters = []
    filters.append({"for_query_parameter": "TIME", "min": f"{mindate}T00:00:00", "max": f"{maxdate}T00:00:00"})
    filters.append({"for_query_parameter": "DEPTH", "min": mindepth, "max": maxdepth})
    filters.append({"for_query_parameter": "LONGITUDE", "min": minlon, "max": maxlon})
    filters.append({"for_query_parameter": "LATITUDE", "min": minlat, "max": maxlat})


    parameter_or_filters = []
    for p01 in matching_p01s:
        parameter_or_filters.append({"is_not_null": {"for_query_parameter": p01}})
    or_filter = {
        "or" : parameter_or_filters
    }
    filters.append(or_filter)
    body = {
        "query_parameters": query_parameters,
        "filters": filters,
        "output": {"format": "ipc"},
    }
    return body

class SeadatanetError(Exception):
    def __init__(self, message):            
        super().__init__(message)

class AuthenticationTokenError(SeadatanetError):
    def __init__(self, message):            
        super().__init__(message)
        logging.info('To request a token, go down at Paul\'s at maris.nl and tell him you want the Bob Marley extra crispy  -> maris.nl/contact')
        
class SeaDataNetBeaconDAO(DataAccessObject):
    
    def __init__(self, token = None, beacon_url = "https://beacon-cdi.maris.nl/api/query", vocabulary_endpoint_url = 'https://vocab.nerc.ac.uk/sparql/sparql'):
        self.token = token
        self.__check_token()
        self.vocabulary_endpoint_url = vocabulary_endpoint_url
        self.beacon_url = beacon_url


    def __check_token(self):
        if self.token is None:
            try:
                self.token = os.environ[token_var_name]
            except:
                raise AuthenticationTokenError(f'No Seadatanet authentication token. pass it as a constructor argument or set the env variable {token_var_name}')

    def _get_cdi_input(self):
        responseinfo = requests.get(self.beacon_url + "/available-columns",headers={"Authorization": f"Bearer {self.token}"},)
        return responseinfo.json()
    

    def _get_EXV_iadopt(self, exv_code):
        # SPARQL endpoint
        endpoint_url = self.vocabulary_endpoint_url
        # Construct full identifier
        exv_identifier = f"SDN:EXV::{exv_code}"

        # Create the query with the user input
        sparql_query = f"""
        PREFIX dce: <http://purl.org/dc/elements/1.1/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX iadopt: <https://w3id.org/iadopt/ont#> 
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT DISTINCT ?p01 ?prefLabel ?notation
        WHERE {{
        ?exv a skos:Concept .
        ?exv dce:identifier "{exv_identifier}" .

        OPTIONAL {{?exv iadopt:hasApplicableMatrix ?matrix .}}
        ?exv iadopt:hasApplicableObjectOfInterest ?ooi .
        ?exv iadopt:hasApplicableProperty ?property .

        <http://vocab.nerc.ac.uk/collection/P01/current/> skos:member ?p01 .

        OPTIONAL {{ ?p01 iadopt:hasMatrix ?matrix . }}
        ?p01 iadopt:hasObjectOfInterest ?ooi .
        ?p01 iadopt:hasProperty ?property .

        OPTIONAL {{ ?p01 skos:prefLabel ?prefLabel . }}
        OPTIONAL {{ ?p01 skos:notation ?notation . }}
        }}
        """
        # Set up the SPARQL request
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)

        # Run the query and parse results
        results = sparql.query().convert()

        codes = []

        # Show results
        for result in results["results"]["bindings"]:
            uri = result.get("p01", {}).get("value", "")
            codes.append(uri.rstrip("/").split("/")[-1])

        params = self._get_cdi_input()
        matching_p01s = []
        for code in codes:
            if code in params:
                matching_p01s.append(code)

        return matching_p01s
    
    def access(self, exv_code, mindate, maxdate, minlon, maxlon, minlat, maxlat, mindepth, maxdepth)->pd.DataFrame:
        '''
        Access method for seadatanet data exposed via the BEACON API
        
        Parameters
        ----------
        exv_code:str
            the Essential Climate Variable you want to retrieved, expressed with 
            a alphanumeric code.
            Example: "EXV017"
        
        mindate:datetime
            time interval lower bound
        
        maxdate:datetime 
            time interval upper bound
        
        minlon, 
        
        maxlon, 
        
        minlat, 
        
        maxlat, 
        
        mindepth, 
        
        maxdepth
        
        '''
        matching_p01s = self._get_EXV_iadopt(exv_code)
        query_body = _format_seadatanet_query_body(to_seadatanet_datetime(mindate), to_seadatanet_datetime(maxdate), minlon, maxlon, minlat, maxlat, mindepth, maxdepth, matching_p01s)
        response = requests.post(self.beacon_url, json.dumps(query_body),
                    headers={"Authorization": f"Bearer {self.token}",
                                "Content-type": "application/json"})
        response.raise_for_status() # this raises errors in case of 40X or 50X
        if response.status_code == 204:
            logging.warning("No data has been found for your query")
            return None
        # otherwise, let's convert it to PANDAS
        df = pd.read_feather(response.content)
        df = df.set_index("TIME").sort_index() 
        cols_to_exclude = ['SDN_STATION', 'SDN_EDMO_CODE', 'SDN_LOCAL_CDI_ID']
        df[df.columns.difference(cols_to_exclude)] = df[df.columns.difference(cols_to_exclude)].apply(pd.to_numeric, errors='coerce')
        df[exv_code] = df[matching_p01s].mean(axis=1)
        df.drop(columns=matching_p01s, inplace=True)
        return df

    
