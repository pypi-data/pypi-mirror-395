from abc import ABC, abstractmethod
from datetime import datetime
import logging
import requests

from .models import Distribution, DistributionError
from .utils import datetime_to_epos_format


class Catalogue(ABC):
    """The interface all catalogue-like objects are expected to implement"""

    @abstractmethod
    def search(self, query=None, **kwargs):
        pass


class EposCatalogue(Catalogue):
    """this class encapsulates interactions with the catalogue of services
    check the Swagger documentation for advanced usage
    https://catalogue.staging.envri.eu/api/v1/ui
    """

    base_address = "https://catalogue.staging.envri.eu/api/v1"
    search_path = "/resources/search"
    details_path = "/resources/details"

    def __init__(self, api_url=None):
        if api_url is None:
            self.api_url = self.base_address
        else:
            self.api_url = api_url

    def __parse_distributions(self, dists, facet=None, build_dao=True):
        """parses distribution JSON into a Distribution object"""
        for d in dists:
            try:
                d["build_dao"] = build_dao
                yield Distribution.from_dict(d)
            except DistributionError as e:
                logging.error(e)

    def search(
        self,
        query: str = "",
        startDate: datetime = None,
        endDate: datetime = None,
        bbox: tuple = None,
        keywords: list[str] = None,
        sciencedomains=None,
        servicetypes=None,
        organisations=None,
        exvs=None,
        facetstype=None,
        facets: bool = False,
        build_dao=True,
    ):
        """
        Allows to retrieve datasets as Distribution objects.
        You can query teh cataloge with a full text query and/or in a faceted way
        including time boundaries, geographical baoundaries, and other types of filter.

        Parameters
        ----------
        query:str
            A textual query in the likes of what you'd insert into a search engine
        startDate:datetime
            the beginning of the time interval of interest
        endDate: datetime
            the end of the time interval of interest
        bbox: tuple
            the four margins of the geographical area of interest.
            e.g. (10.70, 36.17, 28.98, 48.34)
        keywords: list[str]
            a list of keywords to filter research
        sciencedomains:

        servicetypes: str

        organisations: str

        exvs:str
            esential variables to look up

        facestype: str, default None
            one of the following values: 'categories', 'dataproviders', or 'serviceproviders'

        facets:bool
            whether or not to include facets in the search, which changes the structure of the
            output returned by the catalogue

        build_dao:bool, default True
            whether or not to build the data access object for retrieved items

        """
        search_endpoint = self.api_url + self.search_path
        params = {
            "q": query,
            "startDate": (
                datetime_to_epos_format(startDate)
                if isinstance(startDate, datetime)
                else startDate
            ),
            "endDate": (
                datetime_to_epos_format(endDate)
                if isinstance(endDate, datetime)
                else endDate
            ),
            "bbox": str(bbox) if bbox is not None else None,
            "keywords": str(keywords) if keywords is not None else None,
            "sciencedomains": sciencedomains,
            "servicetypes": servicetypes,
            "organisations": organisations,
            "exvs": str(exvs) if exvs is not None else None,
            "facetstype": (
                facetstype
                if facetstype in ["categories", "dataproviders", "serviceproviders"]
                else None
            ),
            "facets": facets,
        }
        response_search = requests.get(search_endpoint, params=params)
        data = response_search.json()
        # parsing the JSON response to find distribution items
        if data.get("results") is not None:
            results = data.get("results")
            # if it's a faceted search, distributions are split into several
            # classes that are represented with a nested structure that looks like this
            # 'results' -> {'children':[
            #                    {'children':[
            #                          {'distributions':[...],
            #                           'name':facet name},
            #                            ...
            #                                ]
            #                           },
            #                           ...
            #                       ]
            #              }
            if facets:
                if isinstance(results.get("children"), list):
                    for child in results.get("children"):
                        if isinstance(child.get("children"), list):
                            for nephew in child.get("children"):
                                if nephew.get("distributions") is not None:
                                    yield from self.__parse_distributions(
                                        nephew.get("distributions"),
                                        facet=nephew.get("name"),
                                        build_dao=build_dao,
                                    )

            # else it's not a faceted search
            elif results.get("distributions") is not None:
                yield from self.__parse_distributions(
                    results.get("distributions"), build_dao=build_dao
                )
        else:
            return None

    def retrieve_resource(self, uid: str) -> Distribution:
        """
        Retrieves a specific Distribution object from the catalogue.
        Parameters
        ----------
        uid:str
            The uid property of the desired distribution
        """
        retrieve_endpoint = self.api_url + self.details_path
        response_retrieve = requests.get(retrieve_endpoint, params={"uid": uid})
        return Distribution.from_dict(response_retrieve.json())
